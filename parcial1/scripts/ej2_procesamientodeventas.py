'''
Ejercicio 2: Procesamiento de Ventas
Descripción: Se tiene un archivo ventas.csv con el formato:
id_venta; fecha; cliente; producto; cantidad; precio_unitario; vendedor  
Ejemplo:
V-1001; 2023-11-20; Juan Pérez; Monitor 24"; 2; 150.00; Laura Gómez  
V-1002; 2023-11-21; Ana López; Teclado inalámbrico; 1; 45.99; Carlos Ruiz  
Requerimientos:
1.	Calcular el total de ventas por vendedor.
2.	Obtener el producto más vendido.
3.	Listar las ventas de un cliente específico.
4.	Determinar el día con mayor volumen de ventas.
5.	Exportar un resumen de ventas por mes en un nuevo archivo, considere el año y mes.
6.	Implementar un menú con las opciones anteriores.
'''

from datetime import datetime

def leer_ventas(archivo):
    """Lee el archivo de ventas y devuelve una lista de diccionarios"""
    ventas = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():  # Ignorar líneas vacías
                datos = [dato.strip() for dato in linea.split(';')]
                ventas.append({
                    'id_venta': datos[0],
                    'fecha': datos[1],
                    'cliente': datos[2],
                    'producto': datos[3],
                    'cantidad': int(datos[4]),
                    'precio_unitario': float(datos[5]),
                    'vendedor': datos[6]
                })
    return ventas

def total_ventas_por_vendedor(ventas):
    """Calcula el total de ventas (cantidad * precio) por cada vendedor"""
    ventas_vendedor: dict[str, float] = {}
    for venta in ventas:
        vendedor = venta['vendedor']
        total_venta = venta['cantidad'] * venta['precio_unitario']
        if vendedor in ventas_vendedor:
            ventas_vendedor[vendedor] += total_venta
        else:
            ventas_vendedor[vendedor] = total_venta
    
    print("\nTotal de ventas por vendedor:")
    for vendedor, total in sorted(ventas_vendedor.items(), key=lambda x: x[1], reverse=True):
        print(f"- {vendedor}: ${total:,.2f}")

def producto_mas_vendido(ventas):
    """Determina el producto con mayor cantidad total vendida"""
    productos : dict[str, int] = {} 
    for venta in ventas:
        producto = venta['producto']
        cantidad = venta['cantidad']
        if producto in productos:
            productos[producto] += cantidad
        else:
            productos[producto] = cantidad
    
    producto_top = max(productos.items(), key=lambda x: x[1])
    print(f"\nProducto más vendido: {producto_top[0]} (Cantidad total: {producto_top[1]})")

def ventas_por_cliente(ventas, nombre_cliente):
    """Lista todas las ventas de un cliente específico"""
    ventas_cliente = []
    for venta in ventas:
        if venta['cliente'].lower() == nombre_cliente.lower():
            ventas_cliente.append(venta)
    
    if not ventas_cliente:
        print(f"\nNo se encontraron ventas para el cliente: {nombre_cliente}")
        return
    
    print(f"\nVentas del cliente {nombre_cliente}:")
    for venta in ventas_cliente:
        total = venta['cantidad'] * venta['precio_unitario']
        print(f"- {venta['fecha']}: {venta['producto']} ({venta['cantidad']} x ${venta['precio_unitario']:.2f}) = ${total:.2f}")

def dia_mayor_volumen(ventas):
    """Determina el día con mayor volumen de ventas (en cantidad de productos)"""
    dias = {}
    for venta in ventas:
        fecha = datetime.strptime(venta['fecha'], '%Y-%m-%d').date()
        if fecha in dias:
            dias[fecha] += venta['cantidad']
        else:
            dias[fecha] = venta['cantidad']
    
    dia_top = max(dias.items(), key=lambda x: x[1])
    print(f"\nDía con mayor volumen de ventas: {dia_top[0]} (Cantidad vendida: {dia_top[1]})")

def exportar_resumen_mensual(ventas, archivo_salida):
    """Exporta un resumen de ventas por mes a un archivo"""
    meses = {}
    for venta in ventas:
        fecha = datetime.strptime(venta['fecha'], '%Y-%m-%d')
        mes_key = f"{fecha.year}-{fecha.month:02d}"
        total_venta = venta['cantidad'] * venta['precio_unitario']
        if mes_key in meses:
            meses[mes_key] += total_venta
        else:
            meses[mes_key] = total_venta
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("Mes;Total de Ventas\n")
        for mes in sorted(meses.keys()):
            f.write(f"{mes};{meses[mes]:.2f}\n")
    
    print(f"\nResumen mensual exportado a: {archivo_salida}")

def menu():
    """Muestra el menú interactivo"""
    ventas = leer_ventas('ventas.csv')
    
    while True:
        print("\n=== MENÚ PROCESAMIENTO DE VENTAS ===")
        print("1. Total de ventas por vendedor")
        print("2. Producto más vendido")
        print("3. Ventas de un cliente específico")
        print("4. Día con mayor volumen de ventas")
        print("5. Exportar resumen mensual de ventas")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == '1':
            total_ventas_por_vendedor(ventas)
        elif opcion == '2':
            producto_mas_vendido(ventas)
        elif opcion == '3':
            cliente = input("Ingrese el nombre del cliente: ")
            ventas_por_cliente(ventas, cliente)
        elif opcion == '4':
            dia_mayor_volumen(ventas)
        elif opcion == '5':
            archivo = input("Ingrese el nombre del archivo de salida (ej. resumen_mensual.csv): ")
            exportar_resumen_mensual(ventas, archivo)
        elif opcion == '6':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu()