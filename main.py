# main.py

from validator.core import Validatore

if __name__ == "__main__":
    files = ["xml", "json", "csv", "xlsx"]
    flags = {
        "birth_date": False,
        "email": False,
        "postal_code": False,
        #"geolocation": False
    }
    for filetype in files:
        file = f"./data/customers.{filetype}"
        report_path = f"./output/reports/validation_report{filetype}.txt"
        print(f"\nValidazione file: '{file}'")
        v = Validatore(file, flags)
        v.main()
        print(f"✅ Clienti validi trovati: {len(v.valid_customers)}")
        print(f"❌ Clienti invalidi trovati: {len(v.invalid_customers)}")
        v.generate_validation_report(report_path)
