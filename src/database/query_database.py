import sqlite3
from loguru import logger
from typing import Tuple

from database import database_file


def get_modified_rows_count(
    table_name: str, db_file: str = database_file
) -> int | None:
    """
    Returns the count of modified rows in the specified table. Used to find out
    if there are any modified rows in the database, to determine if a backup
    needs to be taken. In case of error, returns None to be handled by caller.
    """
    query = f"SELECT COUNT(is_modified) FROM {table_name} WHERE is_modified = 1;"
    try:
        with sqlite3.connect(db_file) as conn:
            return conn.execute(query).fetchone()[0]
    except Exception as e:
        logger.error(f"Exception during get_modified_rows_count: {e}")
        return None


def get_all_database_aliases(
    db_file: str = database_file,
) -> list[Tuple[int, str, str]]:
    """Returns all aliases in the database."""
    query = "SELECT pool_code, name, alias FROM station_alias"
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
