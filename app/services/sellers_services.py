from sqlalchemy.exc import IntegrityError
from app.configs.connector import db
from app.models.sellers import Seller

class SellerService():
    @staticmethod
    def create_seller(data):
        new_seller = Seller(user_id=data['user_id'], 
                            store_name=data['store_name'], 
                            store_description=data['store_description'], 
                            store_logo=data['store_logo'], 
                            address=data['address'], 
                            phone_number=data['phone_number'])
        
        try:
            db.session.add(new_seller)
            db.session.commit()
            return new_seller.to_dict()
        except IntegrityError:     
            db.session.rollback()
            return None
        