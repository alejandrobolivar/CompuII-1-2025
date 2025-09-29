from flask import Flask, render_template, redirect, url_for, request, Response
import sqlite3
import matplotlib.pyplot as plt
import numpy as np
import io

app = Flask(__name__)

# Configuración de la base de datos
DATABASE = 'valores.db'

def init_db():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS valores (id INTEGER PRIMARY KEY, valor INTEGER)''')
        conn.commit()

def generar_valores(n):
    valores = np.random.randint(1, 101, size=n)
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.executemany('INSERT INTO valores (valor) VALUES (?)', [(int(valor),) for valor in valores])
        conn.commit()

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM valores')
        valores = [row[0] for row in cursor.fetchall()]
    
    if valores:
        media = np.mean(valores)
        mediana = np.median(valores)
        varianza = np.var(valores)
        desviacion_estandar = np.std(valores)
    else:
        media = mediana = varianza = desviacion_estandar = None

    return render_template('index.html', valores=valores, media=media, mediana=mediana, varianza=varianza, desviacion_estandar=desviacion_estandar)

@app.route('/generar', methods=['POST'])
def generar():
    n = int(request.form['cantidad'])
    generar_valores(n)
    return redirect(url_for('index'))

@app.route('/borrar', methods=['POST'])
def borrar():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM valores')
        conn.commit()
    return redirect(url_for('index'))

@app.route('/grafico.png')
def grafico():
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT valor FROM valores')
        valores = [row[0] for row in cursor.fetchall()]

    fig, ax = plt.subplots()
    ax.plot(valores, marker='o')
    ax.set_title('Valores Generados')
    ax.set_xlabel('Índice')
    ax.set_ylabel('Valor')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    return Response(img.getvalue(), mimetype='image/png')

if __name__ == '__main__':
    init_db()
    app.run()