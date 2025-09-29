# -*- coding: utf-8 -*-
"""
Created on Sat Oct 12 12:16:26 2024

@author: bolivar
"""

from flask import Flask, request, render_template_string
from prettytable import PrettyTable

app = Flask(__name__)

def guardar_temperatura(temperatura):
    with open('temperatura.txt', 'a') as file:
        file.write(temperatura + '\n')

def leer_temperaturas():
    with open('temperatura.txt', 'r') as file:
        return [float(line.strip()) for line in file]

def calcular_promedio(temperaturas):
    return sum(temperaturas) / len(temperaturas)

def calcular_porcentaje_mayor_promedio(temperaturas, promedio):
    return sum(1 for t in temperaturas if t > promedio) / len(temperaturas) * 100

def encontrar_max_temp(temperaturas):
    max_temp = max(temperaturas)
    max_temp_pos = temperaturas.index(max_temp) + 1
    return max_temp, max_temp_pos

def encontrar_primera_mayor_promedio(temperaturas, promedio):
    for i, t in enumerate(temperaturas):
        if t > promedio:
            return t, i + 1
    return None, None

def generar_tabla_temperaturas(temperaturas):
    tabla = PrettyTable()
    tabla.field_names = ["Posición", "Temperatura"]
    for i, temp in enumerate(temperaturas, start=1):
        tabla.add_row([i, temp])
    return tabla.get_html_string()

@app.route('/')
def index():
    return render_template_string('''
        <form action="/guardar" method="post">
            <label>Temperatura:</label>
            <input type="text" name="temperatura">
            <button type="submit">Guardar</button>
        </form>
        <form action="/menu" method="post">
            <button type="submit">Ir al Menú de Cálculos</button>
        </form>
    ''')

@app.route('/guardar', methods=['POST'])
def guardar():
    temperatura = request.form['temperatura']
    guardar_temperatura(temperatura)
    return 'Temperatura guardada exitosamente.'

@app.route('/menu', methods=['POST'])
def menu():
    return render_template_string('''
        <form action="/calcular_promedio" method="post">
            <button type="submit">Calcular Promedio</button>
        </form>
        <form action="/calcular_porcentaje_mayor_promedio" method="post">
            <button type="submit">Calcular Porcentaje Mayor al Promedio</button>
        </form>
        <form action="/calcular_max_temp" method="post">
            <button type="submit">Calcular Máxima Temperatura</button>
        </form>
        <form action="/calcular_primera_mayor_promedio" method="post">
            <button type="submit">Calcular Primera Mayor al Promedio</button>
        </form>
        <form action="/mostrar_temperaturas" method="post">
            <button type="submit">Mostrar Todas las Temperaturas</button>
        </form>
    ''')

@app.route('/calcular_promedio', methods=['POST'])
def calcular_promedio_ruta():
    temperaturas = leer_temperaturas()
    promedio = calcular_promedio(temperaturas)
    return f'<p>Promedio de temperaturas: {promedio}</p>'

@app.route('/calcular_porcentaje_mayor_promedio', methods=['POST'])
def calcular_porcentaje_mayor_promedio_ruta():
    temperaturas = leer_temperaturas()
    promedio = calcular_promedio(temperaturas)
    porcentaje_mayor_promedio = calcular_porcentaje_mayor_promedio(temperaturas, promedio)
    return f'<p>Porcentaje de temperatura superior al promedio: {porcentaje_mayor_promedio}%</p>'

@app.route('/calcular_max_temp', methods=['POST'])
def calcular_max_temp_ruta():
    temperaturas = leer_temperaturas()
    max_temp, max_temp_pos = encontrar_max_temp(temperaturas)
    return f'<p>Máxima temperatura: {max_temp} en posición {max_temp_pos}</p>'

@app.route('/calcular_primera_mayor_promedio', methods=['POST'])
def calcular_primera_mayor_promedio_ruta():
    temperaturas = leer_temperaturas()
    promedio = calcular_promedio(temperaturas)
    primera_mayor_promedio, primera_mayor_promedio_pos = encontrar_primera_mayor_promedio(temperaturas, promedio)
    return f'<p>Primera temperatura mayor que el promedio: {primera_mayor_promedio} en posición {primera_mayor_promedio_pos}</p>'

@app.route('/mostrar_temperaturas', methods=['POST'])
def mostrar_temperaturas():
    temperaturas = leer_temperaturas()
    tabla_temperaturas = generar_tabla_temperaturas(temperaturas)
    return f'<p>{tabla_temperaturas}</p>'

if __name__ == '__main__':
    app.run(debug=True)
