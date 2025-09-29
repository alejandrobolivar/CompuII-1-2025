# -*- coding: utf-8 -*-
"""
Created on Tue Jul 16 22:43:24 2024

@author: bolivar
"""

from flask import Flask, request

'''
request Contiene información como: Datos de formularios, Archivos subidos,
Método HTTP (GET, POST), Cabeceras de la solicitud, Parámetros de URL, Cookies
'''

# Creas una aplicación Flask
app = Flask(__name__)

# Define una ruta
@app.route('/', methods=['GET', 'POST']) # Acepta ambos métodos
def sumar():
    # Cuando el usuario llena el formulario y hace clic en "Sumar":
    # request.method = 'POST'
    if request.method == 'POST':
        num1 = int(request.form['num1'])
        num2 = int(request.form['num2'])
        resultado = num1 + num2
        return f'El resultado es: {resultado}'
    else:  # Cuando el usuario visita http://localhost:5000/ por primera vez: se ejecuta primero GET
        return '''
    <form method="post">
    <label>Ingrese el primer número:</label>
    <input type="text" name="num1"><br>
    <label>Ingrese el segundo número:</label>
    <input type="text" name="num2"><br>
    <input type="submit" value="Sumar">
    </form>
    '''

if __name__ == '__main__':
    app.run(port=5050)