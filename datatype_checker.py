from Tokens.token import Token


TYPES_VALIDATIONS = {
    'int' : lambda x: x.isdigit(),
    'float' : lambda x: x.replace('.', '', 1).isdigit() and x.count('.') <= 1,
    'double' : lambda x: x.replace('.', '', 1).isdigit() and x.count('.') <= 1,
    'string' : lambda x: isinstance(x, str),
    'char' : lambda x: isinstance(x, str) and len(x) == 1,
    'bool' : lambda x: x in ['true', 'false']
}

def check_type(value, expected_type):
    if expected_type not in TYPES_VALIDATIONS:
        raise ValueError(f"Unsupported type: {expected_type}")
    
    return TYPES_VALIDATIONS[expected_type](value)

def type_exists(type_name):
    return type_name in TYPES_VALIDATIONS

def return_value_type(value):
    for type_name, validation in TYPES_VALIDATIONS.items():
        if validation(value):
            return type_name
    return None