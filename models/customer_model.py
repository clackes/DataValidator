#./models/customer_model.py

from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator, ValidationInfo
from typing import Optional
from datetime import date
import re
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def validate_geolocation(customer) -> None:
    geolocator = Nominatim(user_agent="data_validator", timeout=10)
    try:
        full_address = f"{customer.address}, {customer.city}, {customer.state}, {customer.postal_code}, {customer.country}"
        location = geolocator.geocode(full_address)
        if not location:
            raise ValueError("Indirizzo non riconosciuto dal sistema geografico")
        lat_diff = abs(location.latitude - float(customer.latitude or 0))
        lon_diff = abs(location.longitude - float(customer.longitude or 0))
        if lat_diff > 0.1 or lon_diff > 0.1:
            raise ValueError("Le coordinate geografiche non corrispondono all'indirizzo fornito.")
    except GeocoderTimedOut:
        raise ValueError("Timeout durante la verifica geografica.")

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

class Customer(BaseModel):
    id: str
    name: str = Field(..., min_length=1)
    email: EmailStr
    birth_date: date
    phone_number: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    postal_code: Optional[int] = None
    state: Optional[str] = None
    country: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

    @field_validator('phone_number')
    @classmethod
    def validate_phone_number(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('phone_number', True):
            return v
        if v is None:
            return v
        cleaned = v.replace(" ", "")
        if not re.fullmatch(r'\+?\d{9,15}', cleaned):
            raise ValueError('Numero di telefono non valido. Deve essere 9-15 cifre e può iniziare con +')
        return cleaned

    @field_validator('birth_date')
    @classmethod
    def validate_birth_date(cls, v: date, info: ValidationInfo) -> date:
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('birth_date', True):
            return v
        if v >= date.today():
            raise ValueError('Data di nascita deve essere nel passato')
        return v

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str, info: ValidationInfo) -> str:
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('name', True):
            return v
        if len(v.split()) < 2:
            raise ValueError('Il nome deve contenere almeno un nome e un cognome (es: Mario Rossi)')
        return v

    @field_validator('latitude')
    @classmethod
    def validate_latitude(cls, v: Optional[float], info: ValidationInfo) -> Optional[float]:
        correction_flags = info.context.get('correction_flags', {})
        if not correction_flags.get('latitude', True):
            return v
        if v is not None and not (-90 <= v <= 90):
            raise ValueError('La latitudine deve essere tra -90 e +90')
        return v

    @field_validator('longitude')
    @classmethod
    def validate_longitude(cls, v: Optional[float], info: ValidationInfo) -> Optional[float]:
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
    
    @model_validator(mode='after')
    @classmethod
    def check_geolocation_consistency(cls, model, info: ValidationInfo):
        flags = info.context.get("correction_flags", {})
        if flags.get("geolocation", True):
            validate_geolocation(model)
        return model
