import pytest
from core.processos import Processo
from core.memoria import GerenciadorMemoria
from core.recursos import GerenciadorRecursos
from core.filas import Escalonador

def test_integrado_fluxo_completo():
    # Criar os gerenciadores
    mem = GerenciadorMemoria()
    rec = GerenciadorRecursos()
    fila = Escalonador()

    # Criar processo com prioridade 1, que precisa de 10 blocos, impressora 1, scanner
    p = Processo(pid=1, chegada=0, prioridade=1, tempo_cpu=10, blocos_mem=10, impressora=1, scanner=1, modem=0, sata=0)

    # Alocar memória
    alocou_mem = mem.alocar(p)
    assert alocou_mem is True
    assert p.offset is not None

    # Alocar recursos
    alocou_rec = rec.alocar(p)
    assert alocou_rec is True

    # Adicionar na fila do escalonador
    adicionou_fila = fila.adicionar_processo(p)
    assert adicionou_fila is True

    # Pegar próximo processo da fila e simular execução
    proc_exec = fila.proximo_processo()
    assert proc_exec == p

    # Calcular tempo autorizado
    tempo_cpu = fila.tempo_autorizado(proc_exec)
    assert tempo_cpu == fila.quantum  # pois prioridade 1

    # Executar processo
    proc_exec.executar_processo(tempo_cpu)
    assert proc_exec.executado == 1
    assert proc_exec.tempo_cpu == 9  # 10 - 1

    # Aplicar aging (não deve mudar ainda, executado < aging)
    proc_aging = fila.aplicar_aging(proc_exec)
    assert proc_aging.prioridade == 1

    # Armazenar offset antes de liberar
    offset = p.offset

    # Liberar recursos e memória após execução
    rec.liberar(proc_exec)
    mem.liberar(proc_exec)

    # Verificar se memória e recursos foram liberados
    for i in range(offset, offset + p.blocos_mem):
        assert mem.memoria[i] == -1
    assert rec.impressoras[p.impressora - 1] == -1
    assert rec.scanner == -1
