# Project_LABI

### About the project
A python [TCP client](codigo/client.py) that establishes a connection with a [Speedtest Server](codigo/servers.json), chosen randomly or by the user, and calculates and presents comprehensive details about the internet connection on the console for each test, while simultaneously saving this information in a CSV file <br>
Using RSA cryptosystem, an accompanying signature file, containing the hash (SHA3-512) of the previously obtained CSV file, is generated <br>
The client's constituent functions have been verified through unit testing. These tests can be observed by executing the corresponding [test file](codigo/test_unitario_funcoes.py)

### Detailed description/usage
Read the project report -> [**TrabalhoAP2.pdf**](relatorio/TrabalhoAP2.pdf)

To install necessary dependencies (assuming you are in the base directory):
```
cd codigo
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
```

To test the program:
```
python3 client.py 1 2 14450              # connect to the server with ID 14450 and perform 2 tests with a 1s interval between them
python3 client.py 2 4 Italy              # connect to a random server in Italy and perform 4 tests with a 2s interval between them
python3 client.py 5 3 "United States"    # connect to a random server in the US and perform 3 tests with a 5s interval between them
```


