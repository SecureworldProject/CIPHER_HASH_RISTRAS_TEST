

def xor(a, b):
    return (a and not b) or (not a and b)

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

def FG(elem,frn,pos,clave):
  '''(0)^(x1)^(x2)^(x3)^(x1&x3)^(x2&x3)^(x4)^(x1&x4)^(x2&x4)'''
  clave1 = 14
  clave2 = 5
  elem = (0)^(frn)^(pos)^(clave1)^(frn&clave1)^(pos&clave1)^(clave2)^(frn&clave2)^(pos&clave2)
  elem = elem % 256
  return elem 

def H(elem,frn,pos,clave):
  '''(0) ^ (x1) ^ (x2) ^ (x3)'''
  elem = (0) ^ (frn) ^ (pos) ^ (clave)
  elem = elem % 256
  return elem 

def I(elem,frn,pos,clave):
  '''(0) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x3)'''
  elem = (0) ^ (frn) ^ (pos) ^ (frn&pos) ^ (clave)
  elem = elem % 256
  return elem 

def encryp_Uva (elem,frn,pos,clave):
  '''Uva Real'''
  #Establecer tamaño del mensaje en 11 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]
     
  elem= (hash_uva(message)) %256

  #print ('elem=', elem)
  return elem

def hash_uva (message):
  '''F,G = (0)^(x1)^(x2)^(x3)^(x1&x3)^(x2&x3)^(x4)^(x1&x4)^(x2&x4)
  H = (0) ^ (x1) ^ (x2) ^ (x3)
  I = (0) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x3)
  '''

  
  F= (message[1] ^ message[0]) or (message[2] ^ message[3])
  G= (F ^ message[4]) or (message[5] ^ message[6])
  H= (G ^ message[7] ^ message[8])
  I= (H ^ (message[9] or message[10]))

  

  hash = I % 256

  return hash

def encryp_Uva_bin (elem,frn,pos,clave):
  '''Uva Real or bit'''
  #Establecer tamaño del mensaje en 11 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]
     
  elem= (hash_uva_bin(message)) %256

  #print ('elem=', elem)
  return elem

def hash_uva_bin (message):
  '''F,G = (0)^(x1)^(x2)^(x3)^(x1&x3)^(x2&x3)^(x4)^(x1&x4)^(x2&x4)
  H = (0) ^ (x1) ^ (x2) ^ (x3)
  I = (0) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x3)
  '''

  
  '''F= (message[1] ^ message[0]) | (~(message[2]) ^ message[3])
  G= (F ^ message[4]) | (message[5] ^ ~(message[6]))
  H= (G ^ message[7] ^ message[8])
  I = (H ^ (message[9] | message[10]))'''

  #PARA PROBAR SIN CONFUSION
  F= message[10] ^ message[9] ^ message[8] ^ message[7] ^ message[6] ^ message[5] ^ message[4] ^ message[3] ^ message[2] ^ message[1] ^ message[0]    
  F = message[7]
  

  #hash = I % 256
  resul = F%256

  #return hash
  return resul

def encryp_Uva_fna(elem,frn,pos,clave):
  '''Uva Real or bit'''
  #Establecer tamaño del mensaje en 11 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]
     
  elem= (hash_uva_fna(message)) %256

  #print ('elem=', elem)
  return elem

def hash_uva_fna(message):
  '''F,G = (0)^(x1)^(x2)^(x3)^(x1&x3)^(x2&x3)^(x4)^(x1&x4)^(x2&x4)
  H = (0) ^ (x1) ^ (x2) ^ (x3)
  I = (0) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x3)
  '''

  
  #F= (message[1])^(message[0])^(message[2])^(message[1]&message[2])^(message[0]&message[2])^(message[3])^(message[1]&message[3])^(message[0]&message[3])
  F = (message[3])^(message[2])^(message[0])^(message[3]&message[0])^(message[2]&message[0])^(message[1])^(message[3]&message[1])^(message[2]&message[1])

  #G= (F)^(message[4])^(message[5])^(F&message[5])^(message[4]&message[5])^(message[6])^(F&message[6])^(message[4]&message[6])
  G = (message[6])^(message[5])^(message[4])^(message[6]&message[4])^(message[5]&message[4])^(F)^(message[6]&F)^(message[5]&F)
  
  H= (G ^ message[7] ^ message[8])
  #I = (H) ^ (message[9]) ^ (H&message[9]) ^ (message[10])
  I = (message[10]) ^ (message[9]) ^ (message[10]&message[9]) ^ (H)
  #I = H
  

  hash = I % 256

  return hash

