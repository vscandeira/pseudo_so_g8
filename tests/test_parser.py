import os
from utils.parser import parse_processos, parse_arquivos
from core.processo import Processo

def criar_arquivo(nome, conteudo):
    with open(nome, 'w') as f:
        f.write(conteudo)

def test_parse_processos():
    conteudo = """0,1,5,10,1,0,0,0
2,0,3,5,0,1,1,1"""
    criar_arquivo("processos.txt", conteudo)

    processos = parse_processos("processos.txt")
    assert len(processos) == 2
    assert isinstance(processos[0], Processo)
    assert processos[0].prioridade == 1
    assert processos[1].t_inicio == 2
    os.remove("processos.txt")

def test_parse_arquivos():
    conteudo = """100
2
arq1.txt,0,10
arq2.txt,20,5
0,0,arq3.txt,15
1,1,arq1.txt"""
    criar_arquivo("arquivos.txt", conteudo)

    total_blocos, ocupados, operacoes = parse_arquivos("arquivos.txt")

    assert total_blocos == 100
    assert len(ocupados) == 2
    assert ocupados[0] == ("arq1.txt", 0, 10)
    assert operacoes[0] == (0, 0, "arq3.txt", 15)
    assert operacoes[1] == (1, 1, "arq1.txt", None)
    os.remove("arquivos.txt")

if __name__ == "__main__":
    test_parse_processos()
    test_parse_arquivos()
    print("Todos os testes passaram!")
