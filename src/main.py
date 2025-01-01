import asyncio
import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic
from typing import Annotated

from config import port as api_port
from database.database_check import check_database_tables
from routes import station_alias_router
from schedule_utils import setup_schedules
from security import check_credentials


app = FastAPI()
security = HTTPBasic()

# Add the router for the station aliases
app.include_router(station_alias_router)


@app.get("/")
async def get_root():
    return {"message": "Server is running"}


@app.get("/{version}/credentials-check")
async def do_credentials_check(username: Annotated[str, Depends(check_credentials)]):
    return {"message": f"Welcome, {username}!"}


async def setup_rest_api_server():
    "Starts the FastAPI REST server."
    config_params = {"app": app, "host": "0.0.0.0", "port": api_port}
    rest_server = uvicorn.Server(config=uvicorn.Config(**config_params))
    await rest_server.serve()


async def main():
    "Uses asyncio tasks to avoid the schedule library blocking uvicorn."
    rest_server_task = asyncio.create_task(setup_rest_api_server())
    schedules_task = asyncio.create_task(setup_schedules())
    await asyncio.gather(rest_server_task, schedules_task)


if __name__ == "__main__":
    try:
        # Check the alias table before starting the app
        check_database_tables()

        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print("Error in main:", e)
