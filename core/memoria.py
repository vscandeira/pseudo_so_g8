# Simula os 1024 blocos de memória.
# 64 fixos para tempo real.
# 960 para usuários.
# Verifica disponibilidade, faz alocação contígua.
from core.processos import Processo


class GerenciadorMemoria:
    """
    Gerencia a alocação e liberação de memória para processos no pseudo-SO.
    A memória é um conjunto de blocos contíguos, sem paginação ou memória virtual.
    """

    def __init__(self):
        self.memoria = [0] * 1024

        self.BLOCO_INICIO_TR = 0
        self.BLOCO_FIM_TR = 63

        self.BLOCO_INICIO_USUARIO = 64
        self.BLOCO_FIM_USUARIO = 1023

    def _encontrar_bloco_contiguo(self, inicio_busca: int, fim_busca: int, tamanho_necessario: int) -> int:
        bloco_livre_atual = 0
        bloco_candidato = -1

        for i in range(inicio_busca, fim_busca + 1):
            if self.memoria[i] == 0:
                if bloco_livre_atual == 0:
                    bloco_candidato = i
                bloco_livre_atual += 1
                if bloco_livre_atual == tamanho_necessario:
                    return bloco_candidato
            else:
                bloco_livre_atual = 0
                bloco_candidato = -1
        return -1

    def alocar(self, processo: Processo) -> bool:
        """
        Aloca memória para um processo.
        """
        endereco = -1

        if processo.prioridade == 0:
            endereco = self._encontrar_bloco_contiguo(self.BLOCO_INICIO_TR, self.BLOCO_FIM_TR, processo.blocos_mem)
        else:
            endereco = self._encontrar_bloco_contiguo(
                self.BLOCO_INICIO_USUARIO, self.BLOCO_FIM_USUARIO, processo.blocos_mem
            )

        if endereco != -1:
            for i in range(endereco, endereco + processo.blocos_mem):
                self.memoria[i] = processo.pid

            processo.inicio = endereco
            return True
        else:
            return False

    def liberar(self, processo: Processo) -> None:
        """
        Libera memória alocada para um processo.
        """
        if processo.inicio is not None:
            for i in range(processo.inicio, processo.inicio + processo.blocos_mem):
                if 0 <= i < len(self.memoria):
                    self.memoria[i] = 0

            processo.inicio = None
