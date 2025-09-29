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
    cur.execute('SELECT * FROM invoices')
    invoices = cur.fetchall()
    return render_template('index.html', invoices=invoices)

@app.route('/add', methods=['GET', 'POST'])
def add_invoice():
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        numero_factura = request.form['numero_factura']
        productos = request.form.getlist('producto')
        cantidades = request.form.getlist('cantidad')
        precios_unitarios = request.form.getlist('precio_unitario')
        subtotales = [int(cantidades[i]) * float(precios_unitarios[i]) for i in range(len(productos))]
        total = sum(subtotales)

        conn = get_db()
        cur = conn.cursor()
        cur.execute('INSERT INTO invoices (nombre, apellido, fecha, numero_factura, total) VALUES (?, ?, ?, ?, ?)', 
                    (nombre, apellido, fecha, numero_factura, total))
        invoice_id = cur.lastrowid

        for i in range(len(productos)):
            cur.execute('INSERT INTO products (invoice_id, producto, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)', 
                        (invoice_id, productos[i], cantidades[i], precios_unitarios[i], subtotales[i]))
        conn.commit()
        return redirect(url_for('index'))
    return render_template('add_invoice.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_invoice(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        nombre = request.form['nombre']
        apellido = request.form['apellido']
        fecha = request.form['fecha']
        numero_factura = request.form['numero_factura']
        productos = request.form.getlist('producto')
        cantidades = request.form.getlist('cantidad')
        precios_unitarios = request.form.getlist('precio_unitario')
        subtotales = [int(cantidades[i]) * float(precios_unitarios[i]) for i in range(len(productos))]
        total = sum(subtotales)

        cur.execute('UPDATE invoices SET nombre = ?, apellido = ?, fecha = ?, numero_factura = ?, total = ? WHERE id = ?', 
                    (nombre, apellido, fecha, numero_factura, total, id))
        cur.execute('DELETE FROM products WHERE invoice_id = ?', (id,))
        for i in range(len(productos)):
            cur.execute('INSERT INTO products (invoice_id, producto, cantidad, precio_unitario, subtotal) VALUES (?, ?, ?, ?, ?)', 
                        (id, productos[i], cantidades[i], precios_unitarios[i], subtotales[i]))
        conn.commit()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM invoices WHERE id = ?', (id,))
    invoice = cur.fetchone()
    cur.execute('SELECT * FROM products WHERE invoice_id = ?', (id,))
    products = cur.fetchall()
    return render_template('edit_invoice.html', invoice=invoice, products=products)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_invoice(id):
    conn = get_db()
    cur = conn.cursor()
    if request.method == 'POST':
        cur.execute('DELETE FROM invoices WHERE id = ?', (id,))
        cur.execute('DELETE FROM products WHERE invoice_id = ?', (id,))
        conn.commit()
        return redirect(url_for('index'))
    cur.execute('SELECT * FROM invoices WHERE id = ?', (id,))
    invoice = cur.fetchone()
    return render_template('delete_invoice.html', invoice=invoice)

@app.route('/delete_product/<int:id>', methods=['POST'])
def delete_product(id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM products WHERE id = ?', (id,))
    conn.commit()
    return redirect(request.referrer)

if __name__ == '__main__':
    with get_db() as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS invoices (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        nombre TEXT NOT NULL,
                        apellido TEXT NOT NULL,
                        fecha TEXT NOT NULL,
                        numero_factura TEXT NOT NULL,
                        total REAL NOT NULL)''')
        conn.execute('''CREATE TABLE IF NOT EXISTS products (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        invoice_id INTEGER NOT NULL,
                        producto TEXT NOT NULL,
                        cantidad INTEGER NOT NULL,
                        precio_unitario REAL NOT NULL,
                        subtotal REAL NOT NULL,
                        FOREIGN KEY (invoice_id) REFERENCES invoices (id))''')
    app.run(debug=True)
