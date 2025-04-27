from faker import Faker
import csv
import random

fake = Faker('it_IT')

def generate_fake_customer(valid=True):
    customer = {
        "id": fake.uuid4(),
        "name": fake.name(),
        "email": fake.email(),
        "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=90),
        "phone_number": "+39 3917542572",
        "address": fake.address(),
        "city": fake.city(),
        "postal_code": fake.postcode(),
        "state": fake.state(),
        "country": fake.country(),
        "latitude": fake.latitude(),
        "longitude": fake.longitude(),
    }

    if not valid:
        # Introduciamo errori voluti
        customer["email"] = "email_non_valida"
        customer["postal_code"] = "ABCDE"
        customer["birth_date"] = "3000-01-01"

    return customer

if __name__ == "__main__":
    customers = []

    # 40 validi
    for _ in range(40):
        customers.append(generate_fake_customer(valid=True))

    # 10 invalidi
    for _ in range(10):
        customers.append(generate_fake_customer(valid=False))

    # Mischiamo i clienti
    random.shuffle(customers)

    # Salviamo tutto in un unico file
    if customers:
        with open('./data/customers_mixed.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'email', 'birth_date', 'phone_number', 'address', 'city', 'postal_code', 'state', 'country', 'latitude', 'longitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for customer in customers:
                writer.writerow(customer)
        print(f"\n✅ Salvati {len(customers)} clienti (validi e invalidi) in 'customers_mixed.csv'")
    else:
        print("\n⚠️ Nessun cliente da salvare.")
