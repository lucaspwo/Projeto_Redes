# UNIVERSIDADE FEDERAL DO RIO GRANDE DO NORTE
# DEPARTAMENTO DE ENGENHARIA DE COMPUTACAO E AUTOMACAO
# DISCIPLINA REDES DE COMPUTADORES (DCA0113)
# AUTOR: PROF. CARLOS M D VIEGAS (viegas 'at' dca.ufrn.br)
#
# SCRIPT: Exemplo simples de thread
#

# importacao das bibliotecas
import time # tempo (opcional)
from random import randint # numeros aleatorios (opcional)
from threading import Thread # thread

# funcao a ser executada por cada threads
def minhaFuncao(i):
    # gera um tempo aleatorio no qual cada thread ira dormir
    sono = randint(1,10)
    print "Thread %d: dormindo por %d segundos" % (i, sono)
    time.sleep(sono)
    print "Thread %d: fim do sono" % (i)

n_threads = 10 # quantidade de threads a serem disparadas
print "Disparando %d threads..." %(n_threads)
time.sleep(2)
    
for i in range(1, n_threads+1):
    # disparando as threads
    t = Thread(target=minhaFuncao, args=(i,))
    t.start()