from flask import Flask
from flask import request
from flask import render_template_string
import sqlite3  # maneja la base de datos local
import hashlib  # genera contraseñas encriptadas
import os

DB_nombre = "usuarios.db"

def crear_base_datos():
    if not os.path.exists(DB_nombre):
        conn = sqlite3.connect(DB_nombre)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE usuarios (
                nombre TEXT NOT NULL,
                password_hash TEXT NOT NULL
            )
        ''')
        datos = [
            ("Alejandro", hashlib.sha256("duoc123".encode()).hexdigest()),
            ("Thomas", hashlib.sha256("duoc123".encode()).hexdigest()),
        ]
        cursor.executemany("INSERT INTO usuarios (nombre, password_hash) VALUES (?, ?)", datos)
        conn.commit()
        conn.close()
        print("Base de datos creada con exito")
    else:
        print("Base de datos ya existe.")

def verificar_usuario(nombre, password):
    conn = sqlite3.connect(DB_nombre)
    cursor = conn.cursor()
    cursor.execute("SELECT password_hash FROM usuarios WHERE nombre = ?", (nombre,))
    row = cursor.fetchone()
    conn.close()
    if row:
        hash_ingresado = hashlib.sha256(password.encode()).hexdigest()
        return hash_ingresado == row[0]
    return False

app = Flask(__name__)
crear_base_datos()

HTML = '''
<!doctype html>
<title>Login Examen</title>
<h2>Ingreso de Usuario</h2>
<form method="post">
  Nombre: <input type="text" name="nombre"><br>
  Contraseña: <input type="password" name="password"><br>
  <input type="submit" value="Ingresar">
</form>
<p>{{ mensaje }}</p>
'''

@app.route('/', methods=['GET', 'POST'])
def login():
    mensaje = ""
    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        if verificar_usuario(nombre, password):
            mensaje = f"Bienvenido {nombre}, acceso permitido."
        else:
            mensaje = "Usuario o contraseña incorrectos."
    return render_template_string(HTML, mensaje=mensaje)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5800)
