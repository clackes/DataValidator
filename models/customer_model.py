# models/customer_model.py

from pydantic import BaseModel, EmailStr, Field
from models.base_models import BaseValidator
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

    @BaseValidator.validators('phone_number')
    def validate_phone_number(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return v
        cleaned = v.replace(" ", "")

        if not re.fullmatch(r'\+?\d{9,15}', cleaned):
            raise ValueError('Numero di telefono non valido. Deve essere 9-15 cifre e può iniziare con +')

        return cleaned
    
    @BaseValidator.validators('birth_date')
    def validate_birth_date(cls, v):
        if v >= date.today():
            raise ValueError('Data di nascita deve essere nel passato')
        return v
    

    @BaseValidator.validators('name')
    def validate_name(cls, v):
        if len(v.split()) < 2:
            raise ValueError('Il nome deve contenere almeno un nome e un cognome (es: Mario Rossi)')
        return v
    
    
    @BaseValidator.validators("latitude")    
    def validate_latitude(cls, v):
        if v is not None and not (-90 <= v <= 90):
            raise ValueError('La latitudine deve essere tra -90 e +90')
        return v
    
    @BaseValidator.validators("longitude")  
    def validate_longitude(cls, v):
        if v is not None and not (-180 <= v <= 180):
            raise ValueError('La longitudine deve essere tra -180 e +180')
        return v