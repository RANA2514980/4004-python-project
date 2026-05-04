from repositories.vehicle_repository import VehicleRepository


class VehicleService:

    def __init__(self, auth_service, audit_service=None):
        self.auth = auth_service
        self.repo = VehicleRepository()
        self.audit = audit_service

    def _require_roles(self, roles):
        user = self.auth.get_current_user()
        if not user:
            return None
        if user["role"] not in roles:
            return None
        return user

    def create(self, code, capacity):
        user = self._require_roles(["admin", "manager"])
        if not user:
            return False
        ok = self.repo.create_vehicle(code, capacity)
        if ok and self.audit:
            self.audit.log("create", "vehicle")
        return ok

    def list_all(self):
        user = self._require_roles(["admin", "manager", "driver", "warehouse_staff"])
        if not user:
            return []
        return self.repo.list_vehicles()

    def update(self, vehicle_id, **kwargs):
        user = self._require_roles(["admin", "manager"])
        if not user:
            return False
        ok = self.repo.update_vehicle(vehicle_id, **kwargs)
        if ok and self.audit:
            self.audit.log("update", "vehicle", vehicle_id)
        return ok

    def list_available(self):
        user = self._require_roles(["admin", "manager"])
        if not user:
            return []
        return self.repo.list_available()