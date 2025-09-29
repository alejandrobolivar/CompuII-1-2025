from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

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

        # Graficar las rectas y el punto de solución
        x_vals = np.linspace(-10, 10, 400)
        y1_vals = (c1 - a1 * x_vals) / b1
        y2_vals = (c2 - a2 * x_vals) / b2

        plt.figure()
        plt.plot(x_vals, y1_vals, label=f'{a1}x + {b1}y = {c1}')
        plt.plot(x_vals, y2_vals, label=f'{a2}x + {b2}y = {c2}')
        plt.scatter([x], [y], color='red', zorder=5)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.axhline(0, color='black',linewidth=0.5)
        plt.axvline(0, color='black',linewidth=0.5)
        plt.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        plt.legend()
        plt.title('Sistema de Ecuaciones 2x2')

        # Guardar la gráfica en un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()

    except ValueError:
        result = "Por favor, ingresa valores numéricos válidos."
        img_base64 = None
    except np.linalg.LinAlgError:
        result = "El sistema no tiene solución única."
        img_base64 = None

    return render_template('result.html', result=result, img_base64=img_base64)

if __name__ == '__main__':
    app.run(port=5100)
