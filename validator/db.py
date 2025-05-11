import os
import json
import psycopg2
from dotenv import load_dotenv
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


def ensure_database_exists(db_name: str, db_user: str, db_password: str, db_host: str, db_port: str):
    """Crea il database se non esiste"""
    conn = psycopg2.connect(
        dbname="validator_db",  # DB di default per amministrazione
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(f'CREATE DATABASE "{db_name}"')
        print(f"✅ Database '{db_name}' creato con successo.")
    else:
        print(f"ℹ️ Il database '{db_name}' esiste già.")
    cursor.close()
    conn.close()

def save_to_db(self, db_suffix: str):
    load_dotenv()

    DB_NAME_BASE = os.getenv("POSTGRES_DB")
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")

    if not all([DB_NAME_BASE, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT]):
        raise ValueError("❌ Variabili d'ambiente mancanti nel file .env")

    db_name = f"{DB_NAME_BASE}_{db_suffix}"

    # Crea il database dinamico se non esiste
    ensure_database_exists(db_name, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

    # Connessione al DB specifico
    conn = psycopg2.connect(
        dbname=db_name,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
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
