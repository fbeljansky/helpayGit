from models.wallet_model import WalletModel
from bson import ObjectId

class WalletService:

    @staticmethod
    def create_wallet(user_id, currency, bills):
        wallet = WalletModel(user_id=ObjectId(user_id), currency=currency, bills=bills)
        wallet.save()
        return str(wallet.id)  

    @staticmethod
    def get_wallet(wallet_id):
        try:
            wallet = WalletModel.objects(id=ObjectId(wallet_id)).first()
            if wallet:
                wallet_dict = wallet.to_mongo().to_dict()
                wallet_dict['_id'] = str(wallet_dict['_id']) 
                wallet_dict['user_id'] = str(wallet_dict['user_id']) 
                return wallet_dict
            return None
        except Exception as e:
            raise ValueError(f"Invalid wallet ID: {str(e)}")

    @staticmethod
    def update_wallet(wallet_id, update_data):
        try:
            wallet = WalletModel.objects(id=ObjectId(wallet_id)).first()
            if not wallet:
                raise ValueError("Wallet not found")
            wallet.update(**update_data)
        except Exception as e:
            raise ValueError(f"Invalid wallet ID: {str(e)}")

    @staticmethod
    def delete_wallet(wallet_id):
        try:
            result = WalletModel.objects(id=ObjectId(wallet_id)).delete()
            if result == 0:
                raise ValueError("Wallet not found")
        except Exception as e:
            raise ValueError(f"Invalid wallet ID: {str(e)}")

    @staticmethod
    def get_wallets_by_user(user_id):
        wallets = WalletModel.objects(user_id=ObjectId(user_id))
        wallet_list = []
        for wallet in wallets:
            wallet_dict = wallet.to_mongo().to_dict()
            wallet_dict['_id'] = str(wallet_dict['_id']) 
            wallet_dict['user_id'] = str(wallet_dict['user_id'])  
            wallet_list.append(wallet_dict)
        return wallet_list
