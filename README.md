# Sistema Bancário com Interface Gráfica (Tkinter)

## 1. Introdução
Este projeto simula um sistema bancário com interface gráfica desenvolvida em **Tkinter**, utilizando Python e orientação a objetos. O sistema permite a criação e gerenciamento de contas bancárias (Corrente ou Poupança), operações como depósito, saque, transferência, além de funcionalidades administrativas.

## 2. Objetivos
- Simular operações bancárias: depósitos, saques, transferências.
- Suportar diferentes tipos de conta (Corrente e Poupança).
- Registrar transações com data, valor, tipo e observações.
- Permitir interação por meio de **interface gráfica profissional com Tkinter**.
- Gerenciar exclusões de conta com validação administrativa.
- Permitir edição de dados como endereço.

## 3. Requisitos do Sistema

### Tipos de Conta:
- **Conta Corrente**: permite saldo negativo (cheque especial) e cobra taxa de manutenção.
- **Conta Poupança**: não permite saldo negativo e possui rendimento mensal.

### Funcionalidades para o Cliente:
- **Depósito** (com campo de origem).
- **Saque**.
- **Transferência entre contas**.
- **Extrato filtrado por data**.
- **Visualizar detalhes da conta**.
- **Atualizar endereço**.
- **Solicitar exclusão da conta** (compendente de aprovação).

### Funcionalidades para o Administrador:
- Visualizar solicitações de exclusão e **aprovar/recusar**.
- Listar todas as contas existentes.
- Buscar conta específica e visualizar seus dados.

## 4. Estrutura do Projeto

### Lógica de Negócio:
**Arquivo:** `SistemaBancario.py`

#### Classes:
- `Transaction`: representa operações com tipo, valor, data e info.
- `Account`: classe base de contas.
- `ContaCorrente`: possui limite de cheque especial e taxa.
- `ContaPoupanca`: possui rendimento mensal.
- `Bank`: gerencia as contas.

### Interface Gráfica:
**Arquivo:** `main.py`

Interface moderna e organizada com **Tkinter** e **ttk**, incluindo:
- Tela de login/cadastro para Cliente e Administrador.
- Menus separados por tipo de usuário.
- Cada operação possui sua própria tela.
- Estilo visual padronizado, com fontes, botões e cores consistentes.

## 5. Principais Classes

### 5.1. `Transaction`
Registra uma transação na conta.
- `tipo`: tipo da operação.
- `valor`: valor da operação.
- `data`: data/hora.
- `info`: informação complementar.

### 5.2. `Account`
Classe abstrata para contas.
- `agencia`, `conta`, `titular`, `endereco`, `saldo`.
- `transactions`: lista de transações.
- Métodos: `deposit`, `get_extrato`, `update_address` (e métodos abstratos `withdraw`, `transfer`).

### 5.3. `ContaCorrente`
- `limite_cheque_especial`, `taxa_manutencao`.
- Métodos implementados: `withdraw`, `transfer`.

### 5.4. `ContaPoupanca`
- `rendimento_mensal`.
- Métodos: `withdraw`, `transfer`, `aplicar_rendimento`.

### 5.5. `Bank`
Gerencia todas as contas do sistema.
- Métodos: `add_account`, `find_account`, `remove_account`, `get_pending_deletion_requests`.

## 6. Interface Gráfica (Tkinter)

### 6.1. Menu Inicial
- Cliente: Login ou Cadastro.
- Administrador: Login ou Cadastro.

### 6.2. Menu do Cliente
- Acessa operações de depósito, saque, transferência.
- Permite consultar extrato, atualizar endereço, e solicitar exclusão.

### 6.3. Menu do Administrador
- Acessa lista de contas.
- Aprova/rejeita solicitações de exclusão.
- Busca contas e vê detalhes.

## 7. Como Utilizar

### Requisitos:
- Python 3.9+

### Executando o sistema:
```bash
python main.py
```

### Fluxo sugerido:
1. Execute `main.py`.
2. Crie um cliente e realize operações.
3. Acesse como administrador e aprove/rejeite exclusões.

## 8. Telas Incluídas
- Login/Cadastro de Cliente
- Login/Cadastro de Administrador
- Menu Cliente (com todas as operações)
- Menu Administrador (validação de exclusões, busca e listagem)
- Telas separadas para extrato, depósito, saque, transferência etc.
