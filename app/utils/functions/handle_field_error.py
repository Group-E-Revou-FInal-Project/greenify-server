from pydantic import ValidationError

def handle_field_error(e: ValidationError):
    error_messages = []
    for error in e.errors():
        if error['type'] == 'value_error.missing':
            error_messages.append(f"{error['loc'][0]} - {error['msg']}")
            
    return {"missing_fields" : error_messages}