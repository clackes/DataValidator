# api/api_endpoints.py

from fastapi import FastAPI, UploadFile, File, HTTPException, Form, Body
from validator.core import Validatore
from validator.reporting import generate_validation_report
from models.model_gen import load_model_definitions, build_models
import shutil, os, json
from typing import List, Optional

app = FastAPI(title="Data Validator API")

@app.post("/upload")
async def upload_file(file: UploadFile = File(...), flags_json: Optional[str] = Form(None)):
    file_ext = os.path.splitext(file.filename)[1].lower()
    if file_ext not in [".csv", ".json", ".xml", ".xlsx"]:
        raise HTTPException(status_code=400, detail="Formato file non supportato")

    path = f"./data/{file.filename}"
    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    default_flags = {
        "geolocation": False,
    }
    try:
        user_flags = json.loads(flags_json) if flags_json else {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Flags JSON non valido")
    flags = {**default_flags, **user_flags}
    v = Validatore(path, flags)
    v.main()
    report_path = f"./output/reports/validation_report_{file.filename}.txt"
    v.generate_validation_report(report_path)
    return {
        "validi": len(v.valid_input),
        "invalidi": len(v.invalid_input),
        "report": report_path
    }

@app.post("/validate/record")
async def validate_record(data: dict = Body(...), flags_json: Optional[str] = None):
    from models.base_model import ModelValidator
    from pydantic import ValidationError
    try:
        flags = json.loads(flags_json) if flags_json else {}
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Flags JSON non valido")
    try:
        base = ModelValidator.model_validate(data, context={'correction_flags': flags})
        return {"valid": True, "data": base.model_dump()}
    except ValidationError as e:
        return {"valid": False, "errors": e.errors()}

@app.post("/schema/load")
async def load_schema(schema_file: UploadFile = File(...)):
    try:
        content = await schema_file.read()
        with open("./models/model_schema.json", "wb") as f:
            f.write(content)
        loaded = load_model_definitions()
        models, last_class = build_models(loaded)
        return {"message": f"Schema caricato e modello '{last_class}' generato."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))