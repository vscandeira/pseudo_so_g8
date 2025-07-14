from core.filas import Escalonador
from core.memoria import GerenciadorMemoria
from core.recursos import GerenciadorRecursos
from core.arquivos import GerenciadorArquivos

class SistemaOperacional:
    def __init__(self, processos, operacoes_arquivos):
        self.escalonador = Escalonador()
        self.memoria = GerenciadorMemoria()
        self.recursos = GerenciadorRecursos()
        self.arquivos = GerenciadorArquivos()
        self.processos = processos
        self.operacoes_arquivos = operacoes_arquivos
        self.executando = None
        self.tempo = 0

    def executar(self):
        # ?. Alocar memória e recursos
        # ?. Aplicar operações em arquivos
        # ?. Imprimir saída
        ha_novos_processos = True
        fila_vazia = True
        # Loop de execução do despachante
        while(True):
            # 0. Debug tempo
            print("Tempo:", self.tempo, "ms")
            # 1. Inserir processos nas filas do tempo t
            prov_list_proc_time = [p for p in self.processos if p.inicio <= self.tempo]
            self.processos = [p for p in self.processos if p.inicio > self.tempo]
            if prov_list_proc_time:
                for p in prov_list_proc_time:
                    self.escalonador.adicionar_processo(p)
                    fila_vazia = False
            if not self.processos:
                ha_novos_processos = False
            # 2. Escolhe o próximo processo da fila de pronto
            self.executando = self.escalonador.proximo_processo()
            # 3. Executar processos
            if self.executando is None:
                exec_cpu = 1
            else:
                exec_cpu = self.escalonador.tempo_autorizado(self.executando)
                self.executando.executar_processo(exec_cpu)
                # 3.1. Devolve processo à fila de pronto se ainda tiver tempo de CPU restante
                if self.executando.tempo_cpu > 0:
                    self.executando = self.escalonador.aplicar_aging(self.executando)
                    self.escalonador.adicionar_processo(self.executando)
                    fila_vazia = False
            self.tempo += exec_cpu
            if (not self.escalonador.fila_pronto[0]) and all(not sub for sub in self.escalonador.fila_pronto[1]):
                fila_vazia = True
            if (not ha_novos_processos) and (fila_vazia):
                break
        # Debug tempo
        print("Tempo final:", self.tempo, "ms")