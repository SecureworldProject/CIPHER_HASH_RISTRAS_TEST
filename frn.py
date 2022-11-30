
import logging
import os
import sys
import math
import cifradores
import random

def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length  - Optional  : character length of bar (Int)
    """
    str_format = "{0:." + str(decimals) + "f}"
    percents = str_format.format(100 * (iteration / float(total)))
    filled_length = int(round(length * iteration / float(total)))
    bar = '█' * filled_length + '-' * (length - filled_length)

    sys.stdout.write('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix))
    #print('\r%s |%s| %s%s %s' % (prefix, bar, percents, '%', suffix),end='') #Tambien vale

    if iteration == total:
        sys.stdout.write('\n')
    sys.stdout.flush()

def hash_pruebas(pos,frn,clave):
  pass

def genera_ficheros(lista, total_ficheros, tam):
  '''Generamos 512 ficheros iguales de tam_fichero bytes da igual el relleno, despues lo machacamos'''
  for x in range(total_ficheros):
      lista.append([contenido for y in range(tam)])
  logging.debug(" Se han generado %d ficheros con contenido = %d, de esta forma.\n\t%s",total_ficheros,contenido,lista[0])

def cifra_ficheros(lista,total_ficheros, tam, fun_hash):
  '''Ciframos los 512 ficheros cada uno con un frn distinto y sobreescribimos los valores '''
  for frn in range (total_ficheros):
    for i in range (tam):
      lista_ficheros[frn][i] = fun_hash(lista_ficheros[frn][i], frn, i, clave)
    logging.debug(" Fichero %d cifrado: %s", frn, lista_ficheros[frn])

def cifra_ficheros_completo(lista,total_ficheros, tam, fun_hash):
  '''Ciframos los 512 ficheros cada uno con un frn distinto y sobreescribimos los valores '''
  for frn in range (total_ficheros):
    for i in range (tam):
      lista_ficheros[frn][i] = ((lista_ficheros[frn][i] + fun_hash(lista_ficheros[frn][i], frn, i, clave))%256)
    logging.debug(" Fichero %d cifrado: %s", frn, lista_ficheros[frn])

def descifra_ficheros_completo(lista,total_ficheros, tam, fun_hash):
  '''Ciframos los 512 ficheros cada uno con un frn distinto y sobreescribimos los valores '''
  for frn in range (total_ficheros):
    for i in range (tam):
      lista_ficheros[frn][i] = (lista_ficheros[frn][i] - fun_hash(lista_ficheros[frn][i], frn, i)%256)
    logging.debug(" Fichero %d descifrado: %s", frn, lista_ficheros[frn])

def check_ficheros(lista, total_ficheros, tam):
  '''Comprobamos que no haya 2 ristras iguales'''
  global ristras_generadas
  global ristras_unicas_repetidas
  global media_diferencias

  ristras_generadas = 0
  ristras_unicas_repetidas = "0/0" 
  media_diferencias = 0

  logging.debug(" Comprobando...")
  marcados = set([])
  coincidencias = 0
  ficheros_completamente_diferentes = 0
  dict_ristras = {}
  lista_ristras_unicas = []
  ristras_unicas = 0
  ristras_repetidas = 0
  ristras_generadas = 0
  for frn in range(total_ficheros): 
    if frn in marcados:
      continue
    #para cada secuencia compruebo con el resto (posteriores)
    frns_same_seq = [frn]
    for frn2 in range (frn + 1, total_ficheros):
      if lista_ficheros[frn] == lista_ficheros[frn2]:
        frns_same_seq.append(frn2)
        marcados.add(frn2) #Si es igual a un fichero previamente comprobado lo marco para no comprobarlo otra vez, porque los que sean iguales ya se han registrado
        coincidencias += 1
    if len(frns_same_seq) == 1:
      ristras_unicas += 1
      lista_ristras_unicas.append(frn)
    else:
      dict_ristras[frn] = frns_same_seq
      #ristras_repetidas = len(dict_ristras)
      ristras_repetidas += 1
  
  logging.info("Ristras unicas/ repetidas = %d/%d", ristras_unicas, ristras_repetidas)
  ristras_unicas_repetidas = "{:d}/{:d}".format(ristras_unicas,ristras_repetidas)
  ristras_generadas = ristras_unicas + ristras_repetidas

  # Se incluyen en el diccionario de ristras, las ristras unicas
  for i in lista_ristras_unicas:
    dict_ristras[i] = []
  logging.info("Diccionario de ristras: \n%s",dict_ristras)

  if ristras_generadas>1:
    check_ristras_diferentes(lista,dict_ristras,tam)
  else:
    media_diferencias = 0

def check_ristras_diferentes(lista, dict_ristras, tam):
  global media_diferencias
  global max_dif
  global min_dif
  media_diferencias = 0

  diferencias = 0
  diferencias_totales = 0
  comparaciones = 0
  max_dif = 0
  min_dif = tam + 1
  ristras_unicas = len(dict_ristras)
  lista_ficheros = list(dict_ristras.keys())
  for ristra_act in range(ristras_unicas):
    for ristra_next in range(ristra_act+1,ristras_unicas):      
      diferencias = 0
      for i in range(tam):
        #if lista[ristra_act][i] != lista[ristra_next][i]:
        if lista[lista_ficheros[ristra_act]][i] != lista[lista_ficheros[ristra_next]][i]:
          diferencias_totales+=1
          diferencias += 1
      #logging.info("Comparo las ristras %d y %d = %d diferencias",ristra_act,ristra_next,diferencias)
      if diferencias < tam:
        logging.info("Comparo las ristras %d y %d = %d diferencias",lista_ficheros[ristra_act],lista_ficheros[ristra_next],diferencias)
      if diferencias > max_dif:
        max_dif = diferencias
      if diferencias < min_dif:
        min_dif = diferencias
      comparaciones+=1
      #logging.info("Comparaciones: %d",comparaciones)
  if comparaciones ==0:
    media_diferencias = 0
  else:
    media_diferencias = diferencias_totales/comparaciones


def cifrado_malo(elem, frn, pos, clave):
  '''elem = (elem+ pos + clave + frn) % 256'''
  elem = (elem + pos + clave + frn) % 256
  return elem

def cifrado_bueno(elem, frn, pos, clave):
  '''elem = (elem + (pos^frn + (int)((pos^frn)/256))%256)%256'''
  elem = elem + (pos^frn + (int)((pos^frn)/256))%256
  #elem = elem + ((pos^frn) + ((pos^frn)//256))
  elem = elem % 256
  return elem

def cifrado_test(elem, frn, pos, clave):
  '''elem = (clave or pos)+(frn or pos)'''
  elem = (clave or pos)+(frn or pos)
  elem = elem % 256
  return elem  


def genera_lista_claves():
  '''Esta funcion contiene un generador de claves para ahorra en memoria'''
  a = []
  for i in range(10):
    a.append(random.randint(0,(2**64)))
  return a


if __name__ == "__main__":
  """Programa para calcular las ristras generadas
  Parametros del codigo:
    - FRN: La variable ficheros_totales indica el frn maximo a utilizar, por defecto se usa 512 (se asume que es de 9 bits)
    - Tamano de los ficheros: En el array tams_ficheros estan los distintos tamaños que se pueden utilizar, puedes quitar o añadir el que quieras, pero siempre en forma de lista, aunque sea un solo tamano
    - Variable "contenido": Es irrelevante, por defecto esta a 0, el proposito es que todos los ficheros que se cifren sean iguales.
    - Variable "clave": La clave de cifrado que se usa, es la misma para todos los ficheros (lo que va a mutar es el frn)
    - Funciones de cifrado: En el código por defecto hay tres funciones definidas, pero tu puedes crear todas las que quieras, solamente tienes que añadir la funcion que has generado a la lista de funcs_cifrado

  Tabla de resultados:
    - Cifrador: Indica el cifrador usado
    - Tam fichero: Indica el tamano del fichero cifrado
    - Ristras generadas: El numero de ristras que se generan
    - Ristras unicas/repetidas: Las ristras generadas pueden se pueden repetir varias veces o ser unicas
    - Media de diferencias: Entre las ristras generadas se calculan las diferencias que hay y se hace la media
    - Formula: El docstring de la función, es muy importante que lo incluyas
  """

  # /////////////Inicializacion del programa
  os.system("cls")
  print("Bienvenido al comprobador de ficheros:")
  print("======================================")
  if os.path.exists("ristras.log"): #Borramos el log si existe porque el modo de escritura solo reescribe si abres un nuevo shell de python
    os.remove("ristras.log")
  logging.basicConfig(filename = "ristras.log", filemode = 'w' ,format = '%(message)s',level = logging.DEBUG)

  option = input("Pulsa 1 para probar todos los cifradores. Para probar solo el de test, pulsa cualquier tecla\n")
  if option == "1":
    funcs_cifrado =[cifrado_bueno, cifrado_malo, cifrado_test]
  else:
    if option == "2":
      funcs_cifrado=[cifradores.ejemplo_estandar, cifradores.ejemplo_dependencia_bit, cifradores.ejemplo_no_lineal, cifradores.ejemplo_no_lineal2, cifradores.ejemplo_mejor]
    else: # el cifrado mas comun que se pruebe sera con el que haces tests, pero puedes cambiar este cifrado por el que quieras
      #funcs_cifrado=[cifradores.hash_uva_no_difusion, cifradores.encryp_Uva_no_confusion]
      #funcs_cifrado=[cifradores.hash_uva_no_difusion, cifradores.encryp_Uva_no_confusion, cifradores.encryp_Uva, cifradores.encryp_Uva_bin, cifradores.encryp_Nokia, cifradores.encryp_Nokia_monofuncion,cifradores.encryp_Nokia_test]
      funcs_cifrado=[cifradores.encryp_Nokia_test,cifradores.encryp_Nokia_test_hex, cifradores.encryp_Uva_bin]
      #funcs_cifrado=[cifradores.encryp_Uva_bin, cifradores.encryp_Uva_fna]
  
  ''' Para este cifrador en miniatura tenemos:
  frn de 9 bits en lugar de 32
  clave de 36 bits en lugar de 128/256
  pos de 9 bits en lugar de 32
  '''

  ficheros_totales = 512 #FRN max
  print("Se va a usar una frn de ", ficheros_totales)

  contenido = 0 #Contenido de los ficheros en claro
  
  clave = 14
  #clave = 145
  #clave = 145938748374837
  #clave = 14593874837483793993949982938295397436736873687326473247392489357875483243842648732643433232
  #clave = 170414 #  0b101001100110101110 18 bits

  tams_fichero = [2,8]
  resultados = []
  categorias = ["Cifrador","Tam fichero","Ristras generadas","Ristras unicas/repetidas","Media diferencias(Max/Min)","Formula"]

  ristras_generadas = 0
  ristras_unicas_repetidas = "0/0"
  media_diferencias = 0
  max_dif = 0
  min_dif = 0

  # /////////////////Se testea cada cifrador para los distintos tamaños de fichero. Siempre se testean frnmax ficheros
  num_cifrados = len(funcs_cifrado)
  num_tams = len(tams_fichero)
  pasos_total = 3*num_cifrados*num_tams
  paso_actual = 0
  for cifrado in funcs_cifrado:
    for tam in tams_fichero:
      lista_ficheros = [] #Lista de ficheros vacia que se procede a generar y cifrar
      #Genero ristras vacias, las cifro, y compruebo cambios, todo esto con barra de progreso
      printProgressBar(paso_actual,pasos_total,prefix="Generando ficheros({:s},{:d})".format(cifrado.__name__,tam), suffix="Completado", length=50, printEnd='\r')
      genera_ficheros(lista_ficheros,ficheros_totales,tam)
      
      printProgressBar(paso_actual+1,pasos_total,prefix="Cifrando ficheros ({:s},{:d})".format(cifrado.__name__,tam), suffix="Completado", length=50, printEnd='\r')
      cifra_ficheros_completo(lista_ficheros,ficheros_totales,tam,cifrado) # Se mete en cifrado la funcion de hash que estas probando
      
      printProgressBar(paso_actual+2,pasos_total,prefix="Comprobando ficheros ({:s},{:d})".format(cifrado.__name__,tam), suffix="Completado", length=50, printEnd='\r')
      logging.debug("\n\nPara el cifrador %s, y tam = %d\n=======================================================\n",cifrado.__name__,tam)
      check_ficheros(lista_ficheros,ficheros_totales,tam)
      paso_actual+=3
      if paso_actual == pasos_total:
        printProgressBar(pasos_total,pasos_total,prefix="Finalizando     ({:s},{:d})".format(cifrado.__name__,tam), suffix="Completado", length=50, printEnd='\r')
      media_diferencias_str = "{:.2f}".format(media_diferencias)+"("+str(max_dif)+"/"+str(min_dif)+")"
      #resultados.append([cifrado.__name__,tam, ristras_generadas, ristras_unicas_repetidas ,media_diferencias,cifrado.__doc__])
      resultados.append([cifrado.__name__,tam, ristras_generadas, ristras_unicas_repetidas ,media_diferencias_str,cifrado.__doc__])

  # ///////////////////Presentacion de resultados
  tabla_format = "{:^30}"*(len(categorias))
  print("\n")  
  print(tabla_format.format(*categorias)) 
  for resultado in resultados:
    print(tabla_format.format(*resultado))
  print()
  print("Para una información detallada consulta el fichero ristras.log\n")