import pytest
import client
import json
from Crypto.Hash import SHA3_512 # NECESSÁRIO TER INSTALADO PYCRYPTODOME

#########################################################################################################

# É MUITO IMPORTANTE que o utilizador tenha "pycryptodome" (versão melhorada do PyCrypto) pois o código tem métodos que só funcionam com este pacote
# Ter em atenção que no ficheiro "client.py", as funçoes aqui testadas têm os seguintes valores de return:
# 
#		0 ---> que significa que não houve erro e o código continua a executar normalmente
#		1 ---> que significa "Escreva no formato: python3 client.py interval num [country or id]",
#		2 ---> que significa "Valor do argumento deve ser inteiro positivo",
#		3 ---> que significa "Argumento do tipo errado, deve ser do tipo integer",
#		4 ---> que significa "Country não existe na lista",
#		5 ---> que significa "ID não existe na lista"
#
# Apenas os numeros 1, 2, 3, 4, 5 estão mapeados como erros
#
##########################################################################################################


# Testar a função "validateArgs"
def test_validateArgs():
	print("Teste da função validateArgs")

	# Simular sys.argv com menos de 4 elementos
	a = ["a", "b", "c"] 
	a_lenght = len(a) # sys.argv com 3 elementos

	# Simular sys.argv com 4 elementos
	b = ["a", "b", "c", "d"] 
	b_lenght = len(b) # sys.argv com 4 elementos

	# Simular sys.argv com mais 4 elementos
	c = ["a", "b", "c", "d", "e"] 
	c_lenght = len(c) # sys.argv com 5 elementos

	assert client.validateArgs(a_lenght) == 1  	# Testar sys.argv com 3 elementos ---> Tem de ser 1
	assert client.validateArgs(b_lenght) == 0	# Testar sys.argv com 4 elementos ---> Tem de ser 0
	assert client.validateArgs(c_lenght) == 0	# Testar sys.argv com 5 elementos ---> Tem de ser 0
##########################################################################################################


# Testar a função "isInteger"
def test_isInteger():
	print("Teste de validação da função isInteger")

	a = "y"
	b = '+'
	c = "-1"
	d = "0"
	e = "10"

	assert client.isInteger(a) == 3 	# Quando são strings --------------------> Função da return de 3
	assert client.isInteger(b) == 3    	# Quando são caracteres -----------------> Função da return de 3
	assert client.isInteger(c) == 2 	# Quando são inteiros negativos ---------> Função da return de 2
	assert client.isInteger(d) == 2		# Quando é o número 0 -------------------> Função da return de 2
	assert client.isInteger(e) == 0		# Quando são inteiros positivos ---------> Função da return de 0
##########################################################################################################


# Testar a função "printError"
def test_printError():
	print("Teste de validação da função printError")

	a = 1 
	b = 2 
	c = 3
	d = 4
	e = 5
	f = 312312 # Qualquer número que não esteja mapeado
	g = "rewrwerwe" # Qualquer tipo que não esteja mapeado

# Mensagem de erro equivalente a cada número estão descritas no inicio deste ficheiro

	assert client.printError(a) == "Escreva no formato: python3 client.py interval num [country or id]"
	assert client.printError(b) == "Valor do argumento deve ser inteiro positivo"
	assert client.printError(c) == "Argumento do tipo errado, deve ser do tipo integer"
	assert client.printError(d) == "Country não existe na lista"
	assert client.printError(e) == "ID não existe na lista"
	assert client.printError(f) == "Unknown Error" # Para erros não mapeados, a funçao tem return de "Unknown Error"
	assert client.printError(g) == "Unknown Error" # Para erros não mapeados, a funçao tem return de "Unknown Error"
###############################################################################################################################################################################


# Testar a função "validateIDExist"
def test_validateIDExist():
	print("Teste de validação da função validateIDExist")

	with open("servers.json") as f:
			file = json.load(f) # Ficheiro onde se encontram os servidores

	id_1 = 17228    # ID EXISTENTE, verificado anteriormente de modo a servir como controlo
	id_2 = 34131523 # ID NÃO EXISTENTE, verificado anteriormente de modo a servir como controlo

	assert client.validateIDExist(id_1,file) == 0 # Quando o ID introduzido existe -------> Função da return de 0
	assert client.validateIDExist(id_2,file) == 5 # Quando o ID introduzido não existe ---> Função da return de 5
###############################################################################################################################################################################


