# -*- coding: utf-8 -*-
"""
Calculadora Simple - Aplicación Flask para aprender GET y POST
Versión mejorada manteniendo la simplicidad original
"""

from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def sumar():
    """
    Ejemplo claro de diferencia entre GET (mostrar formulario)
    y POST (procesar datos del formulario)
    """
    
    resultado = None
    num1_val = ''
    num2_val = ''
    
    # PROCESAR FORMULARIO (POST)
    if request.method == 'POST':
        try:
            num1 = int(request.form['num1'])
            num2 = int(request.form['num2'])
            resultado = num1 + num2
            
            # Guardar valores para repoblar el formulario
            num1_val = str(num1)
            num2_val = str(num2)
            
        except ValueError:
            resultado = 'Error: Por favor ingresa números válidos'
        except KeyError:
            resultado = 'Error: Faltan números en el formulario'
    
    # MOSTRAR INTERFAZ (GET o POST con resultado)
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Calculadora Simple</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                max-width: 500px;
                margin: 50px auto;
                padding: 20px;
                line-height: 1.6;
            }}
            
            .container {{
                border: 1px solid #ddd;
                border-radius: 8px;
                padding: 30px;
                background: #f9f9f9;
            }}
            
            h1 {{
                color: #333;
                text-align: center;
                margin-bottom: 30px;
            }}
            
            .form-group {{
                margin-bottom: 20px;
            }}
            
            label {{
                display: block;
                margin-bottom: 5px;
                font-weight: bold;
                color: #555;
            }}
            
            input[type="number"] {{
                width: 100%;
                padding: 10px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-size: 16px;
            }}
            
            input[type="submit"] {{
                background: #4CAF50;
                color: white;
                padding: 12px 24px;
                border: none;
                border-radius: 4px;
                cursor: pointer;
                font-size: 16px;
                width: 100%;
            }}
            
            input[type="submit"]:hover {{
                background: #45a049;
            }}
            
            .resultado {{
                margin-top: 20px;
                padding: 15px;
                border-radius: 4px;
                text-align: center;
                font-size: 18px;
                font-weight: bold;
            }}
            
            .exito {{
                background: #d4edda;
                color: #155724;
                border: 1px solid #c3e6cb;
            }}
            
            .error {{
                background: #f8d7da;
                color: #721c24;
                border: 1px solid #f5c6cb;
            }}
            
            .info {{
                background: #d1ecf1;
                color: #0c5460;
                padding: 15px;
                border-radius: 4px;
                margin-top: 20px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🧮 Calculadora Simple</h1>
            
            <form method="POST">
                <div class="form-group">
                    <label for="num1">Primer número:</label>
                    <input type="number" id="num1" name="num1" value="{num1_val}" 
                           placeholder="Ingresa un número" required>
                </div>
                
                <div class="form-group">
                    <label for="num2">Segundo número:</label>
                    <input type="number" id="num2" name="num2" value="{num2_val}" 
                           placeholder="Ingresa otro número" required>
                </div>
                
                <input type="submit" value="Sumar Números">
            </form>
            
            {f'<div class="resultado {"exito" if "Error" not in str(resultado) else "error"}">{resultado}</div>' if resultado else ''}
            
            <div class="info">
                <strong>💡 ¿Cómo funciona?</strong><br>
                • <strong>1:</strong> Ingresa dos números<br>
                • <strong>2:</strong> Pulsa el botón Sumar Números
            </div>
        </div>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(port=5100)