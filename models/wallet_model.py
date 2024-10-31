# models/wallet_model.py
from mongoengine import Document, fields

class WalletModel(Document):
    user_id = fields.ObjectIdField(required=True)  
    currency = fields.IntField(choices=[0, 1], required=True) 
    bills = fields.ListField(fields.IntField(), required=True)  