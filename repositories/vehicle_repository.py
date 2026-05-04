from db.connection import DatabaseConnection


class VehicleRepository:

    def __init__(self):
        self.db = DatabaseConnection()

    def create_vehicle(self, code, capacity):
        query = """
            INSERT INTO vehicles (vehicle_code, capacity)
            VALUES (?, ?)
        """
        self.db.execute_update(query, (code, capacity))
        return True

    def list_vehicles(self):
        query = "SELECT * FROM vehicles"
        return [dict(r) for r in self.db.execute_query(query)]

    def update_vehicle(self, vehicle_id, **kwargs):
        allowed_fields = [
            "vehicle_code",
            "capacity",
            "status",
            "assigned_driver_id",
            "last_service_date",
            "maintenance_due_date"
        ]
        update_fields = {k: v for k, v in kwargs.items() if k in allowed_fields}
        if not update_fields:
            return False

        set_clause = ", ".join([f"{field} = ?" for field in update_fields.keys()])
        values = list(update_fields.values())
        values.append(vehicle_id)

        query = f"UPDATE vehicles SET {set_clause} WHERE id = ?"
        self.db.execute_update(query, values)
        return True

    def list_available(self):
        query = "SELECT * FROM vehicles WHERE status = 'available'"
        return [dict(r) for r in self.db.execute_query(query)]