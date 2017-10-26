import threading
import re
import socket, os

global conectado

class recebeMsgCliente (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self,client_connection,nick):
        threading.Thread.__init__(self)
        #self.serverSocket = serverSocket
        self.client_connection = client_connection
        self.nick = nick
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        #ouvir o que o servidor vai mandar e imprimir em tela
        print self.nick, 'entrou'
        global conectado
        conectado = True
        while conectado:
            msg = self.client_connection.recv(2048)
            print self.nick, 'escreveu: ', msg
            if msg == 'sair()':
                self.client_connection.close()
                conectado = False
                print self.nick, 'saiu'


class enviaMsgCliente (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self,client_connection,nick):
        threading.Thread.__init__(self)
        #self.serverSocket = serverSocket
        self.client_connection = client_connection
        self.nick = nick
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        global conectado
        #ouvir o que o servidor vai mandar e imprimir em tela
        conectado = True
        while conectado:
            msg = raw_input()
            if msg == 'sair()':
                self.client_connection.send(msg)
                self.client_connection.close()
                conectado = False


HOST = '' # ip do servidor (em branco)
PORT = 12000 # porta do servidor
SERVER = 'bate-papo'

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

print 'Servidor aguardando conexoes na porta %s ...' % PORT
conectado = True
while conectado == True:
    client_connection, client_address = listen_socket.accept()
    nick = client_connection.recv(2048)
    #fazendo o tratamento para obter o nome do cliente
    nome = re.sub('nome\(','',nick)
    nome = re.sub('\)','',nome)
    #crie a thread de receber mensagens de cada cliente
    thread1 = recebeMsgCliente(client_connection,nome)
    thread1.start()
    #crie a thead para enviar as mensagens para os clientes
    thread2 = enviaMsgCliente(client_connection,nome)
    thread2.start()


    #crie uma thread para o servidor digitar as mensagens para cada cliente