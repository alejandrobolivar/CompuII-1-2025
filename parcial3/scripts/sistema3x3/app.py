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
        d1 = float(request.form['d1'])
        a2 = float(request.form['a2'])
        b2 = float(request.form['b2'])
        c2 = float(request.form['c2'])
        d2 = float(request.form['d2'])
        a3 = float(request.form['a3'])
        b3 = float(request.form['b3'])
        c3 = float(request.form['c3'])
        d3 = float(request.form['d3'])

        # Crear las matrices para el sistema de ecuaciones
        A = np.array([[a1, b1, c1], [a2, b2, c2], [a3, b3, c3]])
        B = np.array([d1, d2, d3])

        # Resolver el sistema de ecuaciones
        solution = np.linalg.solve(A, B)
        x, y, z = solution
        result = f"Solución: x = {x}, y = {y}, z = {z}"

        # Graficar las ecuaciones y la línea de intersección
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Crear una malla de puntos
        x_vals = np.linspace(-10, 10, 400)
        y_vals = np.linspace(-10, 10, 400)
        X, Y = np.meshgrid(x_vals, y_vals)

        # Ecuaciones de los planos
        Z1 = (d1 - a1 * X - b1 * Y) / c1
        Z2 = (d2 - a2 * X - b2 * Y) / c2
        Z3 = (d3 - a3 * X - b3 * Y) / c3

        ax.plot_surface(X, Y, Z1, alpha=0.5, rstride=100, cstride=100)
        ax.plot_surface(X, Y, Z2, alpha=0.5, rstride=100, cstride=100)
        ax.plot_surface(X, Y, Z3, alpha=0.5, rstride=100, cstride=100)

        # Línea de intersección
        t_vals = np.linspace(-10, 10, 400)
        x_line = x + t_vals
        y_line = y + t_vals
        z_line = z + t_vals
        ax.plot(x_line, y_line, z_line, color='red')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title('Sistema de Ecuaciones 3x3')

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
    app.run(debug=True)
