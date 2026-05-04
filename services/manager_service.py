import logging
from repositories.warehouse_repository import WarehouseRepository
from repositories.inventory_repository import InventoryRepository
from repositories.vehicle_repository import VehicleRepository

logger = logging.getLogger(__name__)


class ManagerService:

    def __init__(self):
        self.warehouse_repo = WarehouseRepository()
        self.inventory_repo = InventoryRepository()
        self.vehicle_repo = VehicleRepository()

    # ---------------- WAREHOUSES ----------------

    def get_all_warehouses(self):
        return self.warehouse_repo.list_warehouses(active_only=True)

    # ---------------- INVENTORY STATS ----------------

    def get_total_products(self):
        warehouses = self.warehouse_repo.list_warehouses()
        total = 0

        for w in warehouses:
            items = self.inventory_repo.list_inventory_by_warehouse(w["id"])
            total += len(items)

        return total

    def get_low_stock_items(self):
        return self.inventory_repo.get_low_stock_items()

    # ---------------- ACTIVITY ----------------

    def get_recent_activity(self, limit=10):
        try:
            conn = self.inventory_repo.db_conn.get_connection()
            cursor = conn.cursor()

            cursor.execute("""
                SELECT im.*, u.name as user_name, p.name as product_name
                FROM inventory_movements im
                JOIN users u ON u.id = im.created_by
                JOIN products p ON p.id = im.product_id
                ORDER BY im.created_at DESC
                LIMIT ?
            """, (limit,))

            return [dict(row) for row in cursor.fetchall()]

        except Exception as e:
            logger.error(f"Error fetching activity: {e}")
            return []

    def get_vehicle_utilization(self):
        vehicles = self.vehicle_repo.list_vehicles()
        stats = {
            "available": 0,
            "in_use": 0,
            "maintenance": 0
        }

        for vehicle in vehicles:
            status = vehicle.get("status", "available")
            stats[status] = stats.get(status, 0) + 1

        return stats