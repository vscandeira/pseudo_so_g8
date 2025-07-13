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

    def executar(self):
        # Loop principal de despache
        # 1. Inserir processos nas filas
        # 2. Alocar memória e recursos
        # 3. Executar processos
        # 4. Aplicar operações em arquivos
        # 5. Imprimir saída
        pass
