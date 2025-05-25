def procesar_estudiantes_matricula_clave():
    # Diccionario principal con carrera como clave externa
    # y diccionario interno con matrícula como clave
    estudiantes_por_carrera = {}
    
    try:
        with open('estudiantes.txt', 'r', encoding='utf-8') as archivo:
            for linea in archivo:
                datos = linea.strip().split(';')
                
                if len(datos) >= 6:
                    matricula = datos[0].strip()
                    nombre = datos[1].strip()
                    carrera = datos[2].strip()
                    semestre = datos[3].strip()
                    promedio = datos[4].strip()
                    materias = [m.strip() for m in datos[5].split(',')]
                    
                    # Crear diccionario con los datos del estudiante
                    datos_estudiante = [
                        nombre,
                        semestre,
                        promedio,
                        materias
                    ]
                    
                    # Organizar por carrera y matrícula
                    if carrera not in estudiantes_por_carrera:
                        estudiantes_por_carrera[carrera] = {}
                        
                    # Sí se repite la carrera y matricula, se sobreescribe.                    
                    estudiantes_por_carrera[carrera][matricula] = datos_estudiante
    
    except FileNotFoundError:
        print("Error: El archivo 'estudiantes.txt' no fue encontrado.")
    except Exception as e:
        print(f"Error al procesar el archivo: {e}")
    
    return estudiantes_por_carrera

# Ejecutar y mostrar resultados
if __name__ == "__main__":
    diccionario_estudiantes = procesar_estudiantes_matricula_clave()
    
    print("=== Estudiantes organizados por carrera y matrícula ===")
    for carrera, estudiantes in diccionario_estudiantes.items():
        print(f"\nCarrera: {carrera}")
        for matricula, datos in estudiantes.items():
            print(f"\n  Matrícula: {matricula}")
            print(f"  Nombre: {datos[0]}")
            print(f"  Semestre: {datos[1]}")
            print(f"  Promedio: {datos[2]}")
            print(f"  Materias: {', '.join(datos[3])}")