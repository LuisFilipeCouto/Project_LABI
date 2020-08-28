######################################################################
########## NOTAS IMPORTANTES PARA O FUNCIONAMENTO DO CÓDIGO ##########
######################################################################

# 1 --> É MUITO IMPORTANTE que o utilizador tenha "pycryptodome" (versão melhorada do PyCrypto) pois o código tem métodos que só funcionam com este pacote
# 2 --> Para um pais com 2 ou mais nomes, o input tem de ser efetuado entre aspas --> "Russian Federation" ou "United States"
# 3 --> Para correr o cliente, correr na consola:  python3 client.py interval num [country or id]

######################################################################
import sys
import os
import json
import csv
from random import *
import socket
import time
import datetime
import math
import re
from Crypto.Hash import SHA3_512 # NECESSÁRIO TER INSTALADO PYCRYPTODOME
from Crypto.PublicKey import RSA # NECESSÁRIO TER INSTALADO PYCRYPTODOME
from Crypto.Signature import pss # NECESSÁRIO TER INSTALADO PYCRYPTODOME
from base64 import b64encode, b64decode  # NECESSÁRIO TER INSTALADO PYCRYPTODOME


# MAPEAR OS ERROS POSSIVEIS
error_list = {
		1: "Escreva no formato: python3 client.py interval num [country or id]",
		2: "Valor do argumento deve ser inteiro positivo",
		3: "Argumento do tipo errado, deve ser do tipo integer",
		4: "Country não existe na lista",
		5: "ID não existe na lista"
	}
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA VALIDAR O NÚMERO DE ARGUMENTOS
def validateArgs(totalArgs):
	if (totalArgs < 4):
		return 1
	return 0
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA VERIFICAR SE O INPUT É UM INTEIRO POSITIVO
def isInteger(value):  
	try:               
		int(value) # Tenta converter a variável (value) para inteiro
		if(value <= "0"): # Se (value) for inteiro mas não for positivo
			return 2
		else: # Se a variável (value) for inteiro e positivo
			return 0
	except ValueError: # Se não for possível converter a variável (value) para inteiro, obtemos este erro
		return 3
		
# A função isdigit() considera um input "-10" como inválido pois toma "-" como uma string, logo recebia o erro "Argumento do tipo errado".
# Contudo, quero considerar "-10" como inválido e receber o erro "Valor do argumento deve ser inteiro positivo".
# Logo vou usar um try...except, que me permite converter "-10" para um inteiro negativo e receber o erro "Valor do argumento deve ser inteiro positivo"
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA VERIFICAR SE EXISTE ALGUM SERVIDOR COM ID == INPUT [ID] 
def validateIDExist(id, file):
	for x in file["servers"]:
		if (int(x["id"])==int(id)):
			return 0
	return 5
#-----------------------------------------------------------------------------------------------------------------------------------------

	
# FUNÇÃO VERIFICAR SE EXISTE ALGUM SERVIDOR COM COUNTRY == INPUT [COUNTRY] 
def validateCountryExist(country, file):
	for x in file["servers"]:
		if (x["country"]==country):
			return 0
	return 4
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO IMPRIMIR UMA MENSAGEM COM O RESPETIVO ERRO
def printError(error_num):	
	return error_list.get(error_num, "Unknown Error")# Se não for nenhum dos erros mapeados, dá return de "Unknown Error"
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA OBTER O HOST ATRAVES DO INPUT [ID]
def getHostByID(id, file):
	for x in file["servers"]:
		if (int(x["id"])==int(id)):
			return x["host"]
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA OBTER O HOST ATRAVES DO INPUT [COUNTRY]
def getHostByCountry(country,file):
	count=0;
	index=0;
	for x in file["servers"]: 
		if(x["country"]==country): # Ver quantas vezes é que um [country] se repete
			count=count+1; #contar quantos servers em que o país == country

	# Obter um servidor random de um país
	rnd = randint(1, count+1); #random entre 1 e o numero de servidores com países == country que existem.
	for x in file["servers"]:
		if (x["country"]==country):
			index = index+1 # iterar por cada país  == country
			if (index == rnd): # quando index do país == rnd ==> return host
				return x["host"]
#-----------------------------------------------------------------------------------------------------------------------------------------


