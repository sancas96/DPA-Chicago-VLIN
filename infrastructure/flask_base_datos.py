from flask import Flask
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Resource, Api, fields
from werkzeug import cached_property

from src.utils.general import get_db_conn_sql_alchemy


# connecting to db strin
db_conn_str = get_db_conn_sql_alchemy('../../conf/local/credentials.yaml')


# create Flask app
app = Flask(__name__)
app.config['SQLALCHEMY DATABASE_URI'] = db_conn_str
api = Api(app)

db = SQLAlchemy(app)


# Tabla deploy.mockup match_api
class Match(db.Model):
	__table_args__ = {'schema': 'deploy'}
	__tablename__ = 'mockup_match_api'

	id_candidato = db.Column(db.Integer)
	id_oferta = db.Column(db.Integer, primary_key=True)
	match_score = db.Column(db.Float)
	match = db.Column(db.String)
	fecha_prediccion = db.Column(db.DateTime)

	def __repr__(self):
		return(u'<{self.__class__.__name__}: {self.id}>'.format(self = self))


# swagger model dor marshalling outputs
model = api.model("oferta_match_table", {
	'id_oferta': fields.Integer,
	'match_score': fields.Float,
	'match': fields.String,
	'fecha_prediccion': fields.Date
})


# final output id_candidato: '', ofertas: []
model_list = api.model('oferta_match_output', {
	'id_candidato': fields.Integer,
	'ofertas': fields.Nested(model)
})


# endpoints
@api.route('/')
class HelloWorld(Resource):
	def get(self):
		return {'Hello': 'Hello World'}


@api.route('/match_ofertas/<int:id_candidato>')
class ShowMatch(Resource):
	@api.marshal_with(model_list, as_list=True)
	def get(self, id_candidato):
		match = Match.query.filter_by(id_candidato=id_candidato).order_by(Match.match_score.desc()).limit(10).all()
		ofertas = []
		for element in match:
			ofertas.append({'id_oferta': element.id_oferta,
							'match_score': element.match_score,
							'match': element.match,
							'fecha_prediccion': element.fecha_prediccion})

		return {'id_candidato': id_candidato, 'ofertas': ofertas}


if __name__== '__main__':
	app.run(debug=True)