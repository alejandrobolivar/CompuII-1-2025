'''
Ejercicio 3: Sistema de Registro Académico
Descripción:
Un archivo estudiantes.txt contiene datos estructurados así:
matrícula; nombre; carrera; semestre; promedio; materias_aprobadas  
Ejemplo:
E-2023001; María González; Ingeniería de Software; 5; 8.7; ProgAvanzada,BDatos,Redes  
E-2023002; Luis Fernández; Medicina; 3; 9.1; Anatomía,Bioquímica  
Funcionalidades a implementar:
1.	Listar estudiantes por carrera.
2.	Identificar el estudiante con el mejor promedio.
3.	Contar la cantidad de estudiantes por semestre.
4.	Mostrar materias aprobadas por un estudiante dado.
5.	Generar un ranking de carreras según el promedio general.
6.	Diseñar un menú para acceder a cada función.
'''

def leer_estudiantes(archivo):
    """Lee el archivo de estudiantes y devuelve una lista de diccionarios"""
    estudiantes = []
    with open(archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            if linea.strip():
                datos = linea.strip().split('; ')
                estudiantes.append({
                    'matricula': datos[0],
                    'nombre': datos[1],
                    'carrera': datos[2],
                    'semestre': int(datos[3]),
                    'promedio': float(datos[4]),
                    'materias_aprobadas': datos[5].split(',') if datos[5] else []
                })
    return estudiantes

def listar_por_carrera(estudiantes):
    """Lista estudiantes agrupados por carrera"""
    carreras = {}
    for est in estudiantes:
        if est['carrera'] not in carreras:
            carreras[est['carrera']] = []
        carreras[est['carrera']].append(est['nombre'])
    
    print("\nEstudiantes por carrera:")
    for carrera, nombres in carreras.items():
        print(f"\n{carrera}:")
        for nombre in nombres:
            print(f"  - {nombre}")

def mejor_promedio(estudiantes):
    """Identifica al estudiante con el mejor promedio"""
    if not estudiantes:
        print("\nNo hay estudiantes registrados")
        return
    
    mejor = max(estudiantes, key=lambda x: x['promedio'])
    print(f"\nEstudiante con mejor promedio: {mejor['nombre']} ({mejor['carrera']}) - Promedio: {mejor['promedio']}")

def contar_por_semestre(estudiantes):
    """Cuenta estudiantes por semestre"""
    semestres = {}
    for est in estudiantes:
        semestres[est['semestre']] = semestres.get(est['semestre'], 0) + 1
    
    print("\nCantidad de estudiantes por semestre:")
    for sem, cantidad in sorted(semestres.items()):
        print(f"Semestre {sem}: {cantidad} estudiantes")

def materias_estudiante(estudiantes, nombre_busqueda):
    """Muestra materias aprobadas de un estudiante"""
    encontrado = False
    print(f"\nBuscando materias de {nombre_busqueda}:")
    for est in estudiantes:
        if nombre_busqueda.lower() in est['nombre'].lower():
            print(f"{est['nombre']} ({est['carrera']}):")
            print("Materias aprobadas:", ', '.join(est['materias_aprobadas']))
            encontrado = True
    
    if not encontrado:
        print("No se encontró el estudiante")

def ranking_carreras(estudiantes):
    """Genera ranking de carreras por promedio general"""
    carreras = {}
    for est in estudiantes:
        if est['carrera'] not in carreras:
            carreras[est['carrera']] = {'suma': 0, 'cantidad': 0}
        carreras[est['carrera']]['suma'] += est['promedio']
        carreras[est['carrera']]['cantidad'] += 1
    
    # Calcular promedios
    ranking = []
    for carrera, datos in carreras.items():
        promedio = datos['suma'] / datos['cantidad']
        ranking.append((carrera, promedio))
    
    # Ordenar de mayor a menor promedio
    ranking.sort(key=lambda x: x[1], reverse=True)
    
    print("\nRanking de carreras por promedio:")
    for i, (carrera, prom) in enumerate(ranking, 1):
        print(f"{i}. {carrera}: {prom:.2f}")

def menu():
    """Muestra el menú interactivo"""
    estudiantes = leer_estudiantes('estudiantes.txt')
    
    while True:
        print("\n=== SISTEMA DE REGISTRO ACADÉMICO ===")
        print("1. Listar estudiantes por carrera")
        print("2. Identificar estudiante con mejor promedio")
        print("3. Contar estudiantes por semestre")
        print("4. Mostrar materias aprobadas de estudiante")
        print("5. Generar ranking de carreras por promedio")
        print("6. Salir")
        
        opcion = input("Seleccione una opción (1-6): ")
        
        if opcion == '1':
            listar_por_carrera(estudiantes)
        elif opcion == '2':
            mejor_promedio(estudiantes)
        elif opcion == '3':
            contar_por_semestre(estudiantes)
        elif opcion == '4':
            nombre = input("Ingrese nombre del estudiante: ")
            materias_estudiante(estudiantes, nombre)
        elif opcion == '5':
            ranking_carreras(estudiantes)
        elif opcion == '6':
            print("Saliendo del sistema...")
            break
        else:
            print("Opción no válida. Intente nuevamente.")
        
        input("\nPresione Enter para continuar...")

if __name__ == "__main__":
    menu()