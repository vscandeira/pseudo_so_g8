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

    procs_param = sys.argv[1]
    file_ops_param = sys.argv[2]

    # Verificação inicial, será retirado em release final
    print("Processos:", procs_param)
    print("Operações de Arquivos:", file_ops_param)

    # Parseia os processos e arquivos
    procs = parse_processos(procs_param)
    file_ops = parse_arquivos(file_ops_param)

    # Verificação inicial, será retirado em release final
    print("Processos:", procs)
    print("Operações de Arquivos:", file_ops)

    # Instancia o despachante
    # Despachante(processos, operacoes_arquivos).executar()
    #so = SistemaOperacional(processos, operacoes_arquivos)
    #so.executar()

