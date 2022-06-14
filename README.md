# CIPHER_HASH_RISTRAS_TEST
Programa de comprobacion de ristras

## Parametros del codigo:
- FRN: La variable ficheros_totales indica el frn maximo a utilizar, por defecto se usa 512 (se asume que es de 9 bits)
- Tamano de los ficheros: En el array tams_ficheros estan los distintos tamaños que se pueden utilizar, puedes quitar o añadir el que quieras, pero siempre en forma de lista, aunque sea un solo tamano
- Variable "contenido": Es irrelevante, por defecto esta a 0, el proposito es que todos los ficheros que se cifren sean iguales.
- Variable "clave": La clave de cifrado que se usa, es la misma para todos los ficheros (lo que va a mutar es el frn)
- Funciones de cifrado: En el código por defecto hay tres funciones definidas, pero tu puedes crear todas las que quieras, solamente tienes que añadir la funcion que has generado a la lista de funcs_cifrado

## Tabla de resultados:
- Cifrador: Indica el cifrador usado
- Tam fichero: Indica el tamano del fichero cifrado
- Ristras generadas: El numero de ristras que se generan
- Ristras unicas/repetidas: Las ristras generadas pueden se pueden repetir varias veces o ser unicas
- Media de diferencias: Entre las ristras generadas se calculan las diferencias que hay y se hace la media
