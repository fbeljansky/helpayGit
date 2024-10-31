from bson import ObjectId
from flask import Blueprint, abort, json, request, jsonify
from models.user_model import UserModel
from services.user_service import UserService
from services.wallet_service import WalletService

user_controller = Blueprint('user_controller', __name__)

# @user_controller.route('/user', methods=['POST'])
# def create_user():
#     user_data = request.json
#     try:
#         user_id = UserService.create_user(user_data)
#         return jsonify({"message": "User created successfully", "user_id": user_id}), 201
#     except ValueError as e:
#         return jsonify({"message": str(e)}), 400

@user_controller.route('/user', methods=['POST'])
def create_user():
    user_data = request.json
    try:
        # Crear el usuario
        user_id = UserService.create_user(user_data)

        # Crear una billetera para el usuario recién creado
        default_currency = 0  # Por ejemplo, 0 para dólares; se puede ajustar según el caso
        default_bills =   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
        wallet_id = WalletService.create_wallet(user_id, default_currency, default_bills)

        # Actualizar el usuario con el ID de la billetera
        UserModel.objects(id=user_id).update_one(set__wallet_id=wallet_id)

        return jsonify({
            "message": "User and wallet created successfully",
            "user_id": str(user_id),  # Asegúrate de convertir el ID a una cadena
            "wallet_id": str(wallet_id)  # Asegúrate de convertir el ID a una cadena
        }), 201
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@user_controller.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    try:
        user = UserModel.objects(id=user_id).first()
        if user is None:
            abort(404, description="User not found")

        
        user_asociado_data = None
        if user.user_asociado:
            user_asociado = UserModel.objects(id=user.user_asociado.id).first()
            if user_asociado:
                user_asociado_data = {
                    "id": str(user_asociado.id),
                    "email": user_asociado.email,
                    "name": user_asociado.name,
                    "phone": user_asociado.phone,
                    "mercado_pago_on": user_asociado.mercado_pago_on,
                    "sound_on": user_asociado.sound_on,
                    "wallet_id": str(user_asociado.wallet_id) if user_asociado.wallet_id else None,
                    "recientes": user_asociado.recientes,
                    "tipo_usuario": user_asociado.tipo_usuario
                }


        user_data = {
            "email": user.email,
            "name": user.name,
            "phone": user.phone,
            "mercado_pago_on": user.mercado_pago_on,
            "sound_on": user.sound_on,
            "wallet_id": str(user.wallet_id) if user.wallet_id else None,
            "recientes": user.recientes,
            "user_asociado": user_asociado_data, 
            "tipo_usuario": user.tipo_usuario
        }

        return jsonify(user_data)
    except Exception as e:
        return jsonify({"message": str(e)}), 500




@user_controller.route('/user/<user_id>', methods=['PUT'])
def update_user(user_id):
    user_data = request.json
    try:
        UserService.update_user(user_id, user_data)
        return jsonify({"message": "User updated successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@user_controller.route('/user/asociado/<user_id>', methods=['PUT'])
def update_user_asociado(user_id):
    user_data = request.json
    try:
        if not ObjectId.is_valid(user_id):
            raise ValueError("Invalid user ID format")
        user_id = ObjectId(user_id)

        asociado_email = user_data.get('user_asociado')
        if not asociado_email:
            raise ValueError("El campo 'user_asociado' es requerido")
        
        asociado = UserModel.objects(email=asociado_email).first()
        if not asociado:
            raise ValueError("User asociado not found")
        
        user = UserModel.objects(id=user_id).first()
        if not user:
            raise ValueError("User not found")

        UserService.update_user(user_id, {'user_asociado': asociado.id})

        UserService.update_user(asociado.id, {'user_asociado': user_id})

        return jsonify({
            "message": "User asociado updated successfully,",
            "user_asociado": str(asociado.id)}), 200

    except ValueError as e:
        return jsonify({"message": str(e)}), 400
    except Exception as e:
        return jsonify({"message": str(e)}), 500



@user_controller.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    try:
        UserService.delete_user(user_id)
        return jsonify({"message": "User deleted successfully"}), 200
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

@user_controller.route('/users', methods=['GET'])
def get_all_users():
    try:
        users = UserService.get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@user_controller.route('/user/login', methods=['POST'])
def login_user():

    data = request.json
    email = data.get('email')

    print(email)
    
    if not email:
        return jsonify({"message": "Email is required"}), 400
    
    user = UserService.find_user_by_email(email)
    


    if user:
        wallet = WalletService.get_wallet(user["wallet_id"])

        if wallet:
            wallet_data = {
                "id": str(wallet.get('_id', wallet.get('id'))), 
                "currency": wallet.get('currency'),
                "bills": wallet.get('bills')
            }
        else:
            wallet_data = None
        print(f"Wallet found: {wallet}")
        print(f"user ID: {user}")

        user_data = {
            "id": user["_id"],
            "email": user["email"],
            "name": user["name"],
            "phone": user["phone"],
            "mercado_pago_on": user["mercado_pago_on"],
            "sound_on": user["sound_on"],
            "wallet": wallet_data,  
            "recientes": user["recientes"],
            "tipo_usuario": user["tipo_usuario"]
        }
        
        return jsonify(user_data), 200
    else:
        user_data = request.json
        print("email: ", email)
        user_data_dos = {
            "email": email,
            "mercado_pago_on": "false",
            "name": "",
            "phone": "",
            "recientes": [],
            "sound_on": "false",
            "tipo_usuario": "",  
        }
        try:
            user_id = UserService.create_user(user_data_dos)

            default_currency = 0 
            default_bills =   [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0] 
            wallet_id = WalletService.create_wallet(user_id, default_currency, default_bills)

            UserModel.objects(id=user_id).update_one(set__wallet_id=wallet_id)
         
            user_nuevo = UserService.find_user_by_email(email)
            wallet = WalletService.get_wallet(user_nuevo["wallet_id"])

            if wallet:
                wallet_data = {
                    "id": str(wallet.get('_id', wallet.get('id'))), 
                    "currency": wallet.get('currency'),
                    "bills": wallet.get('bills')
                }
            else:
                wallet_data = None

            if user_nuevo:
                user_data = {
                    "id": str(user_nuevo["_id"]),
                    "email": user_nuevo["email"],
                    "name": user_nuevo["name"],
                    "wallet": wallet_data,  
                    "phone": user_nuevo["phone"],
                    "mercado_pago_on": user_nuevo["mercado_pago_on"],
                    "sound_on": user_nuevo["sound_on"],
                    "recientes": user_nuevo["recientes"],
                    "tipo_usuario": user_nuevo["tipo_usuario"]
                }
                return jsonify(user_data), 200
            else:
                return jsonify({"message": "User not found"}), 404

        except ValueError as e:
            return jsonify({"message": str(e)}), 400