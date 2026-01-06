"""
HiveBox Project - Temperature Monitoring API
DevOpsRoadmap.io

FastAPI application that aggregates temperature measurements from multiple
senseBox IoT devices and provides endpoints for version checking and
temperature data retrieval.
"""
import os
from fastapi import FastAPI
import helpers

app = FastAPI()

# Load config once at startup
config = helpers.load_config("/app/config.json")


@app.get("/")
async def root():
    """
    Health check endpoint.
    
    Returns:
        dict: Simple status message
    """
    return {"message": "Hello World"}


@app.get("/version")
async def get_version():
    """
    Get application version endpoint.
    
    Reads APP_VERSION environment variable and validates it follows
    semantic versioning (X.Y.Z format).
    
    Returns:
        dict: Either {"version": "vX.Y.Z"} or error message
    
    Examples:
        >>> GET /version
        {"version": "v1.2.3"}
    """
    app_version = os.getenv("APP_VERSION")
    if not helpers.is_semantic(app_version):
        return {"message": "Error: invalid app version"}
    return {"version": f"v{app_version}"}


@app.get("/temperature")
async def get_temperature():
    """
    Get average temperature from all configured senseBox devices.
    
    Fetches current temperature measurements from multiple senseBox IoT devices
    configured in the config.json file. Only includes measurements that are
    recent (within last_measure_delta days).
    
    Environment Variables:
        - OPEN_SENSEBOX_API_URL: Base URL for senseBox API
        - APP_VERSION: (used by /version endpoint)
    
    Config (from /app/config.json):
        - senseBoxIDs: List of senseBox device IDs
        - last_measure_delta: Maximum age of measurements in days
    
    Returns:
        dict: {"average_temperature": int} with average of recent measurements
        None: If API URL not configured
    
    Examples:
        >>> GET /temperature
        {"average_temperature": 22}
    """
    total_of_temp = 0
    nb_of_temp = 0
    api_url = os.getenv("OPEN_SENSEBOX_API_URL")

    if not api_url:
        return None

    for box_id in config["senseBoxIDs"]:
        url = api_url + box_id
        box = helpers.fetch_sensor_info(url)
        temp = helpers.extract_temp(box, config["last_measure_delta"])
        if temp is None:
            continue
        nb_of_temp += 1
        total_of_temp += temp

    return {"average_temperature": int(total_of_temp / nb_of_temp)}
