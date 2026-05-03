from db.schema import DatabaseSchema
from repositories.user_repository import UserRepository
from repositories.warehouse_repository import WarehouseRepository
from repositories.product_repository import ProductRepository
from repositories.warehouse_assignment_repository import WarehouseAssignmentRepository
from repositories.inventory_repository import InventoryRepository


def seed_users():
    repo = UserRepository()

    users = [
        ("manager1@gmail.com", "manager1", "pass", "manager"),
        ("driver1@gmail.com", "driver1", "pass", "driver"),
        ("driver2@gmail.com", "driver2", "pass", "driver"),
    ]

    # 15 staff
    for i in range(1, 16):
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

    warehouses = [
        ("wh1", "Location 1"),
        ("wh2", "Location 2"),
        ("wh3", "Location 3")
    ]

    for name, location in warehouses:
        repo.create_warehouse(name, location)


def seed_products():
    repo = ProductRepository()

    for i in range(1, 21):
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

    for i in range(1, 7):
        user = user_repo.find_by_email(f"staff{i}@gmail.com")
        if user:
            staff.append(user)

    idx = 0
    for warehouse in warehouses:
        for _ in range(2):
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
        for product in products[:8]:
            inventory_repo.set_inventory(
                warehouse["id"],
                product["id"],
                quantity=50 + product["id"] * 5,
                reorder_level=20
            )


def main():
    DatabaseSchema.initialize_database()

    seed_users()
    seed_warehouses()
    seed_products()
    seed_assignments()
    seed_inventory()

    print("Dummy data seeded successfully")


if __name__ == "__main__":
    main()