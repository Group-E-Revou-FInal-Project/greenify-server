from datetime import datetime


def generate_invoice_number(user_id, count=1, is_temp=True):
    # Get the current date
    current_date = datetime.now().strftime("%Y%m%d")
    
    if count > 999:
        digits = len(str(count))
    else:
        digits = 3
    
    # Format the invoice number
    counter = f"{count:0{digits}d}"  # Zero-padded to 3 digits
    
    if is_temp:
        return f"TEMP/INV/{current_date}/{user_id}/{counter}"
    
    return f"INV/{current_date}/{user_id}/{counter}"
