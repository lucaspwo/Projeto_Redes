import threading
import re
import socket, os

class cliente(object):
    def __init__(self,client_connection,nick,address):
        self.client_socket = client_connection
        self.nick = nick
        self.address = address


HOST = '' # ip do servidor (em branco)
PORT = 12000 # porta do servidor
SERVER = 'bate-papo'

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))

# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

clientes = []

print 'Servidor aguardando conexoes na porta %s ...' % PORT
conectado = True
while conectado == True:
    client_connection, client_address = listen_socket.accept()
    nick = client_connection.recv(2048)
    #fazendo o tratamento para obter o nome do cliente
    nome = re.sub('nome\(','',nick)
    nome = re.sub('\)','',nome)

    Cl = cliente(client_connection,nome,client_address)
    clientes.append(Cl)
    C2 = clientes[0]

    #print Cl
    print C2.client_socket,' ',C2.nick,' ',C2.address