# OBTER O ID DO SERVIDOR ATRAVES DO HOST
def getIDbyHost(host,file):
	for x in file["servers"]:
		if ((x["host"])==host):
			return x["id"]
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA ENVIAR MENSAGEM "HI\n" E RECEBER DE VOLTA "HELLO VERSAO DE SOFTWARE DATA HORA DO SERVIDOR"
def sendHi(host,port):
	TCP_IP = host;
	TCP_PORT = int(port);
	BUFFER_SIZE = 4096;
	MESSAGE = "HI\n";
	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		s.connect((TCP_IP, TCP_PORT));
		s.send(MESSAGE.encode());
		data = s.recv(BUFFER_SIZE);
		s.close();

	except socket.timeout as e: # Caso ocorra um erro e não seja possível conectar ao servidor 
		return("COMANDO HI: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e)+"\n") # Imprimir erro ;	

	except socket.error as e: # Caso ocorra um erro e não seja possível conectar ao servidor 
		return("COMANDO HI: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e)+"\n") # Imprimir erro ;

	except OverflowError as e: # Se, por exmeplo, a porta indicada não seja um valor entre 0-65535
		return("COMANDO HI: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e)+"\n") # Imprimir erro ;

	else:
		return data.decode()
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA CALCULAR A LATÊNCIA
def sendPing(host,port,timestamp):
	TCP_IP = host;
	TCP_PORT = int(port);
	BUFFER_SIZE = 4096;
	MESSAGE = "PING "+str(timestamp)+"\n"; # timestamp é o tempo actual, obtido usando o módulo time (time.time()) na função main

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
		s.connect((TCP_IP, TCP_PORT))
		tmp_lat_sum = 0 # Somatório das latencias de todos os pings

		for i in range(1,11): # Realizar 10 transações PING/PONG
			time_start = time.time()*1000; # Multiplicar por 1000 para termos o tempo em milisegundos

			s.send(MESSAGE.encode('utf-8'));
			data = s.recv(BUFFER_SIZE);

			time_end = time.time()*1000; # Multiplicar por 1000 para termos o tempo em milisegundos
		
			tmp_lat = abs(time_end - time_start); # Latência de cada iteração (por cada PING mandado)

			tmp_lat_sum += tmp_lat; # Somar os valores obtidos para cada transação PING/PONG

		s.close();	

		v_latencia = (tmp_lat_sum)/10 # Calcular a média dos valores obtidos e por fim obter a latẽncia

		latencia = (math.ceil(v_latencia*1000)/1000) # Arredondar para 3 casas decimais

	except socket.timeout as e:
		print("COMANDO DOWNLOAD: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e)) 
		return -1; 	

	except socket.error as e: # Caso ocorra um erro e não seja possível conectar ao servidor 
		print("COMANDO PING: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e)) # Imprimir erro
		return -1;

	except OverflowError as e: # Se, por exmeplo, a porta indicada não seja um valor entre 0-65535
		print("COMANDO PING: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e))
		return -1;	

	else:
		return latencia	
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA CALCULAR A LARGURA DE BANDA
def sendDownload(host,port): 
	size = randint(10000000,100000000) # Descarga entre 10MB e 100MB, logo geramos aleatoriamente um numero neste intervalo
	TCP_IP = host;
	TCP_PORT = int(port);
	BUFFER_SIZE = 4096;
	MESSAGE = "DOWNLOAD "+str(size)+"\n";

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((TCP_IP, TCP_PORT))

		tempo_inicial = time.time()
		tempo_final = tempo_inicial + 10 # Acabar ao fim de 10 segundos

		banda_total = 0
		banda_inicial = 0

		while(time.time() <= tempo_final): 
			
			s.send(MESSAGE.encode("utf-8"));
			data = s.recv(BUFFER_SIZE)
			
			while (banda_total <= 1000000): # Enquanto não for feito um download de 1MB
				tempo_inicial_banda = time.time() # Tempo inicial vai actualizar ate ser feito um download de 1MB, após isso mantem-se o mesmo
				banda_inicial += len(data.decode("utf-8")) # Vamos usar esta banda para subtrair a banda total, para termos o numero total de MB descarregados apos 1 MB
				break
				

			if (size==0): # Se for pedido um download de 0 bytes, consideramos que a largura de banda é 0;
				return 0;
				break

			if not data:
				return 0;
				break	

			banda_total += len(data.decode("utf-8")) # Como fazemos download por pacotes, incrementamos cada pacote. Damos decode para puder usar a funçao len
		s.close()

		banda = banda_total - banda_inicial # Numero de octetos recebidos após ter sido feito download de 1 MB

		tempo_total = tempo_final - tempo_inicial_banda # Calcular o tempo decorrido após ter sido feito  download de 1 MB

		banda_MB = banda * 0.000001; # Calcular o número de Megabytes(MB) que foram descarregados

		taxa_banda_MB = banda_MB / tempo_total # Obter taxa de banda em Megabytes por Segundo

		v_taxa_banda = (taxa_banda_MB)*8 #  Converter MB/s para Mbps (Megabytes por Segundo para Megabits por Segundo)

		taxa_banda = (math.ceil(v_taxa_banda*1000)/1000) # Arredondar para 3 casas decimais
	
	except socket.timeout as e:
		print("COMANDO DOWNLOAD: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e)) 
		return 0; # Taxa de banda toma o valor 0

	except socket.error as e: # Caso ocorra um erro e não seja possível conectar ao servidor 
		print("COMANDO DOWNLOAD: Não foi possível conectar ao servidor, tipo de erro associado: " + str(e)) 
		return 0; # Taxa de banda toma o valor 0

	except OverflowError as e: # Caso a porta indicada não seja um valor entre 0-65535
		print("COMANDO DOWNLOAD: Não foi possível conectar ao servidor --> tipo de erro associado: " + str(e))
		return 0; # Taxa de banda toma o valor 0

	else:   
		return taxa_banda   
#----------------------------------------------------------------------------------------------------------------------------------------- 


# FUNÇÃO PARA CALCULAR A SÍNTESE DOS CAMPOS (JÁ CONCATENADOS E SEM SEPARADORES)
def getSintese(check): 
	try: 
		chave = SHA3_512.new() # Vou usar SHA3_512 pois é das mais seguras
		chave.update(check.encode('utf-8')) 
		sintese = chave.hexdigest()

	except TypeError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))	
		sys.exit(1)

	except ValueError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1)

	except AttributeError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1)

	except NameError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1) 

	else:
		return sintese
#-----------------------------------------------------------------------------------------------------------------------------------------


# FUNÇÃO PARA CALCULAR A SÍNTESE DE UM FICHEIRO COMPLETO
def getFileSintese(filename):
	try: 
		chave  = SHA3_512.new();
		ficheiro = open( filename, "rb" )
		buffer = ficheiro.readline()
		chave.update(buffer)

		while len(buffer) > 0:
			buffer = ficheiro.readline()

			chave.update(buffer)

		sintese = chave.hexdigest()	

	except OSError as e: 
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1)

	except TypeError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))	
		sys.exit(1)

	except ValueError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1)

	except AttributeError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1)

	except NameError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1) 

	else: 
		return sintese	
