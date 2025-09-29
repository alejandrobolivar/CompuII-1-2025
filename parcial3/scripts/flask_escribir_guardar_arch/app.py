from flask import Flask, request, render_template_string

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nombre = request.form['nombre']
        nota1 = request.form['nota1']
        nota2 = request.form['nota2']
        nota3 = request.form['nota3']
        
        with open('notas.txt', 'a', encoding="utf-8") as archivo:
            archivo.write(f'{nombre},{nota1},{nota2},{nota3}\n')
        
        mensaje = "Datos guardados exitosamente"
    else:
        mensaje = ""
    
    return render_template_string('''
    <h1>Ingresar Notas del Estudiante</h1>
    <form method="post">
        Nombre: <input type="text" name="nombre"><br>
        Nota 1: <input type="text" name="nota1"><br>
        Nota 2: <input type="text" name="nota2"><br>
        Nota 3: <input type="text" name="nota3"><br>
        <input type="submit" value="Guardar">
    </form>
    <p>{{ mensaje }}</p>
    ''', mensaje=mensaje)

if __name__ == '__main__':
    app.run()
