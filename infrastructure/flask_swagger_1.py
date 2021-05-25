from flask import Flask
from flask_restplus import Api, Resource

#create Flask app
app = Flask(__name__)
api = Api(app)


# endpoints api en lugar de app en el decorador, clases en lugar de funciones. Tipo Resource
@api.route('/')
class HelloWorld(Resource):
	def get(self):
		return "Hello World Flask"


# con parámetros
@api.route('/test/<int:id_client>')
class Test(Resource):
	def get(self, id_client):
		return 'Flask with parameters, id_client: {}'.format(id_client)


# con parámetros, regresa json
@api.route('/test_json/<nombre>')
class TestJson(Resource):
	def get(self, nombre):
		return nombre


if __name__== '__main__':
	app.run(debug=True)