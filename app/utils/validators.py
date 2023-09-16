# from pydantic import validator, root_validator, FieldValidationInfo

def check_positive(cls, v, field):
    if v < 0:
        raise ValueError(f"{field.name} should be non-negative.")
    return v

def check_normalized(cls, v, field):
    if v < 0 or v > 1:
        raise ValueError(f"{field.name} should be between 0 and 1.")
    return v