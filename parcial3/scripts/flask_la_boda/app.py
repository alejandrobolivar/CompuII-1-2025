from flask import Flask, render_template, request
import os

app = Flask(__name__)

def leer_lista(filename):
    invitados = {}
    with open(filename, 'r') as file:
        for line in file:
            nombre, acompañantes = line.strip().split(',')
            nombre = nombre.strip()
            acompañantes = int(acompañantes.strip())
            if nombre in invitados:
                invitados[nombre] = min(invitados[nombre], acompañantes)
            else:
                invitados[nombre] = acompañantes
    return invitados

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/procesar', methods=['POST'])
def procesar():
    novio_file = request.files['novio']
    novia_file = request.files['novia']

    novio_path = os.path.join('uploads', novio_file.filename)
    novia_path = os.path.join('uploads', novia_file.filename)

    novio_file.save(novio_path)
    novia_file.save(novia_path)

    invitados_novio = leer_lista(novio_path)
    invitados_novia = leer_lista(novia_path)

    invitados = {**invitados_novio, **invitados_novia}
    for nombre in invitados_novio:
        if nombre in invitados_novia:
            invitados[nombre] = min(invitados_novio[nombre], invitados_novia[nombre])

    total_asistentes = sum(invitados.values()) + len(invitados)
    exclusivos_novio = len([nombre for nombre in invitados_novio if nombre not in invitados_novia])
    porcentaje_exclusivos_novio = (exclusivos_novio / len(invitados)) * 100

    with open('Invitaciones.Txt', 'w') as file:
        for nombre, acompañantes in invitados.items():
            file.write(f'{nombre} {acompañantes}\n')

    return render_template('resultado.html', total_asistentes=total_asistentes, porcentaje_exclusivos_novio=porcentaje_exclusivos_novio)

if __name__ == '__main__':
    app.run(debug=True)
