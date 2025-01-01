import sqlite3
from loguru import logger

from database import database_file


def insert_modified_column(table_name: str, db_file: str = database_file) -> bool:
    "Inserts a new modified column into the specified table."
    query = f"""
        ALTER TABLE {table_name}
        ADD COLUMN is_modified INTEGER NOT NULL DEFAULT 1;
    """
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(query)
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"Exception during insert_modified_column in {table_name}: {e}")
        return False


def clear_modified_column(table_name: str, db_file: str = database_file) -> bool:
    "Clears the modified flag in the specified table (after a backup)."
    query = f"UPDATE {table_name} SET is_modified = 0;"
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(query)
            conn.commit()
            return True
    except Exception as e:
        logger.error(f"Exception during clear_modified_column in {table_name}: {e}")
        return False


def check_database_tables(db_file: str = database_file):
    "Checks if al the used tables exist in the database or creates new ones."
    check_station_alias_table(db_file)


def check_station_alias_table(db_file: str = database_file):
    """Checks if the alias table exists or creates a new one."""

    create_table_query = """
    CREATE TABLE IF NOT EXISTS station_alias(
        pool_code INTEGER NOT NULL,
        name TEXT NOT NULL,
        alias TEXT NOT NULL,
        is_modified INTEGER NOT NULL DEFAULT 1,
        PRIMARY KEY (pool_code, name)
        );
    """

    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(create_table_query)
    except Exception as e:
        logger.warning(f"Exception during check_station_alias_table: {e}")
