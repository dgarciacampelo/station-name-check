from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import HTTPBasic
from typing import Annotated

from config import version as api_version
from database.query_database import (
    delete_database_alias,
    insert_database_alias,
    update_database_alias,
)
from schemas import station_alias_dump, get_all_aliases
from security import check_credentials

router = APIRouter()
security = HTTPBasic()

version: str = api_version


"""
This section defines REST API routes to check OCPP station names and aliases.
A station alias is a service that allows a OCPP station name to be changed
without the need to setup the station again.
"""

known_station_aliases: dict[int, str] = dict()


def get_seach_key(pool_code: int, station_name: str) -> int:
    """Provides the logic that allows to find a station alias"""
    return hash((pool_code, station_name))


for item in get_all_aliases():
    search_key: int = get_seach_key(item["pool-code"], item["station-name"])
    known_station_aliases[search_key] = item["station-alias"]


@router.get("/{version}/station-alias/{pool_code}/{station_name}")
async def get_station_alias(
    pool_code: int,
    station_name: str,
    username: Annotated[str, Depends(check_credentials)],
):
    """If an alias was not defined, return the original station name"""
    result: str = station_name
    search_key = get_seach_key(pool_code, station_name)
    if search_key in known_station_aliases:
        result = known_station_aliases[search_key]

    return station_alias_dump(pool_code, station_name, result)


@router.post(
    "/{version}/station-alias/{pool_code}/{station_name}/{station_alias}",
    status_code=status.HTTP_201_CREATED,
)
async def set_station_alias(
    pool_code: int,
    station_name: str,
    station_alias: str,
    username: Annotated[str, Depends(check_credentials)],
):
    """Define a new alias for a station name"""
    search_key = get_seach_key(pool_code, station_name)
    if search_key in known_station_aliases:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Station {station_name} already has an alias",
        )

    known_station_aliases[search_key] = station_alias
    insert_database_alias(pool_code, station_name, station_alias)

    return station_alias_dump(pool_code, station_name, station_alias)


@router.put(
    "/{version}/station-alias/{pool_code}/{station_name}/{station_alias}",
    status_code=status.HTTP_200_OK,
)
async def update_station_alias(
    pool_code: int,
    station_name: str,
    station_alias: str,
    username: Annotated[str, Depends(check_credentials)],
):
    """Update an existing alias for a station name"""
    search_key = get_seach_key(pool_code, station_name)
    if search_key not in known_station_aliases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station {station_name} not found",
        )

    known_station_aliases[search_key] = station_alias
    update_database_alias(pool_code, station_name, station_alias)

    return station_alias_dump(pool_code, station_name, station_alias)


@router.delete(
    "/{version}/station-alias/{pool_code}/{station_name}",
    status_code=status.HTTP_200_OK,
)
async def delete_station_alias(
    pool_code: int,
    station_name: str,
    username: Annotated[str, Depends(check_credentials)],
):
    """Delete an existing alias for a station name"""
    search_key = get_seach_key(pool_code, station_name)
    if search_key not in known_station_aliases:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Station {station_name} not found",
        )

    station_alias: str = known_station_aliases[search_key]
    del known_station_aliases[search_key]
    delete_database_alias(pool_code, station_name)

    return station_alias_dump(pool_code, station_name, station_alias)


station_alias_router = router
