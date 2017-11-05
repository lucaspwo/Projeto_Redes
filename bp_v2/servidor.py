import threading, socket, os, sys, re

HOST = '' # ip do servidor (em branco)
PORT = 12000 # porta do servidor
SERVER = 'bate-papo'

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
# vincula o socket com a porta (faz o "bind" do IP do servidor com a porta)
listen_socket.bind((HOST, PORT))
listen_socket.setblocking(False)
# "escuta" pedidos na porta do socket do servidor
listen_socket.listen(1)

print 'Servidor aguardando conexoes na porta %s ...' % PORT

global conectado
conectado = True

class recebeMsgCliente(threading.Thread):
    def __init__(self,clientes,chave):
        threading.Thread.__init__(self)
        self.clientes = clientes
        self.chave = chave
    def run(self):
        privado = False
        pvtChave = ()
        print self.clientes[self.chave]['nick'], 'entrou'
        thread_enviaEntrou = enviaMsgCliente(self.clientes,self.clientes[self.chave]['nick']+' entrou',self.chave)
        thread_enviaEntrou.start()
        conectado = True
        while conectado:
            if self.chave in self.clientes:
                try:
                    msg = self.clientes[self.chave]['socket'].recv(2048)
                    if msg == 'sair()':
                        self.clientes[self.chave]['socket'].close()
                        conectado = False
                        print self.clientes[self.chave]['nick'], 'saiu'
                        thread_enviarMsgSaiu = enviaMsgCliente(self.clientes,self.clientes[self.chave]['nick'] + ' saiu',self.chave)
                        thread_enviarMsgSaiu.start()
                        for i in self.clientes.keys():
                            if self.clientes[i] == self.clientes[self.chave]:
                                del self.clientes[i]
                                break
                    elif msg == 'lista()':
                        lista = 'Servidor escreveu: Clientes conectados: '
                        for i in self.clientes.keys():
                            lista = lista + self.clientes[i]['nick'] + '\t'
                        self.clientes[self.chave]['socket'].send(lista)
                    elif msg[:5] == 'nome(':
                        nvNome = re.sub('nome\(','',msg)
                        nvNome = re.sub('\)','',nvNome)
                        oldNome = self.clientes[self.chave]['nick']
                        self.clientes[self.chave]['nick'] = nvNome
                        print oldNome + ' agora e ' + self.clientes[self.chave]['nick']
                        thread_enviarMsgNvNome = enviaMsgCliente(self.clientes,oldNome + ' agora e ' + self.clientes[self.chave]['nick'], self.chave)
                        thread_enviarMsgNvNome.start()
                    elif msg[:8] == 'privado(':
                        pvtNome = re.sub('privado\(','',msg)
                        pvtNome = re.sub('\)','',pvtNome)
                        for i in self.clientes.keys():
                            if pvtNome == self.clientes[i]['nick']:
                                pvtChave = i
                        print self.clientes[self.chave]['nick'] + ' pediu para participar de chat privado com ' + self.clientes[pvtChave]['nick']
                        self.clientes[pvtChave]['socket'].send('Servidor escreveu: ' + self.clientes[self.chave]['nick'] + ' deseja iniciar uma conversa privada.\nEnvie \'aceito('+ self.clientes[self.chave]['nick'] +')\' para aceitar ou \'rejeito('+ self.clientes[self.chave]['nick'] +')\' para recusar o convite')
                    elif msg[:7] == 'aceito(':
                        privado = True
                        pvtNome = re.sub('aceito\(','',msg)
                        pvtNome = re.sub('\)','',pvtNome)
                        for i in self.clientes.keys():
                            if pvtNome == self.clientes[i]['nick']:
                                pvtChave = i
                        print self.clientes[self.chave]['nick'] + ' esta numa conversa privada com ' + self.clientes[pvtChave]['nick']
                        self.clientes[self.chave]['socket'].send('Servidor escreveu: Voce entrou na conversa privada.\nEnvie \'rejeito('+ self.clientes[pvtChave]['nick'] +')\' para sair')
                        self.clientes[pvtChave]['socket'].send('priv=1')
                        self.clientes[pvtChave]['socket'].send('Servidor escreveu: ' + self.clientes[self.chave]['nick'] + ' aceitou seu pedido')
                    elif msg[:8] == 'rejeito(':
                        if privado == True:
                            privado = False
                            print self.clientes[self.chave]['nick'] + ' nao esta mais em uma conversa privada'
                            self.clientes[self.chave]['socket'].send('Servidor escreveu: Voce saiu da conversa privada')
                            self.clientes[pvtChave]['socket'].send('Servidor escreveu: ' + self.clientes[self.chave]['nick'] + ' pediu para sair da conversa privada')
                            self.clientes[pvtChave]['socket'].send('priv=0')
                        elif privado == False:
                            pvtNome = re.sub('rejeito\(','',msg)
                            pvtNome = re.sub('\)','',pvtNome)
                            for i in self.clientes.keys():
                                if pvtNome == self.clientes[i]['nick']:
                                    pvtChave = i
                            self.clientes[pvtChave]['socket'].send('Servidor escreveu: ' + self.clientes[self.chave]['nick'] + ' recusou seu pedido')
                    elif msg == 'priv=1':
                        privado = True
                    elif msg == 'priv=0':
                        privado = False
                    elif msg != '':
                        print self.clientes[self.chave]['nick'], 'escreveu:', msg
                        if privado == False:
                            thread_enviarMsgClientes = enviaMsgCliente(self.clientes,self.clientes[self.chave]['nick'] + ' escreveu: ' + msg,self.chave)
                            thread_enviarMsgClientes.start()
                        elif privado == True:
                            self.clientes[pvtChave]['socket'].send(self.clientes[self.chave]['nick'] + ' escreveu em chat privado: ' + msg)

                except:
                    if self.chave not in self.clientes:
                        conectado = False
                        break
            else:
                conectado = False
                break

