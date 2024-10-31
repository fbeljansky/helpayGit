from bson import ObjectId
from models.user_model import UserModel

class UserService:

    @staticmethod
    def get_all_users():
        users = []
        for user in UserModel.objects:
            user_dict = user.to_mongo().to_dict()
            user_dict['_id'] = str(user_dict['_id']) 
            users.append(user_dict)
        return users

    @staticmethod
    def find_user(user_id):
        try:
            user = UserModel.objects(id=ObjectId(user_id)).first()
            if user:
                user_dict = user.to_mongo().to_dict()
                user_dict['_id'] = str(user_dict['_id'])  
                return user_dict
            return None
        except Exception as e:
            raise ValueError(f"Invalid user ID: {str(e)}")

    @staticmethod
    def create_user(user_data):
        if UserModel.objects(email=user_data.get("email")).first():
            raise ValueError("User already exists")
        user = UserModel(**user_data)
        user.save()
        return str(user.id) 

    @staticmethod
    def update_user(user_id, user_data):
        try:
            user_id = ObjectId(user_id)
            user = UserModel.objects(id=user_id).first()
            if not user:
                raise ValueError("User not found")
            
            user.update(**user_data)
        except Exception as e:
            raise ValueError(f"Invalid user ID: {str(e)}")

    @staticmethod
    def delete_user(user_id):
        try:
            result = UserModel.objects(_id=ObjectId(user_id)).delete()
            if result == 0:
                raise ValueError("User not found")
        except Exception as e:
            raise ValueError(f"Invalid user ID: {str(e)}")

    @staticmethod
    def find_user_by_email(email):
        user = UserModel.objects(email=email).first()
        if user:
            user_dict = user.to_mongo().to_dict()
            user_dict['_id'] = str(user_dict['_id']) 
            if user_dict.get('wallet_id'):
                user_dict['wallet_id'] = str(user_dict['wallet_id'])
            if user_dict.get('user_asociado'):
                user_dict['user_asociado'] = str(user_dict['user_asociado'])
            return user_dict
        return None