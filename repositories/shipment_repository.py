from db.connection import DatabaseConnection


class ShipmentRepository:

    def __init__(self):
        self.db = DatabaseConnection()

    def create_shipment(
        self,
        code,
        sender,
        receiver,
        address,
        description,
        warehouse_id
    ):
        query = """
            INSERT INTO shipments
            (
                shipment_code,
                sender_name,
                receiver_name,
                receiver_address,
                description,
                warehouse_id
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """
        self.db.execute_update(query, (
            code,
            sender,
            receiver,
            address,
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
        return [dict(r) for r in self.db.execute_query(query)]

    def assign_driver(self, shipment_id, driver_id):
        query = """
            UPDATE shipments
            SET assigned_driver_id = ?
            WHERE id = ?
        """
        self.db.execute_update(query, (driver_id, shipment_id))
        return True

    def update_status(self, shipment_id, status):
        query = """
            UPDATE shipments
            SET status = ?
            WHERE id = ?
        """
        self.db.execute_update(query, (status, shipment_id))
        return True

    def get_driver_shipments(self, driver_id):
        query = """
            SELECT *
            FROM shipments
            WHERE assigned_driver_id = ?
        """
        return [dict(r) for r in self.db.execute_query(query, (driver_id,))]