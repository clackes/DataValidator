from pydantic import BaseModel, field_validator, model_validator

class BaseValidator(BaseModel):
    """Classe base per facilitare validatori"""

    @classmethod
    def validators(cls, field_name):
        def decorator(func):
            @field_validator(field_name)
            @classmethod
            def wrapper(cls_inner, v):
                return func(cls_inner, v)
            return wrapper
        return decorator

    @classmethod
    def model_validators(cls):
        def decorator(func):
            @model_validator(mode='after')
            @classmethod
            def wrapper(cls_inner, model):
                return func(cls_inner, model)
            return wrapper
        return decorator