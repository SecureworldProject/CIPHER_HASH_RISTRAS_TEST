

def ejemplo_estandar(elem,frn,pos,clave):
  '''elem = (clave or pos or frn)'''
  elem = (clave | pos | frn)%256
  return elem

def ejemplo_dependencia_bit(elem,frn,pos,clave):
  '''elem = (clave or pos or last_bit(frn))'''
  frn = frn & 0b000000001
  elem = (clave | pos | frn)%256
  return elem

def ejemplo_no_lineal2(elem, frn, pos, clave):
  '''elem = ((clave or pos) + frn)'''
  elem = ((clave | pos) + frn)%256
  #elem = ((clave ^ pos) + frn)%256
  return elem 

def ejemplo_no_lineal(elem, frn, pos, clave):
  '''elem = (clave or frn)+(pos or frn)'''
  #elem = (clave | pos)+(frn | pos)
  elem = (clave | frn)+(pos | frn)
  #elem = (clave ^ pos)+(frn ^ pos)
  elem = elem % 256
  return elem

def ejemplo_mejor(elem, frn, pos, clave):
  '''elem = ((clave or frn) + ((pos or frn)>>1))'''
  elem = ((clave | frn) + ((pos | frn)>>1))
  elem = elem % 256
  return elem

def cifrado_test(elem, frn, pos, clave):
  '''Ver el codigo'''
  #elem = (clave ^ (frn>>5))+(pos ^ int (frn*5))
  a = clave ^ frn 
  b = pos ^ frn
  #c = (a | b)>>5 # me da +256 ristras
  c = a | b # me da 256 ristras con el maximo de diferencias
  elem = (a & b)^(~a & c) 
  elem = elem % 256
  return elem

def cifrado_test2(elem,frn,pos,clave):
  '''Cifrado viendo el recetario'''
  #Difusion
  #pos = (pos*97)%512 # a partir de 97 es bueno
  #elem = ((clave | frn) + ((pos | frn)>>1))
  #elem = ((clave ^ frn) + ((pos | frn)>>1))
  #elem = ((clave ^ frn) + ((pos^frn)>>1))
  #elem = ((clave ^ frn) + ((pos^frn)>>1))
  a = clave^frn
  b = pos^frn 
  #print("a = ",a," y b = ", b>>1)
  elem = a + (b>>1)
  elem = elem % 256
  return elem 

def cifrado_test3(elem,frn,pos,clave):
  '''Cifrado viendo el recetario'''
  #Division clave
  key1 = clave & 0x11000000
  key2 = clave & 0x00110000
  
  a = (key1^frn) ^ pos
  b = (key2 ^ frn) ^ elem
  elem = a + b
  elem = elem % 256
  return elem 