def encryp_Uva_no_confusion (elem,frn,pos,clave):
  '''Hash uva no confusion'''
  #Establecer tamaño del mensaje en 11 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]
     
  elem= (hash_uva_no_confusion(message)) %256

  #print ('elem=', elem)
  return elem

def hash_uva_no_confusion (message):
     
     F= message[1] ^ message[0] ^ message[2] ^ message[3] ^ message[4] ^ message[5] ^ message[6] ^ message[7] ^ message[8] ^ message[9] ^ message[10]    

     #F = message[0]

     hash = F % 256
    
     return hash

def hash_uva_no_difusion (elem,frn,pos,clave):
     '''Cifrador UVA completo sin difusion'''
     clave1 = 14
     clave2 = 5
     F= (pos ^ frn) or (clave1 ^ clave2)
     G= (F ^ frn) or (pos ^ clave)
     H= (G ^ frn ^ pos)
     I= (H ^ (frn or pos))
     

     hash = I % 256
    
     return hash

def encryp_Nokia (elem,frn,pos,clave):
  '''Nokia Real'''
  #Establecer tamaño del mensaje en 11 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]
     
  elem= (hash_nokia(message)) %256

  #print ('elem=', elem)
  return elem

def hash_nokia(message):
  '''Hash nokia'''
  '''
  F{'Tabla verdad': '1100001011100100', 'Minterminos': "(x1'x2'x3'x4') + (x1'x2'x3'x4) + (x1'x2x3x4') + (x1x2'x3'x4') + (x1x2'x3'x4) + (x1x2'x3x4') + (x1x2x3'x4)", 'FNA': '(1) ^ (x2) ^ (x3) ^ (x1&x2&x3) ^ (x2&x4) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x1&x2&x3&x4)', 'Equilibrio (1s/0s)': 0.7777777777777778, 'Grado': 4, 'Resiliencia': 1, 'No linealidad': 5}
  G{'Tabla verdad': '0100001110011010', 'Minterminos': "(x1'x2'x3'x4) + (x1'x2x3x4') + (x1'x2x3x4) + (x1x2'x3'x4') + (x1x2'x3x4) + (x1x2x3'x4') + (x1x2x3x4')", 'FNA': '(0) ^ (x1) ^ (x1&x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x3) ^ (x4) ^ (x2&x4) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x1&x2&x3&x4)', 'Equilibrio (1s/0s)': 0.7777777777777778, 'Grado': 4, 'Resiliencia': 1, 'No linealidad': 5}
  H{'Tabla verdad': '01011110', 'Minterminos': "(x1'x2'x3) + (x1'x2x3) + (x1x2'x3') + (x1x2'x3) + (x1x2x3')", 'FNA': '(0) ^ (x1) ^ (x3) ^ (x1&x3) ^ (x1&x2&x3)', 'Equilibrio (1s/0s)': 1.6666666666666667, 'Grado': 3, 'Resiliencia': 1, 'No linealidad': 1}
  I xor lineal
  I {'Tabla verdad': '01000111', 'Minterminos': "(x1'x2'x3) + (x1x2'x3) + (x1x2x3') + (x1x2x3)", 'FNA': '(0) ^ (x1) ^ (x1&x2) ^ (x2&x3)', 'Equilibrio (1s/0s)': 1.0, 'Grado': 2, 'Resiliencia': 0, 'No linealidad': 2}
  '''
  # F = (1) ^ (x2) ^ (x3) ^ (x1&x2&x3) ^ (x2&x4) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x1&x2&x3&x4)
  # G = (0) ^ (x1) ^ (x1&x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x3) ^ (x4) ^ (x2&x4) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x1&x2&x3&x4)
  # H = (0) ^ (x1) ^ (x3) ^ (x1&x3) ^ (x1&x2&x3)
  # I = (0) ^ (x1) ^ (x2) ^ (x3)
  # I = (0) ^ (x1) ^ (x1&x2) ^ (x2&x3)


  F = (1) ^ (message[1]) ^ (message[2]) ^ (message[0]&message[1]&message[2]) ^ (message[1]&message[3]) ^ (message[0]&message[1]&message[3]) ^ (message[0]&message[2]&message[3]) ^ (message[0]&message[1]&message[2]&message[3])
  #F = (1) ^ (message[2]) ^ (message[1]) ^ (message[3]&message[2]&message[1]) ^ (message[2]&message[0]) ^ (message[3]&message[2]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])
  G = (0) ^ (F) ^ (F&message[4]) ^ (F&message[5]) ^ (message[4]&message[5]) ^ (F&message[4]&message[5]) ^ (message[6]) ^ (message[4]&message[6]) ^ (F&message[4]&message[6]) ^ (F&message[5]&message[6]) ^ (F&message[4]&message[5]&message[6])
  #G = (message[6]) ^ (message[6]&message[5]) ^ (message[6]&message[4]) ^ (message[5]&message[4]) ^ (message[6]&message[5]&message[4]) ^ (F) ^ (message[5]&F) ^ (message[6]&message[5]&F) ^ (message[6]&message[4]&F) ^ (message[6]&message[5]&message[4]&F)
  
  #H = (message[8]) ^ (G) ^ (message[8]&G) ^ (message[8]&message[7]&G)
  #I = (message[9]) ^ (message[9]&message[10]) ^ (message[10]&H)
  I = G ^ message[7] ^ message[8] ^ message[9] ^ message[10]

  resul = I%256
  return resul

