# tests/test_api.py

import requests
import json

BASE_URL = "http://127.0.0.1:8000"


def test_upload_file():
    with open("./data/customers.json", "rb") as f:
        response = requests.post(f"{BASE_URL}/upload", files={"file": f})
    print("Upload:", response.status_code, response.json())


def test_validate_file():
    flags = {
        "birth_date": False,
        "postal_code": False
    }
    response = requests.post(
        f"{BASE_URL}/validate",
        data={
            "filename": "customers.json",
            "flags_json": json.dumps(flags)
        }
    )
    print("Validate File:", response.status_code, response.json())


def test_validate_record():
    record = {
        "id": "abc123",
        "name": "Mario Rossi",
        "email": "mario@example.com",
        "birth_date": "1985-06-15",
        "phone_number": "+393931234567",
        "address": "Via Roma, 1",
        "city": "Roma",
        "postal_code": 10010,
        "state": "Lazio",
        "country": "Italia",
        "latitude": 41.9028,
        "longitude": 12.4964
    }
    flags = {
        "geolocation": False
    }
    response = requests.post(
        f"{BASE_URL}/validate/record",
        json=record,
        params={"flags_json": json.dumps(flags)}
    )
    print("Validate Record:", response.status_code, response.json())


if __name__ == "__main__":
    test_upload_file()
    test_validate_file()
    test_validate_record()
