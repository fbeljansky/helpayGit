from flask import Flask, request
from flask_restful import Api, Resource, abort, reqparse
from flask_sqlalchemy import SQLAlchemy
from flask_pymongo import PyMongo

from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configurar la URI de conexión a MongoDB Atlas usando la variable de entorno
app.config["MONGO_URI"] = os.getenv("MONGO_URI")




# Create a new Flask app
app=Flask(__name__)
# Create a new Flask-RESTful API
api=Api(app)



names = {'tim': {'age': 19, 'gender': "male"},
         "bill": {'age': 70, 'gender': "male"},
         }

videos = {}
 
def abort_if_video_id_doesnt_exist(video_id):
    if video_id not in videos:
        abort(404, message="Could not find video...")

def abort_if_video_id_exists(video_id):
    if video_id in videos:
        abort(409, message="Video already exists with that ID...")

video_put_args = reqparse.RequestParser() #creamos un objeto de tipo reqparse
video_put_args.add_argument("name", type=str, help="Name of the video", required=True) #agregamos argumentos al objeto
video_put_args.add_argument("views", type=int, help="Views of the video", required=True)
video_put_args.add_argument("likes", type=int, help="Likes on the video", required=True)

class HelloWorld(Resource): #heredamos de resource que tiene metodos como get/put/delete
    def get(self,name,age): #reescribimos el metodo get, self es el objeto de la clase
        return {'data': name,'edad':age}  # return python dictionary
        #return names[name] y devuelve el que esta en el diccionario 
    def post(self):
        return {'data': 'Posted'}  # return python dictionary
    
class Video (Resource):
    def get(self,video_id):
        abort_if_video_id_doesnt_exist(video_id)
        return {'video_id':video_id}
    
    def post(self,video_id):     #con .parse_args() se obtienen los argumentos que se pasan en el request
        abort_if_video_id_exists(video_id)
        args=video_put_args.parse_args() #parseamos los argumentos que se pasan en el request, si no se pasan los requeridos se manda un error
        videos[video_id] = args
        return videos[video_id], 201  #ese es el status code de que se creo correctamente

api.add_resource(Video, '/video/<int:video_id>')

#agregamos un recurso a la api y agregamos la ruta al recurso
api.add_resource(HelloWorld, '/helloworld/<string:name>/<int:age>') # Add the HelloWorld resource to the API with the route /helloworld
# con <string:name> le decimos que el recurso espera un parametro de tipo string

if __name__ == '__main__': # Only run the app if this script is run directly
    app.run(debug=True) # Run the app in debug mode


