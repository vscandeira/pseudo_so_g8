
# Pseudo-SO Multiprogramado  
**Disciplina:** Fundamentos de Sistemas Operacionais  
**Departamento:** Ciência da Computação  
**Universidade:** Universidade de Brasília (UnB)  

---

## Integrantes
- **Nicole de Oliveira Sena** — 190114860@aluno.unb.br  
- **Filipe de Sousa Fernandes** — 202065879@aluno.unb.br  
- **Victor Santos Candeira** — 170157636@aluno.unb.br  

---

## Objetivo

Este projeto tem como objetivo simular um sistema operacional simplificado (pseudo-SO) multiprogramado, que gerencia processos com diferentes níveis de prioridade, memória, dispositivos de entrada/saída e sistema de arquivos. A aplicação deve ser capaz de:

- Escalonar processos em filas com diferentes políticas (tempo real e usuários).
- Alocar e liberar memória de forma contígua.
- Gerenciar dispositivos compartilhados (scanner, impressoras, modem, discos).
- Criar e deletar arquivos em disco com alocação contígua.
- Realizar a leitura de dois arquivos de entrada e gerar uma saída textual semelhante a um log de sistema.

---

## Estrutura do Projeto

```bash
pseudo_so/
│
├── main.py                    # Arquivo principal (despachante)
├── processos.txt              # Arquivo de entrada com dados dos processos
├── arquivos.txt               # Arquivo de entrada com operações no sistema de arquivos
│
├── core/                      # Lógica principal do sistema
│   ├── processo.py            # Classe Processo
│   ├── filas.py               # Escalonamento e gerenciamento de filas
│   ├── memoria.py             # Gerenciador de memória
│   ├── recursos.py            # Gerenciador de dispositivos de E/S
│   ├── arquivos.py            # Sistema de arquivos simulado
│   └── sistema_operacional.py # Integração geral dos componentes
│
├── utils/
│   └── parser.py              # Funções para leitura e parsing dos arquivos de entrada
│
├── tests/                     # Testes unitários e de integração
│   ├── test_parser.py
│   ├── test_filas.py
│   ├── test_memoria.py
│   ├── test_recursos.py
│   ├── test_arquivos.py
│   └── test_integracao.py
│
├── read_me.md                 # Este arquivo
└── relatorio.pdf              # Documento explicando o desenvolvimento do projeto
```

---

## Requisitos

- Python 3.8+
- Sistema operacional baseado em UNIX (Linux ou macOS)

---

## Como Executar

1. Clone o repositório:
   ```bash
   git clone <url-do-repositorio>
   cd pseudo_so/
   ```

2. Verifique se os arquivos de entrada `processos.txt` e `arquivos.txt` estão corretamente formatados e na raiz do projeto.

3. Execute o programa:
   ```bash
   python3 main.py processos.txt arquivos.txt
   ```

4. A saída será impressa no terminal, com logs de criação, execução e finalização dos processos, além das operações no sistema de arquivos.

---

## Testes

---

## Ferramentas Utilizadas

- Linguagem: **Python 3.8**
- Editor: **VS Code*
- Gerenciamento de versão: **Git**
- Testes: 

---

## Referências
 
- Materiais da disciplina e exemplos fornecidos pela Profa. Aletéia Patrícia Favacho de Araújo.

---
