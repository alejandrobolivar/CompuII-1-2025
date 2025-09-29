# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 11:11:19 2024

@author: bolivar
"""

from flask import Flask, request, render_template_string

app = Flask(__name__)

# Ruta para la página principal con el formulario
@app.route('/')
def index():
    return render_template_string('''
        <form action="/guardar" method="post">
            <label>Temperatura:</label>
            <input type="text" name="temperatura">
            <button type="submit">Guardar</button>
        </form>
        <form action="/calcular" method="post">
            <button type="submit">Calcular</button>
        </form>
    ''')

# Ruta para guardar el valor de la temperatura en un archivo de texto
@app.route('/guardar', methods=['POST'])
def guardar_temperatura():
    temperatura = request.form['temperatura']
    with open('temperatura.txt', 'a') as file:
        file.write(temperatura + '\n')
    return 'Temperatura guardada exitosamente.'

# Ruta para realizar los cálculos y mostrar los resultados
@app.route('/calcular', methods=['POST'])
def calcular():
    with open('temperatura.txt', 'r') as file:
        temperaturas = [float(line.strip()) for line in file]

    promedio = sum(temperaturas) / len(temperaturas)
    porcentaje_mayor_promedio = sum(1 for t in temperaturas if t > promedio) / len(temperaturas) * 100
    max_temp = max(temperaturas)
    max_temp_pos = temperaturas.index(max_temp) + 1
    primera_mayor_promedio = next((t for t in temperaturas if t > promedio), None)
    primera_mayor_promedio_pos = temperaturas.index(primera_mayor_promedio) + 1 if primera_mayor_promedio else None

    resultados = f'''
        <p>Temperaturas: {temperaturas}</p>
        <p>Promedio: {promedio}</p>
        <p>Porcentaje de temperatura superior al promedio: {porcentaje_mayor_promedio}%</p>
        <p>Máxima temperatura: {max_temp} en posición {max_temp_pos}</p>
        <p>Primera temperatura mayor que el promedio: {primera_mayor_promedio} en posición {primera_mayor_promedio_pos}</p>
    '''
    return resultados

if __name__ == '__main__':
    app.run()
