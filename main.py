#Inicia o despachante.
#Lê arquivos de entrada.
#Instancia o pseudo-SO.
#Gera a saída do terminal.

from utils.parser import parse_processos, parse_arquivos
from core.sistema_operacional import SistemaOperacional

if __name__ == "__main__":
    processos = parse_processos("processos.txt")
    operacoes_arquivos = parse_arquivos("arquivos.txt")

    so = SistemaOperacional(processos, operacoes_arquivos)
    so.executar()

