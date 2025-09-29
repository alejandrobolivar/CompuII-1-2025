from flask import Flask, render_template_string

app = Flask(__name__)

def leer_notas():
    estudiantes = []
    with open('notas.txt', 'r') as archivo:
        for linea in archivo:
            nombre, nota1, nota2, nota3 = linea.strip().split(',')
            nota1, nota2, nota3 = float(nota1), float(nota2), float(nota3)
            promedio = calcular_promedio(nota1, nota2, nota3)
            estudiantes.append({
                'nombre': nombre,
                'nota1': nota1,
                'nota2': nota2,
                'nota3': nota3,
                'promedio': promedio
            })
    return estudiantes

def calcular_promedio(nota1, nota2, nota3):
    return (nota1 + nota2 + nota3) / 3

def estudiante_con_mayor_promedio(estudiantes):
    return max(estudiantes, key=lambda x: x['promedio'])

@app.route('/')
def mostrar_notas():
    estudiantes = leer_notas()
    mejor_estudiante = estudiante_con_mayor_promedio(estudiantes)
    return render_template_string('''
    <h1>Lista de Estudiantes</h1>
    <table border="1">
        <tr>
            <th>Nombre</th>
            <th>Nota 1</th>
            <th>Nota 2</th>
            <th>Nota 3</th>
            <th>Promedio</th>
        </tr>
        {% for estudiante in estudiantes %}
        <tr>
            <td>{{ estudiante.nombre }}</td>
            <td>{{ estudiante.nota1 }}</td>
            <td>{{ estudiante.nota2 }}</td>
            <td>{{ estudiante.nota3 }}</td>
            <td>{{ estudiante.promedio }}</td>
        </tr>
        {% endfor %}
    </table>
    <h2>Estudiante con el mayor promedio</h2>
    <p>{{ mejor_estudiante.nombre }} con un promedio de {{ mejor_estudiante.promedio }}</p>
    ''', estudiantes=estudiantes, mejor_estudiante=mejor_estudiante)

if __name__ == '__main__':
    app.run()
