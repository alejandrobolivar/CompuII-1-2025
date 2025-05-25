def leer_archivo(nombre_archivo):
    """Lee el archivo y devuelve una lista de diccionarios con la información"""
    lst_datos = []
    with open(nombre_archivo, 'r', encoding='utf-8') as f:
        for linea in f:
            partes = linea.strip().split(';')
            if len(partes) >= 7:
                registro = {
                    'año': partes[0],
                    'departamento': partes[1],
                    'codigo': partes[2],
                    'asignatura': partes[3],
                    'seccion': partes[4],
                    'profesor': partes[5],
                    'horarios': procesar_horarios_str(' '.join(partes[6:]))
                }
                lst_datos.append(registro)
    return lst_datos

def procesar_horarios_str(horarios_str):
    """Procesa la cadena de horarios en una lista de diccionarios"""
    horarios = []
    partes = horarios_str.split()
    i = 0
    while i < len(partes):
        if len(partes[i]) >= 6:  # Verifica que sea un código de horario (ej: LU0800)
            dia = partes[i][:2]
            hora = partes[i][2:6]
            aula = partes[i+1] if i+1 < len(partes) else ''
            horarios.append({'dia': dia, 'hora': hora, 'aula': aula})
            i += 2
        else:
            i += 1
    return horarios

# 1. Profesores por departamento
def profesores_por_departamento(lst_datos):
    """Devuelve un diccionario con los profesores por departamento"""
    dept_profesores = {}
    for registro in lst_datos:
        dept = registro['departamento']
        profesor = registro['profesor']
        if dept not in dept_profesores:
            dept_profesores[dept] = []
        if profesor not in dept_profesores[dept]:  # Evita duplicados
            dept_profesores[dept].append(profesor)
    dic_ordenado = dict(sorted(dept_profesores.items(), key=lambda item: item[1]))
    return dic_ordenado

# 2. Horario más frecuente (día + hora)
def horario_mas_frecuente(lst_datos):
    """Determina el horario (día+hora+aula) más frecuente"""
    frecuencias = {}
    for registro in lst_datos:
        for horario in registro['horarios']:
            clave = (horario['dia'], horario['hora'])
            frecuencias[clave] = frecuencias.get(clave, 0) + 1
    if not frecuencias:
        return None
    max_clave = max(frecuencias, key=frecuencias.get)
    return (max_clave, frecuencias[max_clave])

# 3. Día más frecuente
def dia_mas_frecuente(lst_datos):
    """Determina el día de la semana más frecuente en los horarios"""
    frecuencias = {}
    for registro in lst_datos:
        for horario in registro['horarios']:
            dia = horario['dia']
            frecuencias[dia] = frecuencias.get(dia, 0) + 1
    if not frecuencias:
        return None
    max_dia = max(frecuencias, key=frecuencias.get)
    return (max_dia, frecuencias[max_dia])

# 4. Hora más frecuente
def hora_mas_frecuente(lst_datos):
    """Determina la hora más frecuente en los horarios"""
    frecuencias = {}
    for registro in lst_datos:
        for horario in registro['horarios']:
            hora = horario['hora']
            frecuencias[hora] = frecuencias.get(hora, 0) + 1
    if not frecuencias:
        return None
    max_hora = max(frecuencias, key=frecuencias.get)
    return (max_hora, frecuencias[max_hora])

# 5. Secciones por cátedra por departamento
def secciones_por_catedra(lst_datos):
    """Calcula la cantidad de secciones por cátedra por departamento"""
    dic_resultado = {}
    for registro in lst_datos:
        dept = registro['departamento']
        asignatura = registro['asignatura']
        if dept not in dic_resultado:
            dic_resultado[dept] = {}
        dic_resultado[dept][asignatura] = dic_resultado[dept].get(asignatura, 0) + 1
    return dic_resultado

