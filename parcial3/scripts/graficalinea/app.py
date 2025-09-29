from flask import Flask, render_template, request
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
        x1 = float(request.form['x1'])
        y1 = float(request.form['y1'])
        x2 = float(request.form['x2'])
        y2 = float(request.form['y2'])

        # Calcular la pendiente (m) y la intersección (b) de la recta
        m = (y2 - y1) / (x2 - x1)
        b = y1 - m * x1
        equation = f"y = {m:.2f}x + {b:.2f}"

        fig, ax = plt.subplots()
        ax.plot([x1, x2], [y1, y2], marker='o')
        ax.text(x1, y1, f'({x1}, {y1})', fontsize=8, ha='right')
        ax.text(x2, y2, f'({x2}, {y2})', fontsize=8, ha='right')
        ax.text((x1 + x2) / 2, (y1 + y2) / 2, equation, fontsize=8, ha='center')
        ax.grid(True)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Línea entre dos puntos')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        plt.close(fig)  # Cerrar la figura para liberar memoria

        return render_template('index.html', plot_url=plot_url)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/clear')
def clear():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()




"""
from flask import Flask, render_template, request
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
        x1 = float(request.form['x1'])
        y1 = float(request.form['y1'])
        x2 = float(request.form['x2'])
        y2 = float(request.form['y2'])

        fig, ax = plt.subplots()
        ax.plot([x1, x2], [y1, y2], marker='o')
        ax.grid(True)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Línea entre dos puntos')

        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        plt.close(fig)  # Cerrar la figura para liberar memoria

        return render_template('index.html', plot_url=plot_url)
    except Exception as e:
        return render_template('index.html', error=str(e))

@app.route('/clear')
def clear():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
"""