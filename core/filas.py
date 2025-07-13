#Estrutura das 4 filas: tempo real (FIFO), usuário (3 níveis, com aging e quantum).
#Política de escalonamento.

class Escalonador:
    def __init__(self):
        self.fila_tempo_real = []
        self.fila_usr_p1 = []
        self.fila_usr_p2 = []
        self.fila_usr_p3 = []
        self.filas_usr = [self.fila_usr_p1, self.fila_usr_p2, self.fila_usr_p3]
        self.fila_pronto = [self.fila_tempo_real, self.filas_usr]
        self.quantum = 1
        self.aging = 5 

    def adicionar_processo(self, processo):
        if processo.prioridade == 0:
            self.fila_tempo_real.append(processo)
        elif processo.prioridade == 1:
            self.fila_usr_p1.append(processo)
        elif processo.prioridade == 2:
            self.fila_usr_p2.append(processo)
        elif processo.prioridade == 3:
            self.fila_usr_p3.append(processo)

    def proximo_processo(self):
        if self.fila_tempo_real:
            return self.fila_tempo_real.pop(0)
        for fila in self.filas_usr:
            if fila:
                return fila.pop(0)
        return None

    def tempo_autorizado(self, processo):
        # Processos Real-Time (prioridade 0) usam todo o tempo de CPU restante sem preempção
        if processo.prioridade == 0:
            return processo.tempo_cpu
        # Demais processos usam o quantum definido
        else:
            return self.quantum

    def aplicar_aging(self, processo):
        if processo.prioridade > 0 and processo.executado >= self.aging:
            processo.executado = 0
            processo.prioridade = 3 if processo.prioridade>2 else processo.prioridade+1 
        return processo