def encryp_Nokia_monofuncion(elem,frn,pos,clave):
  '''Nokia Real Monofuncion'''
  #Establecer tamaño del mensaje en 4 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]

  message_final = [0,0,0,0]
  message_final[0] = message[0]^message[1]^message[2]
  message_final[1] = message[3]^message[4]^message[5]
  message_final[2] = message[6]^message[7]^message[8] 
  message_final[3] = message[9]^message[10]
     
  elem= (hash_nokia_mono(message_final)) %256

  #print ('elem=', elem)
  return elem

def hash_nokia_mono(message):
  #F = (1) ^ (x2) ^ (x3) ^ (x1&x2&x3) ^ (x2&x4) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x1&x2&x3&x4)
  F = (1) ^ (message[1]) ^ (message[2]) ^ (message[0]&message[1]&message[2]) ^ (message[1]&message[3]) ^ (message[0]&message[1]&message[3]) ^ (message[0]&message[2]&message[3]) ^ (message[0]&message[1]&message[2]&message[3])

  hash = F%256
  return hash

def encryp_Nokia_test_old (elem,frn,pos,clave):
  '''Nokia Real'''
  #clave = 170414 #  0b101001100110101110 18 bits
  frn_format = "09b"
  frn_ = format(frn,frn_format)
  pos_format = "05b"
  pos_ = format(pos,pos_format)
  clave_format = "018b"
  clave_ = format(clave,clave_format)

  ###Adaptar la clave
  tam_clave_ideal = 18
  tam_clave = len(bin(clave)[2:])
  if tam_clave<tam_clave_ideal:
    #print(clave_)
    #La clave mide menos de 18 bits hay que repetirla n veces
    clave_ = bin(clave)[2:]*(tam_clave_ideal//tam_clave)
    #print(clave_)
  else: 
    clave_ = bin(clave)[2:tam_clave_ideal+2]

  message = frn_ + pos_ + clave_
  #print(message)
  #11100110 01000010 10011001 10101110
  new_message = [0,0,0,0]
  '''new_message[0] = int(message[0:8],2)
  new_message[1] = int(message[9:16],2)
  new_message[2] = int(message[17:24],2)
  new_message[3] = int(message[25:32],2)'''
  '''new_message[0] = (message[0:8])
  new_message[1] = (message[9:16])
  new_message[2] = (message[17:24])
  new_message[3] = (message[25:32])'''

  #pseudo transformada de hadamard
  a = int(message[0:16],2)
  b = int(message[17:32],2)
  a = a + b 
  b = a * (2*b)
  new_format = "016b"
  a = format(a,new_format)
  b = format(b,new_format)
  new_message[0] = int(a[0:8],2)
  new_message[1] = int(a[9:16],2)
  new_message[2] = int(b[0:8],2)
  new_message[3] = int(b[9:16],2)
  #print(new_message)

     
  elem= (hash_nokia_test(new_message)) %256

  #print ('elem=', elem)
  return elem

def encryp_Nokia_test(elem,frn,pos,clave):
  '''Nokia Real'''
  #clave = 170414 #  0b101001100110101110 18 bits
  frn_format = "032b"
  frn_ = format(frn,frn_format)
  pos_format = "032b"
  pos_ = format(pos,pos_format)
  clave_format = "064b"
  clave_ = format(clave,clave_format)

  #print("FRN: ",frn_)
  #print("POS: ",pos_)
  #print("Clave: ",clave_)

  ###Adaptar la clave
  tam_clave_ideal = 64
  tam_clave = len(bin(clave)[2:])
  trozos_clave = 0
  clave_final = clave_
  #print("la clave mide: ", tam_clave)
  if tam_clave<tam_clave_ideal:
    ##print(clave_)
    #La clave mide menos de 18 bits hay que repetirla n veces
    clave_ = bin(clave)[2:]*(tam_clave_ideal//tam_clave)
    ##print(clave_)
  else:
    if tam_clave > tam_clave_ideal: #Hacer xor
      trozos_clave = tam_clave//tam_clave_ideal
      clave_final = int(clave_[:tam_clave_ideal],2)
      clave_aux = clave_ #quito el 0b
      #print("Como la clave es mayor, la divido en ",trozos_clave, " y hago xor")
      for i in range(1,trozos_clave):# si son 4 lo hago para 1,2 y 3
        clave_aux = clave_[tam_clave_ideal*i:(tam_clave_ideal*i)+tam_clave_ideal]
        ##print("Clave Final: ", clave_final, "\nTam: ",len(clave_final))
        #print("Clave Aux: ", clave_aux, "\nTam: ",len(clave_aux))
        clave_final = clave_final ^ int(clave_aux,2)
      #el ultimo trozo hago xor hasta el final
      clave_aux = clave_[tam_clave_ideal*trozos_clave:(tam_clave_ideal*trozos_clave)+tam_clave_ideal]
      clave_final = clave_final ^ int(clave_aux,2)
      
      clave_ = bin(clave_final)[2:]
    else:
      pass

  #print("Tras adaptar la clave: ", clave_)
  message = frn_ + pos_ + clave_
  #print("Message: ",message)
  #11100110 01000010 10011001 10101110
  new_message = [0,0,0,0]
  '''new_message[0] = int(message[0:8],2)
  new_message[1] = int(message[9:16],2)
  new_message[2] = int(message[17:24],2)
  new_message[3] = int(message[25:32],2)'''
  '''new_message[0] = (message[0:8])
  new_message[1] = (message[9:16])
  new_message[2] = (message[17:24])
  new_message[3] = (message[25:32])'''

  #pseudo transformada de hadamard
  a = int(message[0:64],2)
  b = int(message[65:128],2)
  a = a + b 
  b = a * (2*b)
  new_format = "064b"
  a = format(a,new_format)
  b = format(b,new_format)
  new_message[0] = int(a[0:32],2)
  new_message[1] = int(a[33:64],2)
  new_message[2] = int(b[0:32],2)
  new_message[3] = int(b[33:64],2)
  #print(new_message)

     
  elem= (hash_nokia_test(new_message)) %256

  #print ('elem=', elem)
  return elem

def hash_nokia_test(message):
  '''Hash nokia_ test'''

  #F = '(1) ^ (x1) ^ (x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)
  F = (1) ^ (message[3]) ^ (message[2]) ^ (message[3]&message[1]) ^ (message[2]&message[1]) ^ (message[3]&message[2]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[2]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])
  #F= (message[1] ^ message[0]) | (message[2] ^ message[3])
  resul = F%256
  #resul = message[0]%256
  return resul

def encryp_Nokia_test2 (elem,frn,pos,clave):
  '''Nokia Real'''
  #Establecer tamaño del mensaje en 11 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]
     
  elem= (hash_nokia_test_2(message)) %256

  #print ('elem=', elem)
  return elem

def hash_nokia_test_2(message):
  '''Hash nokia_ test'''
  '''
  Funciones elegidas 2 de 4 vars (max NL y grado) y 2 de 3 vars (max eq y res)
  F:
  {'Tabla verdad': '1111111101111111', 'Minterminos': "(x1'x2'x3'x4') + (x1'x2'x3'x4) + (x1'x2'x3x4') + (x1'x2'x3x4) + (x1'x2x3'x4') + (x1'x2x3'x4) + (x1'x2x3x4') + (x1'x2x3x4) + (x1x2'x3'x4) + (x1x2'x3x4') + (x1x2'x3x4) + (x1x2x3'x4') + (x1x2x3'x4) + (x1x2x3x4') + (x1x2x3x4)", 'FNA': '(1) ^ (x4) ^ (x1&x4) ^ (x2&x4) ^ (x1&x2&x4) ^ (x3&x4) ^ (x1&x3&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)', 'Equilibrio (1s/0s)': '15/1', 'Grado': 4}
  G:
  {'Tabla verdad': '0010000000000000', 'Minterminos': "(x1'x2'x3x4')", 'FNA': '(0) ^ (x2) ^ (x1&x2) ^ (x2&x3) ^ (x1&x2&x3) ^ (x2&x4) ^ (x1&x2&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)', 'Equilibrio (1s/0s)': '1/15', 'Grado': 4}
  H:
  {'Tabla verdad': '01000101', 'Minterminos': "(x1'x2'x3) + (x1x2'x3) + (x1x2x3)", 'FNA': '(0) ^ (x1) ^ (x1&x2) ^ (x1&x2&x3)', 'Equilibrio (1s/0s)': 0.6, 'Grado': 3, 'Resiliencia': 1, 'No linealidad': 1}
  I:
  {'Tabla verdad': '11100101', 'Minterminos': "(x1'x2'x3') + (x1'x2'x3) + (x1'x2x3') + (x1x2'x3) + (x1x2x3)", 'FNA': '(1) ^ (x1&x2) ^ (x3) ^ (x1&x3) ^ (x1&x2&x3)', 'Equilibrio (1s/0s)': 1.6666666666666667, 'Grado': 3, 'Resiliencia': 1, 'No linealidad': 1}
  
  '''

  #F = (message[0]) ^ (message[3]&message[0]) ^ (message[2]&message[0]) ^ (message[3]&message[2]&message[0]) ^ (message[1]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[2]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])
  #G = (message[5]) ^ (message[6]&message[5]) ^ (message[5]&message[4]) ^ (message[6]&message[5]&message[4]) ^ (message[5]&F) ^ (message[6]&message[5]&F) ^ (message[5]&message[4]&F) ^ (message[6]&message[5]&message[4]&F)
  #H = (message[8]) ^ (message[8]&message[7]) ^ (message[8]&message[7]&G)
  #I = (message[10]&message[9]) ^ (H) ^ (message[10]&H) ^ (message[10]&message[9]&H)

  '''
  4 funciones 1 de cada
  F: 4 vars eq y resiliencia
  F de antes  
  G: 4 vars NL y grado
  {'Tabla verdad': '1001111110001001', 'Minterminos': "(x1'x2'x3'x4') + (x1'x2'x3x4) + (x1'x2x3'x4') + (x1'x2x3'x4) + (x1'x2x3x4') + (x1'x2x3x4) + (x1x2'x3'x4') + (x1x2x3'x4') + (x1x2x3x4)", 'FNA': '(1) ^ (x1) ^ (x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)', 'Equilibrio (1s/0s)': 1.2857142857142858, 'Grado': 4, 'Resiliencia': 1, 'No linealidad': 3}
  H: 3 vars eq y res
  {'Tabla verdad': '01100001', 'Minterminos': "(x1'x2'x3) + (x1'x2x3') + (x1x2x3)", 'FNA': '(0) ^ (x1) ^ (x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x3)', 'Equilibrio (1s/0s)': 0.6, 'Grado': 3, 'Resiliencia': 1, 'No linealidad': 1}  
  I: 3 vars NL y grado
  {'Tabla verdad': '01111111', 'Minterminos': "(x1'x2'x3) + (x1'x2x3') + (x1'x2x3) + (x1x2'x3') + (x1x2'x3) + (x1x2x3') + (x1x2x3)", 'FNA': '(0) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x3) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x3)', 'Equilibrio (1s/0s)': 7.0, 'Grado': 3, 'Resiliencia': 1, 'No linealidad': 3}
  '''
  
  F = (1) ^ (message[0]) ^ (message[3]&message[0]) ^ (message[2]&message[0]) ^ (message[3]&message[2]&message[0]) ^ (message[1]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[2]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])
  G = (1) ^ (message[6]) ^ (message[5]) ^ (message[6]&message[4]) ^ (message[5]&message[4]) ^ (message[6]&message[5]&F) ^ (message[6]&message[4]&F) ^ (message[5]&message[4]&F) ^ (message[6]&message[5]&message[4]&F)
  #H = (message[8]) ^ (message[7]) ^ (message[8]&G) ^ (message[7]&G) ^ (message[8]&message[7]&G)
  H = (message[8]) ^ (message[7]) ^ G
  I = (message[9]) ^ (message[10]) ^ (message[9]&message[10]) ^ (H) ^ (message[9]&H) ^ (message[10]&H) ^ (message[9]&message[10]&H)


  resul = I%256
  return resul

