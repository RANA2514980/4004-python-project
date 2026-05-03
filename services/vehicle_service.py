from repositories.vehicle_repository import VehicleRepository


class VehicleService:

    def __init__(self):
        self.repo = VehicleRepository()

    def create(self, code, capacity):
        return self.repo.create_vehicle(code, capacity)

    def list_all(self):
        return self.repo.list_vehicles()