from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import re

app = Flask(__name__)

#Almacenamiento en memoria para usuarios, mascotas y dueños
user = {}
mascota = {}
dueno = {}

#Restricción de contraseña segura
def sec_passwd(password):
    if len(password) < 8 or len(password) > 15:
        return False
    if not any(char.isupper() for char in password):
        return False
    if not any(char in "¡”#$%&/(()" for char in password):
        return False
    return True

#Registrar un nuevo usuario en el sistema
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        return jsonify({"error": "Todos los campos son obligatorios"}), 400

    if not sec_passwd(password):
        return jsonify({"error": "La contraseña debe tener entre 8 y 15 caracteres, al menos una letra mayúscula y un carácter especial"}), 400

    hashed_password = generate_password_hash(password)
    user[username] = {"email": email, "password": hashed_password}
    return jsonify({"message": "El usuario ha sido registrado correctamente!"}), 201

#Logear usuario en el sistema
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    usr = user.get(username)
    if not usr or not check_password_hash(usr['password'], password):
        return jsonify({"error": "Datos de sesión incorrectos!!"}), 401

    return jsonify({"message": f"Bienvenido {username}"}), 200

#Registrar nuevas mascotas en la base de datos
@app.route('/mascotas', methods=['POST'])
def crt_msct():
    data = request.get_json()
    cve = data.get('cve')
    name = data.get('name')
    raza = data.get('raza')
    edad = data.get('edad')
    enferm = data.get('enferm')
    mascota[cve] = {"name": name, "raza": raza, "edad": edad, "enferm": enferm}
    return jsonify({"message": "Mascota registrada correctamente on DB!"}), 201

#Obtener datos de todas las mascotas existentes
@app.route('/mascotas', methods=['GET'])
def get_mscts():
    return jsonify(mascota), 200

#Obtener datos de una mascota en específico
@app.route('/mascotas/<int:cve>', methods=['GET'])
def get_msct(cve):
    msct = mascota[cve] #mascota.get(cve)
    if not msct:
        return jsonify({"error": "Mascota no encontrada"}), 404
    return jsonify(msct), 200

#Actualizar datos de mascota existente
@app.route('/mascotas/<int:cve>', methods=['PUT'])
def upd_msct(cve):
    data = request.get_json()
    if cve not in mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404
    mascota[cve].update(data)
    return jsonify({"message": "Datos actualizados de la mascota: "}, cve), 200

#Eliminar mascota de la base de datos
@app.route('/mascotas/<int:cve>', methods=['DELETE'])
def del_msct(cve):
    if cve not in mascota:
        return jsonify({"error": "Mascota no encontrada"}), 404
    del mascota[cve]
    return jsonify({"message": "Mascota eliminada de la DB"}), 200


#Registrar nuevo dueño en la base de datos
@app.route('/dueños', methods=['POST'])
def crt_duen():
    data = request.get_json()
    cve_msc = data.get('cve_msc')
    name = data.get('name')
    tel = data.get('tel')
    domc = data.get('domc')
    edad = data.get('edad')
    correo = data.get('correo')
    dueno[cve_msc] = {"name": name, "tel": tel, "domc": domc, "edad": edad, "correo": correo}
    return jsonify({"message": "Dueño registrado correctamente on DB!"}), 201

#Obtener datos de dueños existentes
@app.route('/dueños', methods=['GET'])
def get_duens():
    return jsonify(dueno), 200

#Obtener datos de dueño específico
@app.route('/dueños/<int:cve_msc>', methods=['GET'])
def get_duen(cve_msc):
    duen = dueno[cve_msc] #duenos.get(cve_msc)
    if not duen:
        return jsonify({"error": "Dueño no encontrado"}), 404
    return jsonify(duen), 200

#Actualizar datos de dueños existentes
@app.route('/dueños/<int:cve_msc>', methods=['PUT'])
def upd_duen(cve_msc):
    data = request.get_json()
    if cve_msc not in dueno:
        return jsonify({"error": "Dueño no encontrado"}), 404
    dueno[cve_msc].update(data)
    return jsonify({"message": "Datos actualizados del dueño: "}, cve_msc), 200

#Eliminar dueño de la base de datos
@app.route('/dueños/<int:cve_msc>', methods=['DELETE'])
def del_duen(cve_msc):
    if cve_msc not in dueno:
        return jsonify({"error": "Dueño no encontrado"}), 404
    del dueno[cve_msc]
    return jsonify({"message": "Dueño eliminado de la DB"}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)