#-----------------------------------------------------------------------------------------------------------------------------------------



################################################################# FUNÇÃO MAIN ############################################################


def main(argv):	

# DEFINIR AS VARIÁVEIS NECESSÁRIAS
	v_totalArgs = len(sys.argv)
	v_interval = sys.argv[1]
	v_num = sys.argv[2]
	v_country = "" # Um país pode ter um nome (Portugal) ou vários (Russian Federation), por isso, por agora, considero como uma string vazia
	v_country_id = -1 # Um ID pode variar em comprimento (i.g 17228 ou 4231), por isso, por agora, considero como -1
#-----------------------------------------------------------------------------------------------------------------------------------------


# VALIDAR O NÚMERO DE ARGUMENTOS
	validation = validateArgs(v_totalArgs)
	if (validation != 0):
		print (printError(validation));
		sys.exit(0)
#----------------------------------------------------------------------------------------------------------------------------------------


# VALIDAR O TIPO DE ARGUMENTOS INTRODUZIDOS PELO UTILIZADOR
	validation = isInteger(v_interval) # Validar o argumento [interval] 
	if (validation > 0):
		print ("Erro no argumento [interval]: " + printError(validation));

	validation = isInteger(v_num) # Validar o argumento [num]
	if (validation != 0):
		print ("Erro no argumento [num]: " + printError(validation));
		sys.exit(0)
#-----------------------------------------------------------------------------------------------------------------------------------------


# VERIFICAR SE O ARGUMENTO FOI DO TIPO INPUT [ID] OU DO TIPO INPUT [COUNTRY] 
	if (v_totalArgs > 4): # Se forem introduzidos mais que 4 argumentos, significa que temos um input [country] com 2 ou mais strings
		for x in range(3,v_totalArgs): 
			v_country+= sys.argv[x]+" " # Concatenar todos os argumentos para a variável (v_country) para obter o nome completo do país a procurar
	
	if (v_totalArgs == 4): # Se forem introduzidos 4 argumentos, significa que temos um input [country] ou um input [id]
		if(sys.argv[3].isdigit()): # Verificar se argv[3] é uma string(country) ou um inteiro (id)
			v_country_id = sys.argv[3]; # Se for inteiro, significa que é input [id], logo vamos popular a variável (v_country_id)
		else:
			v_country = sys.argv[3]; # Se for string, significa que é input [country], logo vamos popular a variável (v_country)
