import psycopg  # ty:ignore[unresolved-import]  # noqa: F401
from psycopg.rows import dict_row  # ty:ignore[unresolved-import]


def get_db_connection():
    try:
        conn = psycopg.connect(
            host="127.0.0.1",
            dbname="library_management_system",
            user="postgres",
            password="lol",
            port=5432,
            row_factory=dict_row,
        )
        return conn
    except Exception as e:
        raise RuntimeError(f"Failed to connect to the database: {e}")
    finally:
        print("Database connection attempt finished.")
