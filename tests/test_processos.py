import pytest
from core.processos import Processo
from io import StringIO
import sys

@pytest.fixture
def processo():
    return Processo(pid=1, chegada=0, prioridade=1, tempo_cpu=10, blocos_mem=5, impressora=0, scanner=0, modem=0, sata=0)

def test_atributos_iniciais(processo):
    assert processo.pid == 1
    assert processo.chegada == 0
    assert processo.prioridade == 1
    assert processo.tempo_cpu == 10
    assert processo.blocos_mem == 5
    assert processo.impressora == 0
    assert processo.scanner == 0
    assert processo.modem == 0
    assert processo.sata == 0
    assert processo.executado == 0
    assert processo.instrucoes_executadas == 0
    assert processo.lista_id_operacoes == []

def test_executar_processo_atualiza_estado(processo):
    processo.executar_processo(autorizacao_cpu=3)
    assert processo.executado == 1
    assert processo.instrucoes_executadas == 3
    assert processo.tempo_cpu == 7  # 10 - 3

def test_executar_processo_com_printar(processo, capsys):
    processo.executar_processo(autorizacao_cpu=2, printar=True)
    captured = capsys.readouterr()
    # Deve conter linhas básicas da execução e instruções
    assert f"process {processo.pid} =>" in captured.out
    assert f"P{processo.pid} STARTED" in captured.out
    assert "instruction 1" in captured.out
    assert "instruction 2" in captured.out

def test_executar_processo_com_termino(processo, capsys):
    processo.tempo_cpu = 2
    processo.executar_processo(autorizacao_cpu=2, printar=True)
    captured = capsys.readouterr()
    assert "return SIGINT" in captured.out
