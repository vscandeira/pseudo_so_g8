from core.filas import Escalonador
from core.memoria import GerenciadorMemoria, MemoryOverflowError
from core.recursos import GerenciadorRecursos, UnknownResourceError
from core.arquivos import GerenciadorArquivos


class SistemaOperacional:
    def __init__(self, processos, operacoes_arquivos):
        self.escalonador = Escalonador()
        self.memoria = GerenciadorMemoria()
        self.recursos = GerenciadorRecursos()
        self.arquivos = GerenciadorArquivos()
        self.processos = processos
        self.operacoes_arquivos = operacoes_arquivos
        self.executando = None
        self.tempo = 0
        self.proc_criados = 0
        self.proc_executados = 0

    def executar(self):
        ha_novos_processos = True
        fila_vazia = True
        self.arquivos.iniciar_filesystem(self.operacoes_arquivos)
        # Loop de execução do despachante
        while True:
            # 0. Debug tempo
            print(f"##########Tempo: {self.tempo} ms")
            # 1. Inserir processos nas filas do tempo t
            prov_list_proc_time = [p for p in self.processos if p.chegada <= self.tempo]
            self.processos = [p for p in self.processos if p.chegada > self.tempo]
            if prov_list_proc_time:
                for p in prov_list_proc_time:
                    for id in self.arquivos.identificadores_ops_de_processo(p.pid):
                        p.lista_id_operacoes.append(id)
                    # Alocar memória
                    # assume um retorno booleano
                    try:
                        if self.memoria.alocar(p, True):
                            if self.escalonador.adicionar_processo(p):
                                self.msg_processo_criado(p)
                                fila_vazia = False
                                self.proc_criados += 1
                            # Recoloca o processo em espera por limite da fila de prontos
                            else:
                                self.processos.append(p)
                        # Recoloca o processo em espera por limite de memória
                        else:
                            self.processos.append(p)
                    except MemoryOverflowError as e:
                        print(f"Erro: {e} - Encerrando processo {p.pid}.")

            if not self.processos:
                ha_novos_processos = False
            # 2. Escolhe o próximo processo da fila de pronto
            self.executando = self.escalonador.proximo_processo()
            # 3. Executar processos
            if self.executando is None:
                exec_cpu = 1
            else:
                # Alocar E/S
                # assume um retorno booleano
                try:
                    if self.recursos.alocar(self.executando, True):
                        exec_cpu = self.escalonador.tempo_autorizado(self.executando)
                        self.executando.executar_processo(exec_cpu, printar=True)
                    # 3.1. Devolve processo à fila de pronto se ainda tiver tempo de CPU restante
                    if self.executando.tempo_cpu > 0:
                        self.executando = self.escalonador.aplicar_aging(self.executando)
                        self.escalonador.adicionar_processo(self.executando)
                        fila_vazia = False
                    # 3.2. Aplicar operações em arquivos
                    # Como não há tempo determinado, operações de arquivos são aplicadas na última execução do processo
                    else:
                        for id_op in self.executando.lista_id_operacoes:
                            self.arquivos.aplicar_operacao(id_op, self.executando.prioridade)
                        # Liberar memória
                        self.memoria.liberar(self.executando)
                        self.proc_executados += 1
                    # Liberar E/S, ainda não implementado
                    self.recursos.liberar(self.executando, True)
                except UnknownResourceError as e:
                    print(f"Erro: {e} - Encerrando processo {self.executando.pid}.")
                    self.memoria.liberar(self.executando)
                    self.recursos.liberar(self.executando, True)
                    exec_cpu = 1
            self.tempo += exec_cpu
            if (not self.escalonador.fila_pronto[0]) and all(not sub for sub in self.escalonador.fila_pronto[1]):
                fila_vazia = True
            if (not ha_novos_processos) and (fila_vazia):
                break
        # Debug tempo
        print(f"##########Tempo Final: {self.tempo} ms\n")
        # Imprime operações de arquivos
        self.arquivos.print_resultado_operacoes()
        # Imprime mapa de ocupação do disco
        self.arquivos.print_mapa_ocupacao()
        # Imprime quantitativo total de processos criados (incluídos na fila de prontos) e executados
        print(f"Total de processos criados: {self.proc_criados}")
        print(f"Total de processos executados: {self.proc_executados}")

    def msg_processo_criado(self, processo) -> None:
        print("dispatcher =>")
        print(f"\tPID: {processo.pid}")
        print(f"\ttime arrived: {processo.chegada} ms")
        print(f"\toffset: {processo.offset}")
        print(f"\tblocks: {processo.blocos_mem}")
        print(f"\tpriority: {processo.prioridade}")
        print(f"\ttime: {processo.tempo_cpu} ms")
        print(f"\tprinters: {processo.impressora}")
        print(f"\tscanners: {processo.scanner}")
        print(f"\tmodems: {processo.modem}")
        print(f"\tdrives: {processo.sata}")
        print()
