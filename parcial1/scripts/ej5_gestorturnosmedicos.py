'''
Ejercicio 5: Gestión de Turnos Médicos
Descripción:
Un archivo turnos.txt almacena datos en este formato:
id_turno; paciente; médico; especialidad; fecha; hora; duración  
Ejemplo:
T-001; Sofía Ramírez; Dr. Pérez; Cardiología; 2023-12-10; 09:00; 30  
T-002; Pedro Vargas; Dra. López; Pediatría; 2023-12-11; 10:30; 20  
Desarrollar funciones para:
1.	Listar turnos por especialidad.
2.	Calcular la cantidad de turnos por médico.
3.	Verificar disponibilidad en una fecha y hora específica.
4.	Mostrar el médico con más turnos asignados.
5.	Exportar un archivo con los turnos de la semana.
6.	Crear un menú para gestionar las opciones.
'''

def leer_turnos(archivo):
    """Lee el archivo de turnos y devuelve una lista de diccionarios"""
    turnos = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                datos = [dato.strip() for dato in linea.split(';')]
                turnos.append({
                    'id': datos[0],
                    'paciente': datos[1],
                    'medico': datos[2],
                    'especialidad': datos[3],
                    'fecha': datos[4],
                    'hora': datos[5],
                    'duracion': int(datos[6])
                })
    return turnos

def listar_por_especialidad(turnos):
    """Lista turnos agrupados por especialidad médica"""
    especialidades = {}
    for turno in turnos:
        esp = turno['especialidad']
        if esp not in especialidades:
            especialidades[esp] = []
        especialidades[esp].append(turno)
    
    print("\nTurnos por especialidad:")
    for esp, turnos_esp in especialidades.items():
        print(f"\n{esp}:")
        for t in turnos_esp:
            print(f"  - {t['fecha']} {t['hora']}: {t['paciente']} con {t['medico']}")

def turnos_por_medico(turnos):
    """Calcula cantidad de turnos asignados por médico"""
    medicos = {}
    for turno in turnos:
        med = turno['medico']
        medicos[med] = medicos.get(med, 0) + 1
    
    print("\nCantidad de turnos por médico:")
    for med, cantidad in sorted(medicos.items(), key=lambda x: x[1], reverse=True):
        print(f"- {med}: {cantidad} turnos")

def verificar_disponibilidad(turnos, fecha, hora):
    """Verifica si hay disponibilidad en una fecha y hora específica"""
    hora_parts = list(map(int, hora.split(':')))
    hora_min = hora_parts[0] * 60 + hora_parts[1]
    
    print(f"\nVerificando disponibilidad para {fecha} a las {hora}:")
    ocupado = False
    
    for turno in turnos:
        if turno['fecha'] == fecha:
            # Calcular rangos de tiempo
            t_hora_parts = list(map(int, turno['hora'].split(':')))
            # la siguiente instrucción utilizando listas por comprensión
            # t_hora_parts = [int(part) for part in turno['hora'].split(':')]
            # también se puede hacer por separado con map
            # horas, minutos = map(int, turno['hora'].split(':'))
            t_inicio = t_hora_parts[0] * 60 + t_hora_parts[1]
            t_fin = t_inicio + turno['duracion']
            
            # Verificar superposición
            if hora_min >= t_inicio and hora_min < t_fin:
                print(f"❌ Ocupado: {turno['medico']} atiende a {turno['paciente']} ({turno['hora']}-{t_fin//60:02d}:{t_fin%60:02d})")
                ocupado = True
    
    if not ocupado:
        print("✅ Horario disponible")

def medico_mas_turnos(turnos):
    """Identifica al médico con más turnos asignados"""
    if not turnos:
        print("\nNo hay turnos registrados")
        return
    
    conteo = {}
    for turno in turnos:
        med = turno['medico']
        conteo[med] = conteo.get(med, 0) + 1
    
    medico_top = max(conteo.items(), key=lambda x: x[1])
    print(f"\nMédico con más turnos: {medico_top[0]} ({medico_top[1]} turnos)")

def exportar_turnos_semana(turnos, archivo_salida):
    """Exporta los turnos de la semana actual a un archivo"""
    from datetime import datetime, timedelta
    
    hoy = datetime.now().date()
    semana = [hoy + timedelta(days=i) for i in range(7)]
    str_semana = [d.strftime("%Y-%m-%d") for d in semana]
    
    turnos_semana = [t for t in turnos if t['fecha'] in str_semana]
    
    with open(archivo_salida, 'w', encoding='utf-8') as f:
        f.write("Turnos de la semana:\n\n")
        for dia in str_semana:
            f.write(f"=== {dia} ===\n")
            turnos_dia = [t for t in turnos_semana if t['fecha'] == dia]
            for t in sorted(turnos_dia, key=lambda x: x['hora']):
                f.write(f"{t['hora']} - {t['medico']} ({t['especialidad']}): {t['paciente']}\n")
            f.write("\n")
    
    print(f"\nTurnos de la semana exportados a {archivo_salida}")

def menu():
    """Menú interactivo para gestión de turnos"""
    turnos = leer_turnos('turnos.txt')
    
    while True:
        print("\n=== GESTIÓN DE TURNOS MÉDICOS ===")
        print("1. Listar turnos por especialidad")
        print("2. Mostrar cantidad de turnos por médico")
        print("3. Verificar disponibilidad")
        print("4. Mostrar médico con más turnos")
        print("5. Exportar turnos de la semana")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == '1':
            listar_por_especialidad(turnos)
        elif opcion == '2':
            turnos_por_medico(turnos)
        elif opcion == '3':
            fecha = input("Ingrese fecha (AAAA-MM-DD): ")
            hora = input("Ingrese hora (HH:MM): ")
            verificar_disponibilidad(turnos, fecha, hora)
        elif opcion == '4':
            medico_mas_turnos(turnos)
        elif opcion == '5':
            nombre_archivo = input("Ingrese nombre del archivo de salida: ")
            exportar_turnos_semana(turnos, nombre_archivo)
        elif opcion == '6':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu()