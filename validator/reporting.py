# validator/reporting.py
import os
from datetime import datetime

def generate_validation_report(valid_customers, invalid_customers, report_path="./output/reports/validation_report.txt"):
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total_valid = len(valid_customers)
    total_invalid = len(invalid_customers)
    error_summary = {}

    for entry in invalid_customers:
        if isinstance(entry, dict):
            errors = entry.get("error", [])
            if isinstance(errors, list):
                for error in errors:
                    error_summary[error] = error_summary.get(error, 0) + 1
            else:
                error_summary[errors] = error_summary.get(errors, 0) + 1
        else:
            error_summary[str(entry)] = error_summary.get(str(entry), 0) + 1

    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(f"=== Validation Report ===\n")
        f.write(f"Data validazione: {now}\n\n")
        f.write(f"Totale clienti validi: {total_valid}\n")
        f.write(f"Totale clienti invalidi: {total_invalid}\n\n")
        f.write(f"--- Riepilogo errori trovati ---\n")
        for error, count in error_summary.items():
            f.write(f"{error}: {count} occorrenze\n")

    print(f"✅ Validation report generato in: {report_path}")
