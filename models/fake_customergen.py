# models/fake_customergen.py

from faker import Faker
import csv

fake = Faker('it_IT')  

def generate_fake_customer():
    return {
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

if __name__ == "__main__":
    customers = []
    for _ in range(50):  
        data = generate_fake_customer()
        customers.append(data)
    if customers:
        with open('./data/valid_customers.csv', mode='w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'name', 'email', 'birth_date', 'phone_number', 'address','city', 'postal_code', 'state', 'country', 'latitude', 'longitude']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for customer in customers:
                writer.writerow(customer)
            csvfile.close()
            
        print(f"\n✅ Salvati {len(customers)} clienti validi in 'valid_customers.csv'")
    else:
        print("\n⚠️ Nessun cliente valido da salvare.")
    
