import pandas as pd
import xml.etree.ElementTree as ET

def convert_csv_to_excel(csv_file_path, excel_file_path):
    df = pd.read_csv(csv_file_path)
    df.to_excel(excel_file_path, index=False)
    print(f"✅ File Excel creato: {excel_file_path}")

def convert_csv_to_xml(csv_file_path, xml_file_path):
    df = pd.read_csv(csv_file_path)

    root = ET.Element('customers')

    for _, row in df.iterrows():
        customer = ET.SubElement(root, 'customer')
        for field in df.columns:
            field_element = ET.SubElement(customer, field)
            field_element.text = str(row[field]) if pd.notnull(row[field]) else ''

    tree = ET.ElementTree(root)
    tree.write(xml_file_path, encoding='utf-8', xml_declaration=True)
    print(f"✅ File XML creato: {xml_file_path}")

if __name__ == "__main__":
    csv_file = "./data/customers.csv"        
    excel_file = "./data/customers.xlsx"
    xml_file = "./data/customers.xml"

    convert_csv_to_excel(csv_file, excel_file)
    convert_csv_to_xml(csv_file, xml_file)
