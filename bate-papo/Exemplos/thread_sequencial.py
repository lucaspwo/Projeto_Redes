# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Thread com execucao sequencial
#

# importacao das bibliotecas
import threading # threads
import time # tempo (opcional)
 
# define uma classe para a criacao de threads
class minhaThread (threading.Thread):
    # redefine a funcao __init__ para aceitar a passagem parametros de entrada
    def __init__(self, threadID, threadName, threadCounter):
        threading.Thread.__init__(self)
        self.id = threadID
        self.name = threadName
        self.counter = threadCounter
    # a funcao run() e executada por padrao por cada thread 
    def run(self):
        # aviso de inicio da thread
        print "Iniciando Thread %d [%s] com %d tarefas" % (self.id, self.name, self.counter)
        # faz lock (bloqueio) para sincronizar a thread
        threadLock.acquire()
        # chama a funcao a ser executada por cada thread
        executa_tarefa(self.id, self.name, self.counter)
        # aviso de que a thread terminou de executar suas tarefas
        print "\nFim da Thread %d [%s]" % (self.id, self.name)
        # libera o bloqueio para proxima thread
        threadLock.release()

# funcao a ser chamada por cada thread em execucao       
def executa_tarefa(id, name, counter):
    while counter:
        time.sleep(2) # atraso em cada thread
        print "\nThread %d [%s] executando a tarefa %d em %s" % (id, name, counter, time.ctime(time.time()))
        counter -= 1
        
# faz bloqueio da thread principal
threadLock = threading.Lock()
 
# criando duas threads
# a classe minhaThread() recebe: identificador da thread, nome da thread, numero de processos
thread1 = minhaThread (1, "Alice", 4)
thread2 = minhaThread (2, "Bob", 4)
 
# disparando as threads
thread1.start()
thread2.start()
 
# criacao de uma lista de threads
threadList = []
threadList.append(thread1)
threadList.append(thread2)
 
# executando o join() em cada uma das threads na lista de threads
for t in threadList:
    t.join() # quando ha bloqueio, uma thread so e executada quando a outra terminar