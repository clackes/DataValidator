#./models/base.py

from pydantic import field_validator, model_validator, ValidationInfo
from typing import Optional, Dict
from datetime import date, datetime
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

#def validate_geolocation(user) -> None:
#    geolocator = Nominatim(user_agent="data_validator", timeout=10)
#    try:
#        full_address = f"{user.address}, {user.city}, {user.state}, {user.postal_code}, {user.country}"
#        location = geolocator.geocode(full_address)
#        if not location:
#            raise ValueError("Indirizzo non riconosciuto dal sistema geografico")
#        lat_diff = abs(location.latitude - float(user.latitude or 0))
#        lon_diff = abs(location.longitude - float(user.longitude or 0))
#        if lat_diff > 0.1 or lon_diff > 0.1:
#            raise ValueError("Le coordinate geografiche non corrispondono all'indirizzo fornito.")
#    except GeocoderTimedOut:
#        raise ValueError("Timeout durante la verifica geografica.")

def is_malicious_input(text: str) -> bool:
    patterns = [
        r"(--|/\*|\*/)",                
        r"(select|update|delete|insert|drop|alter)",     
        r"<script.*?>.*?</script.*?>",                  
        r"on\w+\s*=",                                   
        r"exec\(|eval\(|system\(",                       
    ]
    for pattern in patterns:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False

class ModelValidator():
    @field_validator('phone_number', check_fields=False)
    @classmethod
    def validate_phone_number(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        if v is None:
            return v 
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('phone_number', True):
            return v
        if v is None:
            return v
        cleaned = v.replace(" ", "")
        if not re.fullmatch(r'\+?\d{9,15}', cleaned):
            raise ValueError('Numero di telefono non valido. Deve essere 9-15 cifre e può iniziare con +')
        return cleaned

    @field_validator('birth_date', check_fields=False)
    @classmethod
    def validate_birth_date(cls, v: date, info: ValidationInfo) -> date:
        if v is None:
            return v 
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('birth_date', True):
            return v
        if v >= date.today():
            raise ValueError('Data di nascita deve essere nel passato')
        return v

    @field_validator('name', check_fields=False)
    @classmethod
    def validate_name(cls, v: str, info: ValidationInfo) -> str:
        if v is None:
            return v 
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('name', True):
            return v
        if len(v.split()) < 2:
            raise ValueError('Il nome deve contenere almeno un nome e un cognome (es: Mario Rossi)')
        return v

    @field_validator('latitude', check_fields=False)
    @classmethod
    def validate_latitude(cls, v: Optional[float], info: ValidationInfo) -> Optional[float]:
        if v is None:
            return v 
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('latitude', True):
            return v
        if v is not None and not (-90 <= v <= 90):
            raise ValueError('La latitudine deve essere tra -90 e +90')
        return v

    @field_validator('longitude', check_fields=False)
    @classmethod
    def validate_longitude(cls, v: Optional[float], info: ValidationInfo) -> Optional[float]:
        if v is None:
            return v 
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('longitude', True):
            return v
        if v is not None and not (-180 <= v <= 180):
            raise ValueError('La longitudine deve essere tra -180 e +180')
        return v

    @model_validator(mode='after')
    @classmethod
    def check_malicious_fields(cls, model, info: ValidationInfo):
        correction_flags = info.context.get('correction_flags', {}) if info.context else {}
        for field_name, value in model.__dict__.items():
            if isinstance(value, str) and correction_flags.get(field_name, True):
                if is_malicious_input(value):
                    raise ValueError(f"Valore potenzialmente pericoloso rilevato nel campo '{field_name}'")
        return model

    @field_validator('price', check_fields=False)
    @classmethod
    def validate_price(cls, v: float, info: ValidationInfo) -> float:
        if v is None:
            return v
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('price', True):
            return v
        if v <= 0:
            raise ValueError('Il prezzo deve essere maggiore di 0')
        return v

    @field_validator('stock_quantity', check_fields=False)
    @classmethod
    def validate_stock(cls, v: int, info: ValidationInfo) -> int:
        if v is None:
            return v
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('stock_quantity', True):
            return v
        if v < 0:
            raise ValueError('La quantità in stock non può essere negativa')
        return v

    @field_validator('weight_kg', check_fields=False)
    @classmethod
    def validate_weight(cls, v: float, info: ValidationInfo) -> float:
        if v is None:
            return v
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('weight_kg', True):
            return v
        if v <= 0:
            raise ValueError('Il peso deve essere maggiore di 0')
        return v

    @field_validator('dimensions_cm', check_fields=False)
    @classmethod
    def validate_dimensions(cls, v: Dict[str, float], info: ValidationInfo) -> Dict[str, float]:
        if v is None:
            return v
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('dimensions_cm', True):
            return v
        for dim in ['length', 'width', 'height']:
            if v.get(dim, 0) <= 0:
                raise ValueError(f'La dimensione "{dim}" deve essere maggiore di 0')
        return v

    @field_validator('updated_at', check_fields=False)
    @classmethod
    def validate_updated_at(cls, v: datetime, info: ValidationInfo) -> datetime:
        if v is None:
            return v
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('updated_at', True):
            return v
        created = info.data.get('created_at')
        if created and v < created:
            raise ValueError('La data di aggiornamento non può precedere la data di creazione')
        return v
    

def get_validators_mixin():
    return ModelValidator
    #@model_validator(mode='after')
    #@classmethod
    #def check_geolocation_consistency(cls, model, info: ValidationInfo):
    #    flags = info.context.get("correction_flags", {})
    #    if flags.get("geolocation", True):
    #        validate_geolocation(model)
    #    return model
