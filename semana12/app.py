import os
import json
import csv
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

# --- Configuración de la Aplicación Flask ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'una_clave_secreta_muy_segura'

# --- Persistencia con SQLite y SQLAlchemy ---
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'database', 'usuarios.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return f'<Usuario {self.nombre}>'

# --- Rutas de la Aplicación ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/formulario', methods=['GET', 'POST'])
def formulario():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        
        # Guardar en diferentes formatos de datos
        guardar_en_txt(nombre, email)
        guardar_en_json(nombre, email)
        guardar_en_csv(nombre, email)
        guardar_en_db(nombre, email)
        
        flash('Datos guardados con éxito!', 'success')
        return redirect(url_for('resultado'))
    
    return render_template('formulario.html')

@app.route('/resultado')
def resultado():
    datos_txt = leer_de_txt()
    datos_json = leer_de_json()
    datos_csv = leer_de_csv()
    datos_db = leer_de_db()
    
    return render_template(
        'resultado.html',
        datos_txt=datos_txt,
        datos_json=datos_json,
        datos_csv=datos_csv,
        datos_db=datos_db
    )

# --- Funciones para Persistencia con Archivos ---
def guardar_en_txt(nombre, email):
    with open('datos/datos.txt', 'a') as f:
        f.write(f'Nombre: {nombre}, Email: {email}\n')

def leer_de_txt():
    if not os.path.exists('datos/datos.txt'):
        return []
    with open('datos/datos.txt', 'r') as f:
        return f.readlines()

def guardar_en_json(nombre, email):
    datos = []
    if os.path.exists('datos/datos.json') and os.path.getsize('datos/datos.json') > 0:
        with open('datos/datos.json', 'r') as f:
            datos = json.load(f)
    
    datos.append({'nombre': nombre, 'email': email})
    
    with open('datos/datos.json', 'w') as f:
        json.dump(datos, f, indent=4)

def leer_de_json():
    if not os.path.exists('datos/datos.json') or os.path.getsize('datos/datos.json') == 0:
        return []
    with open('datos/datos.json', 'r') as f:
        return json.load(f)

def guardar_en_csv(nombre, email):
    file_exists = os.path.exists('datos/datos.csv')
    with open('datos/datos.csv', 'a', newline='') as f:
        writer = csv.writer(f)
        if not file_exists or os.path.getsize('datos/datos.csv') == 0:
            writer.writerow(['nombre', 'email'])
        writer.writerow([nombre, email])

def leer_de_csv():
    if not os.path.exists('datos/datos.csv') or os.path.getsize('datos/datos.csv') == 0:
        return []
    
    datos = []
    with open('datos/datos.csv', 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            datos.append(row)
    return datos

# --- Funciones para Persistencia con la Base de Datos ---
def guardar_en_db(nombre, email):
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    try:
        db.session.add(nuevo_usuario)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        flash(f'Error al guardar en la base de datos: {e}', 'danger')

def leer_de_db():
    try:
        return Usuario.query.all()
    except Exception as e:
        flash(f'Error al leer de la base de datos: {e}', 'danger')
        return []

if __name__ == '__main__':
    # Asegúrate de que los directorios existan
    os.makedirs('datos', exist_ok=True)
    os.makedirs('database', exist_ok=True)
    
    # Crear las tablas de la base de datos si no existen
    with app.app_context():
        db.create_all()
        
    app.run(debug=True)