# Simula os 1024 blocos de memória.
# 64 fixos para tempo real.
# 960 para usuários.
# Verifica disponibilidade, faz alocação contígua.
from core.processos import Processo


class MemoryOverflowError(Exception):
    """Exceção para estouro de memória."""

    pass


class GerenciadorMemoria:
    """
    Gerencia a alocação e liberação de memória para processos no pseudo-SO.
    A memória é um conjunto de blocos contíguos, sem paginação ou memória virtual.
    """

    def __init__(self):
        self.memoria = [-1] * 1024

        self.BLOCO_INICIO_TR = 0
        self.BLOCO_FIM_TR = 63

        self.BLOCO_INICIO_USUARIO = 64
        self.BLOCO_FIM_USUARIO = 1023

    def _encontrar_bloco_contiguo(self, inicio_busca: int, fim_busca: int, tamanho_necessario: int) -> int:
        """
        Busca um endereço livre para alocação
        """
        bloco_livre_atual = 0
        bloco_candidato = -1

        for i in range(inicio_busca, fim_busca + 1):
            if self.memoria[i] == -1:
                if bloco_livre_atual == 0:
                    bloco_candidato = i
                bloco_livre_atual += 1
                if bloco_livre_atual == tamanho_necessario:
                    return bloco_candidato
            else:
                bloco_livre_atual = 0
                bloco_candidato = -1
        return -1

    def alocar(self, processo: Processo, printar=False) -> bool:
        """
        Aloca memória para um processo.
        Se um processo de tempo real não encontrar espaço em sua região,
        ele buscará na região de usuário.
        """
        endereco = -1

        if processo.prioridade == 0:
            if processo.blocos_mem > (self.BLOCO_FIM_TR - self.BLOCO_INICIO_TR + 1):
                raise MemoryOverflowError("Processo de tempo real não tem blocos suficientes para alocação.")
            endereco = self._encontrar_bloco_contiguo(self.BLOCO_INICIO_TR, self.BLOCO_FIM_TR, processo.blocos_mem)
        else:
            if processo.blocos_mem > (self.BLOCO_FIM_USUARIO - self.BLOCO_INICIO_USUARIO + 1):
                raise MemoryOverflowError("Processo de usuário não tem blocos suficientes para alocação.")
            endereco = self._encontrar_bloco_contiguo(
                self.BLOCO_INICIO_USUARIO, self.BLOCO_FIM_USUARIO, processo.blocos_mem
            )

        if endereco != -1:
            for i in range(endereco, endereco + processo.blocos_mem):
                self.memoria[i] = processo.pid

            processo.offset = endereco
            if printar:
                self.print_mapa_ocupacao()
            return True
        else:
            if printar:
                self.print_mapa_ocupacao()
            return False

    def liberar(self, processo: Processo) -> None:
        """
        Libera memória alocada para um processo.
        """
        if processo.offset is not None:
            for i in range(processo.offset, processo.offset + processo.blocos_mem):
                if 0 <= i < len(self.memoria):
                    self.memoria[i] = -1

            processo.offset = None

    def print_mapa_ocupacao(self) -> None:
        """
        Imprime o mapa de ocupação da memória.
        """
        print("Ocupação da memória =>")
        i = 0
        while i <= self.BLOCO_FIM_USUARIO:
            proc = self.memoria[i]
            j = i + 1
            while j <= self.BLOCO_FIM_USUARIO:
                if self.memoria[j] != proc:
                    break
                else:
                    j += 1
            if proc == -1:
                print(f"\tBlocos {i}-{j - 1}: Livre")
            else:
                print(f"\tBlocos {i}-{j - 1}: Processo {proc}")
            i = j
        print()
