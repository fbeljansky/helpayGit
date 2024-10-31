from flask import Blueprint, request, jsonify
from services.wallet_service import WalletService

wallet_controller = Blueprint('wallet_controller', __name__)

@wallet_controller.route('/wallet', methods=['POST'])
def create_wallet():
    data = request.json
    try:
        user_id = data['user_id']
        currency = data['currency']
        bills = data['bills']
        wallet_id = WalletService.create_wallet(user_id, currency, bills)
        return jsonify({"message": "Wallet created successfully", "wallet_id": wallet_id}), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@wallet_controller.route('/wallet/<wallet_id>', methods=['GET'])
def get_wallet(wallet_id):
    try:
        wallet = WalletService.get_wallet(wallet_id)
        if wallet:
            return jsonify(wallet), 200
        else:
            return jsonify({"message": "Wallet not found"}), 404
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@wallet_controller.route('/wallet/<wallet_id>', methods=['PUT'])
def update_wallet(wallet_id):
    update_data = request.json
    try:
        WalletService.update_wallet(wallet_id, update_data)
        return jsonify({"message": "Wallet updated successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@wallet_controller.route('/wallet/<wallet_id>', methods=['DELETE'])
def delete_wallet(wallet_id):
    try:
        WalletService.delete_wallet(wallet_id)
        return jsonify({"message": "Wallet deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@wallet_controller.route('/wallets/user/<user_id>', methods=['GET'])
def get_wallets_by_user(user_id):
    try:
        wallets = WalletService.get_wallets_by_user(user_id)
        return jsonify(wallets), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400
