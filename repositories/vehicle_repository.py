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