class enviaMsgCliente(threading.Thread):
    def __init__(self,clientes,mensagem,chave):
        threading.Thread.__init__(self)
        self.clientes = clientes
        self.msg = mensagem
        self.chave = chave
    def run(self):
        if self.msg == 'lista()':
            print 'Nada a fazer aqui'
        else:
            if bool(self.clientes) == True:
                for i in self.clientes.keys():
                    if i != self.chave:
                        self.clientes[i]['socket'].send(self.msg)
            else:
                print 'Servidor vazio. Ninguem para enviar mensagem'

class servidor(threading.Thread):
    def __init__(self,clientes):
        threading.Thread.__init__(self)
        self.clientes = clientes
    def run(self):
        global conectado
        while conectado:
            msg = raw_input()
            if msg == 'sair()':
                print 'Fechando o servidor'
                if bool(self.clientes) == True:
                    for i in self.clientes.keys():
                        self.clientes[i]['socket'].send(msg)
                        self.clientes[i]['socket'].close()
                        print self.clientes[i]['nick'], 'saiu'
                        del self.clientes[i]
                listen_socket.close()
                conectado = False
                # sys.exit(1)
            elif msg == 'lista()':
                if bool(self.clientes) == True:
                    for i in self.clientes.keys():
                        print '('+self.clientes[i]['nick']+','+self.clientes[i]['ip']+','+self.clientes[i]['porta']+')'
                else:
                    print 'Servidor vazio'

clientes = {}

#crie a thread para o servidor
threadServ = servidor(clientes)
threadServ.start()

conn = False

while conectado:
    try:
        client_connection, client_address = listen_socket.accept()
        conn = True
        # print 'Conn = ', conn
    except:
        if conn == True:
            nick = client_connection.recv(2048)
            #fazendo o tratamento para obter o nome do cliente
            nome = re.sub('nome\(','',nick)
            nome = re.sub('\)','',nome)
            #armazenar no dicionario de clientes as informacoes da conexao
            clientes.update({client_address:{'ip':str(client_address[0]), 'porta':str(client_address[1]), 'nick':nome, 'socket':client_connection}})
            client_connection.send('Servidor escreveu: Voce esta conectado')
            #crie a thread de receber mensagens de cada cliente
            threadRecebe = recebeMsgCliente(clientes,client_address)
            threadRecebe.start()
            conn = False