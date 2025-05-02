
---

```markdown
# 🧪 DataValidator

**DataValidator** è un'applicazione Python avanzata per la validazione, pulizia e ispezione di dati strutturati provenienti da file `.csv`, `.json`, `.xml`, `.xlsx`.

---

## ⚙️ Funzionalità principali

- ✅ Validazione dei dati tramite modelli dinamici generati da JSON
- 🧠 Controlli semantici, formali e geografici
- 🔐 Protezione da input malevoli (SQL/XSS injection)
- 📦 Output dei risultati in `.json`, `.csv`, `.xlsx`, `.xml`
- 🗃️ Persistenza dei dati in SQLite
- 🌐 API REST per uso via web/frontend
- 🧪 Test automatici delle API

---

## 🚀 Come funziona

### 1. Definizione dello schema

Nel file `data/model_schema.json` definisci la struttura dei modelli. Esempio:

```json
{
  "Customer": {
    "id": "str",
    "name": "str",
    "email": "EmailStr",
    "birth_date": "date",
    "postal_code": "Optional[int]",
    "latitude": "Optional[float]"
  }
}
```

Viene generato dinamicamente un modello `BaseCustomer`.

---

### 2. Esecuzione via CLI

```bash
python main.py
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
| POST   | `/upload`                | Carica un file da validare     |
| POST   | `/validate`              | Valida un file con flags       |
| POST   | `/validate/record`       | Valida un record singolo       |

---

### 4. Test API

Lancia:

```bash
python tests/test_api.py
```

Esegue test automatici su:

- Upload file
- Validazione file
- Validazione record singolo

---

## 🧠 Validazioni implementate

- ✔️ Tipi dinamici (str, date, EmailStr, Optional)
- ⚠️ Flag per disattivare validazioni specifiche
- 🌍 Verifica geografica coerente tra latitudine, città, stato, CAP
- 🔐 Filtraggio input malevoli (regex anti-injection)
- 🧩 Estendibilità semplice con nuovi validatori

---

## 📦 Requisiti

```bash
pip install -r requirements.txt
```

---

## 💡 To-do / Roadmap

- [ ] Caricamento modelli via API
- [ ] Interfaccia web (React)
- [ ] Logging avanzato e tracciamento
- [ ] Supporto multiutente

---

## 🤝 Autore

Creato con passione da clackes  
Contatti: `clackes.work@gmail.com`

---
