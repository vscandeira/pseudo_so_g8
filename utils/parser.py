from core.processo import Processo

def parse_processos(caminho):
    processos = [] #lista vazia para armazenar os processos
    with open(caminho, 'r') as f:
        linhas = f.readlines() #abre arquivo no caminho dado e lê todas as linhas
        for pid, linha in enumerate(linhas):
            t_inicio, prioridade, t_cpu, blocos, impressora, scanner, modem, disco = map(int, linha.strip().split(','))
            processos.append(Processo(pid, t_inicio, prioridade, t_cpu, blocos, impressora, scanner, modem, disco))
    return processos
#usa enumerate para obter o PID, tira espaços e quebras de linha com .strip() e divide a linha por vírgulas
#converte em inteiros (map(int, ...)) e atribui às variáveis
#cria objeto Processo com esses dados e adiciona à lista

def parse_arquivos(caminho):
    with open(caminho, 'r') as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]
    #abre arquivo, lê as linhas, remove espaços em branco e ignora linhas vazias

    total_blocos = int(linhas[0]) #extrai número total de blocos de memória livre
    qtd_ocupados = int(linhas[1]) #extrai quantos trechos estão ocupados

    ocupados = []
    for i in range(2, 2 + qtd_ocupados):
        nome, inicio, qtd = linhas[i].split(',')
        ocupados.append((nome, int(inicio), int(qtd)))
        #lê as próximas qtd_ocupados linhas e adiciona à lista ocupados tuplas com: 
        # nome, posicao inicial do bloco, quantidade de blocos ocupados

    operacoes = []
    for linha in linhas[2 + qtd_ocupados:]:
        partes = linha.split(',')
        id_proc = int(partes[0])
        op = int(partes[1])
        nome = partes[2]
        tam = int(partes[3]) if op == 0 else None
        operacoes.append((id_proc, op, nome, tam))
    #processa as linhas restantes (operações de arquivos)
    #op == 0 criar arquivo (usa tam)
    #op == 1 deletar arquivo (ignora tam)
    #cria uma tupla com o ID do processo, tipo da operação, nome e tamanho.

    return total_blocos, ocupados, operacoes
