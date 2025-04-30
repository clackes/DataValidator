# api/api_endpoints.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from validator.core import Validatore
from validator.reporting import generate_validation_report
import shutil, os, json
from typing import List, Optional

app = FastAPI(title="Data Validator API")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".csv", ".json", ".xml", ".xlsx"]:
        raise HTTPException(status_code=400, detail="Formato file non supportato")

    path = f"./data/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"File caricato in {path}"}

@app.post("/validate")
async def validate_file(filename: str = Form(...), flags_json: Optional[str] = Form(None)):
    path = f"./data/{filename}"
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="File non trovato")

    default_flags = {
        "birth_date": False,
        "email": False,
        "postal_code": False,
        "geolocation": False
    }

    try:
        user_flags = json.loads(flags_json) if flags_json else {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Flags JSON non valido")

    flags = {**default_flags, **user_flags}

    v = Validatore(path, flags)
    v.main()

    report_path = f"./output/reports/validation_report_{filename}.txt"
    v.generate_validation_report(report_path)

    return {
        "validi": len(v.valid_customers),
        "invalidi": len(v.invalid_customers),
        "report": report_path
    }

@app.post("/validate/record")
async def validate_record(data: dict, flags_json: Optional[str] = None):
    from models.customer_model import Customer
    from pydantic import ValidationError

    try:
        flags = json.loads(flags_json) if flags_json else {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Flags JSON non valido")

    try:
        customer = Customer.model_validate(data, context={'correction_flags': flags})
        return {"valid": True, "data": customer.model_dump()}
    except ValidationError as e:
        return {"valid": False, "errors": e.errors()}
