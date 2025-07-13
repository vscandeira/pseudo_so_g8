#Simula os 1024 blocos de memória.
#64 fixos para tempo real.
#960 para usuários.
#Verifica disponibilidade, faz alocação contígua.

class GerenciadorMemoria:
    def __init__(self):
        self.memoria = [0] * 1024

    def alocar(self, processo):
        pass

    def liberar(self, processo):
        pass
