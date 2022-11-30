
import cifradores
import random
import logging
import time

def genera_ficheros(lista, total_ficheros, tam):
	'''Generamos 512 ficheros iguales de tam_fichero bytes da igual el relleno, despues lo machacamos'''
	for x in range(total_ficheros):
			lista.append([contenido for y in range(tam)])

def cifra_ficheros_completo(lista,total_ficheros, tam, fun_hash):
	'''Ciframos los 512 ficheros cada uno con un frn distinto y sobreescribimos los valores '''
	#print("			Clave = ",clave)
	for frn in range (total_ficheros):
		for i in range (tam):
			#print("elem: ", lista_ficheros[frn][i], "hash: ", fun_hash(lista_ficheros[frn][i], frn, i, clave))
			lista_ficheros[frn][i] = ((lista_ficheros[frn][i] + fun_hash(lista_ficheros[frn][i], frn, i, clave))%256)

def check_ficheros_new(lista, total_ficheros, tam):
	'''Comprobamos que no haya 2 ristras iguales'''
	global ristras_generadas

	ristras_generadas = 0

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
	ristras_generadas = ristras_unicas + ristras_repetidas
	print("		Restras unicas/repetidas: ", ristras_unicas, ristras_repetidas)

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
	
	#logging.info("Ristras unicas/ repetidas = %d/%d", ristras_unicas, ristras_repetidas)
	ristras_unicas_repetidas = "{:d}/{:d}".format(ristras_unicas,ristras_repetidas)
	ristras_generadas = ristras_unicas + ristras_repetidas

	# Se incluyen en el diccionario de ristras, las ristras unicas
	for i in lista_ristras_unicas:
		dict_ristras[i] = []
	#logging.info("Diccionario de ristras: \n%s",dict_ristras)

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
				#logging.info("Comparo las ristras %d y %d = %d diferencias",lista_ficheros[ristra_act],lista_ficheros[ristra_next],diferencias)
				pass
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



def genera_lista_claves():
	'''Esta funcion contiene un generador de claves para ahorra en memoria'''
	a = []
	for i in range(10000):
		a.append(random.randint(0,(2**64)))
	return a

def pruebas():
	#xor entre dos variables es igual qe la de c con byte array
	variable_0 = 0x01a5ff12d3#{ 0x01, 0xA5, 0xFF, 0x12, 0xD3 };
	variable_1 = 0x2b4534a13e#{ 0x2B, 0x45, 0x34, 0xA1, 0x3E };
	variable_2 = 0x4023114512
	variable_3 = 0xBE0149A25F
	#print(hex(variable_0^variable_1))

	#F = (1) ^ (variable_3) ^ (variable_2)	^ (variable_3&variable_1) ^ (variable_2&variable_1)	^ (variable_3&variable_2&variable_0) ^ (variable_3&variable_1&variable_0)	^ (variable_2&variable_1&variable_0)^ (variable_3&variable_2&variable_1&variable_0)
	F = (0xFF) ^ (variable_3) ^ (variable_2)	^ (variable_3&variable_1) ^ (variable_2&variable_1)	^ (variable_3&variable_2&variable_0) ^ (variable_3&variable_1&variable_0)	^ (variable_2&variable_1&variable_0)^ (variable_3&variable_2&variable_1&variable_0)
	print(F,F%256)

	'''#prueba de transformada

	#Pseudo transformada
	#a = int(cadena_total[0:80],2)
	#b = int(cadena_total[81:160],2)
	a = 0xFFFFFFFFFFFFFFFFFFFF
	b = 0xFFFFFFFFFFFFFFFFFFFF
	#a = 0x0123456789abcdef1234
	#b = 0x0123456789abcdef1234
	a = a+b
	#a = int(cadena_total[0:80],2)
	b = a+(2*b) 


	len_a = len(hex(a))-2
	if len_a == 21: #10bytes + 10bytes puede dar 11bytes, en este caso se ha quedado medio byte y python no pone el 0
		a = "0"+hex(a)[2:]
	len_b = len(hex(b))-2
	if len_b == 21: #10bytes + 10bytes puede dar 11bytes, en este caso se ha quedado medio byte y python no pone el 0
		b = "0"+hex(b)[2:]
	print(a)
	print(b)
	new_message = [0,0,0,0]
	new_message[0] = a[0:10]
	new_message[1] = a[10:20]
	new_message[2] = b[0:10]
	new_message[3] = b[10:20]
	print(new_message)
	#for i in new_message:
	#	print(len(i))

	new_message[0] = int(a[0:10],16)
	new_message[1] = int(a[10:20],16)
	new_message[2] = int(b[0:10],16)
	new_message[3] = int(b[10:20],16)
	print(new_message)'''


	

if __name__ == "__main__":
	#Parametros 
	#pruebas()
	lista_ficheros = []
	ficheros_totales = 512
	contenido = 0
	ristras_generadas = 0
	error = 0

	ristras_generadas = 0
	ristras_unicas_repetidas = "0/0"
	media_diferencias = 0
	max_dif = 0
	min_dif = 0

	#cifrado = cifradores.encryp_Nokia_test
	cifradores = [cifradores.encryp_Nokia_test_hex]#, cifradores.encryp_Uva_bin]
	#Lo primero es generar una lista de claves de muchos tipos
	lista_claves = genera_lista_claves()
	lista_tams = [2,8]
	#Itero sobre claves
	print(f"Para {ficheros_totales} ristras y 10K claves aleatorias")
	start = time.time()
	for cifrado in cifradores:
		print("Para el cifrado: ",cifrado.__name__)
		for tam in lista_tams:	
			error = 0	
			#lista_ficheros = []
			for clave_actual in lista_claves:
				clave = clave_actual
				#print("Clave es: ", clave, " de tamaño: ", len(bin(clave)))
				error_nuevo = 0
				#Calculo las ristras generadas y le resto 512
				lista_ficheros = []
				genera_ficheros(lista_ficheros,ficheros_totales,tam)
				cifra_ficheros_completo(lista_ficheros,ficheros_totales,tam,cifrado) 
				check_ficheros(lista_ficheros,ficheros_totales,tam)
				#print("		Ristras generadas: ", ristras_generadas, "para la clave: ", clave)
				error_nuevo = (ristras_generadas - ficheros_totales)**2
				error += error_nuevo
				#print(ristras_generadas, error, error_nuevo)
			print("	Para el tam: ",tam, "error cuadratico medio = ", error/len(lista_claves),"\n\t\tError" ,error)
	end = time.time()
	print("Duracion: ", end-start)
	#'''