def encryp_Nokia_test_64(elem,frn,pos,clave):
  '''Nokia Real'''
  #clave = 170414 #  0b101001100110101110 18 bits
  frn_format = "032b"
  frn_ = format(frn,frn_format)
  pos_format = "064b"
  pos_ = format(pos,pos_format)
  clave_format = "064b"
  clave_ = format(clave,clave_format)

  #print("FRN: ",frn_)
  #print("POS: ",pos_)
  #print("Clave: ",clave_)


  ###Adaptar la pos
  
  '''tam_pos_ideal = 64
  tam_pos = len(bin(pos)[2:])
  trozos_pos = 0
  pos_final = pos_
  print("la pos mide: ", tam_pos)
  if tam_pos<tam_pos_ideal:
    print(pos_)
    #La pos mide menos de 18 bits hay que repetirla n veces
    pos_ = bin(pos)[2:]*(tam_pos_ideal//tam_pos)
    print(pos_)
  else:
    pass

  ###Adaptar la clave
  tam_clave_ideal = 64
  tam_clave = len(bin(clave)[2:])
  trozos_clave = 0
  clave_final = clave_
  #print("la clave mide: ", tam_clave)
  if tam_clave<tam_clave_ideal:
    ##print(clave_)
    #La clave mide menos de 18 bits hay que repetirla n veces
    clave_ = bin(clave)[2:]*(tam_clave_ideal//tam_clave)
    ##print(clave_)
  else:
    if tam_clave > tam_clave_ideal: #Hacer xor
      trozos_clave = tam_clave//tam_clave_ideal
      clave_final = int(clave_[:tam_clave_ideal],2)
      clave_aux = clave_ #quito el 0b
      #print("Como la clave es mayor, la divido en ",trozos_clave, " y hago xor")
      for i in range(1,trozos_clave):# si son 4 lo hago para 1,2 y 3
        clave_aux = clave_[tam_clave_ideal*i:(tam_clave_ideal*i)+tam_clave_ideal]
        ##print("Clave Final: ", clave_final, "\nTam: ",len(clave_final))
        #print("Clave Aux: ", clave_aux, "\nTam: ",len(clave_aux))
        clave_final = clave_final ^ int(clave_aux,2)
      #el ultimo trozo hago xor hasta el final
      clave_aux = clave_[tam_clave_ideal*trozos_clave:(tam_clave_ideal*trozos_clave)+tam_clave_ideal]
      clave_final = clave_final ^ int(clave_aux,2)
      
      clave_ = bin(clave_final)[2:]
    else:
      pass'''

  #print("Tras adaptar la clave: ", clave_)
  message = frn_ + pos_ + clave_
  print(message)

  new_message = [0,0,0,0]

  #pseudo transformada de hadamard
  '''  a = int(message[0:80],2)
  b = int(message[81:160],2)
  a = a + b 
  a = int(message[0:80],2)
  b = a * (2*b)
  #print("a",a)
  #print("b",b)
  a = a%(2**80)
  b = b%(2**80)'''
  print("\n")
  a = message[0:80]
  b = message[81:160]
  print(a,b)
  new_a = ""
  new_b = ""
  for i in range(2):
    pass

  new_format = "080b"
  a = format(a,new_format)
  b = format(b,new_format)
  #print("a",a[0:40],"\t",a[41:80])
  #print("b",b[0:40],"\t",b[41:80])
  #print(a,len(a))
  #print(b,len(b))
  new_message[0] = int(a[0:40],2)
  new_message[1] = int(a[41:80],2)
  new_message[2] = int(b[0:40],2)
  new_message[3] = int(b[41:80],2)
  #print(new_message)

     
  elem = (hash_nokia_test_64(new_message)) %256

  #print ('elem=', elem)
  return elem

