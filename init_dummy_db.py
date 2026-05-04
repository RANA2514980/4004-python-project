from db.schema import DatabaseSchema
from repositories.user_repository import UserRepository
from repositories.warehouse_repository import WarehouseRepository
from repositories.product_repository import ProductRepository
from repositories.warehouse_assignment_repository import WarehouseAssignmentRepository
from repositories.inventory_repository import InventoryRepository
from repositories.shipment_repository import ShipmentRepository
from repositories.vehicle_repository import VehicleRepository
from repositories.incident_repository import IncidentRepository


def seed_users():
    repo = UserRepository()

    users = [
        ("manager1@gmail.com", "manager1", "pass", "manager"),
        ("manager2@gmail.com", "manager2", "pass", "manager"),
    ]

    for i in range(1, 6):
        users.append((
            f"driver{i}@gmail.com",
            f"driver{i}",
            "pass",
            "driver"
        ))

    for i in range(1, 21):
        users.append((
            f"staff{i}@gmail.com",
            f"staff{i}",
            "pass",
            "warehouse_staff"
        ))

    for email, name, password, role in users:
        repo.create_user(email, name, password, role)


def seed_warehouses():
    repo = WarehouseRepository()

    for i in range(1, 6):
        repo.create_warehouse(f"wh{i}", f"Location {i}")


def seed_products():
    repo = ProductRepository()

    for i in range(1, 16):
        repo.create_product(
            f"prod{i}",
            f"prod{i}"
        )


def seed_assignments():
    user_repo = UserRepository()
    warehouse_repo = WarehouseRepository()
    assign_repo = WarehouseAssignmentRepository()

    warehouses = warehouse_repo.list_warehouses()

    staff = []

    for i in range(1, 16):
        user = user_repo.find_by_email(f"staff{i}@gmail.com")
        if user:
            staff.append(user)

    idx = 0
    for warehouse in warehouses:
        for _ in range(3):
            if idx < len(staff):
                assign_repo.assign_user(
                    staff[idx]["id"],
                    warehouse["id"]
                )
                idx += 1


def seed_inventory():
    warehouse_repo = WarehouseRepository()
    product_repo = ProductRepository()
    inventory_repo = InventoryRepository()

    warehouses = warehouse_repo.list_warehouses()
    products = product_repo.list_products()

    for warehouse in warehouses:
        for product in products[:10]:
            inventory_repo.set_inventory(
                warehouse["id"],
                product["id"],
                quantity=50 + product["id"] * 5,
                reorder_level=20
            )


def seed_driver_profiles():
    user_repo = UserRepository()

    for i in range(1, 6):
        user = user_repo.find_by_email(f"driver{i}@gmail.com")
        if user:
            user_repo.update_driver_profile(
                user["id"],
                license_number=f"DL{i:04d}",
                phone=f"+100000000{i}",
                address=f"Driver Address {i}"
            )


def seed_vehicles():
    repo = VehicleRepository()

    for i in range(1, 7):
        repo.create_vehicle(f"v{i}", capacity=1000 + i * 250)


def seed_vehicle_assignments():
    vehicle_repo = VehicleRepository()
    user_repo = UserRepository()

    vehicles = vehicle_repo.list_vehicles()
    drivers = []
    for i in range(1, 6):
        user = user_repo.find_by_email(f"driver{i}@gmail.com")
        if user:
            drivers.append(user)

    for idx, vehicle in enumerate(vehicles[:4]):
        driver = drivers[idx % len(drivers)] if drivers else None
        if driver:
            vehicle_repo.update_vehicle(
                vehicle["id"],
                assigned_driver_id=driver["id"],
                status="in_use"
            )


def seed_shipments():
    shipment_repo = ShipmentRepository()
    warehouse_repo = WarehouseRepository()
    user_repo = UserRepository()

    warehouses = warehouse_repo.list_warehouses()
    drivers = []
    for i in range(1, 6):
        user = user_repo.find_by_email(f"driver{i}@gmail.com")
        if user:
            drivers.append(user)

    for i in range(1, 13):
        warehouse = warehouses[(i - 1) % len(warehouses)]
        shipment_repo.create_shipment(
            f"s{i}",
            f"ord{i}",
            f"sender{i}",
            f"receiver{i}",
            f"Receiver Address {i}",
            f"+200000000{i}",
            f"Shipment {i} description",
            warehouse["id"]
        )

    shipments = shipment_repo.list_shipments()
    for idx, shipment in enumerate(shipments):
        driver = drivers[idx % len(drivers)] if drivers else None
        if driver:
            shipment_repo.assign_driver(shipment["id"], driver["id"])

        if idx % 5 == 0:
            shipment_repo.update_status(shipment["id"], "delivered")
            shipment_repo.update_delivery_info(shipment["id"], "2026-05-01", "Route A")
            shipment_repo.update_financials(shipment["id"], 120.5, "paid", f"pay{shipment['id']}")
        elif idx % 5 == 1:
            shipment_repo.update_status(shipment["id"], "in_transit")
            shipment_repo.update_delivery_info(shipment["id"], "2026-05-05", "Route B")
        elif idx % 5 == 2:
            shipment_repo.update_status(shipment["id"], "delayed")
        elif idx % 5 == 3:
            shipment_repo.update_status(shipment["id"], "returned")


def seed_incidents():
    incident_repo = IncidentRepository()
    shipment_repo = ShipmentRepository()
    user_repo = UserRepository()

    reporter = user_repo.find_by_email("driver1@gmail.com")
    shipments = shipment_repo.list_shipments()

    if reporter:
        for shipment in shipments[:4]:
            incident_repo.create_incident(
                shipment["id"],
                "delay",
                "Traffic delay",
                reporter["id"]
            )


def seed_inventory_movements():
    inventory_repo = InventoryRepository()
    warehouse_repo = WarehouseRepository()
    product_repo = ProductRepository()
    user_repo = UserRepository()

    reporter = user_repo.find_by_email("manager1@gmail.com")
    if not reporter:
        return

    warehouses = warehouse_repo.list_warehouses()
    products = product_repo.list_products()

    for warehouse in warehouses:
        for product in products[:5]:
            inventory_repo.adjust_inventory(
                warehouse["id"],
                product["id"],
                5,
                "adjustment",
                "Initial adjustment",
                reporter["id"]
            )


def main():
    DatabaseSchema.initialize_database()

    seed_users()
    seed_warehouses()
    seed_products()
    seed_assignments()
    seed_inventory()
    seed_driver_profiles()
    seed_vehicles()
    seed_vehicle_assignments()
    seed_shipments()
    seed_incidents()
    seed_inventory_movements()

    print("Dummy data seeded successfully")


if __name__ == "__main__":
    main()