from flask import Flask, request, render_template, send_file
import numpy as np
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/integrate', methods=['POST'])
def integrate():
    try:
        # Obtener los límites de integración y la función
        a = float(request.form['a'])
        b = float(request.form['b'])
        func_str = request.form['func']
        
        # Definir la función a integrar
        def func(x):
            return eval(func_str)
        
        # Calcular la integral definida
        x = np.linspace(a, b, 1000)
        y = func(x)
        result = np.trapz(y, x)
        
        # Generar el gráfico
        fig, ax = plt.subplots()
        ax.plot(x, y, label=f'y = {func_str}')
        ax.fill_between(x, y, where=[(a <= xi <= b) for xi in x], color='skyblue', alpha=0.4)
        ax.axhline(0, color='black',linewidth=0.5)
        ax.axvline(0, color='black',linewidth=0.5)
        ax.grid(color = 'gray', linestyle = '--', linewidth = 0.5)
        ax.legend()
        plt.title(f'Integral de {func_str} desde {a} hasta {b}')
        
        # Guardar el gráfico en un objeto BytesIO
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode('utf8')
        
        return render_template('result.html', result=result, plot_url=plot_url)
    except Exception as e:
        return f"Error: {e}"

if __name__ == '__main__':
    app.run(debug=True)
