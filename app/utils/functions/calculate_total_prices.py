from decimal import Decimal
def calculate_total_prices(price, quantity, product_discount=None, voucher_discount=None):
    # Ensure discounts are not None; default to 0 if they are
    product_discount = product_discount or 0
    voucher_discount = voucher_discount or 0

    # Calculate the effective discount percentage
    total_discount = Decimal((product_discount + voucher_discount) / 100)
    
    # Calculate total price
    return round(price * quantity * (1 - total_discount), 2)

        
        
