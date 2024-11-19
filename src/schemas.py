from pydantic import BaseModel
from typing import Optional

from database import get_all_database_aliases


class StationAlias(BaseModel):
    pool_code: int
    station_name: str
    station_alias: Optional[str]

    def model_dump(self, **kwargs) -> dict:
        """Function overload for JSON compatible output keys"""
        data = super().model_dump(**kwargs)
        return {
            "pool-code": data["pool_code"],
            "station-name": data["station_name"],
            "station-alias": data["station_alias"],
        }


def station_alias_dump(
    pool_code: int, station_name: str, station_alias: Optional[str]
) -> dict:
    """Helper function to dump a station alias class"""
    alias: str = station_alias if station_alias else station_name
    return StationAlias(
        pool_code=pool_code, station_name=station_name, station_alias=alias
    ).model_dump()


def get_all_aliases() -> list[dict]:
    """For each row, provides an alias dump as a dictionary"""
    return [station_alias_dump(*row) for row in get_all_database_aliases()]
