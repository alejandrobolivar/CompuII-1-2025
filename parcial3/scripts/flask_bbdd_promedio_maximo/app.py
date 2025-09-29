from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('notas.db')
    conn.row_factory = sqlite3.Row  # Esto permite acceder a los datos de las filas como si fueran diccionarios,
                                    # es decir, puedes acceder a las columnas por nombre en lugar de por índice.
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    students = conn.execute('SELECT cedula, nombre, nota1, nota2, nota3 FROM estudiantes').fetchall()
    conn.close()

    student_averages = []
    for student in students:
        average = (student['nota1'] + student['nota2'] + student['nota3']) / 3
        student_averages.append((student['cedula'], student['nombre'], average))

    top_student = max(student_averages, key=lambda x: x[2])

    return render_template('index.html', student_averages=student_averages, top_student=top_student)

if __name__ == '__main__':
    app.run()
