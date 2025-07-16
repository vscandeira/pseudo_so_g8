import pytest
from core.memoria import GerenciadorMemoria, MemoryOverflowError


class Processo:
    def __init__(self, pid, prioridade, blocos_mem):
        self.pid = pid
        self.prioridade = prioridade
        self.blocos_mem = blocos_mem
        self.offset = None


@pytest.fixture
def gerenciador():
    return GerenciadorMemoria()


def test_alocar_tempo_real_com_sucesso(gerenciador):
    p = Processo(pid=1, prioridade=0, blocos_mem=10)
    sucesso = gerenciador.alocar(p)
    assert sucesso
    assert p.offset is not None
    # deve estar na região TR
    assert 0 <= p.offset <= gerenciador.BLOCO_FIM_TR


def test_alocar_tempo_real_sem_espaco_no_tr_mas_com_espaco_usuario(gerenciador):
    # preenche região TR toda
    for i in range(gerenciador.BLOCO_INICIO_TR, gerenciador.BLOCO_FIM_TR + 1):
        gerenciador.memoria[i] = 99  # processo fictício

    p = Processo(pid=2, prioridade=0, blocos_mem=10)
    sucesso = gerenciador.alocar(p)
    assert sucesso
    # deve estar na região usuário, pois TR está cheia
    assert gerenciador.BLOCO_INICIO_USUARIO <= p.offset <= gerenciador.BLOCO_FIM_USUARIO


def test_alocar_usuario(gerenciador):
    p = Processo(pid=3, prioridade=1, blocos_mem=20)
    sucesso = gerenciador.alocar(p)
    assert sucesso
    # deve estar na região usuário
    assert gerenciador.BLOCO_INICIO_USUARIO <= p.offset <= gerenciador.BLOCO_FIM_USUARIO


def test_alocar_falha_por_espaco(gerenciador):
    # preenche toda região usuário
    for i in range(gerenciador.BLOCO_INICIO_USUARIO, gerenciador.BLOCO_FIM_USUARIO + 1):
        gerenciador.memoria[i] = 88

    p = Processo(pid=4, prioridade=1, blocos_mem=5)
    sucesso = gerenciador.alocar(p)
    assert not sucesso
    assert p.offset is None


def test_liberar_memoria(gerenciador):
    p = Processo(pid=5, prioridade=1, blocos_mem=5)
    gerenciador.alocar(p)
    assert any(block == p.pid for block in gerenciador.memoria)
    gerenciador.liberar(p)
    assert all(block != p.pid for block in gerenciador.memoria)
    assert p.offset is None


def test_alocar_memoria_invalida_tr(gerenciador):
    p = Processo(pid=5, prioridade=0, blocos_mem=70)
    try:
        gerenciador.alocar(p)
        assert False
    except MemoryOverflowError as e:
        assert str(e) == "Processo de tempo real não tem blocos suficientes para alocação."


def test_alocar_memoria_invalida_user(gerenciador):
    p = Processo(pid=6, prioridade=1, blocos_mem=1000)
    try:
        gerenciador.alocar(p)
        assert False
    except MemoryOverflowError as e:
        assert str(e) == "Processo de usuário não tem blocos suficientes para alocação."
