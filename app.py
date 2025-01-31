from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuración de la base de datos
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Crear la tabla de preguntas
def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS preguntas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descripcion TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = get_db_connection()
    preguntas = conn.execute('SELECT * FROM preguntas').fetchall()
    conn.close()
    return render_template('index.html', preguntas=preguntas)

@app.route('/pregunta/nueva', methods=('GET', 'POST'))
def nueva_pregunta():
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']
        conn = get_db_connection()
        conn.execute('INSERT INTO preguntas (titulo, descripcion) VALUES (?, ?)',
                     (titulo, descripcion))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('pregunta.html')

if __name__ == '__main__':
    app.run(debug=True)