import requests
import json
from time import sleep

# Base URL of the FastAPI server
BASE_URL = "http://127.0.0.1:8000"

# Log file path
LOG_FILE = "api_test_log.txt"

def log_message(message):
    with open(LOG_FILE, "a") as log_file:
        log_file.write(message + "\n")

def test_fetch_last_hour_data():
    url = f"{BASE_URL}/fetch_last_hour_data"
    response = requests.get(url)
    if response.status_code == 200:
        log_message("fetch_last_hour_data - Success")
        log_message(json.dumps(response.json(), indent=4))
    else:
        log_message("fetch_last_hour_data - Failed")
        log_message(f"Status Code: {response.status_code}")
        log_message(response.text)

def test_predict(timestamp):
    url = f"{BASE_URL}/predict"
    params = {"timestamp": timestamp}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        log_message("predict - Success")
        log_message(json.dumps(response.json(), indent=4))
    else:
        log_message("predict - Failed")
        log_message(f"Status Code: {response.status_code}")
        log_message(response.text)

def test_fetch_preprocess_finetune(hours):
    url = f"{BASE_URL}/fetch_preprocess_finetune"
    params = {"hours": hours}
    response = requests.post(url, params=params)
    if response.status_code == 200:
        log_message("fetch_preprocess_finetune - Success")
        log_message(json.dumps(response.json(), indent=4))
    else:
        log_message("fetch_preprocess_finetune - Failed")
        log_message(f"Status Code: {response.status_code}")
        log_message(response.text)

log_message("Testing fetch_last_hour_data endpoint...")
test_fetch_last_hour_data()

log_message("\nTesting predict endpoint...")
test_predict("2024-06-24T06:00:00")

log_message("\nTesting fetch_preprocess_finetune endpoint...")
test_fetch_preprocess_finetune(24)

input("\nPress Enter to exit...")


