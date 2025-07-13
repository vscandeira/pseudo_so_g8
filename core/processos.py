#atributos como PID, prioridade, tempo, blocos, etc.

class Processo:
    def __init__(self, pid, inicio, prioridade, tempo_cpu, blocos_mem, impressora, scanner, modem, sata):
        self.pid = pid
        self.inicio = inicio
        self.prioridade = prioridade
        self.tempo_cpu = tempo_cpu
        self.blocos_mem = blocos_mem
        self.impressora = impressora
        self.scanner = scanner
        self.modem = modem
        self.sata = sata
        self.executado = 0
    
    def executar_processo(self, autorizacao_cpu):
        self.executado += 1
        self.tempo_cpu -= autorizacao_cpu
        #Debugger
        print("Executado o processo PID:", self.pid, "Por ", autorizacao_cpu, "ms - Prioridade: ", self.prioridade , " - Tempo restante de CPU:", self.tempo_cpu)