def hash_nokia_test_64(message):
  '''Hash nokia_ test'''

  #F = '(1) ^ (x1) ^ (x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)
  F = (1) ^ (message[3]) ^ (message[2]) ^ (message[3]&message[1]) ^ (message[2]&message[1]) ^ (message[3]&message[2]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[2]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])
  #F= (message[1] ^ message[0]) | (message[2] ^ message[3])
  resul = F%256
  #resul = message[0]%256
  return resul

def encryp_Nokia_test_mix(elem,frn,pos,clave):
  '''Nokia Real'''
  #cadena_total = bin(frn)[2:]+bin(pos)[2:]+bin(clave)[2:]
  #cadena_total = bin(frn)[2:]+bin(clave)[2:]+bin(pos)[2:]
  cadena_total = bin(pos)[2:]+bin(frn)[2:]+bin(clave)[2:]
  #print(cadena_total, len(cadena_total))
  while len(cadena_total) < 160:
    cadena_total+=cadena_total
    #junto todos sin 0b, y los repito n veces
  cadena_total = cadena_total[0:160]

  #Pseudo transformada
  a = int(cadena_total[0:80],2)
  b = int(cadena_total[81:160],2)
  a = a+b
  #a = int(cadena_total[0:80],2)
  b = a+(2*b) 

  #a = a%(2**80)
  #b = b%(2**80)
  new_format = "080b"
  a = format(a,new_format)
  b = format(b,new_format)
  new_message = [0,0,0,0]
  new_message[0] = int(a[0:40],2)
  new_message[1] = int(a[41:80],2)
  new_message[2] = int(b[0:40],2)
  new_message[3] = int(b[41:80],2)
     
  elem = (hash_nokia_test_mix(new_message)) %256

  #print ('elem=', elem)
  return elem

