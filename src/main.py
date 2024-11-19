import uvicorn
from fastapi import FastAPI, Depends
from fastapi.security import HTTPBasic
from typing import Annotated

from config import port as api_port
from database import check_alias_table
from routes import station_alias_router
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


if __name__ == "__main__":
    # Check the alias table before starting the app
    check_alias_table()

    uvicorn.run(app, host="0.0.0.0", port=api_port)
