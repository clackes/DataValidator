# validator/core.py

from models.composed import build_combined_model_class
from pydantic import ValidationError
from validator.validators import csv_validator, json_validator, excel_validator #,xml_validator
from validator.io_handlers import save_validate_data
from validator.db import save_to_db
from validator.reporting import generate_validation_report
import warnings
import os

warnings.filterwarnings("ignore", category=UserWarning)

class Validatore:
    def __init__(self, file_path: str, flags: dict = {}):
        self.valid_input = []
        self.invalid_input = []
        self.file_path = file_path
        self.flags = flags
        self.supported_files = [".xml", ".json", ".csv", ".xlsx"]
        self.check_filetype()

    def check_filetype(self):
        if any(filetype in self.file_path for filetype in self.supported_files):
            print("✅ FileType supported.")
        else:
            print("❌ FileType not supported.")

    def main(self):
        #if "xml" in self.file_path:
        #    xml_validator(self)
        if "json" in self.file_path:
            json_validator(self)
        if "csv" in self.file_path:
            csv_validator(self)
        if "xlsx" in self.file_path:
            excel_validator(self)
        save_validate_data(self)
        save_to_db(self,str(os.path.splitext(os.path.basename(self.file_path))[0]))

    def generate_validation_report(self, report_path):
        generate_validation_report(self.valid_input, self.invalid_input, report_path)

    def model_validator(self, data: dict):
        CombinedModel = build_combined_model_class()
        try:
            # Prova a validare i dati con il contesto dei flag di correzione
            validated = CombinedModel.model_validate(data, context={'correction_flags': self.flags})
            self.valid_input.append(validated)
        except ValidationError as e:
            filtered_errors = []
            for error in e.errors():
                loc = error.get('loc', [])
                field = loc[0] if loc else 'model'
                if self.flags.get(field, True):
                    filtered_errors.append(error['msg'])

            if not filtered_errors:
                # Se gli errori non sono rilevanti secondo i flag, accetta comunque i dati
                fallback_obj = CombinedModel.model_construct(**data)
                self.valid_input.append(fallback_obj)
            else:
                # Altrimenti segna l’input come invalido
                self.invalid_input.append({
                    "data": data,
                    "error": filtered_errors
                })
