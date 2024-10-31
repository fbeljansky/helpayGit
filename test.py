import requests

BASE = "http://127.0.0.1:5000/"

#enviar get a la url que es la base + helloworld

#response = requests.get(BASE + "helloworld")
#response = requests.get(BASE + "helloworld/bill") #para la de diccionario 

#response = requests.get(BASE + "helloworld/Carlos/29")
response = requests.post(BASE + "video/1",{"name":"video1", "views":100, "likes":10}) #para acceder a esa parte es el request cuerpo digamos print(request.form['likes'])

print(response.json()) #imprime el json que se recibe