from db.tables.registry import register


@register
def create_vehicles_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            vehicle_code TEXT UNIQUE NOT NULL,
            capacity INTEGER NOT NULL,
            status TEXT NOT NULL DEFAULT 'available'
                CHECK(status IN (
                    'available',
                    'in_use',
                    'maintenance'
                )),
            assigned_driver_id INTEGER,
            last_service_date TEXT,
            maintenance_due_date TEXT,

            FOREIGN KEY (assigned_driver_id) REFERENCES users(id)
        )
    """)