#-----------------------------------------------------------------------------------------------------------------------------------------


# ABRIR FICHEIRO SERVERS.JSON
	try: # Tentar abrir o ficheiro, se existir algum problema, imprimir erro e sair
		with open("servers.json") as f:
			file = json.load(f)
	except OSError as e: 
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1)
#-----------------------------------------------------------------------------------------------------------------------------------------


# VERIFICAR SE O INPUT [ID] OU O INPUT [COUNTRY] EXISTEM NO FICHEIRO JSON
	if(int(v_country_id)>-1): # Se (v_country_id > 1), significa que o input foi um [id]
		validation = validateIDExist(v_country_id,file) # Verificar se o id existe 
		if(validation != 0):
			print("Erro no argumento [id]: " + printError(validation));
			sys.exit(0);
	else: # Se o input for um [country]
		validation = validateCountryExist(v_country, file) # Verificar se o país existe
		if(validation != 0):
			print("Erro no argumento [country]: " + printError(validation));
			sys.exit(0);
#-----------------------------------------------------------------------------------------------------------------------------------------


# OBTER O HOST DO SERVIDOR
	if(int(v_country_id)>-1): # Temos um input do tipo [id]
		v_url = getHostByID(v_country_id,file) # Procurar host por [id]
	else: # Temos um input do tipo [country]
		v_url = getHostByCountry(v_country,file) # Procurar host por [country]
#-----------------------------------------------------------------------------------------------------------------------------------------


# OBTER O URL E A PORTA PARA LIGAR AO SERVIDOR
	v_tmp = v_url.split(":") # Temos um HOST do tipo "speedtest4.xj.chinamobile.com:8080", separamos por ":" para obter o URL e a porta
	v_host = v_tmp[0]
	v_port = v_tmp[1]
	print("\n" +"TESTE DE INTERNET PARA O HOST: " + str(v_url)) # Indicar qual o servidor que está a ser testado
#-----------------------------------------------------------------------------------------------------------------------------------------


# OBTER O ID DO SERVIDOR 
	if(int(v_country_id)>-1): # Se tivermos um input do tipo [id])
		v_id_server = v_country_id # O id do servidor é o id introduzido
	else:	
		v_id_server = getIDbyHost(v_url,file) # Obter o id atraves do host do servidor
#-----------------------------------------------------------------------------------------------------------------------------------------


