from db.tables.registry import register


@register
def create_shipments_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_code TEXT UNIQUE NOT NULL,
            order_number TEXT,
            sender_name TEXT NOT NULL,
            receiver_name TEXT NOT NULL,
            receiver_address TEXT NOT NULL,
            receiver_phone TEXT,
            description TEXT,
            warehouse_id INTEGER NOT NULL,
            assigned_driver_id INTEGER,
            status TEXT NOT NULL DEFAULT 'pending'
                CHECK(status IN (
                    'pending',
                    'in_transit',
                    'delivered',
                    'delayed',
                    'returned'
                )),
            transport_cost REAL DEFAULT 0,
            payment_status TEXT DEFAULT 'unpaid'
                CHECK(payment_status IN ('paid', 'unpaid')),
            payment_reference TEXT,
            delivery_date TEXT,
            route_details TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (warehouse_id) REFERENCES warehouses(id),
            FOREIGN KEY (assigned_driver_id) REFERENCES users(id)
        )
    """)