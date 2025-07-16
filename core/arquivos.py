#Simula disco com alocação contígua.
#Cria e deleta arquivos com controle de permissões.

class GerenciadorArquivos:
    def __init__(self):
        self.mapa_ocupacao = []  # Representação do disco do ponto de vista lógico, similar a uma tabela FAT
        self.num_blocos = 0  # Como a linguagem tem a especificidade de não ter tamanho máximo, a variável é necessária
        self.operacoes = []
        self.livre = (' ', -1)  # Representa um bloco livre no disco
    
    def iniciar_filesystem(self, operacoes_arquivos) -> None:
        self.num_blocos = operacoes_arquivos[0]
        for i in range(self.num_blocos):
            self.mapa_ocupacao.append(self.livre)
        for oc in operacoes_arquivos[1]:
            for i in range(oc[2]):
                self.mapa_ocupacao[oc[1]+i] = (oc[0], -1)  # Preenche o mapa de ocupação com os blocos já alocados e sem dono (só processos real time podem acessá-los)
        i = 1
        for op in operacoes_arquivos[2]:
            self.operacoes.append(OperacaoArquivo(op[0], op[1], op[2], i, op[3] if len(op) > 3 else None))
            i +=1

    def identificadores_ops_de_processo(self, pid) -> int:
        # retorna lista de identificação das operações para indexação no respectivo processo
        return [operacao.id_operacao for operacao in self.operacoes if operacao.pid == pid]

    def aplicar_operacao(self, id_op, prioridade) -> None:
        for i in range(len(self.operacoes)):
            if (self.operacoes[i].id_operacao == id_op) and (not self.operacoes[i].executado):
                self.operacoes[i].executado = True
                if self.operacoes[i].cod_operacao == 0:
                    self.criar_arquivo(i, prioridade)
                elif self.operacoes[i].cod_operacao == 1:
                    self.deletar_arquivo(i, prioridade)
                else:
                    print(f"Operação {self.operacoes[i].cod_operacao} desconhecida.")

    def criar_arquivo(self, index, prioridade) -> None:
        for i in range(self.num_blocos):
            if self.mapa_ocupacao[i] == self.livre:
                num_livres = 1
                j = i + 1
                livre = True if j < self.num_blocos else False
                while (livre):
                    if self.mapa_ocupacao[j] == self.livre:
                        num_livres += 1
                        j += 1
                        if j >= self.num_blocos:
                            livre = False
                    else:
                        livre = False
                if num_livres >= self.operacoes[index].num_blocos:
                    escrito = 0
                    while (escrito < self.operacoes[index].num_blocos):
                        self.mapa_ocupacao[i + escrito] = (self.operacoes[index].nome_arquivo, self.operacoes[index].pid)
                        escrito += 1
                    self.operacoes[index].sucesso = True
                    return
                else: 
                    i = i + num_livres - 1  # Pula os blocos livres já contados

    def deletar_arquivo(self, index, prioridade) -> None:
        for i in range(self.num_blocos):
            if(self.mapa_ocupacao[i][0] == self.operacoes[index].nome_arquivo):
                if (self.mapa_ocupacao[i][1] != self.operacoes[index].pid) and (prioridade != 0):  # Prioridade 0 é real-time, que pode deletar qualquer arquivo
                    self.operacoes[index].permitido = False
                    return
                j = i
                while (self.mapa_ocupacao[j][0] == self.operacoes[index].nome_arquivo):
                    self.mapa_ocupacao[j] = self.livre
                    j += 1
                self.operacoes[index].sucesso = True
                return


    def print_mapa_ocupacao(self) -> None:
        print("Mapa de ocupação do disco:")
        for bloco in self.mapa_ocupacao:
            print(f"|{bloco}", end="")
        print("|")
    
    def print_resultado_operacoes(self) -> None:
        print("Sistema de arquivos =>\n")
        for operacao in self.operacoes:
            if operacao.executado and operacao.sucesso:
                print(f"Operação {operacao.id_operacao} => Sucesso")
                if operacao.cod_operacao == 0:  # Criação de arquivo
                    print(f"O processo {operacao.pid} criou o arquivo {operacao.nome_arquivo} (blocos {[ind for ind, b in enumerate(self.mapa_ocupacao) if b[0] == operacao.nome_arquivo]}).")
                elif operacao.cod_operacao == 1:  # Deleção de arquivo
                    print(f"O processo {operacao.pid} deletou o arquivo {operacao.nome_arquivo}.")
                else:
                    print(f"O processo {operacao.pid} solicitou uma operação não reconhecida para o arquivo {operacao.nome_arquivo}.")
            elif (not operacao.permitido) and operacao.executado:
                print(f"Operação {operacao.id_operacao} => Falha")
                print(f"O processo {operacao.pid} não tem permissão para realizar operações sobre o arquivo {operacao.nome_arquivo}.")
            elif operacao.executado:
                print(f"Operação {operacao.id_operacao} => Falha")
                if operacao.cod_operacao == 0:  # Criação de arquivo
                    print(f"O processo {operacao.pid} não pode criar o arquivo {operacao.nome_arquivo} (falta de espaço).")
                elif operacao.cod_operacao == 1:  # Deleção de arquivo
                    print(f"O processo {operacao.pid} não pode deletar o arquivo {operacao.nome_arquivo}, porque ele não existe.")
                else:
                    print(f"O processo {operacao.pid} solicitou uma operação não reconhecida para o arquivo {operacao.nome_arquivo}.")
            else:
                print(f"Operação {operacao.id_operacao} => Falha")
                print(f"O processo {operacao.pid} não existe.")
        print()
    
class OperacaoArquivo:
    def __init__(self, pid, cod_operacao, nome_arquivo, id_operacao, num_blocos=0):
       self.pid = pid
       self.cod_operacao = cod_operacao  # 0: criar, 1: deletar
       self.nome_arquivo = nome_arquivo
       self.id_operacao = id_operacao
       self.num_blocos = num_blocos
       self.executado = False
       self.sucesso = False
       self.permitido = True  # Assume que o processo tem permissão para a operação
