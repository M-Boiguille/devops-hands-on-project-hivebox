"""
HiveBox Project - Temperature Monitoring API
DevOpsRoadmap.io

FastAPI application that aggregates temperature measurements from multiple
senseBox IoT devices and provides endpoints for version checking and
temperature data retrieval.
"""
import os
from fastapi import FastAPI, Depends, HTTPException
from . import helpers

app = FastAPI()

# Load config once at startup
def load_conf():
    try:
        return helpers.load_config()
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Configuration load failed") from exc


@app.get("/")
async def root():
    """
    Health check endpoint.
    
    Returns:
        dict: Simple status message
    """
    return {"message": "Hello World"}


@app.get("/version")
async def get_version(config=Depends(load_conf)):
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
    try:
        # Validate that config has version key
        if "version" not in config:
            raise HTTPException(status_code=500, detail="Version not found in configuration")

        app_version = os.getenv("APP_VERSION")
        if not helpers.is_semantic(app_version):
            message = f"Error: invalid app version ({app_version})"
            raise HTTPException(status_code=500, detail=message)
        return {"version": app_version}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc


@app.get("/temperature")
async def get_temperature(config=Depends(load_conf)):
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
        dict: {"temperature": float} with average of recent measurements
    
    Examples:
        >>> GET /temperature
        {"temperature": 22.5}
    """
    try:
        avg_temp = helpers.get_average_temperature(config)
        if avg_temp is None:
            raise HTTPException(status_code=503, detail="No temperature data available")
        return {"temperature": avg_temp}
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e)) from e
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail="Internal server error") from exc
