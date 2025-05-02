# validator/io_handlers.py
import os
import json
import csv
import pandas as pd
import xml.etree.ElementTree as ET

def save_validate_data(self):
    base_name = self.file_path.split("./data/")[1].split(".")[0]
    valid_data = [customer.model_dump(mode='json') for customer in self.valid_input]

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

    #if "xml" in self.file_path:
    #    root = ET.Element('input')
    #    for customer in valid_data:
    #        cust_elem = ET.SubElement(root, 'customer')
    #        for key, value in customer.items():
    #            field = ET.SubElement(cust_elem, key)
    #            field.text = str(value)
    #    tree = ET.ElementTree(root)
    #    tree.write(f"./output/valid/{base_name}_valid.xml", encoding='utf-8', xml_declaration=True)
    invalid_data = self.invalid_input

    if "json" in self.file_path:
        with open(f"./output/invalid/{base_name}_invalid.json", 'w', encoding='utf-8') as f:
            processed = [
                {
                    "data": entry['data'],
                    "error": "; ".join(entry['error']) if isinstance(entry['error'], list) else str(entry['error'])
                } for entry in invalid_data
            ]
            json.dump(processed, f, ensure_ascii=False, indent=4)

    if "csv" in self.file_path:
        with open(f"./output/invalid/{base_name}_invalid.csv", mode='w', encoding='utf-8', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=['data', 'error'])
            writer.writeheader()
            for item in invalid_data:
                writer.writerow({
                    'data': json.dumps(item['data'], ensure_ascii=False),
                    'error': "; ".join(item['error']) if isinstance(item['error'], list) else str(item['error'])
                })

    if "xlsx" in self.file_path:
        processed = [
            {
                "data": json.dumps(entry['data'], ensure_ascii=False),
                "error": "; ".join(entry['error']) if isinstance(entry['error'], list) else str(entry['error'])
            } for entry in invalid_data
        ]
        df_invalid = pd.DataFrame(processed)
        df_invalid.to_excel(f"./output/invalid/{base_name}_invalid.xlsx", index=False)

    #if "xml" in self.file_path:
    #    root_invalid = ET.Element('invalid_input')
    #    for entry in invalid_data:
    #        cust_elem = ET.SubElement(root_invalid, 'customer')
    #        data_elem = ET.SubElement(cust_elem, 'data')
    #        data_elem.text = json.dumps(entry['data'], ensure_ascii=False)
    #        error_elem = ET.SubElement(cust_elem, 'error')
    #        error_elem.text = "; ".join(entry['error']) if isinstance(entry['error'], list) else str(entry['error'])
    #    tree = ET.ElementTree(root_invalid)
    #    tree.write(f"./output/invalid/{base_name}_invalid.xml", encoding='utf-8', xml_declaration=True)

    print("✅ Dati salvati correttamente!")
