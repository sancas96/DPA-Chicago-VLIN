from flask import Flask
from flask import jsonify


# create Flask app
app = Flask(__name__)


# endpoints
@app.route('/')
def hello_wold():
	return "Hello World Flask!"


# con parámetros
@app.route('/test/<int:id_client>')
def test(id_client):
	return 'Flask with parameters, id_client: {}'.format(id_client)


#con parámetros, regresa json
@app.route('/test_json/<nombre>')
def test_json(nombre):
	return jsonify(nombre)


if __name__== '__main__':
	app.run(debug=True)