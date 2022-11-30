import os
import logging
import math

def dist_hamming(cadena1:str, cadena2:str) -> int:
	"""Función para medir la distancia hamming entre dos numeros binarios"""
	first = int(cadena1,2)
	second = int(cadena2, 2)
	return bin(first^second).count("1")

def verdad_to_minter(cadena:str) -> str:
	"""Esta funcion convierte una tabla de la verdad en una funcion booleana formada por minterminos
	Las variables son del tipo x0 .. xn siendo la mas significativa x0
	"""
	if cadena.startswith("0b"):
		cadena = cadena[2:] #Quitamos el 0b del principio
	if len(cadena)%2 != 0:
		raise ValueError("Tabla de la verdad incompleta", cadena)

	#n_vars = int(math.log2(len(cadena)))
	n_vars = math.log2(len(cadena))
	n_vars = int(math.ceil(n_vars))
	formato = "0"+str(n_vars)+"b" #para tener los indices con el numero correcto de bits
	result = ""
	primer = True
	for index,i in enumerate(cadena):
		if i == "1":
			index_bin = format(index,formato)
			if primer:
				result = "("
				primer = False
			else:
				result += " + ("
			for index2,j in enumerate(index_bin):
				#uso index2+1 para tener indices a partir de x1
				if j == "0":
					result += "x"+str(index2+1)+"'"
				else:
					result += "x"+str(index2+1)
			result += ")"
	return result

def check_function(index_bin:str, result:str) -> int:
	""" Esta funcion evalua una funcion booleana con los valores dados por el index_bin
	y devuelve 1 o 0
	Entradas:
		-Una cadena binaria del tipo: 010101
		-Una funcion para evaluar del tipo: (0) ^ (x1&x2)
		Los indices de la cadena binaria van de 1 a n y se sustituyen en la funcion
	"""
	for idx,i in enumerate(index_bin):
		if i == "0":
			result = result.replace("x"+str(idx+1),"0")
		else:
			result = result.replace("x"+str(idx+1),"1")
	return eval(result)

def new_expression(index_bin:str) -> str:
	"""Esta funcion genera la expresion en forma normal algebraica correspondiente
	"""
	new_exp = ""
	primer = True
	for idx,i in enumerate(index_bin):
		idx_aux = idx+1
		if i == "1":
			if primer:
				new_exp += "(x"+str(idx_aux)
				primer = False
				continue
			new_exp += "&x"+str(idx_aux)
	new_exp += ")"
	return new_exp

def verdad_to_FNA(cadena:str) -> str:
	"""Esta funcion obtiene la Forma Normal Algebraica de una funcion booleana partiendo de su tabla de la verdad
	"""
	if cadena.startswith("0b"):
		cadena = cadena[2:] #Quitamos el 0b del principio
	n_vars = int(math.log2(len(cadena)))
	formato = "0"+str(n_vars)+"b" #para tener los indices con el numero correcto de bits
	result = ""
	primer = True
	for index,i in enumerate(cadena):
		#print("==============================")
		#print("Para el indice ", index, "y valor ", i)
		index_bin = format(index,formato)
		if index == 0:
			result+= "("+str(i)+")"
			#print("Result actual: ",result)
		else:
			'''if primer:
				result+= " ^ "
				primer = False
			else:
				#comparo cadena[i] con la formula result aplicado al index_bin
				last_result = check_function(index_bin, result)
				if cadena[i] == last_result:
					result = result
				else:
					result+= new_expression(index_bin) #nueva operacion	'''
			#comparo cadena[i] con la formula result aplicado al index_bin
			#print("Result anterior: ", result)
			last_result = check_function(index_bin[::-1], result)
			if int(cadena[index]) == last_result:
				#print("Coinciden f= ", cadena[index],  "y p", last_result)
				result = result
			else:
				result += " ^ "
				#result+= new_expression(index_bin) #nueva operacion
				result+= new_expression(index_bin[::-1]) #nueva operacion
				#print("No coinciden f= ", cadena[index],  "y p", last_result)
				#print("genero nueva expresion: ", index_bin[::-1] , "=>" , new_expression(index_bin[::-1]))
				#todo el index bin al reves comprobar
			#print("Result actual: ", result)
	return result

def verdad_to_FNA_new(cadena:str) -> str:
	"""Esta funcion obtiene la Forma Normal Algebraica de una funcion booleana partiendo de su tabla de la verdad
	"""
	if cadena.startswith("0b"):
		cadena = cadena[2:] #Quitamos el 0b del principio
	n_vars = int(math.log2(len(cadena)))
	formato = "0"+str(n_vars)+"b" #para tener los indices con el numero correcto de bits
	result = ""
	primer = True
	for index,i in enumerate(cadena):
		print("==============================")
		print("Para el indice ", index, "y valor ", i)
		index_bin = format(index,formato)
		if index == 0:
			result+= "("+str(i)+")"
			print("Result actual: ",result)
		else:
			#comparo cadena[i] con la formula result aplicado al index_bin
			print("Result anterior: ", result)
			last_result = check_function(index_bin[::-1], result)
			if int(cadena[index]) == last_result:
				print("Coinciden f= ", cadena[index],  "y p", last_result)
				result = result
			else:
				result += " ^ "
				result+= new_expression(index_bin[::-1]) #nueva operacion
				print("No coinciden f= ", cadena[index],  "y p", last_result)
				print("genero nueva expresion: ", index_bin[::-1] , "=>" , new_expression(index_bin[::-1]))
				#todo el index bin al reves comprobar
			print("Result actual: ", result)
	return result

