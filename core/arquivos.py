#Simula disco com alocação contígua.
#Lida com .txt de arquivos.
#Cria e deleta arquivos com controle de permissões.

class GerenciadorArquivos:
    def __init__(self):
        self.disco = []  # Representação do disco
        self.mapa_ocupacao = []

    def aplicar_operacoes(self, operacoes):
        pass