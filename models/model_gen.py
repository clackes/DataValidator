# models/generated_models.py

import json
from typing import Optional, Any
from pydantic import BaseModel
from datetime import date
import datetime
from pydantic import EmailStr

def load_model_definitions(schema_path: str = "./models/model_schema.json") -> dict:
    with open(schema_path, 'r') as f:
        return json.load(f)

def build_models(schema: dict) -> dict:
    models = {}
    namespace = {
        "BaseModel": BaseModel,
        "Optional": Optional,
        "EmailStr": EmailStr,
        "date": date,
        "datetime": datetime,
        "Any": Any
    }

    for class_name, fields in schema.items():
        annotations = {}
        defaults = {}

        for field_name, field_type_str in fields.items():
            # Eval safely using known types
            field_type = eval(field_type_str, namespace)
            annotations[field_name] = field_type
            if "Optional" in field_type_str:
                defaults[field_name] = None

        model = type(
            f"Base{class_name}",
            (BaseModel,),
            {
                "__annotations__": annotations,
                **defaults
            }
        )
        models[class_name] = model
    return models, class_name

def get_model():
    models, class_name = build_models(load_model_definitions())
    return models[f"{class_name}"]
