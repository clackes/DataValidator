from faker import Faker
import random
import json
import csv
import xml.etree.ElementTree as ET
import pandas as pd

fake = Faker('it_IT')

def generate_fake_customer(valid=True):
    customer = {
        "id": fake.uuid4(),
        "name": fake.word().capitalize() + " " + fake.word().capitalize(),
        "description": fake.sentence(nb_words=12),
        "price": round(random.uniform(5.0, 500.0), 2),
        "currency": "EUR",
        "sku": fake.bothify(text='???-########'),
        "category": random.choice(["Elettronica", "Abbigliamento", "Casa", "Sport", "Giochi", "Libri"]),
        "stock_quantity": random.randint(0, 1000),
        "available": random.choice([True, False]),
        "created_at": fake.date_time_between(start_date='-2y', end_date='now').isoformat(),
        "updated_at": fake.date_time_between(start_date='-1y', end_date='now').isoformat(),
        "weight_kg": round(random.uniform(0.1, 10.0), 2),
    }

    if not valid:
        customer["email"] = "email_non_valida"
        customer["postal_code"] = "ABCDE"
        customer["birth_date"] = "3000-01-01"

    return customer

if __name__ == "__main__":
    customers = []

    for _ in range(50):
        customers.append(generate_fake_customer(valid=True))
    #for _ in range(10):
    #    customers.append(generate_fake_customer(valid=False))
# 1. JSON
    with open("data/products.json", "w", encoding="utf-8") as f:
        json.dump(customers, f, ensure_ascii=False, indent=4)

    # 2. CSV
    csv_fields = list(customers[0].keys())
    with open("data/products.csv", "w", newline='', encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=csv_fields)
        writer.writeheader()
        writer.writerows(customers)

    # 3. XML
    root = ET.Element("products")
    for p in customers:
        prod_elem = ET.SubElement(root, "product")
        for key, value in p.items():
            ET.SubElement(prod_elem, key).text = str(value)
    tree = ET.ElementTree(root)
    tree.write("data/products.xml", encoding="utf-8", xml_declaration=True)

    # 4. XLSX
    df = pd.DataFrame(customers)
    df.to_excel("data/products.xlsx", index=False)