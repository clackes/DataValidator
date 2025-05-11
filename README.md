
---
# 🧪 DataValidator

DataValidator è un'applicazione Python avanzata per la validazione, pulizia e ispezione di dati 
strutturati provenienti da file `.csv`, `.json`, `.xml`, `.xlsx`.

---

## ⚙️ Funzionalità principali
```markdown
- ✅ Validazione dei dati runtime tramite modelli dinamici JSON
- 🧠 Controlli semantici, formali e geografici
- 🔐 Protezione da input malevoli (SQL/XSS injection)
- 📦 Output dei risultati in `.json`, `.csv`, `.xlsx`, `.xml`
- 🗃️ Persistenza dei dati in SQLite
- 🌐 API REST per uso via web/frontend
- 🧪 Test automatici delle API
```
---

## 🚀 Come funziona

### 1. Definizione dello schema

Nel file `model_schema.json` definisci la struttura dei modelli. Esempio:

```json
{
  "Customer": {
    "id": "str",
    "name": "str",
    "email": "EmailStr",
    "birth_date": "date",
    "phone_number": "Optional[str]",
    "address": "Optional[str]",
    "city": "Optional[str]",
    "postal_code": "Optional[int]",
    "state": "Optional[str]",
    "country": "Optional[str]",
    "latitude": "Optional[float]",
    "longitude": "Optional[float]"
  }
}
```

Viene generato dinamicamente un modello `BaseCustomer`.

---

### 2. Esecuzione via Docker
-Rinominare e modificare il file `.env.example` in `.env`.
-Rinominare e modificare il file `docker-compose-example.yml` in `docker-compose.yml`.

-Per avviare il contenitore Docker.
```bash
docker-compose up --build -d  
```
Per resettare/eliminare Docker
```bash
docker-compose down -v 
```

- Valida ogni file in `./data/`
- Applica flags per saltare la validazione di campi specifici
- Genera output validi/invalidi
- Salva su database SQLite (`output/validation_data.db`)
- Crea un report leggibile in `output/reports/`

---

### 3. API REST

Avvia con:

```bash
uvicorn api.api_endpoints:app --reload
```

#### Endpoint disponibili:

| Metodo | URL                      | Descrizione                    |
|--------|--------------------------|--------------------------------|
| POST   | `/schema/load`           | Carica schema prima di validare|
| POST   | `/upload`                | Carica un file da validare     |
| POST   | `/validate/record`       | Valida un record singolo       |

---

### 4. Test API

Lancia:

```bash
python test.py
```

Esegue test automatici su:

- Upload e validazione file
- Upload schema
- Validazione record singolo

---

## 🧠 Validazioni implementate

- ✔️ Tipi dinamici runtime (str, date, EmailStr, Optional)
- ⚠️ Flag per disattivare validazioni specifiche
- 🌍 Verifica geografica coerente tra latitudine, città, stato, CAP
- 🔐 Filtraggio input malevoli (regex anti-injection)
- 🧩 Estendibilità semplice con nuovi validatori

---

## 🤝 Autore

Creato con passione da clackes  
Contatti: `clackes.work@gmail.com`

---
