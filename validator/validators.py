# validator/validators.py
import csv
import json
import pandas as pd
import xml.etree.ElementTree as ET

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