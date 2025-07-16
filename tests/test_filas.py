import pytest
from core.filas import Escalonador

class Processo:
    def __init__(self, prioridade, tempo_cpu=10, executado=0):
        self.prioridade = prioridade
        self.tempo_cpu = tempo_cpu
        self.executado = executado

@pytest.fixture
def escalonador():
    return Escalonador()

def test_adicionar_processo_prioridade(escalonador):
    p0 = Processo(prioridade=0)
    p1 = Processo(prioridade=1)
    p2 = Processo(prioridade=2)
    p3 = Processo(prioridade=3)

    assert escalonador.adicionar_processo(p0)
    assert escalonador.fila_tempo_real == [p0]

    assert escalonador.adicionar_processo(p1)
    assert escalonador.fila_usr_p1 == [p1]

    assert escalonador.adicionar_processo(p2)
    assert escalonador.fila_usr_p2 == [p2]

    assert escalonador.adicionar_processo(p3)
    assert escalonador.fila_usr_p3 == [p3]

def test_limite_maximo(escalonador):
    escalonador.max = 3
    p1 = Processo(prioridade=1)
    p2 = Processo(prioridade=2)
    p3 = Processo(prioridade=3)
    p4 = Processo(prioridade=0)

    assert escalonador.adicionar_processo(p1)
    assert escalonador.adicionar_processo(p2)
    assert escalonador.adicionar_processo(p3)
    # Agora deve recusar, limite atingido
    assert not escalonador.adicionar_processo(p4)

def test_proximo_processo_ordem(escalonador):
    p0 = Processo(prioridade=0)
    p1 = Processo(prioridade=1)
    p2 = Processo(prioridade=2)
    p3 = Processo(prioridade=3)

    escalonador.adicionar_processo(p1)
    escalonador.adicionar_processo(p0)
    escalonador.adicionar_processo(p3)
    escalonador.adicionar_processo(p2)

    # Próximo deve ser p0 (tempo real)
    assert escalonador.proximo_processo() == p0
    # Depois as filas usr na ordem de prioridade
    assert escalonador.proximo_processo() == p1
    assert escalonador.proximo_processo() == p2
    assert escalonador.proximo_processo() == p3
    # Depois nada
    assert escalonador.proximo_processo() is None

def test_tempo_autorizado(escalonador):
    p0 = Processo(prioridade=0, tempo_cpu=10)
    p1 = Processo(prioridade=1)
    p3 = Processo(prioridade=3)

    assert escalonador.tempo_autorizado(p0) == 10
    assert escalonador.tempo_autorizado(p1) == escalonador.quantum
    assert escalonador.tempo_autorizado(p3) == escalonador.quantum

def test_aplicar_aging(escalonador):
    p = Processo(prioridade=1, executado=5)
    # Deve promover para prioridade 2 e resetar executado
    p = escalonador.aplicar_aging(p)
    assert p.prioridade == 2
    assert p.executado == 0

    p = Processo(prioridade=3, executado=5)
    # Deve manter prioridade 3 (máximo)
    p = escalonador.aplicar_aging(p)
    assert p.prioridade == 3
    assert p.executado == 0

    p = Processo(prioridade=1, executado=4)
    # Não promove se executado < aging
    p = escalonador.aplicar_aging(p)
    assert p.prioridade == 1
    assert p.executado == 4
