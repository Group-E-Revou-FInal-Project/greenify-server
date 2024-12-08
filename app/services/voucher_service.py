from app.models import voucher
from app.models.sellers import Seller
from app.models.users import User
from app.models.voucher import Voucher
from app.configs.connector import db
from app.models.wishlist import Wishlist
from app.utils.functions.send_emails import send_email

class VoucherService:
    @staticmethod
    def create_voucher(data):
        new_voucher = Voucher(
            seller_id=data['seller_id'],
            product_id=data['product_id'],
            kode_voucher=data['kode_voucher'],
            expired=data['expired'],
            voucher_desc=data.get('voucher_desc'),
            nama_voucher=data['nama_voucher'],
            discount_percentage=data['discount_percentage'],
            is_active=data.get('is_active', True)
        )
        try:
            db.session.add(new_voucher)
            db.session.commit()
            
            # Notify users after successfully creating the voucher
            notifications = VoucherService.notify_wishlist_users(
                product_id=data['product_id'], 
                voucher=new_voucher
            )
            return {
                "voucher": new_voucher.to_dict(),
                "notifications": notifications
            }
        except Exception as error:
            db.session.rollback()
            return {"error": f"Failed to create voucher: {str(error)}"}

    @staticmethod
    def get_voucher_by_id(voucher_id):
        return Voucher.query.filter_by(id=voucher_id).first()

    @staticmethod
    def update_voucher(voucher_id, data):
        voucher = Voucher.query.filter_by(id=voucher_id).first()
        
        if not voucher:
            return None
        
   
        for key, value in data.items():
            if value is not None:  
                setattr(voucher, key, value)
        
        try:
            db.session.commit()
            return voucher.to_dict()
        except Exception as error:
            db.session.rollback()
            return {"error": f"Failed to create voucher: {str(error)}"}

            

    @staticmethod
    def delete_voucher(voucher_id):
        voucher = Voucher.query.filter_by(id=voucher_id).first()
        
        if not voucher:
            return None
        
        try:
            db.session.delete(voucher)
            db.session.commit()
            return True
        except Exception as error:
            db.session.rollback()
            return {"error": f"Failed to create voucher: {str(error)}"}
        
        
    @staticmethod
    def notify_wishlist_users(product_id, voucher):
        try:
            seller_user_id = voucher.seller.user_id  # Fetch seller's user_id
            wishlisted_users = (
                db.session.query(Wishlist)
                .join(User, Wishlist.user_id == User.id)
                .filter(Wishlist.product_id == product_id)
                .filter(User.id != seller_user_id)  # Exclude the seller's user ID
                .all()
            )

            notifications = {"success": 0, "failed": 0}

            for wishlist in wishlisted_users:
                user = wishlist.user  # Access associated user
                if user and user.email:
                    # Prepare the email content
                    recipient_name = user.name if user.name else "Pengguna"
                    email_body = f"""
                    <p>Hai, {recipient_name}!</p>
                    <p>Sebuah voucher baru tersedia untuk produk yang Anda simpan di daftar keinginan:</p>
                    <ul>
                        <li><strong>Nama Voucher:</strong> {voucher.nama_voucher}</li>
                        <li><strong>Kode:</strong> {voucher.kode_voucher}</li>
                        <li><strong>Diskon:</strong> {voucher.discount_percentage}%</li>
                        <li><strong>Kadaluwarsa:</strong> {voucher.expired.strftime('%Y-%m-%d')}</li>
                    </ul>
                    <p>Jangan lewatkan kesempatan ini untuk menggunakan voucher tersebut!</p>
                    """
                    subject = "Voucher Baru untuk Wishlist Anda!"
                    header = "Greenify Notification"

                    # Send email using the provided `send_email` function
                    response = send_email(user.email, header, email_body, subject)
                    if response is not None and 'error' in response:
                        notifications["failed"] += 1
                        print(f"Failed to send email to {user.email}: {response['error']}")
                    else:
                        notifications["success"] += 1

            return notifications

        except Exception as error:
            print(f"Error notifying wishlist users: {str(error)}")
            return {"error": f"Notification process failed: {str(error)}"}

