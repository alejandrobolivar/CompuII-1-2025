from flask import Flask, request, g, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'notas.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['POST'])
def add_student():
    db = get_db()
    db.execute('INSERT INTO estudiantes (cedula, nombre, nota1, nota2, nota3) VALUES (?, ?, ?, ?, ?)',
               [request.form['cedula'], request.form['nombre'], request.form['nota1'], request.form['nota2'], request.form['nota3']])
    db.commit()
    return redirect(url_for('index'))

@app.route('/show')
def show_students():
    db = get_db()
    cur = db.execute('SELECT cedula, nombre, nota1, nota2, nota3 FROM estudiantes')
    students = cur.fetchall()
    return render_template('show.html', students=students)

if __name__ == '__main__':
    app.run()
