import threading
import re
import socket, os
import sys

global conectado
global clientes

class cliente(object):  #classe que vai guardar o socket, o nick e o endereco
    def __init__(self,client_connection,nick,address):
        self.client_socket = client_connection
        self.nick = nick
        self.address = address

class recebeMsgCliente (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self,Cl):
        threading.Thread.__init__(self)
        #self.serverSocket = serverSocket
        self.client = Cl
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        global clientes
        #ouvir o que o servidor vai mandar e imprimir em tela
        print self.client.nick, 'entrou'
        # envia para todos os clientes: <nick> entrou
        thread_enviar1 = enviaMsgCliente(self.client,self.client.nick+' entrou',self.client.nick)
        thread_enviar1.start()
        global conectado
        # conectado = True
        while conectado:
            msg = self.client.client_socket.recv(2048)
            if msg == 'sair()':
                self.client.client_socket.close()
                conectado = False
                print self.client.nick, 'saiu'
                for i in clientes:
                    if i.client_socket == self.client.client_socket:
                        clientes.remove(i)
            elif msg == 'lista()':
                lista = 'Lista de usuarios:' + '\n'
                if clientes != []:
                    for i in clientes:
                        lista = lista + str(i.nick) + '\n'
                    thread_enviar2 = enviaMsgCliente(self.client,lista,self.client.nick)
                    thread_enviar2.start()
                        # print lista
                else:
                    print 'vazio'
            else:
                print self.client.nick, 'escreveu: ', msg

            # thread para enviar a mensagem recebida para todos os clientes
            thread_enviar = enviaMsgCliente(self.client,self.client.nick + ' escreveu: ' + msg,self.client.nick)
            thread_enviar.start()

class enviaMsgCliente(threading.Thread):
    def __init__(self,cl,mensagem,nome):
        threading.Thread.__init__(self)
        self.client = Cl
        self.msg = mensagem
        self.nick = nome
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        global clientes
        #percorre a lista global de clientes e envia a mensagem para todos
        #menos para quem escreveu a mensagem
        if self.msg != 'sair()':
            for i in clientes:
                if i.nick != self.nick:
                    i.client_socket.send(self.msg)
        else self.msg 

class fechaServidor (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self):
        threading.Thread.__init__(self)
    # a funcao run() e executada por padrao por cada thread
    def run(self):
        #se o servidor mandar sair() envia para todos os clientes
        #e fecha a conexao
        msg = raw_input()
        if msg == 'sair()':
            if clientes != []:
                for i in clientes:
                    # print 'i = ' + str(i)
                    # i.client_socket.send('Servidor fechou')
                    i.client_socket.send(msg)
                    i.client_socket.close()
                    global conectado
                    conectado = False
            listen_socket.close()
            sys.exit(1)
        elif msg == 'lista()':
            if clientes != []:
                for i in clientes:
                    print '('+str(i.nick)+','+str(i.address[0])+','+str(i.address[1])+')'


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

    #armazenar na lista de clientes a conexao que foi estabelecida
    Cl = cliente(client_connection,nome,client_address)
    clientes.append(Cl)

    #crie a thread de receber mensagens de cada cliente
    thread1 = recebeMsgCliente(Cl)
    thread1.start()

    #crie a thead para enviar as mensagens para os clientes
    thread2 = fechaServidor()
    thread2.start()


    #crie uma thread para o servidor digitar as mensagens para cada cliente