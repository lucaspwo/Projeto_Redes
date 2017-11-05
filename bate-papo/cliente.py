import threading
from socket import *
import sys

global conectado
conectado = True
class recebeMsg (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self,clientSocket):
        threading.Thread.__init__(self)
        self.client_Socket = clientSocket
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        global conectado
        #ouvir o que o servidor vai mandar e imprimir em tela
        while conectado == True:
            msg = self.client_Socket.recv(2048)
            # print msg
            if msg == 'sair()':
                conectado = False
                clientSocket.close()
                sys.exit(1)
            else:
                print msg





#Parte principal
serverName = '127.0.0.1' #inserir o ip do servidor
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

sentence = raw_input('Insira o nickname que deseja: ')
clientSocket.send('nome('+sentence+')')
#criar a thread de escuta
thread = recebeMsg (clientSocket)
thread.start()

while conectado == True:
    #Parte para enviar as mensagens
    sentence = raw_input()
    clientSocket.send(sentence)
    if sentence == 'sair()':
        conectado = False
        clientSocket.close()
        break
# clientSocket.close()