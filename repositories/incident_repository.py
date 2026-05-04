import logging
from db.connection import DatabaseConnection

logger = logging.getLogger(__name__)


class IncidentRepository:
    def __init__(self):
        self.db = DatabaseConnection()

    def create_incident(self, shipment_id, incident_type, description, reported_by):
        query = """
            INSERT INTO shipment_incidents
            (shipment_id, incident_type, description, reported_by)
            VALUES (?, ?, ?, ?)
        """
        try:
            self.db.execute_update(query, (shipment_id, incident_type, description, reported_by))
            return True
        except Exception as e:
            logger.error(f"Incident create error: {e}")
            return False

    def list_by_shipment(self, shipment_id):
        query = """
            SELECT * FROM shipment_incidents
            WHERE shipment_id = ?
            ORDER BY reported_at DESC
        """
        return [dict(r) for r in self.db.execute_query(query, (shipment_id,))]

    def resolve_incident(self, incident_id, resolution_note):
        query = """
            UPDATE shipment_incidents
            SET status = 'resolved', resolved_at = CURRENT_TIMESTAMP, resolution_note = ?
            WHERE id = ?
        """
        try:
            self.db.execute_update(query, (resolution_note, incident_id))
            return True
        except Exception as e:
            logger.error(f"Incident resolve error: {e}")
            return False