def hash_nokia_test_mix(message):
  '''Hash nokia_ test'''

  #F = '(1) ^ (x1) ^ (x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)
  F = (1) ^ (message[3]) ^ (message[2]) ^ (message[3]&message[1]) ^ (message[2]&message[1]) ^ (message[3]&message[2]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[2]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])
  #F= (message[1] ^ message[0]) | (message[2] ^ message[3])
  resul = F%256
  #resul = message[0]%256
  return resul


####DEFINITIVOS


def encryp_Nokia_test_hex(elem,frn,pos,clave):
  '''Nokia Real'''
  #cadena_total = bin(frn)[2:]+bin(pos)[2:]+bin(clave)[2:]
  #cadena_total = bin(frn)[2:]+bin(clave)[2:]+bin(pos)[2:]
  cadena_total = bin(pos)[2:]+bin(frn)[2:]+bin(clave)[2:]
  #print(cadena_total, len(cadena_total))
  while len(cadena_total) < 160:
    cadena_total+=cadena_total
    #junto todos sin 0b, y los repito n veces
  cadena_total = cadena_total[0:160]

  a = int(cadena_total[0:80],2)
  b = int(cadena_total[81:160],2)

  #Transformacion lineal
  a = a+b
  b = a+(2*b) 

  a = hex(a)[2:]
  b = hex(b)[2:]
  len_a = len(a)
  if len_a == 21: #10bytes + 10bytes puede dar 11bytes, en este caso se ha quedado medio byte y python no pone el 0
    a = "0"+a
  len_b = len(b)
  if len_b == 21: #10bytes + 10bytes puede dar 11bytes, en este caso se ha quedado medio byte y python no pone el 0
    b = "0"+b
  #print(a)
  #print(b)
  new_message = [0,0,0,0]
  new_message[0] = a[0:10]
  new_message[1] = a[10:20]
  new_message[2] = b[0:10]
  new_message[3] = b[10:20]
  #print(new_message)
  #for i in new_message:
  # print(len(i))

  new_message[0] = int(a[0:10],16)
  new_message[1] = int(a[10:20],16)
  new_message[2] = int(b[0:10],16)
  new_message[3] = int(b[10:20],16)
  #print(new_message)
     
  elem = (hash_nokia_test_mix(new_message)) %256

  #print ('elem=', elem)
  return elem

