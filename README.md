# Sistema Bancário 

## 1. Introdução

Este projeto tem como objetivo simular um sistema bancário utilizando a linguagem Python e o paradigma de orientação a objetos. O sistema permite operações básicas de contas bancárias (como depósito, saque e transferência) e suporta dois tipos de conta: **Conta Corrente** e **Conta Poupança**. A interação é feita por meio de uma interface de linha de comando (CLI).

## 2. Objetivos

- **Simular operações bancárias:** Realizar depósitos, saques e transferências entre contas.
- **Gerenciar diferentes tipos de contas:** Implementar regras específicas para Conta Corrente (como limite de cheque especial e taxa de manutenção) e Conta Poupança (como rendimento mensal e não permitir saldo negativo).
- **Registrar transações:** Todas as operações realizadas são registradas com detalhes como data, tipo, valor e informações complementares.
- **Interface via CLI:** Permitir a interação com o usuário por meio do terminal.
- **Processo de exclusão de conta:** O cliente pode solicitar a exclusão da conta, que deverá ser aprovada por um administrador.
- **Atualização de dados:** O cliente pode atualizar seu endereço, e também emitir extratos filtrados por data.

## 3. Requisitos do Sistema

- **Contas:**  
  - *Conta Corrente:* Possui limite de cheque especial e taxa de manutenção mensal. Permite saldo negativo até o limite definido.  
  - *Conta Poupança:* Não permite saldo negativo e oferece rendimento mensal.

- **Operações Bancárias:**  
  - **Depósito:** Informando a origem do depósito.
  - **Saque:** Retira valor da conta.
  - **Transferência:** Realiza a transferência entre contas, registrando a conta de origem e destino.
  - **Extrato:** Emite um extrato das operações realizadas, podendo ser filtrado por período.

- **Gerenciamento de Conta:**  
  - Solicitação de exclusão de conta pelo cliente, com aprovação do administrador.
  - Atualização do endereço do titular.

- **Tratamento de Erros:**  
  - Validação de valores (não permitir operações com valores negativos ou que ultrapassem os limites permitidos).
  - Exibição de mensagens de erro para operações inválidas (ex.: conta inexistente, saldo insuficiente, etc.).

## 4. Estrutura do Projeto

O projeto está implementado em Python e toda a lógica se encontra em um único arquivo, por exemplo, `sistema_bancario.py`. A estrutura do código é a seguinte:

- **Classes de Modelo:**
  - **`Transaction`:**  
    Representa cada operação realizada na conta, registrando tipo, valor, data e informações complementares.
  
  - **`Account`:**  
    Classe base com atributos comuns a todas as contas (agência, número da conta, titular, endereço, saldo e histórico de transações). Inclui métodos para depósito, atualização de endereço e emissão de extrato.
  
  - **`ContaCorrente`:**  
    Herda de `Account` e implementa regras específicas para conta corrente, como limite de cheque especial e taxa de manutenção. Permite saldo negativo até o limite definido.
  
  - **`ContaPoupanca`:**  
    Herda de `Account` e implementa regras para conta poupança, que não permite saldo negativo e possui rendimento mensal.
  
  - **`Bank`:**  
    Responsável pelo gerenciamento das contas. Permite adicionar, buscar, remover contas e listar solicitações de exclusão.

- **Interface de Linha de Comando (CLI):**
  - Menus interativos para clientes e administradores.
  - Funcionalidades para criação de conta, acesso à conta, realização de operações e gerenciamento (exclusão de conta, atualização de endereço, emissão de extrato).

## 5. Descrição das Principais Classes

### 5.1. `Transaction`

- **Descrição:**  
  Registra os detalhes de cada operação realizada na conta.

- **Atributos:**
  - `tipo`: Tipo da operação (ex.: "Depósito", "Saque", "Transferência - Enviada", etc.).
  - `valor`: Valor da operação (positivo para crédito, negativo para débito).
  - `data`: Data e hora da operação.
  - `info`: Informação complementar (ex.: conta de destino ou origem).

