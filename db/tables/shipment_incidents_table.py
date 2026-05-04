from db.tables.registry import register


@register
def create_shipment_incidents_table(connection):
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS shipment_incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shipment_id INTEGER NOT NULL,
            incident_type TEXT NOT NULL CHECK(incident_type IN (
                'delay',
                'damage',
                'lost',
                'route_change',
                'failed_attempt',
                'other'
            )),
            description TEXT,
            status TEXT NOT NULL DEFAULT 'open'
                CHECK(status IN ('open', 'resolved', 'closed')),
            reported_by INTEGER,
            reported_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            resolution_note TEXT,

            FOREIGN KEY (shipment_id) REFERENCES shipments(id),
            FOREIGN KEY (reported_by) REFERENCES users(id)
        )
    """)