def grado_FNA(cadena:str) -> int:
	""" Esta funcion te devuelve el grado algebraico de una funcion booleana se interpreta al reves, el x4 (o el mas alto) es x0 en la funcion real"""
	cadena_separada = cadena.split("^")
	num_terms = 0
	for i in cadena_separada:
		num_terms_aux = i.count("x")
		if num_terms_aux > num_terms:
			num_terms = num_terms_aux
	return num_terms
	
def bool_n(n:int) -> dict:
	"""Esta funcion calcula todas las funciones booleanas posibles para un
	numero de variables n """
	logging.info("\nGetting all boolean functions of "+str(n)+" variables, best candidates")
	logging.info("===============================================================")
	n_fun_booleanas = 2**(2**n)
	len_tabla_verdad = 2**n

	#Diccionarios de resultados
	lista_fun_afines = []
	lista_no_lineales = []
	dict_no_lineales = {}

	#Saco todas las funciones (tabla verdad) y separo entre afines y no lineales
	formato = "0"+str(2**n)+"b" #formato de los strings q representan las funciones booleanas con los bits necesarios
	for i in range(0, n_fun_booleanas):
		actual = format(i, formato) #convertimos un entero en su representacion binaria con los bits necesarios
		grado = grado_FNA(verdad_to_FNA(actual))
		if grado == 1:
			lista_fun_afines.append(actual)
		else:
			lista_no_lineales.append(actual)
	print("	Hay ", len(lista_fun_afines),"funciones afines y", len(lista_no_lineales),"no lineales")
	#Calculo la distancia de las no lineales y las guardo con toda la info segun sus diferencias
	for no_lineal_actual in lista_no_lineales:
		diferencias = []
		diferencia_min = 0
		for afin_actual in lista_fun_afines:
			#no_lineal_actual = "0b"+no_lineal_actual
			#afin_actual = "0b"+afin_actual
			diferencias.append(dist_hamming(no_lineal_actual,afin_actual))
			diferencia_min = min(diferencias)
			#diferencias = min(dist_hamming(no_lineal_actual,afin_actual))
		dict_aux = {}
		dict_aux["Tabla verdad"] = no_lineal_actual
		dict_aux["Minterminos"] = verdad_to_minter(no_lineal_actual)
		dict_aux["FNA"] = verdad_to_FNA(no_lineal_actual)
		try:
			dict_aux["Equilibrio (1s/0s)"] = no_lineal_actual.count("1")/no_lineal_actual.count("0")	#str(no_lineal_actual.count("1"))+"/"+str(no_lineal_actual.count("0"))
		except:
			if no_lineal_actual.count("0") == 0:
				dict_aux["Equilibrio (1s/0s)"] = no_lineal_actual.count("1")
		grado_fun = grado_FNA(verdad_to_FNA(no_lineal_actual))
		dict_aux["Grado"] = grado_fun #grado_FNA(verdad_to_FNA(no_lineal_actual))
		dict_aux["Resiliencia"] = grado_fun - n + 1
		dict_aux["No linealidad"] = diferencia_min

		try:
			dict_no_lineales[diferencia_min].append(dict_aux)
		except:
			dict_no_lineales[diferencia_min] = []
			dict_no_lineales[diferencia_min].append(dict_aux)
	return (lista_fun_afines,dict_no_lineales)
		
			
if __name__ == "__main__":
	if os.path.exists("ristras.log"): #Borramos el log si existe porque el modo de escritura solo reescribe si abres un nuevo shell de python
		os.remove("ristras.log")
	logging.basicConfig(filename = "funciones.log", filemode = 'w' ,format = '%(message)s',level = logging.DEBUG)
	lista_variables = [3]
	
	#Para buscar todas
	'''for i in lista_variables:
		afines = []
		no_lineales = {}
		print("Para ",i," variables")
		afines, no_lineales = bool_n(i)
		logging.info("\nAFINES")
		for funcion_afin in afines:
			logging.info(funcion_afin)
		logging.info("\nNO LINEALES")
		for diferencias in no_lineales:
			logging.info(str(diferencias)+" Diferencias")
			for funcion in no_lineales[diferencias]:
				logging.info("	"+str(funcion))'''
				
	#Para buscar las mejores

	for i in lista_variables:
		afines = []
		no_lineales = {}
		print("Para ",i," variables")
		afines, no_lineales = bool_n(i)
		#logging.info("\nAFINES")
		#for funcion_afin in afines:
			#logging.info(funcion_afin)
		#logging.info("\nNO LINEALES")
		for diferencias in no_lineales:
			#logging.info(str(diferencias)+" Diferencias")
			for funcion in no_lineales[diferencias]:
				#logging.info("	"+str(funcion))
				
				if funcion["Resiliencia"] >= -1 and funcion["No linealidad"] >=3:
					logging.info("	"+str(funcion))


	#F y G =  (0) ^ (x1) ^ (x2) ^ (x3) ^ (x1&x3) ^ (x2&x3) ^ (x4) ^ (x1&x4) ^ (x2&x4)
	#H =  (0) ^ (x1) ^ (x2) ^ (x3)
	#I =  (0) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x3)
	#print("F y G = ",verdad_to_FNA("0b0110111111110110"))
	#print("H = ",verdad_to_FNA("0b01101001"))
	#print("I = ",verdad_to_FNA("0b01111000"))
	#print("I = ",verdad_to_FNA_new("0b01111000"))



	