def hash_nokia_test_hex(message):
  '''Hash nokia_ test'''
  '''{'Tabla verdad': '1000110000011101', 
  'Minterminos': "(x1'x2'x3'x4') + (x1'x2x3'x4') + (x1'x2x3'x4) + (x1x2'x3x4) + (x1x2x3'x4') + (x1x2x3'x4) + (x1x2x3x4)", 
  'FNA': '(1) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x1&x3) ^ (x1&x2&x3) ^ (x4) ^ (x1&x4) ^ (x2&x4) ^ (x3&x4) ^ (x1&x3&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)', 
  'Equilibrio (1s/0s)': 0.7777777777777778, 
  'Grado': 4, 'Resiliencia': 1, 'No linealidad': 5}'''

  #F = (0xFF) ^ (message[3]) ^ (message[2]) ^ (message[3]&message[2]) ^ (message[3]&message[1]) ^ (message[3]&message[2]&message[1]) ^ (message[0]) ^ (message[3]&message[0]) ^ (message[2]&message[0]) ^ (message[1]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[2]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])

  #F = '(1) ^ (x1) ^ (x2) ^ (x1&x3) ^ (x2&x3) ^ (x1&x2&x4) ^ (x1&x3&x4) ^ (x2&x3&x4) ^ (x1&x2&x3&x4)
  
  #ESTE ES EL QUE USO
  #F = (0xFF) ^ (message[3]) ^ (message[2]) ^ (message[3]&message[1]) ^ (message[2]&message[1]) ^ (message[3]&message[2]&message[0]) ^ (message[3]&message[1]&message[0]) ^ (message[2]&message[1]&message[0]) ^ (message[3]&message[2]&message[1]&message[0])
  #SIN CONFUSIÓN
  #F= (message[3] ^ message[2] ^ message[1] ^ message[0])
  F = message[2]
  resul = F%256
  #resul = message[0]%256
  return resul


