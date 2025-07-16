# test_arquivos.py
import pytest
from core.arquivos import GerenciadorArquivos, OperacaoArquivo

@pytest.fixture
def gerenciador():
    g = GerenciadorArquivos()
    # (10 blocos, [[nome, início, tamanho]], [operações])
    g.iniciar_filesystem([
        10,
        [['X', 0, 3]],  # Blocos 0,1,2 já ocupados
        [
            [1, 0, 'A', 3],  # pid 1 cria 'A' com 3 blocos
            [1, 1, 'X'],     # pid 1 deleta 'X'
            [2, 0, 'B', 4],  # pid 2 cria 'B' com 4 blocos
            [2, 1, 'A'],     # pid 2 deleta 'A'
        ]
    ])
    return g

def test_identificadores_ops_de_processo(gerenciador):
    assert gerenciador.identificadores_ops_de_processo(1) == [1, 2]
    assert gerenciador.identificadores_ops_de_processo(2) == [3, 4]

def test_criar_arquivo_sucesso(gerenciador):
    gerenciador.aplicar_operacao(1)
    op = gerenciador.operacoes[0]
    assert op.executado
    assert op.sucesso
    assert gerenciador.mapa_ocupacao.count('A') == 3

def test_deletar_arquivo_existente(gerenciador):
    gerenciador.aplicar_operacao(2)
    op = gerenciador.operacoes[1]
    assert op.executado
    assert op.sucesso
    assert gerenciador.mapa_ocupacao[:3] == [' ', ' ', ' ']

def test_criar_arquivo_sem_espaco(gerenciador):
    # Preenche todos os blocos com arquivos fictícios
    for i in range(10):
        gerenciador.mapa_ocupacao[i] = 'Z'
    gerenciador.aplicar_operacao(1)
    op = gerenciador.operacoes[0]
    assert op.executado
    assert not op.sucesso

def test_deletar_arquivo_inexistente(gerenciador):
    gerenciador.aplicar_operacao(4)
    op = gerenciador.operacoes[3]
    assert op.executado
    assert not op.sucesso
