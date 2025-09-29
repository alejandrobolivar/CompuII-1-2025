from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'invoice.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM products')
    products = cur.fetchall()
    total = sum([product['subtotal'] for product in products])
    return render_template('index.html', products=products, total=total)

@app.route('/add', methods=['GET', 'POST'])
def add_product():
    if request.method == 'POST':
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        precio_unitario = float(request.form['precio_unitario'])
        subtotal = cantidad * precio_unitario
        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO products (codigo, descripcion, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)', 
                    (codigo, descripcion, cantidad, precio_unitario, subtotal))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add_product.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_product(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        codigo = request.form['codigo']
        descripcion = request.form['descripcion']
        cantidad = int(request.form['cantidad'])
        precio_unitario = float(request.form['precio_unitario'])
        subtotal = cantidad * precio_unitario
        cur.execute('UPDATE products SET codigo = ?, descripcion = ?, cantidad = ?, precio_unitario = ?, subtotal = ? WHERE id = ?', 
                    (codigo, descripcion, cantidad, precio_unitario, subtotal, id))
        conn.commit()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cur.fetchone()
    return render_template('edit_product.html', product=product)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        cur.execute('DELETE FROM products WHERE id = ?', (id,))
        conn.commit()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM products WHERE id = ?', (id,))
    product = cur.fetchone()
    return render_template('delete_product.html', product=product)

if __name__ == '__main__':
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        codigo TEXT NOT NULL,
                        descripcion TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        precio_unitario REAL NOT NULL,
                        subtotal REAL NOT NULL)''')
    app.run(debug=True)
