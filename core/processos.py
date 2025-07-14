#atributos como PID, prioridade, tempo, blocos, etc.

class Processo:
    def __init__(self, pid, chegada, prioridade, tempo_cpu, blocos_mem, impressora, scanner, modem, sata):
        self.pid = pid
        self.offset = None
        self.prioridade = prioridade
        self.tempo_cpu = tempo_cpu
        self.blocos_mem = blocos_mem
        self.impressora = impressora
        self.scanner = scanner
        self.modem = modem
        self.sata = sata
        self.executado = 0
        self.instrucoes_executadas = 0
        self.lista_id_operacoes = [] 
        self.chegada = chegada
    
    def executar_processo(self, autorizacao_cpu, printar=False):
        if printar:
            self.print_execucao_processo(autorizacao_cpu)
        self.executado += 1
        self.instrucoes_executadas += autorizacao_cpu
        self.tempo_cpu -= autorizacao_cpu
    
    def print_execucao_processo(self, autorizacao_cpu):
        print(f"process {self.pid} =>")
        if self.executado < 1:
            print(f"P{self.pid} STARTED")
        else:
            print(f"P{self.pid} RESUMED")
        for i in range(self.instrucoes_executadas, autorizacao_cpu):
            print(f"P{self.pid} instruction {i+1}")
        if (self.tempo_cpu-autorizacao_cpu) <= 0:
            print(f"P{self.pid} return SIGINT")
        print()