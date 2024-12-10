from datetime import datetime
import uuid

def generate_invoice_number(user_id):
    """Generate a unique invoice number."""
    current_time = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"INV-{current_time}-{user_id}-{uuid.uuid4().hex[:6].upper()}"
