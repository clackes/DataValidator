# main.py

from models.customer_model import Customer
from pydantic import ValidationError
import csv
import json
import pandas as pd
import xml.etree.ElementTree as ET
import os
from datetime import datetime


class Validatore:
    def __init__(self, file_path:str):
        self.valid_customers = []
        self.invalid_customers = []
        self.file_path= file_path
        self.supported_files = [".xml", ".json", ".csv", ".xlsx"]
        self.check_filetype()

    def check_filetype(self):
        if any(filetype in self.file_path for filetype in self.supported_files):
            print("✅ FileType supported.")
        else:
            print("❌ FileType not supported.")        
    def main(self,):
        if "xml" in self.file_path:
            v.xml_validator()
        if "json" in self.file_path:
            v.json_validator()
        if "csv" in self.file_path:
            v.csv_validator()
        if "xlsx" in self.file_path:
            v.excel_validator()
        self.save_validate_data()
        

    def save_validate_data(self):
        base_name = self.file_path.split("./data/")[1].split(".")[0]
        valid_data = [customer.model_dump(mode='json') for customer in self.valid_customers]
        if "json" in self.file_path:
            with open(f"./output/valid/{base_name}_valid.json", 'w', encoding='utf-8') as f:
                json.dump(valid_data, f, ensure_ascii=False, indent=4)
        if "csv" in self.file_path:
            with open(f"./output/valid/{base_name}_valid.csv", mode='w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=valid_data[0].keys())
                writer.writeheader()
                writer.writerows(valid_data)
        if "xlsx" in self.file_path:
            df = pd.DataFrame(valid_data)
            df.to_excel(f"./output/valid/{base_name}_valid.xlsx", index=False)
        if "xml" in self.file_path:
            root = ET.Element('customers')
            for customer in valid_data:
                cust_elem = ET.SubElement(root, 'customer')
                for key, value in customer.items():
                    field = ET.SubElement(cust_elem, key)
                    field.text = str(value)
            tree = ET.ElementTree(root)
            tree.write(f"./output/valid/{base_name}_valid.xml", encoding='utf-8', xml_declaration=True)
        invalid_data = self.invalid_customers
        if "json" in self.file_path:
            with open(f"./output/invalid/{base_name}_invalid.json", 'w', encoding='utf-8') as f:
                json.dump(invalid_data, f, ensure_ascii=False, indent=4)
        if "csv" in self.file_path:
            with open(f"./output/invalid/{base_name}_invalid.csv", mode='w', encoding='utf-8', newline='') as f:
                fieldnames = ['data', 'error']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in invalid_data:
                    writer.writerow({
                        'data': json.dumps(item['data'], ensure_ascii=False),
                        'error': item['error']
                    })
        if "xlsx" in self.file_path:
            df_invalid = pd.DataFrame(invalid_data)
            df_invalid.to_excel(f"./output/invalid/{base_name}_invalid.xlsx", index=False)
        if "xml" in self.file_path:
            root_invalid = ET.Element('invalid_customers')
            for entry in invalid_data:
                cust_elem = ET.SubElement(root_invalid, 'customer')
                data_elem = ET.SubElement(cust_elem, 'data')
                data_elem.text = json.dumps(entry['data'], ensure_ascii=False)
                error_elem = ET.SubElement(cust_elem, 'error')
                error_elem.text = entry['error']
            tree = ET.ElementTree(root_invalid)
            tree.write(f"./output/invalid/{base_name}_invalid.xml", encoding='utf-8', xml_declaration=True)
        print("✅ Dati salvati correttamente!")

    def generate_validation_report(self, valid_customers, invalid_customers, report_path="./output/reports/validation_report.txt"):
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        total_valid = len(valid_customers)
        total_invalid = len(invalid_customers)
        error_summary = {}
        for invalid_entry, errors in invalid_customers:
            if isinstance(errors, list):
                for error in errors:
                    if isinstance(error, dict):
                        error_type = error.get('msg', 'Errore sconosciuto')
                    else:
                        error_type = error or 'Errore sconosciuto'
                    
                    error_summary[error_type] = error_summary.get(error_type, 0) + 1
            else:
                error_type = errors or 'Errore sconosciuto'
                error_summary[error_type] = error_summary.get(error_type, 0) + 1
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(f"=== Validation Report ===\n")
            f.write(f"Data validazione: {now}\n")
            f.write(f"\n")
            f.write(f"Totale clienti validi: {total_valid}\n")
            f.write(f"Totale clienti invalidi: {total_invalid}\n")
            f.write(f"\n")
            f.write(f"--- Riepilogo errori trovati ---\n")
            for error, count in error_summary.items():
                f.write(f"{error}: {count} occorrenze\n")
        print(f"✅ Validation report generato in: {report_path}")

    def customer_validator(self, data:dict):
        try:
            customer = Customer(**data)
            self.valid_customers.append(customer)
        except (ValidationError, ValueError) as e:
            self.invalid_customers.append({
                "data": data,
                "error": str(e)
            })

    def csv_validator(self):
        with open(self.file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                self.customer_validator(row)

    def json_validator(self):
        with open(self.file_path, mode='r', encoding='utf-8') as jsonfile:
            data = json.load(jsonfile)
            for entry in data:
                self.customer_validator(entry)

    def excel_validator(self):
        df = pd.read_excel(self.file_path)

        for _, row in df.iterrows():
            data = row.to_dict()
            self.customer_validator(data)

    def xml_validator(self):
        tree = ET.parse(self.file_path)
        root = tree.getroot()

        for customer_element in root.findall('customer'):
            data = {}
            for field in customer_element:
                data[field.tag] = field.text
            self.customer_validator(data)


if __name__ == "__main__":
    files = ["xml", "json", "csv", "xlsx"]

    for filetype in files:
        file = "./data/customers."+filetype
        report_path = f"./output/reports/validation_report{filetype}.txt"
        print(f"\nValidazione file: '{file}'")
        v = Validatore(file)
        v.main()

        print(f"✅ Clienti validi trovati: {len(v.valid_customers)}")
        print(f"❌ Clienti invalidi trovati: {len(v.invalid_customers)}")
        v.generate_validation_report(v.valid_customers, v.invalid_customers,report_path)
