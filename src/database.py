import sqlite3
from loguru import logger
from typing import Tuple


database_file: str = "database_files/database.sqlite3"


def check_alias_table(db_file: str = database_file):
    """Checks if the alias table exists or creates a new one."""

    create_table_query = """
    CREATE TABLE IF NOT EXISTS station_alias(
        pool_code INTEGER NOT NULL,
        name TEXT NOT NULL,
        alias TEXT NOT NULL,
        PRIMARY KEY (pool_code, name)
        );
    """

    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(create_table_query)
    except Exception as e:
        logger.warning(f"Exception during table station_alias check: {e}")


def get_all_database_aliases(
    db_file: str = database_file,
) -> list[Tuple[int, str, str]]:
    """Returns all aliases in the database."""
    query = "SELECT * FROM station_alias"
    try:
        with sqlite3.connect(db_file) as conn:
            return conn.execute(query).fetchall()
    except Exception as e:
        logger.warning(f"Exception during get_all_database_aliases: {e}")
        return []


def get_database_alias(pool_code: int, station_name: str, db_file: str = database_file):
    """Returns the alias for a given pool code and station name."""
    query = "SELECT alias FROM station_alias WHERE pool_code = ? AND name = ?"
    try:
        with sqlite3.connect(db_file) as conn:
            return conn.execute(query, (pool_code, station_name)).fetchone()
    except Exception as e:
        logger.warning(f"Exception during get_database_alias: {e}")
        return None


def insert_database_alias(
    pool_code: int, station_name: str, alias: str, db_file: str = database_file
):
    """Inserts a new alias into the database."""
    query = "INSERT INTO station_alias (pool_code, name, alias) VALUES (?, ?, ?)"
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(query, (pool_code, station_name, alias))
            conn.commit()
    except Exception as e:
        logger.warning(f"Exception during insert_database_alias: {e}")


def update_database_alias(
    pool_code: int, station_name: str, alias: str, db_file: str = database_file
):
    """Updates an existing alias in the database."""
    query = "UPDATE station_alias SET alias = ? WHERE pool_code = ? AND name = ?"
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(query, (alias, pool_code, station_name))
            conn.commit()
    except Exception as e:
        logger.warning(f"Exception during update_database_alias: {e}")


def delete_database_alias(
    pool_code: int, station_name: str, db_file: str = database_file
):
    """Deletes an existing alias from the database."""
    query = "DELETE FROM station_alias WHERE pool_code = ? AND name = ?"
    try:
        with sqlite3.connect(db_file) as conn:
            conn.execute(query, (pool_code, station_name))
            conn.commit()
    except Exception as e:
        logger.warning(f"Exception during delete_database_alias: {e}")