# Testar a função "validateCountryExist"
def test_validateCountryExist():
	print("Teste de validação da função validateCountryExist")

	with open("servers.json") as f:
			file = json.load(f) # Ficheiro onde se encontram os servidores

	country_1 = "Portugal" 			 # País com 1 nome EXISTENTE, verificado anteriormente de modo a servir como controlo
	country_2 = "Russian Federation" # País com varios nomes EXISTENTE, verificado anteriormente de modo a servir como controlo
	country_3 = "PaisImaginário" 	 # País com 1 nome NÃO EXISTENTE, verificado anteriormente de modo a servir como controlo
	country_4 = "Pais Imaginário"    # País com varios nomes NÃO EXISTENTE, verificado anteriormente de modo a servir como controlo

	assert client.validateCountryExist(country_1,file) == 0 # O país introduzido existe -------> Tem de ser 0
	assert client.validateCountryExist(country_2,file) == 0 # O país introduzido existe--------> Tem de ser 0
	assert client.validateCountryExist(country_3,file) == 4 # O páis introduzido não existe ---> Tem de ser 4
	assert client.validateCountryExist(country_4,file) == 4 # O páis introduzido não existe ---> Tem de ser 4
###############################################################################################################################################################################



# Testar a função "getHostByID"
def test_getHostByID():
	print("Teste de validação da função getHostByID")

	with open("servers.json") as f:
			file = json.load(f) # Ficheiro onde se encontram os servidores

	# Vou usar 3 IDs como controlo, sendo que sei que 2 deles correspondem a um host e outro não corresponde a nenhum host	

	id_1 = 1902 	   # ID pertencente ao host "speedtest-po.vodafone.pt:8080"
	id_2 = 10014       # ID pertencente ao host "speed1.globalforway.com:8080"
	id_3 = 3423742384  # ID não pertence a nenhum host

	assert client.getHostByID(id_1,file) == "speedtest-po.vodafone.pt:8080" # ID corresponde a este host
	assert client.getHostByID(id_2,file) == "speed1.globalforway.com:8080"  # ID corresponde a este host 
	assert client.getHostByID(id_3,file) == None # Quando o ID não corresponde a nenhum host, a função não tem return
###############################################################################################################################################################################


# Testar a função "getIDbyHost"
def test_getIDbyHost():
	print("Teste de validação da função getIDbyHost")

	with open("servers.json") as f:
			file = json.load(f) # Ficheiro onde se encontram os servidores

	# Vou usar 2 IDs e 2 hosts que verifiquei e tenho a certeza que são correspondentes um ao outro		

	host_1 = "speedtest-po.vodafone.pt:8080" # Host pertencente ao ID 1902
	host_2 = "speed1.globalforway.com:8080"  # Host pertencente ao ID 10014
	host_3 = "www.17aLABIPORFAVOR"           # Host não existente
	
	assert client.getIDbyHost(host_1,file) == 1902   # Host corresponde a este ID
	assert client.getIDbyHost(host_2,file) == 10014  # Host corresponde a este ID 
	assert client.getIDbyHost(host_3,file) == None   # Quando o host não existe, a função não tem return
###############################################################################################################################################################################


# Testar a função "getSintese"
def test_getSintese():
	print("Teste de validação da função getSintese")

	# Vou usar 2 checks onde sei, à partida, qual será a sua síntese resultante (existem ferramentas online para calcular SHA3_512)
	check_1 = "12345olaOLA"
	check_2 = "LABI2019" 

	assert client.getSintese(check_1) == "8ace8c4face9f6413fba0df34673e0660d1c96dc64b1abab3b9e53a79ddf73c415dc85301dfa53d65f617df78102d5b52ff9a724c0d2454e276999502c933994"
	assert client.getSintese(check_2 ) == "b5e5aa85e6d2c051fa07c336ea95b32fc5b7a9022797169d750d7ccacf432ffbdce3d390769136b50615047a614a38aa0d7be9f8a45a897f69656d27add0ea10"
	assert len(client.getSintese(check_1)) == 128 # O comprimento de um output de SHA3_512 tem de ser 128 caracteres
	assert len(client.getSintese(check_2)) == 128 # O comprimento de um output de SHA3_512 tem de ser 128 caracteres
###############################################################################################################################################################################


# Testar a função "getFileSintese"
def test_getFileSintese():
	print("Teste de validação da função getFileSintese")

	# Vou usar o ficheiro "servers.json" original que, como é fornecido pelos professores e nunca vai ser ser alterado, vai ter sempre a mesma hash (obtida por ferramenta online para usar como controlo)
	file = "servers.json" 

	assert client.getFileSintese(file) == "339a7fec102d696127934092e305d9b245d6125c72fa5f17171607076e16325b54769906f3ad048f3de2ffc091c8d15ce74883e555850a52eab899fb79fd4599"
	assert len(client.getFileSintese(file)) == 128 # O comprimento de um output de SHA3_512 tem de ser 128 caracteres
###############################################################################################################################################################################	