# CORRER OS TESTES [NUM] VEZES COM UM INTERVALO DE [INTERVAL] SEGUNDOS
	v_numero_testes = int(v_num)+1 # Por exemplo, se queremos fazer 10 testes, temos de ter range(1,11) pois nao itera o ultimo numero
	v_tempo_espera = int(v_interval) # Tempo de espera entre cada teste


	# CRIAR E ESCEVER FIELDNAMES DO FICHEIRO REPORT.CSV
	fout = open("report.csv", "w")
	writer = csv.DictWriter(fout, fieldnames=['contador', 'id', 'data ISO', 'latência','largura de banda', 'check'], delimiter=',') 
	writer.writeheader()

	for i in range(1, v_numero_testes): 
		print("----------------------------------------------------------------------------")
		print("TESTE NÚMERO: " + str(i)+"\n")


		# OBTER O NUMERO DO TESTE ACTUAL
		v_contador = i;
		#-----------------------------------------------------------------------------------------------------------------------------------------


		# OBTER O ID DO SERVIDOR 
		v_id = v_id_server;
		#-----------------------------------------------------------------------------------------------------------------------------------------
		

		# OBTER A DATA NO FORMATO ISO
		v_data_actual = datetime.datetime.now(datetime.timezone(datetime.timedelta(seconds=time.localtime().tm_gmtoff))).replace(microsecond=0).isoformat()
		print("DATA ACTUAL: " + str(v_data_actual) + "\n");
		#-----------------------------------------------------------------------------------------------------------------------------------------


		# ENVIAR A MENSAGEM ["HI\n"]
		v_get_hi = sendHi(v_host,v_port);
		print(v_get_hi);
		#-----------------------------------------------------------------------------------------------------------------------------------------


		# OBTER A LATÊNCIA DA COMUNICAÇÃO
		v_timestamp = int((time.time()*1000));
		v_get_ping = sendPing(v_host, v_port, v_timestamp)
		print("VALOR DA LATÊNCIA AO FIM DE 10 TRANSAÇÕES PING/PONG: " + str(v_get_ping) + " ms" + "\n")
		#-----------------------------------------------------------------------------------------------------------------------------------------


		# OBTER A LARGURA DA BANDA
		v_get_download = sendDownload(v_host, v_port)
		print("VALOR DA LARGURA DE BANDA: " + str(v_get_download) + " Mbits/s" + "\n")
		#-----------------------------------------------------------------------------------------------------------------------------------------
 

		# OBTER A SINTESE (CHECK)
		v_tmp_check1 = str(v_contador)+str(v_id)+v_data_actual+str(v_get_ping)+str(v_get_download) # Concatenar todos os campos

		v_tmp_check2 = re.sub(r'\W+', '', v_tmp_check1) # \W remove tudo except letras, numeros e "_" logo vou remover "_" separadamente
		v_check = re.sub("|".join('_'), "", v_tmp_check2) # Caso existam "_", remover
		v_sintese = getSintese(v_check)

		print("SÍNTESE: " + str(v_sintese))
		print("----------------------------------------------------------------------------")
		#------------------------------------------------------------------------------------------------------------------------------------------ 


		# ESCREVER OS CAMPOS NO FICHEIRO REPORT.CSV
		v_data = {'contador': v_contador, 'id' : v_id , 'data ISO' : v_data_actual, 'latência' : v_get_ping, 'largura de banda' : v_get_download, 'check' : v_sintese}
		writer.writerow(v_data)
		fout.flush()
		#-----------------------------------------------------------------------------------------------------------------------------------------


		if(i < (v_numero_testes-1)): # Para não imprimir esta mensagem após o ultimo teste acabar
			print("###### Intervalo de " + str(v_tempo_espera) + " segundos até ao próximo teste ######")
		
		time.sleep(v_tempo_espera) # Tempo de espera entre cada teste

	fout.close() # FECHAR FICHEIRO REPORT.CSV
	#-----------------------------------------------------------------------------------------------------------------------------------------


# CRIAR O FICHEIRO KEY.PRIV QUE CONTEM A CHAVE PRIVADA RSA ---> CASO NÃO SEJA PRECISO GERAR ESTE FICHEIRO, COMENTAR ESTE BLOCO DE CODIGO
	v_keypair = RSA.generate(2048)

	v_key = "LABI" # Chave para abrir o ficheiro key.priv

	fich_rsa = open( "key.priv", "wb" )

	v_kp = v_keypair.exportKey("PEM", v_key )

	fich_rsa.write(v_kp)

	fich_rsa.close()
#-----------------------------------------------------------------------------------------------------------------------------------------


# ABRIR O FICHEIRO QUE CONTEM A CHAVE PRIVADA E USAR ESSA CHAVE PARA CRIAR AO FICHEIRO REPORT.SIG COM A ASSINATURA DO FICHEIRO REPORT.CSV
	try: 
		v_key_fich = open("key.priv", "r").read() 

		v_data = getFileSintese("report.csv")

		v_key_rsa = RSA.importKey(v_key_fich,v_key) 

		v_signer = pss.new(v_key_rsa) # PSS vai dar sempre uma assinatura diferente, mesmo que seja para o mesmo conjunto de dados

		v_digest = SHA3_512.new() # Usamos SHA3_512 pois é das mais seguras

		v_digest.update(b64decode(v_data)) # Assume-se que os dados estão codificados em base64 por isso damos decode antes do digest

		v_sign = v_signer.sign(v_digest) 

		print("\n" + "ASSINATURA DO FICHEIRO REPORT.CSV: " + "\n" + str(b64encode(v_sign))) # Fazer: "str((v_sign)))" se quiser imprimir assinatura não codificada


		# ESCEVER O FICHEIRO REPORT.SIG
		f = open("report.sig", "wb")
		f.write((b64encode(v_sign))) # Fazer: "f.write((v_sign)))" se quiser assinatura não codificada
		f.close()

	except OSError as e: 
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1) 

	except TypeError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1) 

	except ValueError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1) 

	except AttributeError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1) 

	except NameError as e:
		print("Erro na linha {},".format(sys.exc_info()[-1].tb_lineno) + " do tipo: " + str(e))
		sys.exit(1)    
#-----------------------------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
	main(sys.argv)

