from repositories.shipment_repository import ShipmentRepository


class ShipmentService:

    def __init__(self):
        self.repo = ShipmentRepository()

    def create(self, *args):
        return self.repo.create_shipment(*args)

    def list_all(self):
        return self.repo.list_shipments()

    def assign_driver(self, shipment_id, driver_id):
        return self.repo.assign_driver(shipment_id, driver_id)

    def update_status(self, shipment_id, status):
        return self.repo.update_status(shipment_id, status)

    def driver_shipments(self, driver_id):
        return self.repo.get_driver_shipments(driver_id)