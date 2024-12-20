from app.models.users_address import UserAddress
from app.configs.connector import db
from datetime import datetime

class UserAddressService:
    @staticmethod
    def create_address(data):
        new_address = UserAddress(
            user_id=data['user_id'],
            name=data['name_address'],
            address=data['address'],
            city=data['city'],
            postal_code=data['postal_code'],
            province=data['province'],
            phone_number=data['phone_number'],
        )
        try:
            db.session.add(new_address)
            db.session.commit()
            return new_address.to_dict()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to create address: {str(e)}"}

    @staticmethod
    def get_address_by_id(address_id):
        return UserAddress.query.filter_by(id=address_id).first()

    @staticmethod
    def update_address(address_id, data):
        address = UserAddress.query.filter_by(id=address_id, user_id=data['user_id']).first()
        if not address:
            return None

        for key, value in data.items():
            if hasattr(address, key) and value is not None:
                setattr(address, key, value)

        try:
            address.updated_at = datetime.utcnow()
            db.session.commit()
            return address.to_dict()
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to update address: {str(e)}"}

    @staticmethod
    def delete_address(address_id):
        address = UserAddress.query.filter_by(id=address_id).first()
        if not address:
            return None

        try:
            db.session.delete(address)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to delete address: {str(e)}"}

    @staticmethod
    def toggle_active_status(address_id, is_active):
        address = UserAddress.query.filter_by(id=address_id).first()
        if not address:
            return {"error": "Address not found"}

        try:
            address.is_active = is_active
            db.session.commit()
            return {"message": f"Address {'activated' if is_active else 'deactivated'} successfully"}
        except Exception as e:
            db.session.rollback()
            return {"error": f"Failed to toggle active status: {str(e)}"}
    
    
    @staticmethod
    def get_addresses_by_user_id(user_id):
        return UserAddress.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_address_by_user_id_and_address_id(user_id, address_id):    
        return UserAddress.query.filter_by(user_id=user_id, id=address_id).first()
    
