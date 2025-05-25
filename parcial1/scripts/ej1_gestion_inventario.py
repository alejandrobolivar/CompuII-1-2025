'''
Ejercicio 1: Gestión de Inventario
Descripción: Dado un archivo de texto inventario.txt con la siguiente estructura:
código; categoría; producto; stock; precio; proveedor; fecha_ingreso  
Ejemplo:
INV-001; Electrónica; Laptop HP; 15; 1200.50; TechSupplies; 2023-10-05  
INV-002; Oficina; Silla ergonómica; 30; 199.99; OfficePro; 2023-09-15  
Desarrollar un script en Python que:
1.	Liste los productos por categoría.
2.	Determine el producto con mayor stock.
3.	Calcule el valor total del inventario (stock × precio).
4.	Identifique al proveedor con más productos en inventario.
5.	Genere un informe de productos con stock menor a un umbral dado.
6.	Implemente un menú interactivo para acceder a cada función.
'''

def leer_inventario(archivo):
    """Lee el archivo de inventario y devuelve una lista de diccionarios"""
    inventario = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():  # Ignorar líneas vacías
                codigo, categoria, producto, stock, precio, proveedor, fecha = linea.strip().split('; ')
                inventario.append({
                    'codigo': codigo,
                    'categoria': categoria,
                    'producto': producto,
                    'stock': int(stock),
                    'precio': float(precio),
                    'proveedor': proveedor,
                    'fecha_ingreso': fecha
                })
    return inventario

def productos_por_categoria(inventario):
    """Lista los productos agrupados por categoría"""
    categorias = {}
    for item in inventario:
        if item['categoria'] not in categorias:
            categorias[item['categoria']] = []
        categorias[item['categoria']].append(item['producto'])
    
    print("\nProductos por categoría:")
    for categoria, productos in categorias.items():
        print(f"\n{categoria}:")
        for producto in productos:
            print(f"  - {producto}")

def producto_mayor_stock(inventario):
    """Determina el producto con mayor stock"""
    max_stock = max(inventario, key=lambda x: x['stock'])
    print(f"\nProducto con mayor stock: {max_stock['producto']} (Stock: {max_stock['stock']})")

def valor_total_inventario(inventario):
    """Calcula el valor total del inventario"""
    total = sum(item['stock'] * item['precio'] for item in inventario)
    print(f"\nValor total del inventario: ${total:,.2f}")

def proveedor_mas_productos(inventario):
    """Identifica al proveedor con más productos en inventario"""
    proveedores = {}
    for item in inventario:
        if item['proveedor'] not in proveedores:
            proveedores[item['proveedor']] = 0
        proveedores[item['proveedor']] += 1
    
    proveedor_top = max(proveedores.items(), key=lambda x: x[1])
    print(f"\nProveedor con más productos: {proveedor_top[0]} ({proveedor_top[1]} productos)")

def productos_stock_bajo(inventario, umbral):
    """Genera un informe de productos con stock menor al umbral dado"""
    bajos = [item for item in inventario if item['stock'] < umbral]
    
    print(f"\nProductos con stock bajo (menos de {umbral} unidades):")
    for item in bajos:
        print(f"  - {item['producto']} (Stock: {item['stock']}, Categoría: {item['categoria']})")

def menu():
    """Muestra el menú interactivo"""
    inventario = leer_inventario('inventario.txt')
    
    while True:
        print("\n=== MENÚ GESTIÓN DE INVENTARIO ===")
        print("1. Listar productos por categoría")
        print("2. Mostrar producto con mayor stock")
        print("3. Calcular valor total del inventario")
        print("4. Identificar proveedor con más productos")
        print("5. Generar informe de stock bajo")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == '1':
            productos_por_categoria(inventario)
        elif opcion == '2':
            producto_mayor_stock(inventario)
        elif opcion == '3':
            valor_total_inventario(inventario)
        elif opcion == '4':
            proveedor_mas_productos(inventario)
        elif opcion == '5':
            umbral = int(input("Ingrese el umbral de stock mínimo: "))
            productos_stock_bajo(inventario, umbral)
        elif opcion == '6':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu()