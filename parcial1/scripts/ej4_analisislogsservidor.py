'''
Ejercicio 4: Análisis de Logs de Servidor
Descripción:
Un archivo server_log.txt registra accesos con el formato:
timestamp; dirección_ip; recurso; código_respuesta; tiempo_respuesta  
Ejemplo:
2023-11-20 14:30:22; 192.168.1.5; /index.html; 200; 0.45  
2023-11-20 14:31:10; 192.168.1.7; /api/data; 404; 0.12  
Tareas a realizar:
1.	Contar solicitudes por código de respuesta (200, 404, 500, etc.).
2.	Identificar la dirección IP con más solicitudes.
3.	Calcular el tiempo promedio de respuesta.
4.	Filtrar registros con errores (códigos 4xx y 5xx).
5.	Exportar un reporte de tráfico por hora del día.
6.	Implementar un menú para seleccionar el análisis.
'''

def leer_logs(archivo):
    """Lee el archivo de logs y devuelve una lista de registros"""
    logs = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                partes = linea.strip().split('; ')
                logs.append({
                    'timestamp': partes[0],
                    'ip': partes[1],
                    'recurso': partes[2],
                    'codigo': int(partes[3]),
                    'tiempo': float(partes[4])
                })
    return logs

def contar_por_codigo(logs):
    """Cuenta solicitudes por código de respuesta"""
    conteo = {}
    for log in logs:
        codigo = log['codigo']
        conteo[codigo] = conteo.get(codigo, 0) + 1
    
    print("\nSolicitudes por código de respuesta:")
    for codigo, cantidad in sorted(conteo.items()):
        print(f"Código {codigo}: {cantidad} solicitudes")

def ip_mas_solicitudes(logs):
    """Identifica la IP con más solicitudes"""
    ips = {}
    for log in logs:
        ip = log['ip']
        ips[ip] = ips.get(ip, 0) + 1
    
    if not ips:
        print("\nNo hay registros de IPs")
        return
    
    ip_top = max(ips.items(), key=lambda x: x[1])
    print(f"\nIP con más solicitudes: {ip_top[0]} ({ip_top[1]} solicitudes)")

def tiempo_promedio_respuesta(logs):
    """Calcula el tiempo promedio de respuesta"""
    if not logs:
        print("\nNo hay registros para calcular el promedio")
        return
    
    total = sum(log['tiempo'] for log in logs)
    promedio = total / len(logs)
    print(f"\nTiempo promedio de respuesta: {promedio:.2f} segundos")

def filtrar_errores(logs):
    """Filtra registros con códigos de error (4xx y 5xx)"""
    errores = [log for log in logs if log['codigo'] >= 400]
    
    print("\nRegistros con errores (4xx y 5xx):")
    for error in errores[:10]:  # Mostrar solo los primeros 10 para no saturar
        print(f"{error['timestamp']} - {error['ip']} - {error['recurso']} - Código: {error['codigo']}")
    
    if len(errores) > 10:
        print(f"\n... y {len(errores) - 10} registros más")

def reporte_trafico_por_hora(logs):
    """Genera reporte de tráfico por hora del día"""
    horas = {}
    for log in logs:
        hora = log['timestamp'].split()[1][:2]  # Extraer solo la hora
        horas[hora] = horas.get(hora, 0) + 1
    
    print("\nTráfico por hora del día:")
    for hora, cantidad in sorted(horas.items()):
        print(f"Hora {hora}:00 - {cantidad} solicitudes")

def exportar_reporte_horas(logs, archivo_salida):
    """Exporta el reporte por horas a un archivo"""
    horas = {}
    for log in logs:
        hora = log['timestamp'].split()[1][:2]
        horas[hora] = horas.get(hora, 0) + 1
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("Hora;Solicitudes\n")
        for hora, cantidad in sorted(horas.items()):
            f.write(f"{hora}:00;{cantidad}\n")
    
    print(f"\nReporte exportado a {archivo_salida}")

def menu():
    """Menú interactivo para el análisis de logs"""
    logs = leer_logs('server_log.txt')
    
    while True:
        print("\n=== ANALIZADOR DE LOGS DEL SERVIDOR ===")
        print("1. Contar solicitudes por código de respuesta")
        print("2. Identificar IP con más solicitudes")
        print("3. Calcular tiempo promedio de respuesta")
        print("4. Filtrar registros con errores (4xx y 5xx)")
        print("5. Ver reporte de tráfico por hora")
        print("6. Exportar reporte por hora a archivo")
        print("7. Salir")
        
        opcion = input("Seleccione una opción (1-7): ")
        
        if opcion == '1':
            contar_por_codigo(logs)
        elif opcion == '2':
            ip_mas_solicitudes(logs)
        elif opcion == '3':
            tiempo_promedio_respuesta(logs)
        elif opcion == '4':
            filtrar_errores(logs)
        elif opcion == '5':
            reporte_trafico_por_hora(logs)
        elif opcion == '6':
            nombre_archivo = input("Ingrese nombre del archivo de salida (ej. reporte_horas.csv): ")
            exportar_reporte_horas(logs, nombre_archivo)
        elif opcion == '7':
            print("Saliendo del analizador...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu()