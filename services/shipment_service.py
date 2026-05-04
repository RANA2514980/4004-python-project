from repositories.shipment_repository import ShipmentRepository
from repositories.incident_repository import IncidentRepository


class ShipmentService:

    def __init__(self, auth_service, audit_service=None):
        self.auth = auth_service
        self.repo = ShipmentRepository()
        self.incident_repo = IncidentRepository()
        self.audit = audit_service

    def _require_roles(self, roles):
        user = self.auth.get_current_user()
        if not user:
            return None
        if user["role"] not in roles:
            return None
        return user

    def create(self, *args):
        user = self._require_roles(["admin", "manager", "warehouse_staff"])
        if not user:
            return False
        ok = self.repo.create_shipment(*args)
        if ok and self.audit:
            self.audit.log("create", "shipment")
        return ok

    def list_all(self):
        user = self._require_roles(["admin", "manager", "warehouse_staff"])
        if not user:
            return []
        return self.repo.list_shipments()

    def assign_driver(self, shipment_id, driver_id):
        user = self._require_roles(["admin", "manager"])
        if not user:
            return False
        ok = self.repo.assign_driver(shipment_id, driver_id)
        if ok and self.audit:
            self.audit.log("assign_driver", "shipment", shipment_id, f"driver={driver_id}")
        return ok

    def update_status(self, shipment_id, status):
        user = self._require_roles(["admin", "manager", "driver", "warehouse_staff"])
        if not user:
            return False
        ok = self.repo.update_status(shipment_id, status)
        if ok and self.audit:
            self.audit.log("update_status", "shipment", shipment_id, f"status={status}")
        return ok

    def update_delivery_info(self, shipment_id, delivery_date, route_details):
        user = self._require_roles(["admin", "manager", "driver"])
        if not user:
            return False
        ok = self.repo.update_delivery_info(shipment_id, delivery_date, route_details)
        if ok and self.audit:
            self.audit.log("update_delivery", "shipment", shipment_id)
        return ok

    def update_financials(self, shipment_id, transport_cost, payment_status, payment_reference=None):
        user = self._require_roles(["admin", "manager"])
        if not user:
            return False
        ok = self.repo.update_financials(shipment_id, transport_cost, payment_status, payment_reference)
        if ok and self.audit:
            self.audit.log("update_payment", "shipment", shipment_id, f"status={payment_status}")
        return ok

    def driver_shipments(self, driver_id):
        user = self._require_roles(["admin", "manager", "driver"])
        if not user:
            return []
        if user["role"] == "driver" and user["id"] != driver_id:
            return []
        return self.repo.get_driver_shipments(driver_id)

    def report_incident(self, shipment_id, incident_type, description):
        user = self._require_roles(["admin", "manager", "driver", "warehouse_staff"])
        if not user:
            return False
        ok = self.incident_repo.create_incident(
            shipment_id,
            incident_type,
            description,
            user["id"]
        )
        if ok and self.audit:
            self.audit.log("report_incident", "shipment", shipment_id, incident_type)
        return ok

    def list_incidents(self, shipment_id):
        user = self._require_roles(["admin", "manager", "driver", "warehouse_staff"])
        if not user:
            return []
        return self.incident_repo.list_by_shipment(shipment_id)

    def get_status_report(self):
        shipments = self.repo.list_shipments()
        report = {"pending": 0, "in_transit": 0, "delivered": 0, "delayed": 0, "returned": 0}
        for s in shipments:
            status = s.get("status", "pending")
            report[status] = report.get(status, 0) + 1
        return report