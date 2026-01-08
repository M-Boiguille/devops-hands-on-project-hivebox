import os
import re
import json
from datetime import datetime, timedelta, timezone
import requests

def is_semantic(version: str | None):
    """
    Validate if a version string follows semantic versioning format (X.Y.Z).
    
    Args:
        version: Version string to validate (e.g., "1.2.3")
    
    Returns:
        bool: True if version matches semantic versioning pattern, False otherwise
    
    Examples:
        >>> is_semantic("1.2.3")
        True
        >>> is_semantic("1.2")
        False
        >>> is_semantic(None)
        False
    """
    if not version:
        return False
    pattern = r"\d+\.\d+\.\d+"
    if re.fullmatch(pattern, version):
        return True
    return False

def fetch_sensor_info(url: str) -> dict:
    """
    Fetch sensor information from a remote API endpoint.
    
    Args:
        url: The API endpoint URL to fetch sensor data from
    
    Returns:
        dict: Parsed JSON response from the API, or empty dict if request fails
    
    Note:
        - Timeout is set to 5 seconds
        - Exceptions are silently caught and return empty dict
    """
    try:
        response = requests.get(url, timeout=5)
        # response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError, KeyError):
        return {}

def time_less_than_delta(sensor: dict, delta: int) -> float | None:
    """
    Extract temperature value if measurement is within the specified time delta.
    
    Args:
        sensor: Sensor data dict containing lastMeasurement with createdAt and value
        delta: Time delta in days to check against current UTC time
    
    Returns:
        float: Temperature value if measurement is recent, None otherwise
    
    Raises:
        KeyError: If required keys (lastMeasurement, createdAt, value) are missing
        ValueError: If ISO timestamp cannot be parsed
    """
    measurement = sensor["lastMeasurement"]
    iso_time = measurement["createdAt"].replace("Z", "+00:00")
    f_time = datetime.fromisoformat(iso_time)
    if f_time >= datetime.now(timezone.utc) - timedelta(delta):
        return None
    return float(measurement["value"])

def extract_temp(data: dict, delta: int) -> float | None:
    """
    Extract temperature measurement from sensor data dictionary.
    
    Searches for a sensor with title "Temperatur" and returns its value
    if the measurement is recent (within delta days).
    
    Args:
        data: Dictionary containing "sensors" list with sensor objects
        delta: Time delta in days for measurement freshness check
    
    Returns:
        float: Temperature value if found and recent, None otherwise
    
    Note:
        Gracefully handles missing keys, type errors, and value errors
    """
    try:
        sensors = data["sensors"]
        for sensor in sensors:
            if sensor.get("title") == "Temperatur":
                return time_less_than_delta(sensor, delta)
        return None
    except (KeyError, TypeError, ValueError):
        return None

def get_average_temperature(config: dict) -> float | None:
    """
    Calculate average temperature from all configured senseBox devices.
    
    Args:
        config: Configuration dictionary containing senseBoxIDs and last_measure_delta
    
    Returns:
        float: Average temperature from recent measurements, or None if no data
    
    Raises:
        ValueError: If data is too old or invalid
        Exception: For other unexpected errors
    """
    api_url = os.getenv("OPEN_SENSEBOX_API_URL")
    if not api_url:
        return None
 
    total_of_temp = 0
    nb_of_temp = 0

    for box_id in config.get("senseBoxIDs", []):
        url = api_url + box_id
        box = fetch_sensor_info(url)
        temp = extract_temp(box, config.get("last_measure_delta", 1))
        if temp is None:
            continue
        nb_of_temp += 1
        total_of_temp += temp

    if nb_of_temp == 0:
        return None

    return total_of_temp / nb_of_temp


def load_config(path: str | None = None) -> dict:
    """
    Load JSON configuration file from filesystem.
    
    Args:
        path: File path to JSON configuration file
    
    Returns:
        dict: Parsed JSON configuration object
    
    Raises:
        FileNotFoundError: If configuration file does not exist
        json.JSONDecodeError: If file content is not valid JSON
    """
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(path, encoding="utf-8") as f:
        return json.load(f)
