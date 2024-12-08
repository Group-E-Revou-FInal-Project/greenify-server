from datetime import datetime, timezone
from app.configs.connector import db

class Voucher(db.Model):
    __tablename__ = 'voucher'

    id = db.Column(db.BigInteger, primary_key=True)
    seller_id = db.Column(db.BigInteger, db.ForeignKey('seller.id'), nullable=False)
    product_id = db.Column(db.BigInteger, db.ForeignKey('product.id'), nullable=False)
    kode_voucher = db.Column(db.String(50), unique=True, nullable=False)
    expired = db.Column(db.DateTime, nullable=False)
    voucher_desc = db.Column(db.String(255), nullable=True)
    nama_voucher = db.Column(db.String(100), nullable=False)
    discount_percentage = db.Column(db.Float, nullable=False)
    is_active = db.Column(db.Boolean, nullable=False, default=True)
    created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = db.Column(db.DateTime, onupdate=datetime.now(timezone.utc))

    seller = db.relationship('Seller', backref='vouchers')
    product = db.relationship('Product', backref='vouchers')

    def to_dict(self):
        return {
            "id": self.id,
            "seller_id": self.seller_id,
            "product_id": self.product_id,
            "kode_voucher": self.kode_voucher,
            "expired": self.expired,
            "voucher_desc": self.voucher_desc,
            "nama_voucher": self.nama_voucher,
            "discount_percentage": self.discount_percentage,
            "is_active": self.is_active,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
    # call this function if we need to deactivate the voucher
    def deactivate(self):
        self.is_active = False
        db.session.commit()
    # call this function if we need to active the voucher
    def reactivate(self):
        self.is_active = True
    
