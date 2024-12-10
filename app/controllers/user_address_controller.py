from flask import request
from pydantic import ValidationError
from app.services.user_address_services import UserAddressService
from app.constants.response_status import Response
from app.utils.validators import createAddress, updateAddress

class UserAddressController:
    @staticmethod
    def create_address():
        data = request.get_json()
        try:
            validate_address = createAddress.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)
        
        response = UserAddressService.create_address(validate_address.model_dump())
        if "error" in response:
            return Response.error(message=response["error"], code=400)
        return Response.success(data=response, message="Address created successfully", code=201)

    @staticmethod
    def get_address(address_id):
        address = UserAddressService.get_address_by_id(address_id)
        if not address:
            return Response.error(message="Address not found", code=404)
        return Response.success(data=address.to_dict(), message="Address fetched successfully", code=200)

    @staticmethod
    def update_address(address_id):
        data = request.get_json()
        try:
            validate_address = updateAddress.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)
        
        response = UserAddressService.update_address(address_id, validate_address.model_dump())
        if response is None:
            return Response.error(message="Address not found", code=404)
        if "error" in response:
            return Response.error(message=response["error"], code=400)
        return Response.success(data=response, message="Address updated successfully", code=200)

    @staticmethod
    def delete_address(address_id):
        response = UserAddressService.delete_address(address_id)
        if response is None:
            return Response.error(message="Address not found", code=404)
        if "error" in response:
            return Response.error(message=response["error"], code=400)
        return Response.success(message="Address deleted successfully", code=200)

    @staticmethod
    def toggle_active_status(address_id, is_active):
        response = UserAddressService.toggle_active_status(address_id, is_active)
        if "error" in response:
            return Response.error(message=response["error"], code=404)
        return Response.success(data=response, message=response["message"], code=200)
    
    @staticmethod
    def get_address_by_user_address_id(user_id, address_id):
        response = UserAddressService.get_address_by_user_id_and_address_id(user_id, address_id)    
        if response is None:
            return Response.error(message="Address not found", code=404)
        return Response.success(data=response, message="Address fetched successfully", code=200)
    
    @staticmethod
    def get_addresses_by_user_id(user_id):    
        response = UserAddressService.get_addresses_by_user_id(user_id)
        if response is None:
            return Response.error(message="Addresses not found", code=404)
        return Response.success(data=response, message="Addresses fetched successfully", code=200)  
