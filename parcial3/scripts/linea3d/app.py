from flask import Flask, request, render_template
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plot', methods=['POST'])
def plot():
    try:
        # Obtener los puntos inicial y final de la línea del formulario
        x1 = float(request.form['x1'])
        y1 = float(request.form['y1'])
        z1 = float(request.form['z1'])
        x2 = float(request.form['x2'])
        y2 = float(request.form['y2'])
        z2 = float(request.form['z2'])

        # Crear los puntos de la línea
        x_vals = np.linspace(x1, x2, 100)
        y_vals = np.linspace(y1, y2, 100)
        z_vals = np.linspace(z1, z2, 100)

        # Crear la figura y el eje 3D
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Graficar la línea
        ax.plot(x_vals, y_vals, z_vals, label='Línea 3D')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.title('Gráfica de una Línea en 3D')
        plt.legend()

        # Guardar la gráfica en un buffer
        buf = io.BytesIO()
        plt.savefig(buf, format='png')
        buf.seek(0)
        img_base64 = base64.b64encode(buf.getvalue()).decode('utf8')
        plt.close()

    except ValueError:
        img_base64 = None

    return render_template('result.html', img_base64=img_base64)

if __name__ == '__main__':
    app.run(debug=True)
