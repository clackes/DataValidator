import os
import sqlite3
import json

def save_to_sqlite(self, db_path="./output/validation_data.db"):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    if self.valid_input:
        sample = self.valid_input[0].model_dump() if hasattr(self.valid_input[0], "model_dump") else dict(self.valid_input[0])
        valid_fields = list(sample.keys())
        valid_columns_sql = ",\n".join([f"{field} TEXT" for field in valid_fields])
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS valid_input (
                {valid_columns_sql}
            )
        ''')
        for customer in self.valid_input:
            data = customer.model_dump() if hasattr(customer, "model_dump") else dict(customer)
            values = tuple(data.get(field) for field in valid_fields)
            placeholders = ','.join(['?'] * len(valid_fields))
            cursor.execute(f'''
                INSERT OR REPLACE INTO valid_input ({",".join(valid_fields)})
                VALUES ({placeholders})
            ''', values)
    if self.invalid_input:
        sample_invalid = self.invalid_input[0]['data']
        invalid_fields = list(sample_invalid.keys())
        invalid_columns_sql = ",\n".join([f"{field} TEXT" for field in invalid_fields])
        invalid_columns_sql += ",\nerrors TEXT"
        cursor.execute(f'''
            CREATE TABLE IF NOT EXISTS invalid_input (
                {invalid_columns_sql}
            )
        ''')
        for item in self.invalid_input:
            data = item['data']
            errors = json.dumps(item['error'], ensure_ascii=False)
            values = tuple(data.get(field) for field in invalid_fields) + (errors,)
            placeholders = ','.join(['?'] * (len(invalid_fields) + 1))
            cursor.execute(f'''
                INSERT INTO invalid_input ({",".join(invalid_fields)}, errors)
                VALUES ({placeholders})
            ''', values)
    conn.commit()
    conn.close()
    print(f"✅ Dati salvati su database SQLite in: {db_path}")