def encryp_Uva_bin (elem,frn,pos,clave):
  '''Uva Real or bit'''
  #Establecer tamaño del mensaje en 11 bytes, tanto si es mayor como si es menor
  message = str(frn) + str(pos) + str(clave)
 

  if len(message) > 33:
      sep = [message[i:i+33] for i in range(0,len(message), 33)]
         
      message=sep[0]
 
      for i in message:
          message = int(message) ^ int(sep[i])  
          message = str(message)

  else:
      while len(message) < 33:
          dif= 33 - len(message)
          m= message [0:dif]
          message= message + m
      
  
  #Formar lista de 11 números (bloques) %256
  message= [message[i:i+3] for i in range(0,len(message), 3)]
  message= [int(message[i])%256 for i in range(0,len(message))]
     
  elem= (hash_uva_bin(message)) %256

  #print ('elem=', elem)
  return elem

def hash_uva_bin (message):
  '''F,G = (0)^(x1)^(x2)^(x3)^(x1&x3)^(x2&x3)^(x4)^(x1&x4)^(x2&x4)
  H = (0) ^ (x1) ^ (x2) ^ (x3)
  I = (0) ^ (x1) ^ (x2) ^ (x1&x2) ^ (x3)
  '''

  
  '''F= (message[1] & message[0]) | (~(message[2]) & message[3])
  G= (F & message[4]) | (message[5] & ~(message[6]))
  H= (G ^ message[7] ^ message[8])
  I = (H ^ (message[9] | message[10]))'''

  #PARA PROBAR SIN CONFUSION
  #F= message[10] ^ message[9] ^ message[8] ^ message[7] ^ message[6] ^ message[5] ^ message[4] ^ message[3] ^ message[2] ^ message[1] ^ message[0]    
  F = message[7]
  

  #hash = I % 256
  resul = F%256

  #return hash
  return resul