# 6. Asignaturas de Estudios Básicos por semestre (con 'B' en tercer dígito del código)
def asignaturas_estudios_basicos_por_semestre(lst_datos):
    """Calcula la cantidad de asignaturas de Estudios Básicos por semestre"""
    dic_resultado = {}
    for registro in lst_datos:
        codigo = registro['codigo']
        # Verificar si el código tiene al menos 3 caracteres y el tercero es 'B'
        if len(codigo) >= 3 and codigo[3].upper() == 'B':
            semestre = registro["codigo"][2]
            dic_resultado[semestre] = dic_resultado.get(semestre, 0) + 1
    return dic_resultado

def mostrar_menu():
    """Muestra el menú de opciones"""
    print("\n" + "="*50)
    print("ANÁLISIS DE HORARIOS ACADÉMICOS".center(50))
    print("="*50)
    print("1. Profesores por departamento")
    print("2. Horario más frecuente (día+hora+aula)")
    print("3. Día más frecuente")
    print("4. Hora más frecuente")
    print("5. Secciones por cátedra por departamento")
    print("6. Asignaturas de Estudios Básicos por semestre")
    print("7. Salir")
    print("="*50)

def ejecutar_opcion(opcion, lst_datos):
    """Ejecuta la opción seleccionada"""
    if opcion == 1:
        print("\n" + "PROFESORES POR DEPARTAMENTO".center(50, "-"))
        profes_dept = profesores_por_departamento(lst_datos)
        for dept, profes in profes_dept.items():
            print(f"\nDepartamento: {dept}")
            print("Profesores:")
            for i, profesor in enumerate(profes, 1):
                print(f"  {i}. {profesor}")
            print(f"Total: {len(profes)} profesores")
    
    elif opcion == 2:
        print("\n" + "HORARIO MÁS FRECUENTE".center(50, "-"))
        horario_frec = horario_mas_frecuente(lst_datos)
        if horario_frec:
            print(f"Día: {horario_frec[0][0]}")
            print(f"Hora: {horario_frec[0][1]}")
            print(f"Ocurrencias: {horario_frec[1]}")
        else:
            print("No hay horarios registrados")
    
    elif opcion == 3:
        print("\n" + "DÍA MÁS FRECUENTE".center(50, "-"))
        dia_frec = dia_mas_frecuente(lst_datos)
        if dia_frec:
            print(f"Día: {dia_frec[0]}")
            print(f"Ocurrencias: {dia_frec[1]}")
        else:
            print("No hay días registrados")
    
    elif opcion == 4:
        print("\n" + "HORA MÁS FRECUENTE".center(50, "-"))
        hora_frec = hora_mas_frecuente(lst_datos)
        if hora_frec:
            print(f"Hora: {hora_frec[0]}")
            print(f"Ocurrencias: {hora_frec[1]}")
        else:
            print("No hay horas registradas")
    
    elif opcion == 5:
        print("\n" + "SECCIONES POR CÁTEDRA".center(50, "-"))
        secciones = secciones_por_catedra(lst_datos)
        for dept, catedras in secciones.items():
            print(f"\nDepartamento: {dept}")
            for catedra, cantidad in catedras.items():
                print(f"  - {catedra}: {cantidad} sección(es)")
    
    elif opcion == 6:
        print("\n" + "ASIGNATURAS DE ESTUDIOS BÁSICOS".center(50, "-"))
        asig_eb = asignaturas_estudios_basicos_por_semestre(lst_datos)
        if asig_eb:
            for semestre, cantidad in asig_eb.items():
                print(f"Semestre {semestre}: {cantidad} asignatura(s)")
        else:
            print("No se encontraron asignaturas de Estudios Básicos")
    
    elif opcion == 7:
        print("\nSaliendo del programa...")
        return True
    else:
        print("\nOpción no válida. Intente nuevamente.")
    
    input("\nPresione Enter para continuar...")
    return False

def main():
    lst_datos = leer_archivo("horarios.txt")
    
    while True:
        mostrar_menu()
        try:
            opcion = int(input("\nSeleccione una opción (1-7): "))
            salir = ejecutar_opcion(opcion, lst_datos)
            if salir:
                break
        except ValueError:
            print("\nError: Debe ingresar un número del 1 al 7")
            input("Presione Enter para continuar...")

if __name__ == "__main__":
    main()