import requests
import json

def test_fetch_last_hour_data():
    url = "http://127.0.0.1:8000/fetch_last_hour_data"
    response = requests.get(url)
    print("Testing fetch_last_hour_data endpoint...")
    if response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed with status code: {response.status_code}")

def test_predict():
    url = "http://127.0.0.1:8000/predict?timestamp=2024-06-24T06:00:00"
    response = requests.get(url)
    print("Testing predict endpoint...")
    if response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed with status code: {response.status_code}")

def test_fetch_preprocess_finetune():
    url = "http://127.0.0.1:8000/fetch_preprocess_finetune?hours=24"
    response = requests.post(url)
    print("Testing fetch_preprocess_finetune endpoint...")
    if response.status_code == 200:
        print("Success!")
        print(json.dumps(response.json(), indent=4))
    else:
        print(f"Failed with status code: {response.status_code}")

if __name__ == "__main__":
    test_fetch_last_hour_data()
    test_predict()
    test_fetch_preprocess_finetune()
    input("Press Enter to close...")
