# 1 scanner, 2 impressoras, 1 modem, 2 discos SATA.
# Implementa semáforos ou locks.
from core.processos import Processo


class GerenciadorRecursos:
    def __init__(self):
        self.scanner = -1
        self.impressoras = [-1, -1]
        self.modem = -1
        self.sata = [-1, -1]

    def _alocar(self, recurso: str, processo: Processo) -> tuple[bool, str]:
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
            if self.impressoras[processo.impressora]:
                self.impressoras[processo.impressora] = processo.pid
                return True, f"impressora_{processo.impressora}"
        elif recurso == "sata":
            if self.sata[processo.sata]:
                self.sata[processo.sata] = processo.pid
                return True, f"sata_{processo.sata}"
        return False, None

    def alocar(self, processo: Processo) -> bool:
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
            return True

        alocacoes = {}

        for recurso in recursos_solicitados:
            sucesso, identificador = self._alocar(recurso, processo)
            if sucesso:
                alocacoes[recurso] = identificador
            else:
                self._rollback_alocacao(processo.pid, alocacoes)
                return False

        return True

    def _rollback_alocacao(self, processo_pid: int, recursos_alocados_temp: dict[str, str]) -> None:
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
                idx = int(identificador.split("_")[1])
                if self.impressoras[idx] == processo_pid:
                    self.impressoras[idx] = -1
            elif recurso_tipo == "sata":
                idx = int(identificador.split("_")[1])
                if self.sata[idx] == processo_pid:
                    self.sata[idx] = -1

    def liberar(self, processo: Processo) -> None:
        """
        Libera os recursos de E/S previamente alocados por um processo.
        """
        if processo.scanner:
            if self.scanner == processo.pid:
                self.scanner = -1
        if processo.impressora is not None:
            if self.impressoras[processo.impressora] == processo.pid:
                self.impressoras[processo.impressora] = -1
        if processo.modem:
            if self.modem == processo.pid:
                self.modem = -1
        if processo.sata is not None:
            if self.sata[processo.sata] == processo.pid:
                self.sata[processo.sata] = -1
