from flask import Flask, render_template, request

app = Flask(__name__)
app.secret_key = 'clave_secreta_para_mensajes_flash'  # Agregado para mejor seguridad

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    
    # POST: Cuando el usuario envía el formulario
    if request.method == 'POST':
        try:
            # Obtener y validar datos del formulario
            peso = float(request.form['peso'])
            altura = float(request.form['altura'])
            
            # Validación adicional para evitar división por cero
            if altura <= 0:
                resultado = {'error': 'La altura debe ser mayor a cero'}
            elif peso <= 0:
                resultado = {'error': 'El peso debe ser mayor a cero'}
            else:
                # Fórmula del IMC: peso / (altura^2)
                imc = peso / (altura ** 2)
                
                # Clasificación según OMS
                if imc < 18.5:
                    clasificacion = "Bajo peso"
                    recomendacion = "Consulta a un nutricionista para ganar peso saludablemente"
                    color = "warning"
                elif imc < 25:
                    clasificacion = "Peso normal"
                    recomendacion = "¡Excelente! Mantén tus hábitos saludables"
                    color = "success"
                elif imc < 30:
                    clasificacion = "Sobrepeso"
                    recomendacion = "Considera aumentar tu actividad física y mejorar la alimentación"
                    color = "warning"
                else:
                    clasificacion = "Obesidad"
                    recomendacion = "Recomendamos consultar con un profesional de la salud"
                    color = "danger"
                
                resultado = {
                    'imc': imc,
                    'clasificacion': clasificacion,
                    'peso': peso,
                    'altura': altura,
                    'recomendacion': recomendacion,
                    'color': color
                }
            
        except ValueError:
            resultado = {'error': 'Por favor ingresa números válidos'}
        except KeyError:
            resultado = {'error': 'Faltan datos en el formulario'}
    
    # GET: Muestra el formulario vacío (también se ejecuta después del POST)
    return render_template('imc.html', resultado=resultado)

if __name__ == '__main__':
    app.run(port=5050)  