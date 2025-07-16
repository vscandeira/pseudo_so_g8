from typing import Tuple, Dict
from core.processos import Processo

class UnknownResourceError(Exception):
    """Exceção para códigos de recurso inválidos."""
    pass


class GerenciadorRecursos:
    def __init__(self):
        self.scanner = -1
        self.impressoras = [-1, -1]
        self.modem = -1
        self.sata = [-1, -1]

    def _alocar(self, recurso: str, processo: Processo) -> Tuple[bool, str]:
        """
        Tenta alocar um recurso específico.
        Retorna True e o nome do recurso alocado se bem-sucedido, False caso contrário.
        """
        if recurso == "scanner":
            if self.scanner == -1:
                self.scanner = processo.pid
                return True, "scanner"
        elif recurso == "modem":
            if self.modem == -1:
                self.modem = processo.pid
                return True, "modem"
        elif recurso == "impressora":
            if processo.impressora not in (1, 2):
                raise UnknownResourceError(f"Código de impressora ({processo.impressora}) inválido.")
            if self.impressoras[processo.impressora - 1]:
                self.impressoras[processo.impressora - 1] = processo.pid
                return True, f"impressora_{processo.impressora}"
        elif recurso == "sata":
            if processo.sata not in (1, 2):
                raise UnknownResourceError(f"Código de dispositivo SATA ({processo.sata}) inválido.")
            if self.sata[processo.sata - 1]:
                self.sata[processo.sata - 1] = processo.pid
                return True, f"sata_{processo.sata}"
        return False, None

    def alocar(self, processo: Processo, printar = False) -> bool:
        """
        Aloca os recursos de um processo
        """
        recursos_solicitados = []
        if processo.scanner:
            recursos_solicitados.append("scanner")
        if processo.impressora:
            recursos_solicitados.append("impressora")
        if processo.modem:
            recursos_solicitados.append("modem")
        if processo.sata:
            recursos_solicitados.append("sata")

        if not recursos_solicitados:
            if printar:
                self.print_aloc_recursos()
            return True

        alocacoes = {}

        for recurso in recursos_solicitados:
            sucesso, identificador = self._alocar(recurso, processo)
            if sucesso:
                alocacoes[recurso] = identificador
            else:
                self._rollback_alocacao(processo.pid, alocacoes)
                if printar:
                    self.print_aloc_recursos()
                return False

        if printar:
            self.print_aloc_recursos()
        return True

    def _rollback_alocacao(self, processo_pid: int, recursos_alocados_temp: Dict[str, str]) -> None:
        """
        Libera os recursos que foram alocados em uma tentativa falha de alocação.
        """
        for recurso_tipo, identificador in recursos_alocados_temp.items():
            if recurso_tipo == "scanner":
                if self.scanner == processo_pid:
                    self.scanner = -1
            elif recurso_tipo == "modem":
                if self.modem == processo_pid:
                    self.modem = -1
            elif recurso_tipo == "impressora":
                idx = int(identificador.split("_")[1]) - 1
                if self.impressoras[idx] == processo_pid:
                    self.impressoras[idx] = -1
            elif recurso_tipo == "sata":
                idx = int(identificador.split("_")[1]) - 1
                if self.sata[idx] == processo_pid:
                    self.sata[idx] = -1

    def liberar(self, processo: Processo, printar = False) -> None:
        """
        Libera os recursos de E/S previamente alocados por um processo.
        """
        if processo.scanner:
            if self.scanner == processo.pid:
                self.scanner = -1
        if processo.impressora:
            if processo.impressora in (1, 2) and self.impressoras[processo.impressora - 1] == processo.pid:
                self.impressoras[processo.impressora - 1] = -1
        if processo.modem:
            if self.modem == processo.pid:
                self.modem = -1
        if processo.sata:
            if processo.sata in (1, 2) and self.sata[processo.sata - 1] == processo.pid:
                self.sata[processo.sata - 1] = -1
        if printar:
            self.print_aloc_recursos()

    
    def print_aloc_recursos(self) -> None:
        """
        Imprime o estado atual dos recursos alocados.
        """
        print("Gerenciador de recursos =>")
        print(f"\tScanner: {'Ocupado' if self.scanner != -1 else 'Livre'}")
        print(f"\tImpressoras: {[f'Ocupada por {pid}' if pid != -1 else 'Livre' for pid in self.impressoras]}")
        print(f"\tModem: {'Ocupado' if self.modem != -1 else 'Livre'}")
        print(f"\tSATA: {[f'Ocupada por {pid}' if pid != -1 else 'Livre' for pid in self.sata]}")
        print()
