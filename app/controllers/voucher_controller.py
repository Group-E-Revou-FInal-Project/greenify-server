from flask import request
from pydantic import ValidationError
from app.services.voucher_service import VoucherService
from app.constants.response_status import Response
from app.utils.validators import UpdateVoucher

class VoucherController:
    @staticmethod
    def create_voucher():
        data = request.get_json()

        # Validate input using Pydantic model
        try:
            validated_data = UpdateVoucher.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)

        # Call service layer to create voucher
        response = VoucherService.create_voucher(validated_data.model_dump())
        if "error" in response:
            return Response.error(message=response["error"], code=400)

        return Response.success(data=response, message="Voucher created successfully", code=201)

    @staticmethod
    def get_voucher(voucher_id):
        voucher = VoucherService.get_voucher_by_id(voucher_id)
        if not voucher:
            return Response.error(message='Voucher not found', code=404)
        
        return Response.success(data=voucher, message="Voucher fetched successfully", code=200)

    @staticmethod
    def update_voucher(voucher_id):
        data = request.get_json()
        
        existing_voucher = VoucherService.get_voucher_by_id(voucher_id)
        if not existing_voucher:
            return Response.error(message='Voucher not found', code=404)
        # Validate input using Pydantic model
        try:
            validated_data = UpdateVoucher.model_validate(data)
        except ValidationError as e:
            return Response.error(f"{str(e)}", 400)

        # Call service layer to update voucher
        response = VoucherService.update_voucher(voucher_id, validated_data.model_dump())
        if response is None:
            return Response.error(message="Voucher not found", code=404)
        if "error" in response:
            return Response.error(message=response["error"], code=400)

        return Response.success(data=response, message="Voucher updated successfully", code=200)

    @staticmethod
    def delete_voucher(voucher_id):
        response = VoucherService.delete_voucher(voucher_id)

        if response is None:
            return Response.error(message="Voucher not found", code=404)
        if "error" in response:
            return Response.error(message=response["error"], code=400)

        return Response.success(data=None, message="Voucher deleted successfully", code=200)
