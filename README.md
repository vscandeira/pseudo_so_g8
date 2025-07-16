
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
├── validation_files/
│   └── process*.txt              # Arquivos de entrada com dados dos processos
│   └── files*.txt               # Arquivo de entrada com operações no sistema de arquivos
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

2. Escolher um arquivo de processos e um de files para teste. Os arquivos estão no diretório `validation_files`. É possível criar os próprios arquivos seguindo o formato da especificação do requisito do trabalho da disciplina.

3. Execute o programa. 
   + O primeiro parâmetro é o arquivo de processos e o segundo o arquivo contendo operações sobre arquivos.
   + Exemplo com escolha dos arquivos **process03.txt** e **files03.txt**:
      ```bash
      python3 main.py validation_files/process03.txt validation_files/files03.txt
      ```

4. A saída será impressa no terminal, com logs de criação, execução e finalização dos processos, além das operações no sistema de arquivos, estados de memória e do gerenciador de recursos.

---

## Testes

Este projeto conta com uma suíte de testes automatizados desenvolvidos com `pytest`, localizada na pasta `tests/`.


Os testes estão divididos por módulos:

- `test_processos.py`: valida o comportamento da classe `Processo`, como execução e controle de tempo de CPU.
- `test_memoria.py`: verifica a alocação e liberação de blocos de memória para processos.
- `test_recursos.py`: testa a alocação e liberação de recursos de E/S (impressoras, modem, scanner e SATA).
- `test_arquivos.py`: garante o funcionamento correto do sistema de arquivos simulado, incluindo criação e exclusão de arquivos.
- `test_parser.py`: confere a leitura, validação e transformação dos arquivos de entrada.
- `test_integrado.py`: executa uma simulação completa do sistema operacional com entrada real, validando o funcionamento integrado dos módulos.

### Como rodar os testes

1. No terminal, dentro do diretório do projeto:

```bash
pytest
```
É necessário ter o pytest instalado. Para instalar:

```bash
pip install pytest
```

## Ferramentas Utilizadas

- Linguagem: **Python 3.8**
- Editor: **VS Code**
- Gerenciamento de versão: **Git**

---

## Referências
 
- Materiais da disciplina e exemplos fornecidos pela Profa. Aletéia Patrícia Favacho de Araújo.

---
