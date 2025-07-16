import pytest
from core.recursos import GerenciadorRecursos

class Processo:
    def __init__(self, pid, scanner=0, impressora=0, modem=0, sata=0):
        self.pid = pid
        self.scanner = scanner
        self.impressora = impressora
        self.modem = modem
        self.sata = sata

@pytest.fixture
def gerenciador():
    return GerenciadorRecursos()

def test_alocar_recursos_sucesso(gerenciador):
    p = Processo(pid=1, scanner=1, impressora=1, modem=1, sata=1)
    sucesso = gerenciador.alocar(p)
    assert sucesso
    assert gerenciador.scanner == 1
    assert gerenciador.impressoras[0] == 1
    assert gerenciador.modem == 1
    assert gerenciador.sata[0] == 1

def test_alocar_recursos_sem_solicitacao(gerenciador):
    p = Processo(pid=2)  # não pede recursos
    sucesso = gerenciador.alocar(p)
    assert sucesso

def test_alocar_recurso_indisponivel_rollback(gerenciador):
    p1 = Processo(pid=1, scanner=1, impressora=1)
    p2 = Processo(pid=2, scanner=1, impressora=1)  # tenta alocar os mesmos recursos

    assert gerenciador.alocar(p1)
    sucesso_p2 = gerenciador.alocar(p2)
    assert not sucesso_p2

    # os ecursos do p1 devem permanecer alocados
    assert gerenciador.scanner == 1
    assert gerenciador.impressoras[0] == 1

def test_liberar_recursos(gerenciador):
    p = Processo(pid=1, scanner=1, impressora=1, modem=1, sata=1)
    gerenciador.alocar(p)
    gerenciador.liberar(p)
    assert gerenciador.scanner == -1
    assert gerenciador.impressoras[0] == -1
    assert gerenciador.modem == -1
    assert gerenciador.sata[0] == -1

def test_alocar_impressora_invalida(gerenciador):
    # impressora = 3 (inválida, só 1 ou 2)
    p = Processo(pid=3, impressora=3)
    sucesso = gerenciador.alocar(p)
    assert not sucesso

def test_alocar_sata_invalido(gerenciador):
    # sata = 3 (inválido, só 1 ou 2)
    p = Processo(pid=4, sata=3)
    sucesso = gerenciador.alocar(p)
    assert not sucesso
