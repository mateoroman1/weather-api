import sqlite3
from contextlib import contextmanager
import os
import config
import json

from models.schemas import RequestRecord

@contextmanager
def get_db():

    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row

    try:
        yield conn

    finally:
        conn.commit()
        conn.close()

def init_db():

    os.makedirs(os.path.dirname(config.DATABASE_PATH), exist_ok=True)

    with get_db() as conn:
        cursor = conn.cursor()

        cursor.execute('''
                    CREATE TABLE IF NOT EXISTS weather_requests (
                    id INTEGER PRIMARY KEY,
                    response INTEGER,
                    timestamp TEXT NOT NULL,
                    requested_location TEXT NOT NULL,
                    resolved_location TEXT NOT NULL,
                    latitude REAL NOT NULL,
                    longitude REAL NOT NULL,
                    data TEXT)
                    ''')

class WeatherRepository:
    def __init__(self):
        init_db()

    def save_request(self, record: RequestRecord):
        with get_db() as conn:
            cursor = conn.cursor()

            statement = "INSERT INTO weather_requests (" \
            "id, " \
            "response, " \
            "timestamp, " \
            "requested_location, " \
            "resolved_location," \
            "latitude, " \
            "longitude, " \
            "data" \
            ") VALUES (?, ?, ?, ?, ?, ?, ?, ?)"

            cursor.execute(statement, (
                record.id,
                record.response,
                record.timestamp,
                record.requested_location,
                record.resolved_location,
                record.latitude,
                record.longitude,
                json.dumps(record.data)
            ))

            return cursor.lastrowid

    def get_request_history(self):
        # Pagination would be a good idea for this
        with get_db() as conn:
            cursor = conn.cursor()

            statement = "SELECT * FROM weather_requests ORDER BY timestamp"

            cursor.execute(statement)

            rows = cursor.fetchall()

            # ty Google AI
            return [RequestRecord(**dict(row)) for row in rows]