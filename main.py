#Inicia o despachante.
#Lê arquivos de entrada.
#Instancia o pseudo-SO.
#Gera a saída do terminal.

import sys
from utils.parser import parse_processos, parse_arquivos
from core.sistema_operacional import SistemaOperacional

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python main.py <processos.txt> <arquivos.txt>")
        sys.exit(1)

    procs_filename = sys.argv[1]
    ops_arqs_filename = sys.argv[2]

    # Parseia os processos e arquivos
    procs = parse_processos(procs_filename)
    ops_arqs = parse_arquivos(ops_arqs_filename)

    # Instancia o despachante
    so = SistemaOperacional(procs, ops_arqs)
    so.executar()

