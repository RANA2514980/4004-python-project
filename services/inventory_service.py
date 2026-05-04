import logging

from repositories.inventory_repository import InventoryRepository
from repositories.product_repository import ProductRepository

logger = logging.getLogger(__name__)


class InventoryService:

    def __init__(self, auth_service, audit_service=None):
        self.auth = auth_service
        self.audit = audit_service
        self.inventory_repo = InventoryRepository()
        self.product_repo = ProductRepository()

    def _require_inventory_role(self):
        user = self.auth.get_current_user()
        if not user:
            return None

        if user["role"] not in ["admin", "manager", "warehouse_staff"]:
            return None

        return user

    def list_inventory(self, warehouse_id):
        return self.inventory_repo.list_inventory_by_warehouse(warehouse_id)

    def add_product_to_warehouse(
        self,
        warehouse_id,
        sku,
        name,
        quantity,
        reorder_level=0
    ):
        user = self._require_inventory_role()
        if not user:
            return False

        product = self.product_repo.find_by_sku(sku)

        if not product:
            ok = self.product_repo.create_product(sku, name)
            if not ok:
                return False
            product = self.product_repo.find_by_sku(sku)

        ok = self.inventory_repo.set_inventory(
            warehouse_id,
            product["id"],
            quantity,
            reorder_level
        )

        if ok and self.audit:
            self.audit.log("set_inventory", "inventory", product["id"])

        return ok

    def adjust_stock(self, warehouse_id, product_id, change_qty, note=""):
        user = self._require_inventory_role()
        if not user:
            return False

        movement = "load" if change_qty > 0 else "unload"

        ok = self.inventory_repo.adjust_inventory(
            warehouse_id,
            product_id,
            change_qty,
            movement,
            note,
            user["id"]
        )

        if ok and self.audit:
            self.audit.log("adjust_inventory", "inventory", product_id, f"delta={change_qty}")

        return ok