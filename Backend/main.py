
from flask import Flask, request, jsonify
from models import db, Equipos, Jugadores
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI']= 'postgresql+psycopg2://postgres:fumi1016@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False



@app.route('/')
def hello_world():
    return 'Hello world!'

@app.route('/equipos', methods=['GET'])
def get_equipos():
    try: 
        equipos = Equipos.query.order_by(Equipos.nombre).all()
        #print(equipos)
        equipos_data = []
        for equipo in equipos:
            equipo_data = {
                'id': equipo.id,
                'nombre': equipo.nombre,
                'titulos': equipo.titulos,
                'estadio': equipo.estadio,
                'image': equipo.image
            }
            equipos_data.append(equipo_data)
        return jsonify({'equipos': equipos_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500

@app.route('/jugadores/<id>', methods=['GET'])
def get_jugadores_individuales(id):
    try: 
        jugador = Jugadores.query.get(id)
        #print(equipos)
        jugador_data = {
            'id': jugador.id,
            'id_equipo': jugador.id_equipo,
            'nombre': jugador.nombre,
            'edad': jugador.edad,
            'altura': jugador.altura,
            'posicion': jugador.posicion,
            'nacionalidad': jugador.nacionalidad
        }
        return jugador_data
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/equipos/<id_equipo>', methods=['GET'])
def get_equipo_individual(id_equipo):    
    try: 
        equipo = Equipos.query.get(id_equipo)
        #print(equipos)       
        equipo_data = {
           #'id': equipo.id,
            'nombre': equipo.nombre,
            'titulos': equipo.titulos,
            'estadio': equipo.estadio,
            'image': equipo.image   
        }
        return equipo_data
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/equipos/<id_equipo>/jugadores', methods=['GET'])
def get_jugadores_equipo(id_equipo):
    try: 
        equipo = Equipos.query.get(id_equipo)
        #print(equipos) 
        equipo_data = {
            #'nombre': equipo.nombre,
            #'id': equipo.id,
            #'titulos': equipo.titulos,
            #'estadio': equipo.estadio,
            'jugadores': []
            
        }
        for jugador in equipo.jugadores:      
            jugador_data = {
                'id': jugador.id,
                'id_equipo': jugador.id_equipo,
                'nombre': jugador.nombre,
                'edad': jugador.edad,
                'altura': jugador.altura,
                'posicion': jugador.posicion,
                'nacionalidad': jugador.nacionalidad
            }
            equipo_data['jugadores'].append(jugador_data)
        return equipo_data 
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500


@app.route('/agregar_jugador', methods=['POST'])
def nuevo_jugador():
    try:
        data = request.json

        id_equipo = data.get('id_equipo')
        nombre = data.get('nombre')
        edad = data.get('edad')
        altura = data.get('altura')
        posicion = data.get('posicion')
        nacionalidad = data.get('nacionalidad')

        nuevo_jugador = Jugadores(
            id_equipo=id_equipo,
            nombre=nombre,
            edad=edad,
            altura=altura,
            posicion=posicion,
            nacionalidad=nacionalidad
        )
        db.session.add(nuevo_jugador)
        db.session.commit()

        return jsonify({
            'message': 'Jugador agregado exitosamente',
            'jugador': {
                'id': nuevo_jugador.id,
                'id_equipo': nuevo_jugador.id_equipo,
                'nombre': nuevo_jugador.nombre,
                'edad': nuevo_jugador.edad,
                'altura': nuevo_jugador.altura,
                'posicion': nuevo_jugador.posicion,
                'nacionalidad': nuevo_jugador.nacionalidad
            }
        }), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



@app.route('/jugadores/<int:id>', methods=['PUT'])
def update_jugador(id):
    jugador = Jugadores.query.get(id)
    if jugador is None:
        abort(404, description="Jugador no encontrado")

    datos = request.get_json()
    
    if 'nombre' not in datos or 'edad' not in datos or 'altura' not in datos or 'posicion' not in datos or 'nacionalidad' not in datos:
        abort(400, description="Datos incompletos")
    
    jugador.nombre = datos['nombre']
    jugador.edad = datos['edad']
    jugador.altura = datos['altura']
    jugador.posicion = datos['posicion']
    jugador.nacionalidad = datos['nacionalidad']
    
    db.session.commit()
    
    return jsonify({
        'id': jugador.id,
        'nombre': jugador.nombre,
        'edad': jugador.edad,
        'altura': jugador.altura,
        'posicion': jugador.posicion,
        'nacionalidad': jugador.nacionalidad
    })

@app.route('/jugadores/<id>', methods=['DELETE'])
def eliminar_jugador(id):
    try:
        jugador = Jugadores.query.get(id)
        if jugador is None:
            return jsonify({'message': 'Jugador no encontrado'}), 404

        db.session.delete(jugador)
        db.session.commit()

        return jsonify({'message': 'Jugador eliminado correctamente'}), 200

    except Exception as error:
        print(f'Error al eliminar el jugador: {error}')
        return jsonify({'message': 'Error interno del servidor'}), 500



if __name__ == '__main__':
    print('Starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(host='0.0.0.0', debug=True, port=port)