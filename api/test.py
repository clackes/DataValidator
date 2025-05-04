# tests/test_api.py

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_upload_file(flags, f):
    
    response = requests.post(
        f"{BASE_URL}/upload", 
        files={"file": f},
        data={"flags_json": json.dumps(flags)})
    print("Upload:", response.status_code, response.json())

def test_validate_record(record, flags):

    response = requests.post(
        f"{BASE_URL}/validate/record",
        json=record,
        params={"flags_json": json.dumps(flags)}
    )
    print("Validate Record:", response.status_code, response.json())

def test_load_schema(file_path:str = "./models/model_schema.json"):
    with open("./models/model_schema.json", "rb") as f:
        response = requests.post(f"{BASE_URL}/schema/load", files={"schema_file": f})
    print("Load Schema:", response.status_code, response.json())

if __name__ == "__main__":

    test_load_schema("./models/model_schema.json")
    files = ["xml", "json", "csv", "xlsx"]
    for filetype in files:
        with open(f"./data/customers.{filetype}", "rb") as f:
            test_upload_file({
                "birth_date": False,
                "email": False,
                "postal_code": False,
                "geolocation": False
            },f)
    test_validate_record({
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
    },
    {
        "geolocation": False
    }
    )

