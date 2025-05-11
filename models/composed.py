from models.model_gen import get_model
from models.base_model import get_validators_mixin

def build_combined_model_class():
    DynamicModel = get_model()  # <- restituisce una classe BaseModel dinamica
    ValidatorsMixin = get_validators_mixin()  # <- contiene solo validatori, non eredita da BaseModel

    class CombinedModel(DynamicModel, ValidatorsMixin):
        pass

    return CombinedModel