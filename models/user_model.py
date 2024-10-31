# models/user_model.py
from flask_mongoengine import MongoEngine

db = MongoEngine()

class UserModel(db.Document):
    email = db.StringField(required=True, unique=True) 
    name = db.StringField() 
    phone = db.StringField() 
    mercado_pago_on = db.BooleanField(default=True)  
    sound_on = db.BooleanField(default=False) 
    wallet_id = db.ObjectIdField() 
    recientes = db.ListField(db.DictField()) 
    persona_asociada = db.ReferenceField('self') 
    tipo_usuario = db.StringField()  
    user_asociado = db.ReferenceField('UserModel') 
