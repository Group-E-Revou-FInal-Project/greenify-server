import re
from datetime import datetime

def validate_invoice_number(value):
    """
    Validate the invoice number format.
    Accepts:
    - TEMP/INV/YYYYMMDD/ID_USER/COUNTER
    - INV/YYYYMMDD/ID_USER/COUNTER
    """
    pattern = r"^(TEMP/)?INV/\d{8}/\d+/[0-9]{3}$"  # Regex for both formats
    if not re.match(pattern, value):
        raise ValueError(
            "Invoice number must follow the format [TEMP/]INV/YYYYMMDD/ID_USER/COUNTER"
        )

    # Validate the date part (YYYYMMDD) to ensure it's a valid date
    parts = value.split("/")
    date_part = parts[2]
    try:
        datetime.strptime(date_part, "%Y%m%d")
    except ValueError:
        raise ValueError(f"Invalid date in invoice number: {date_part}")

    return value