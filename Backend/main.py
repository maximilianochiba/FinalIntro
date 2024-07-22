
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



@app.route('/jugadores', methods=['GET'])
def get_jugadores2():
    try: 
        jugadores = Jugadores.query.order_by(Jugadores.nombre).all()
        #print(equipos)
        jugadores_data = []
        for juagador in jugadores:
            jugador_data = {
                'id': jugador.id,
                'id_equipo': jugador.id_equipo,
                'nombre': jugador.nombre,
                'edad': jugador.edad,
                'altura': jugador.altura,
                'posicion': jugador.posicion,
                'nacionalidad': jugador.nacionalidad
            }
            jugadores_data.append(jugador_data)
        return jsonify({'jugadores': jugadores_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



@app.route('/jugadores/<id>', methods=['GET'])
def get_jugadores3(id):
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
def data(id_equipo):    
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
def data2(id_equipo):
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



@app.route('/equipos/<id_equipo>', methods=['POST'])
def nuevo_jugador(id_equipo):
    try: 
        #equipo = Equipos.query.get(id_equipo)

        data = request.json
        
        id_equipo = data.get('id_equipo')
        nombre = data.get('nombre')
        edad = data.get('edad')
        altura = data.get('altura')
        posicion = data.get('posicion')
        nacionalidad = data.get('nacionalidad')
        if not id_equipo or not nombre or not edad or not altura or not posicion or not nacionalidad:
            return jsonify({'message': 'Bad request, isbn or name or cantPages or author not found'}), 400
        new_jugador = Jugadores(id_equipo=id_equipo, nombre=nombre, edad=edad, altura=altura, posicion=posicion, nacionalidad=nacionalidad)
        db.session.add(new_jugador)
        db.session.commit()
        return jsonify({'jugador': {'id': new_jugador.id, 'id_equipo': new_jugador.id_equipo, 'nombre': new_jugador.nombre, 'edad': new_jugador.edad, 
        'altura': new_jugador.altura, 'posicion': new_jugador.posicion, 'nacionalidad': new_jugador.nacionalidad}}), 201
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500



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



@app.route('/equipos/river', methods=['GET'])
def get_jugadores():
    try: 
        jugadores = Jugadores.query.where(Jugadores.id_equipo == 1).all()
        #print(equipos)
        jugadores_data = []
        for jugador in jugadores:
            jugador_data = {
                'id': jugador.id,
                'id_equipo': jugador.id_equipo,
                'nombre': jugador.nombre,
                'edad': jugador.edad,
                'altura': jugador.altura,
                'posicion': jugador.posicion,
                'nacionalidad': jugador.nacionalidad
            }
            jugadores_data.append(jugador_data)
        return jsonify({'jugadores': jugadores_data})
    except Exception as error:
        print('Error', error)
        return jsonify({'message': 'Internal server error'}), 500








if __name__ == '__main__':
    print('Starting server...')
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print('Started...')
    app.run(host='0.0.0.0', debug=True, port=port)