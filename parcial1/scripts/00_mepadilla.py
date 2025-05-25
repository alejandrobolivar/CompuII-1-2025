# Ejercicio 0: Gestión de horarios.
#Descripción:
#Dado un archivo de texto “horarios.txt” con la siguiente información:
#año; departamento; código; asignatura; sección; profesor; LU0800 SD1 LU0850 SD1 MI0800 SD1 MI0850 SD1
#El horario tiene la misma estructura de la presentada en la página de control de estudios, la misma contiene el
#día, la hora y el aula. Utilice datos estructurados para la elaboración del script.
#Realice funciones para:
#1. Profesores por departamento.
#2. Determinar el horario más frecuente.
#3. El día más frecuente.
#4. La hora más frecuente.
#5. Cantidad de secciones por cátedra de cada departamento.
#6. Cantidad de asignaturas de Estudios Básicos por semestre, el tercer carácter del código representa el
#semestre y el cuarto indica que es de Estudia Básicos si es el carácter B.
#7. Aula más utilizada cada día.
#8. Menú de opciones.
#creo una lista para almacenar las lineas de txt
lst_txt_b=[]
with open("00_horarios_mepadilla.txt") as archivo:
    for linea in archivo:
        lst_txt_b.append(linea.strip().split(';'))
#print(lst_txt_b)
print('\n')
print("LISTA CON LINEAS CARGADAS DEL ARCHIVO DE TEXTO\n")
for elemento in lst_txt_b:
    print(elemento)
#1. Profesores por departamento.
# Si cada linea del txt representa una seccion, y cada seccion tiene un departamento, contar las veces que aparece un departamento podria darma la cantidad de profesores
#pero puedo tener un profesor con mas de una seccion, asi que solo eso no vasta, ademas puedo tener al mismo profesor dando otra seccion
#de otro departamento
#print(len(lst_txt_b))
#creo una nueva lista con departamentos y profesores
lst_dep_prof=[]
lst_dep_gen=[] #lista con todos los departamentos
for indice in range(len(lst_txt_b)):
    #print('Departamento: ' + lst_txt_b[indice][1] + ' Profesor: ' + lst_txt_b[indice][5])
    str_dep_a = lst_txt_b[indice][1] + '/' + lst_txt_b[indice][5]
    lst_dep_prof.append(str_dep_a)
    lst_dep_gen.append(lst_txt_b[indice][1])
#print(lst_dep_prof)
lst_dep=list(set(lst_dep_gen))
lst_dep_prof_no_dupli=list(set(lst_dep_prof))
#print('LISTA SIN DUPLICADOS DE DEPARTAMENTOS Y PROFESORES')
#for elemento in lst_dep_prof_no_dupli:
    #print(elemento)
#  Repetir de la lista sin duplicados de departamentos y profesores hago un truncado para quedar solo con los departamentos
lst_count_prof=[]
for elemento in range(len(lst_dep_prof_no_dupli)):
    cadena=str(lst_dep_prof_no_dupli[elemento])
    str_trunc=cadena.split('/')
    lst_count_prof.append(str_trunc[0])
#print('LISTA SIN DUPLICADOS DE DEPARTAMENTOS')
#for elemento in lst_dep:
#    print(elemento)
# AHORA CUENTO LA CANTIDAD DE VECES QUE EL DEPARTAMENT APARECE EN LA LISTA DE DEPARTAMENTOS Y PROFESOR Y OBTENGO EL NUMERO DE PROFESORES POR DEPARTAMENTO
#print('LISTA DE DEPARTAMENTOS POR PROFESOR PARA CONTEO DE PROFESORES')
#for elemento in lst_count_prof:
#    print(elemento)
#IMPRESION DE CANTIDAD DE PROFESORES POR DEPARTAMENTO
print('\n')
print('CANTIDAD DE PROFESORES POR DEPARTAMENTO\n')
for elemento in lst_dep:
    print('El departamento de ' + elemento + ' tiene ' + str(lst_count_prof.count(elemento)) + ' Profesores Asignados')
