from flask import Flask
from flask_restplus import *
from flask_sqlalchemy import SQLAlchemy

from src.utils.general import get_db_conn_sql


# Creando app de flask
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_conn_str
api = Api(app)
db = SQLAlchemy(app)


class Match(db.Model):
    __table_args__ = {'schema': 'api'}
    __tablename__ = 'api_prediccion'


    fecha_parametro = db.Column(db.String)
    inspection_id = db.Column(db.Integer, primary_key=True)
    dba_name = db.Column(db.Integer)
    prediccion = db.Column(db.Integer)
    prediccion_proba = db.Column(db.Float)


# swagger model for marshalling outputs
probabilidades = api.model(
                    "probabilidad_establecimiento", 
                    {
                        'fecha_parametro': fields.String,
                        'inspection_id': fields.Integer,
                        'dba_name': fields.Integer,
                        'prediccion': fields.Integer,
                        'prediccion_proba': fields.Float
                    }        
                 )


#Endpoint1: Obtiene probabilidad con base en el id del establecimiento
@api.route('/prob_establecimiento/<int:dba_name>')
class ShowMatch(Resource):
    @api.marshal_with(probabilidades, as_list=True)
    def get(self, dba_name):
        match = Match.query.filter_by(dba_name=dba_name).all()
        return match


#Endpoint2: Obtiene todas las proabilidades con base en una fecha
@api.route('/prob_fecha/<string:fecha_parametro>')
class ShowMatch2(Resource):
    @api.marshal_with(probabilidades, as_list=True)
    def get(self, fecha_parametro):
        match2 = Match.query.filter_by(fecha_parametro=fecha_parametro).all()
        return match2


if __name__== '__main__':
    app.run(debug=True)