### 5.2. `Account`

- **Descrição:**  
  Classe base para representar uma conta bancária.

- **Atributos:**
  - `agencia`: Número da agência.
  - `conta`: Número da conta.
  - `titular`: Nome do titular.
  - `endereco`: Endereço do titular.
  - `saldo`: Saldo atual da conta.
  - `transactions`: Lista com o histórico de operações.
  - `deletion_requested`: Flag para indicar se o cliente solicitou a exclusão da conta.

- **Métodos Principais:**
  - `deposit(amount, origem)`: Realiza um depósito e registra a transação.
  - `update_address(novo_endereco)`: Atualiza o endereço do titular.
  - `get_extrato(start_date, end_date)`: Retorna as transações realizadas entre duas datas.

### 5.3. `ContaCorrente`

- **Descrição:**  
  Implementa uma conta corrente com limite de cheque especial e taxa de manutenção.

- **Atributos Adicionais:**
  - `limite_cheque_especial`: Limite de saldo negativo permitido.
  - `taxa_manutencao`: Taxa cobrada mensalmente.

- **Métodos Específicos:**
  - `withdraw(amount)`: Realiza o saque permitindo saldo negativo até o limite do cheque especial.
  - `transfer(destino, amount)`: Realiza a transferência debitando o valor da conta de origem e creditando na conta de destino.

### 5.4. `ContaPoupanca`

- **Descrição:**  
  Implementa uma conta poupança que não permite saldo negativo e oferece rendimento mensal.

- **Atributos Adicionais:**
  - `rendimento_mensal`: Taxa de rendimento aplicada mensalmente (ex.: 0.01 para 1%).

- **Métodos Específicos:**
  - `withdraw(amount)`: Realiza o saque, impedindo que o saldo se torne negativo.
  - `transfer(destino, amount)`: Realiza a transferência garantindo saldo suficiente.
  - `aplicar_rendimento()`: Aplica o rendimento mensal ao saldo da conta.

### 5.5. `Bank`

- **Descrição:**  
  Gerencia o conjunto de contas do sistema.

- **Métodos Principais:**
  - `add_account(account)`: Adiciona uma nova conta ao sistema.
  - `find_account(agencia, conta)`: Busca e retorna uma conta com base na agência e no número da conta.
  - `remove_account(account)`: Remove uma conta do sistema.
  - `get_pending_deletion_requests()`: Retorna a lista de contas que solicitaram exclusão.

## 6. Interface de Linha de Comando (CLI)

O sistema utiliza menus interativos para a comunicação com o usuário, dividindo as funcionalidades entre cliente e administrador.

### 6.1. Menu Principal

- **Opções:**
  - Cliente
  - Administrador
  - Sair

### 6.2. Menu do Cliente

- **Funcionalidades:**
  - **Criar nova conta:** Escolha entre Conta Corrente e Conta Poupança e informe os dados necessários.
  - **Acessar conta existente:** Informe a agência e o número da conta para realizar operações.
  - **Dentro da conta, o usuário pode:**
    - Realizar depósito, saque e transferência.
    - Emitir extrato filtrado por data.
    - Atualizar o endereço.
    - Solicitar a exclusão da conta.

### 6.3. Menu do Administrador

- **Acesso:**  
  Exige a senha do administrador (padrão: `admin123`).

- **Funcionalidades:**
  - Visualizar as solicitações de exclusão de conta e aprovar ou recusar cada solicitação.
  - Listar todas as contas cadastradas no sistema.

### 7. Como Utilizar
Acesso como Cliente:

No menu principal, escolha a opção "Cliente".
Selecione entre criar uma nova conta ou acessar uma conta existente.
Siga as instruções do menu para realizar operações (depósito, saque, transferência, etc.).

Acesso como Administrador:

No menu principal, escolha a opção "Administrador".
Digite a senha do administrador (admin123).
No menu do administrador, visualize as solicitações de exclusão de conta e aprove ou recuse conforme necessário.
