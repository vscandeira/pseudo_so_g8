#Simula disco com alocação contígua.
#Lida com .txt de arquivos.
#Cria e deleta arquivos com controle de permissões.

class GerenciadorArquivos:
    def __init__(self):
        self.mapa_ocupacao = []  # Representação do disco do ponto de vista lógico, similar a uma tabela FAT
        self.num_blocos = 0  # Como a linguagem tem a especificidade de não ter tamanho máximo, a variável é necessária
        self.operacoes = []
    
    def iniciar_filesystem(self, operacoes_arquivos):
        self.mapa_ocupacao = operacoes_arquivos[0] 
        self.operacoes = operacoes_arquivos[2]

    def aplicar_operacoes(self, operacoes):
        pass

    def criar_arquivo(self, nome, tamanho, permissao):
        # Cria um arquivo no disco com o nome, tamanho e permissões especificados
        pass

    def deletar_arquivo(self, nome):
        # Deleta um arquivo do disco
        pass