#1 scanner, 2 impressoras, 1 modem, 2 discos SATA.
#Implementa semáforos ou locks.

class GerenciadorRecursos:
    def __init__(self):
        self.scanner = False
        self.impressoras = [False, False]
        self.modem = False
        self.sata = [False, False]

    def alocar(self, processo):
        pass

    def liberar(self, processo):
        pass
