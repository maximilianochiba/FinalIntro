import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Equipos(db.Model):
    __tablename__ = 'equipos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    titulos = db.Column(db.Integer, nullable=False)
    estadio = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(100), nullable=False)
    jugadores = db.relationship("Jugadores")

class Jugadores(db.Model):
    __tablename__ = 'jugadores'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_equipo = db.Column(db.Integer, db.ForeignKey('equipos.id'))
    nombre = db.Column(db.String(255), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    altura = db.Column(db.Integer, nullable=False)
    posicion = db.Column(db.String(255), nullable=False)
    nacionalidad = db.Column(db.String(255), nullable=False)
