# -*- coding: utf-8 -*-
"""
Created on Fri Jul 19 06:23:15 2024

@author: bolivar
"""

from flask import Flask, render_template, request
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        function = request.form['function']
        x = range(-10, 11)
        y = [eval(function) for x in x]

        plt.figure()
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel('y')
        plt.title(f'Gráfica de {function}')
        
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plot_url = base64.b64encode(img.getvalue()).decode()

        return render_template('index.html', plot_url=plot_url)

    return render_template('index.html')

if __name__ == '__main__':
    app.run()