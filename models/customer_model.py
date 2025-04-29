from pydantic import BaseModel, EmailStr, Field, field_validator, ValidationInfo
from typing import Optional
from datetime import date
import re

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