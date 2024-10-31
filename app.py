from flask import Flask, jsonify
from flask_mongoengine import MongoEngine
from controllers.user_controller import user_controller
from controllers.billete_controller import billete_controller
from controllers.wallet_controller import wallet_controller
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
# app.config["MONGO_URI"] = "mongodb+srv://fbeljansky:<password>@helpaydb.a2u15.mongodb.net/?retryWrites=true&w=majority&appName=helPayDb&tlsCAFile=isrgrootx1.pem"


# This would usually come from your config file
DB_URI = "mongodb+srv://fbeljansky:Rio3ro34@helpaydb.a2u15.mongodb.net/?retryWrites=true&w=majority&appName=helPayDb"

app.config["MONGODB_HOST"] = DB_URI

db = MongoEngine(app)


app.register_blueprint(user_controller)
# Registrar el controlador
app.register_blueprint(billete_controller)

# Registrar el blueprint de billetera
app.register_blueprint(wallet_controller)

# Verificar la conexión a MongoDB al iniciar la aplicación
def check_mongo_connection():
    try:
        with app.app_context():  # Establece el contexto de la aplicación
            # Intenta obtener información del servidor para verificar la conexión
            db.connection.server_info()  # Lanza una excepción si la conexión falla
            print("Successfully connected to MongoDB!")
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        raise

check_mongo_connection()  # Llamada para verificar la conexión

# Manejador global de errores
@app.errorhandler(Exception)
def handle_exception(e):
    response = {
        "message": str(e),
        "type": e.__class__.__name__
    }
    return jsonify(response), 500


if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0')

@app.route('/')
def index():
    return jsonify(status=200, message="Hello, world!")

