from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def mostrar_notas():
    # Leer el archivo de texto
    with open('notas.txt', 'r') as file:
        lineas = file.readlines()

    # Procesar las líneas del archivo
    estudiantes = []
    for linea in lineas:
        nombre, nota1, nota2, nota3 = linea.strip().split(',')
        estudiantes.append({
            'nombre': nombre,
            'nota1': nota1,
            'nota2': nota2,
            'nota3': nota3
        })

    # Crear una plantilla HTML simple para mostrar los datos
    plantilla = '''
    <!doctype html>
    <html lang="es">
      <head>
        <meta charset="utf-8">
        <title>Notas de Estudiantes</title>
      </head>
      <body>
        <h1>Notas de Estudiantes</h1>
        <table border="1">
          <tr>
            <th>Nombre</th>
            <th>Nota 1</th>
            <th>Nota 2</th>
            <th>Nota 3</th>
          </tr>
          {% for estudiante in estudiantes %}
          <tr>
            <td>{{ estudiante.nombre }}</td>
            <td>{{ estudiante.nota1 }}</td>
            <td>{{ estudiante.nota2 }}</td>
            <td>{{ estudiante.nota3 }}</td>
          </tr>
          {% endfor %}
        </table>
      </body>
    </html>
    '''

    return render_template_string(plantilla, estudiantes=estudiantes)

if __name__ == '__main__':
    app.run()
