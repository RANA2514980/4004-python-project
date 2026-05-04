import logging
from repositories.warehouse_repository import WarehouseRepository
from repositories.product_repository import ProductRepository
from repositories.inventory_repository import InventoryRepository

logger = logging.getLogger(__name__)


class WarehouseService:

    def __init__(self, auth_service, audit_service=None):
        self.auth_service = auth_service
        self.audit = audit_service
        self.warehouse_repo = WarehouseRepository()
        self.product_repo = ProductRepository()
        self.inventory_repo = InventoryRepository()

    def _require_authenticated(self):
        user = self.auth_service.get_current_user()
        if not user:
            return None
        return user

    def _require_roles(self, roles):
        user = self.auth_service.get_current_user()
        if not user:
            return None
        if user['role'] not in roles:
            return None
        return user

    def create_warehouse(self, name, location, status='active'):
        if not self._require_roles(['admin', 'manager']):
            return False
        ok = self.warehouse_repo.create_warehouse(name, location, status)
        if ok and self.audit:
            self.audit.log("create", "warehouse")
        return ok

    def list_warehouses(self, active_only=True):
        if not self._require_authenticated():
            return []
        return self.warehouse_repo.list_warehouses(active_only)

    def update_warehouse(self, warehouse_id, **kwargs):
        if not self._require_roles(['admin', 'manager']):
            return False
        return self.warehouse_repo.update_warehouse(warehouse_id, **kwargs)

    def create_product(self, sku, name, description=None, unit='unit'):
        if not self._require_roles(['admin', 'manager']):
            return False
        ok = self.product_repo.create_product(sku, name, description, unit)
        if ok and self.audit:
            self.audit.log("create", "product")
        return ok

    def list_products(self, active_only=True):
        if not self._require_authenticated():
            return []
        return self.product_repo.list_products(active_only)

    def update_product(self, product_id, **kwargs):
        if not self._require_roles(['admin', 'manager']):
            return False
        return self.product_repo.update_product(product_id, **kwargs)

    def set_inventory(self, warehouse_id, product_id, quantity, reorder_level=0):
        if not self._require_roles(['admin', 'manager']):
            return False
        return self.inventory_repo.set_inventory(warehouse_id, product_id, quantity, reorder_level)

    def adjust_inventory(self, warehouse_id, product_id, change_qty, movement_type, note=None):
        user = self._require_roles(['admin', 'manager', 'warehouse_staff'])
        if not user:
            return False
        valid_types = ['load', 'unload', 'transfer_in', 'transfer_out', 'adjustment']
        if movement_type not in valid_types:
            return False
        return self.inventory_repo.adjust_inventory(
            warehouse_id,
            product_id,
            change_qty,
            movement_type,
            note,
            user['id']
        )

    def list_inventory_by_warehouse(self, warehouse_id):
        if not self._require_authenticated():
            return []
        return self.inventory_repo.list_inventory_by_warehouse(warehouse_id)
