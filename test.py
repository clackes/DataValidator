# tests/test_api.py

import requests
import json

BASE_URL = "http://127.0.0.1:8000"

def test_upload_file(flags, f):
    
    response = requests.post(
        f"{BASE_URL}/upload", 
        files={"file": f},
        data={"flags_json": json.dumps(flags)})
    try:
        print("Upload:", response.status_code, response.json())
    except requests.exceptions.JSONDecodeError:
        print("Upload (non-JSON):", response.status_code, response.text)


def test_validate_record(record, flags):

    response = requests.post(
        f"{BASE_URL}/validate/record",
        json=record,
        params={"flags_json": json.dumps(flags)}
    )
    print("Validate Record:", response.status_code, response.json())

def test_load_schema(file_path:str):
    with open(file_path, "rb") as f:
        response = requests.post(f"{BASE_URL}/schema/load", files={"schema_file": f})
    print("Load Schema:", response.status_code, response.json())

if __name__ == "__main__":

    test_load_schema("model_schema1.json")
    files = ["xml", "json", "csv", "xlsx"]
    for filetype in files:
        with open(f"./data/products.{filetype}", "rb") as f:
            test_upload_file({
                "updated_at":False,
                "geolocation": False
            },f)

    test_validate_record({
        "id": "prod001",
        "name": "Cuffie Wireless",
        "description": "Cuffie Bluetooth con cancellazione del rumore e autonomia di 30 ore.",
        "price": 89.99,
        "currency": "EUR",
        "sku": "CWF-12345678",
        "category": "Elettronica",
        "stock_quantity": 150,
        "available": True,
        "created_at": "2023-08-10T14:30:00",
        "updated_at": "2024-04-22T09:15:00",
        "weight_kg": 0.25
    },
    {
        "geolocation": False
    })


    test_load_schema("model_schema2.json")
    files = ["xml", "json", "csv", "xlsx"]
    for filetype in files:
        with open(f"./data/customers.{filetype}", "rb") as f:
            test_upload_file({
                "birth_date":False,
                "phone_number":False,
                "email":False,
                "postal_code":False,
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
        "updated_at":False,
        "geolocation": False
    }
    )