# FIN DE CALCULO DE PROFESORES POR DEPARTAMENTO
#2. Determinar el horario más frecuente.
lst_hor=[]
for indice in range(len(lst_txt_b)):
    lst_hor.append(lst_txt_b[indice][6])
print('\n')
print(lst_hor)
#3. El día más frecuente.
lst_str_trunc=[]
lst_count_day=[]
for elemento in range(len(lst_hor)):
    cadena=str(lst_hor[elemento])
    lst_str_trunc=cadena.split(' ')
    lst_count_day.append(lst_str_trunc[0])
    lst_count_day.append(lst_str_trunc[2])
    lst_count_day.append(lst_str_trunc[4])
print(lst_count_day)
lst_dia=[]
for elemento in range(len(lst_count_day)):
    lst_dia.append(lst_count_day[elemento][0:2])
print(lst_dia)
lst_dia_non_dupli=list(set(lst_dia))
print(lst_dia_non_dupli)
lst_frec_dia=[]
lst_frec_dia_cant=[]
for elemento in lst_dia_non_dupli:
    print('La frecuencia del dia ' + elemento + ' es: ' + str(lst_dia.count(elemento)))
    lst_frec_dia.append(lst_dia.count(elemento))
    lst_frec_dia_cant.append(str(lst_dia.count(elemento)) + '00' + str(elemento))
tpl_max_min_day=tuple(lst_frec_dia)
print(lst_frec_dia)
print(lst_frec_dia_cant)
print(tpl_max_min_day)
str_max_frec = str(max(lst_frec_dia_cant))
str_trunc_b=str_max_frec.split('00')
lst_day_b=[]
lst_day_b.append(str_trunc_b[1])
dic_day_a={'LU':'LUNES','MA':'MARTES','MI':'MIERCOLES','JU':'JUEVES','VI':'VIERNES'}
print(lst_day_b)
print()
print('EL DIA CON MAYOR FRECUENCIA ES: ' + dic_day_a[str_trunc_b[1]] + ' CON UN TOTAL DE ' + str_trunc_b[0] + ' ASIGNACIONES\n')
#4. La hora más frecuente.
print('CALCULO DE LA HORA MAS FRECUENTE\n')
lst_hor=[]
for elemento in range(len(lst_count_day)):
    lst_hor.append(lst_count_day[elemento][2:])
print(lst_hor)
lst_hor_non_dupli=list(set(lst_hor))
print(lst_hor_non_dupli)
lst_frec_hor=[]
lst_frec_hor_cant=[]
for elemento in lst_hor_non_dupli:
    print('La frecuencia de la hora ' + elemento + ' es: ' + str(lst_hor.count(elemento)))
    lst_frec_hor.append(lst_hor.count(elemento))
    lst_frec_hor_cant.append(str(lst_hor.count(elemento)) + 'xx' + str(elemento))
tpl_max_min_hor=tuple(lst_frec_hor)
print(lst_frec_hor)
print(lst_frec_hor_cant)
print(tpl_max_min_hor)
str_max_frec_b = str(max(lst_frec_hor_cant))
print(str_max_frec_b)
str_trunc_c=str_max_frec_b.split('xx')
print('LA HORA CON MAYOR FRECUENCIA ES: ' + str_trunc_c[1] + ' CON UN TOTAL DE : ' + str_trunc_c[0] + ' OCUPACIONES\n')
#5. Cantidad de secciones por cátedra de cada departamento.
lst_secc=[]
for indice in range(len(lst_txt_b)):
    lst_secc.append(lst_txt_b[indice][3])
print('\n')
print(lst_secc)
lst_secc_non_dupli=list(set(lst_secc))
print(lst_secc_non_dupli)
print('CANTIDAD DE SECCIONES POR CATEDRA\n')
for elemento in lst_secc_non_dupli:
    print('La catedra ' + elemento + ' tiene: ' + str(lst_secc.count(elemento)) + ' secciones activas')
#6. Cantidad de asignaturas de Estudios Básicos por semestre, el tercer carácter del código representa el
#semestre y el cuarto indica que es de Estudia Básicos si es el carácter B.