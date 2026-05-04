import logging
from db.connection import DatabaseConnection
from db.crypto import SimpleCrypto

logger = logging.getLogger(__name__)


class ShipmentRepository:

    def __init__(self):
        self.db = DatabaseConnection()
        self.crypto = SimpleCrypto()

    def create_shipment(
        self,
        code,
        order_number,
        sender,
        receiver,
        address,
        receiver_phone,
        description,
        warehouse_id
    ):
        enc_address = self.crypto.encrypt(address)
        query = """
            INSERT INTO shipments
            (
                shipment_code,
                order_number,
                sender_name,
                receiver_name,
                receiver_address,
                receiver_phone,
                description,
                warehouse_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.db.execute_update(query, (
            code,
            order_number,
            sender,
            receiver,
            enc_address,
            receiver_phone,
            description,
            warehouse_id
        ))
        return True

    def list_shipments(self):
        query = """
            SELECT s.*, w.name as warehouse_name
            FROM shipments s
            JOIN warehouses w ON s.warehouse_id = w.id
        """
        rows = [dict(r) for r in self.db.execute_query(query)]
        for row in rows:
            row["receiver_address"] = self.crypto.decrypt(row.get("receiver_address"))
            row["payment_reference"] = self.crypto.decrypt(row.get("payment_reference"))
        return rows

    def get_by_id(self, shipment_id):
        query = """
            SELECT s.*, w.name as warehouse_name
            FROM shipments s
            JOIN warehouses w ON s.warehouse_id = w.id
            WHERE s.id = ?
        """
        results = self.db.execute_query(query, (shipment_id,))
        if not results:
            return None

        row = dict(results[0])
        row["receiver_address"] = self.crypto.decrypt(row.get("receiver_address"))
        row["payment_reference"] = self.crypto.decrypt(row.get("payment_reference"))
        return row

    def assign_driver(self, shipment_id, driver_id):
        query = """
            UPDATE shipments
            SET assigned_driver_id = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.db.execute_update(query, (driver_id, shipment_id))
        return True

    def update_status(self, shipment_id, status):
        query = """
            UPDATE shipments
            SET status = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.db.execute_update(query, (status, shipment_id))
        return True

    def update_delivery_info(self, shipment_id, delivery_date, route_details):
        query = """
            UPDATE shipments
            SET delivery_date = ?, route_details = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.db.execute_update(query, (delivery_date, route_details, shipment_id))
        return True

    def update_financials(self, shipment_id, transport_cost, payment_status, payment_reference=None):
        enc_reference = self.crypto.encrypt(payment_reference) if payment_reference else None
        query = """
            UPDATE shipments
            SET transport_cost = ?, payment_status = ?, payment_reference = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """
        self.db.execute_update(query, (transport_cost, payment_status, enc_reference, shipment_id))
        return True

    def get_driver_shipments(self, driver_id):
        query = """
            SELECT *
            FROM shipments
            WHERE assigned_driver_id = ?
        """
        rows = [dict(r) for r in self.db.execute_query(query, (driver_id,))]
        for row in rows:
            row["receiver_address"] = self.crypto.decrypt(row.get("receiver_address"))
            row["payment_reference"] = self.crypto.decrypt(row.get("payment_reference"))
        return rows