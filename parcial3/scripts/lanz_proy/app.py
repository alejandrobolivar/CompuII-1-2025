from flask import Flask, render_template, request, redirect, url_for
import sqlite3


app = Flask(__name__)

# Función para crear las bases de datos
def init_db():
    with sqlite3.connect('entrada.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS entrada
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         variable TEXT,
                         valor REAL)''')
    with sqlite3.connect('salidas.db') as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS salida
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         variable TEXT,
                         valor REAL)''')

# Ruta principal
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        variables = ['vx', 'vy', 'ax', 'ay', 't']
        known_vars = {var: request.form.get(var) for var in variables if request.form.get(var)}

        with sqlite3.connect('entrada.db') as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM entrada')
            for var, val in known_vars.items():
                cursor.execute('INSERT INTO entrada (variable, valor) VALUES (?, ?)', (var, float(val)))
            conn.commit()

        return redirect(url_for('result'))

    return render_template('index.html')

# Ruta para mostrar los resultados
@app.route('/result')
def result():
    with sqlite3.connect('entrada.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT variable, valor FROM entrada')
        known_vars = {row[0]: row[1] for row in cursor.fetchall()}

    # Cálculos de cinemática
    vx = known_vars.get('vx', 0)
    vy = known_vars.get('vy', 0)
    ax = known_vars.get('ax', 0)
    ay = known_vars.get('ay', 0)
    t = known_vars.get('t', 0)

    # Ejemplo de cálculo: posición final en x y y
    x = vx * t + 0.5 * ax * t**2
    y = vy * t + 0.5 * ay * t**2

    calculated_vars = {'x': x, 'y': y}

    with sqlite3.connect('salidas.db') as conn:
        cursor = conn.cursor()
        cursor.execute('DELETE FROM salida')
        for var, val in calculated_vars.items():
            cursor.execute('INSERT INTO salida (variable, valor) VALUES (?, ?)', (var, val))
        conn.commit()

    return render_template('result.html', known_vars=known_vars, calculated_vars=calculated_vars)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
