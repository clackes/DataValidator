import os
import json
import psycopg2
from dotenv import load_dotenv

def save_to_db(self):
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")

    if not db_url:
        raise ValueError("❌ DATABASE_URL non definito nel file .env")

    conn = psycopg2.connect(db_url)
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
            placeholders = ','.join(['%s'] * len(valid_fields))
            cursor.execute(f'''
                INSERT INTO valid_input ({",".join(valid_fields)})
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING
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
            placeholders = ','.join(['%s'] * len(values))
            cursor.execute(f'''
                INSERT INTO invalid_input ({",".join(invalid_fields)}, errors)
                VALUES ({placeholders})
                ON CONFLICT DO NOTHING
            ''', values)

    conn.commit()
    conn.close()
    print("✅ Dati salvati su PostgreSQL con successo!")
