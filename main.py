# main.py

from models.customer_model import Customer
from pydantic import ValidationError
import csv

file_path="./data/valid_customers.csv"

class Validatore:
    def __init__(self,):
        self.valid_customers = []
        self.invalid_customers = []

    def csv_validator(self):
        with open(file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:
                self.customer_validator(row)

        return self.valid_customers, self.invalid_customers

    def customer_validator(self, data):
        try:
            customer = Customer(**data)
            self.valid_customers.append(customer)
        except (ValidationError, ValueError) as e:
            self.invalid_customers.append({
                "data": data,
                "error": str(e)
            })



if __name__ == "__main__":
    valid_customers, invalid_customers = Validatore().csv_validator()

    print(f"✅ Clienti validi trovati: {len(valid_customers)}")
    print(f"❌ Clienti invalidi trovati: {len(invalid_customers)}")

