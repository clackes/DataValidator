import csv
import json

csv_file_path = './data/customers.csv'   
json_file_path = './data/customers.json'   

data = []

with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        data.append({
            "id": row["id"],
            "name": row["name"],
            "email": row["email"],
            "birth_date": row["birth_date"],
            "phone_number": row["phone_number"],
            "address": row["address"],
            "city": row["city"],
            "postal_code": row["postal_code"],
            "state": row["state"],
            "country": row["country"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"])
        })

with open(json_file_path, mode='w', encoding='utf-8') as jsonfile:
    json.dump(data, jsonfile, indent=4, ensure_ascii=False)

print(f"✅ File JSON creato: {json_file_path}")
