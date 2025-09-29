from flask import Flask, request, render_template
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/solve', methods=['POST'])
def solve():
    try:
        # Obtener los coeficientes de las ecuaciones del formulario
        a1 = float(request.form['a1'])
        b1 = float(request.form['b1'])
        c1 = float(request.form['c1'])
        a2 = float(request.form['a2'])
        b2 = float(request.form['b2'])
        c2 = float(request.form['c2'])

        # Crear las matrices para el sistema de ecuaciones
        A = np.array([[a1, b1], [a2, b2]])
        B = np.array([c1, c2])

        # Resolver el sistema de ecuaciones
        solution = np.linalg.solve(A, B)
        x, y = solution
        result = f"Solución: x = {x}, y = {y}"
    except ValueError:
        result = "Por favor, ingresa valores numéricos válidos."
    except np.linalg.LinAlgError:
        result = "El sistema no tiene solución única."

    return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(port=5100)
