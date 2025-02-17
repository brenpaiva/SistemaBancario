from datetime import datetime

# Classe para representar uma transação realizada na conta.
class Transaction:
    def __init__(self, tipo, valor, data, info=""):
        self.tipo = tipo              # Ex.: "Depósito", "Saque", "Transferência - Enviada", etc.
        self.valor = valor            # Valor da operação (positivo para crédito, negativo para débito)
        self.data = data              # Data/hora da operação (objeto datetime)
        self.info = info              # Informação complementar (ex.: origem do depósito, conta destino, etc.)

    def __str__(self):
        sign = "-" if self.valor < 0 else ""
        return f"{self.data.strftime('%d/%m/%Y %H:%M:%S')} - {self.tipo}: {sign}R$ {abs(self.valor):.2f} ({self.info})"

# Classe base para contas bancárias.
class Account:
    def __init__(self, agencia, conta, titular, endereco, saldo=0.0):
        self.agencia = agencia
        self.conta = conta
        self.titular = titular
        self.endereco = endereco
        self.saldo = saldo
        self.transactions = []         # Lista com objetos Transaction
        self.deletion_requested = False  # Flag que indica se o cliente solicitou a exclusão da conta

    def deposit(self, amount, origem=""):
        if amount <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self.saldo += amount
        t = Transaction("Depósito", amount, datetime.now(), origem)
        self.transactions.append(t)
        print("Depósito realizado com sucesso.")

    def get_extrato(self, start_date, end_date):
        # Retorna uma lista de transações cujas datas estão entre start_date e end_date.
        return [t for t in self.transactions if start_date <= t.data <= end_date]

    def update_address(self, novo_endereco):
        self.endereco = novo_endereco
        print("Endereço atualizado com sucesso.")

# Conta corrente: permite saldo negativo até o limite do cheque especial e possui taxa de manutenção.
class ContaCorrente(Account):
    def __init__(self, agencia, conta, titular, endereco, saldo=0.0, limite_cheque_especial=1000.0, taxa_manutencao=10.0):
        super().__init__(agencia, conta, titular, endereco, saldo)
        self.limite_cheque_especial = limite_cheque_especial
        self.taxa_manutencao = taxa_manutencao

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if self.saldo - amount < -self.limite_cheque_especial:
            raise ValueError("Saldo insuficiente, ultrapassa o limite de cheque especial.")
        self.saldo -= amount
        t = Transaction("Saque", -amount, datetime.now(), "Saque realizado")
        self.transactions.append(t)
        print("Saque realizado com sucesso.")

    def transfer(self, destino, amount):
        if amount <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if self.saldo - amount < -self.limite_cheque_especial:
            raise ValueError("Saldo insuficiente para transferência, ultrapassa o limite de cheque especial.")
        # Debita a conta de origem
        self.saldo -= amount
        t = Transaction("Transferência - Enviada", -amount, datetime.now(), f"Para conta {destino.conta}")
        self.transactions.append(t)
        # Atualiza o saldo da conta destino e registra a transação de crédito
        destino.saldo += amount
        t2 = Transaction("Transferência - Recebida", amount, datetime.now(), f"De conta {self.conta}")
        destino.transactions.append(t2)
        print("Transferência realizada com sucesso.")

# Conta poupança: não permite saldo negativo e possui rendimento mensal.
class ContaPoupanca(Account):
    def __init__(self, agencia, conta, titular, endereco, saldo=0.0, rendimento_mensal=0.01):
        super().__init__(agencia, conta, titular, endereco, saldo)
        self.rendimento_mensal = rendimento_mensal  # Por exemplo, 0.01 para 1% de rendimento mensal

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if self.saldo - amount < 0:
            raise ValueError("Saldo insuficiente, conta poupança não permite saldo negativo.")
        self.saldo -= amount
        t = Transaction("Saque", -amount, datetime.now(), "Saque realizado")
        self.transactions.append(t)
        print("Saque realizado com sucesso.")

    def transfer(self, destino, amount):
        if amount <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if self.saldo - amount < 0:
            raise ValueError("Saldo insuficiente para transferência.")
        self.saldo -= amount
        t = Transaction("Transferência - Enviada", -amount, datetime.now(), f"Para conta {destino.conta}")
        self.transactions.append(t)
        destino.saldo += amount
        t2 = Transaction("Transferência - Recebida", amount, datetime.now(), f"De conta {self.conta}")
        destino.transactions.append(t2)
        print("Transferência realizada com sucesso.")

    def aplicar_rendimento(self):
        rendimento = self.saldo * self.rendimento_mensal
        self.saldo += rendimento
        t = Transaction("Rendimento", rendimento, datetime.now(), "Aplicação de rendimento mensal")
        self.transactions.append(t)
        print("Rendimento aplicado com sucesso.")

# Classe que gerencia as contas do sistema.
class Bank:
    def __init__(self):
        self.accounts = []  # Lista de objetos do tipo Account (pode ser ContaCorrente ou ContaPoupanca)

    def add_account(self, account):
        self.accounts.append(account)

    def find_account(self, agencia, conta):
        for acc in self.accounts:
            if acc.agencia == agencia and acc.conta == conta:
                return acc
        return None

    def remove_account(self, account):
        if account in self.accounts:
            self.accounts.remove(account)

    def get_pending_deletion_requests(self):
        return [acc for acc in self.accounts if acc.deletion_requested]

# --------------------- Funções de Interface (CLI) --------------------- #

def client_account_menu(account, bank):
    while True:
        print("\n-------------------------------------")
        print(f"Conta: {account.conta} | Agência: {account.agencia} | Titular: {account.titular}")
        print(f"Saldo atual: R$ {account.saldo:.2f}")
        if isinstance(account, ContaCorrente):
            print(f"Limite de cheque especial: R$ {account.limite_cheque_especial:.2f}")
        print("-------------------------------------")
        print("Escolha uma operação:")
        print("1. Depósito")
        print("2. Saque")
        print("3. Transferência")
        print("4. Extrato")
        print("5. Atualizar endereço")
        print("6. Solicitar exclusão da conta")
        print("7. Sair da conta")
        op = input("Opção: ")

        if op == "1":
            try:
                amount = float(input("Valor do depósito: "))
                origem = input("Origem do depósito: ")
                account.deposit(amount, origem)
            except ValueError as e:
                print("Erro:", e)

        elif op == "2":
            try:
                amount = float(input("Valor do saque: "))
                account.withdraw(amount)
            except ValueError as e:
                print("Erro:", e)

        elif op == "3":
            try:
                dest_agencia = input("Agência do destinatário: ")
                dest_conta = input("Conta do destinatário: ")
                dest_account = bank.find_account(dest_agencia, dest_conta)
                if dest_account is None:
                    print("Erro: Conta de destino não encontrada.")
                else:
                    amount = float(input("Valor da transferência: "))
                    account.transfer(dest_account, amount)
            except ValueError as e:
                print("Erro:", e)

        elif op == "4":
            start_date_str = input("Data de início (dd/mm/aaaa): ")
            end_date_str = input("Data de fim (dd/mm/aaaa): ")
            try:
                start_date = datetime.strptime(start_date_str, "%d/%m/%Y")
                end_date = datetime.strptime(end_date_str, "%d/%m/%Y")
            except Exception:
                print("Formato de data inválido. Tente novamente.")
                continue
            extrato = account.get_extrato(start_date, end_date)
            print("\n----- Extrato -----")
            if extrato:
                for t in extrato:
                    print(t)
            else:
                print("Nenhuma operação realizada neste período.")
            print("--------------------")

        elif op == "5":
            novo_endereco = input("Novo endereço: ")
            account.update_address(novo_endereco)

        elif op == "6":
            confirm = input("Deseja solicitar a exclusão da conta? (s/n): ")
            if confirm.lower() == "s":
                account.deletion_requested = True
                print("Solicitação de exclusão enviada para análise do administrador.")
            else:
                print("Operação cancelada.")

        elif op == "7":
            print("Saindo da conta...")
            break

        else:
            print("Opção inválida. Tente novamente.")

def client_menu(bank):
    while True:
        print("\n========== Menu Cliente ==========")
        print("1. Criar nova conta")
        print("2. Acessar conta existente")
        print("3. Voltar ao menu principal")
        opc = input("Opção: ")

        if opc == "1":
            tipo = input("Tipo de conta (1 - Corrente, 2 - Poupança): ")
            agencia = input("Número da agência: ")
            conta = input("Número da conta: ")
            titular = input("Nome do titular: ")
            endereco = input("Endereço do titular: ")
            try:
                saldo_inicial = float(input("Saldo inicial: "))
            except:
                saldo_inicial = 0.0

            if tipo == "1":
                try:
                    limite = float(input("Limite de cheque especial: "))
                except:
                    limite = 1000.0
                try:
                    taxa = float(input("Taxa de manutenção mensal: "))
                except:
                    taxa = 10.0
                new_account = ContaCorrente(agencia, conta, titular, endereco, saldo_inicial, limite, taxa)
            elif tipo == "2":
                try:
                    rendimento = float(input("Rendimento mensal (em decimal, ex: 0.01 para 1%): "))
                except:
                    rendimento = 0.01
                new_account = ContaPoupanca(agencia, conta, titular, endereco, saldo_inicial, rendimento)
            else:
                print("Tipo de conta inválido.")
                continue

            bank.add_account(new_account)
            print("Conta criada com sucesso.")

        elif opc == "2":
            agencia = input("Informe a agência: ")
            conta = input("Informe a conta: ")
            acc = bank.find_account(agencia, conta)
            if acc is None:
                print("Conta não encontrada.")
            else:
                client_account_menu(acc, bank)

        elif opc == "3":
            break

        else:
            print("Opção inválida. Tente novamente.")

def admin_menu(bank):
    senha = input("Digite a senha do administrador: ")
    # Senha padrão: admin123
    if senha != "admin123":
        print("Senha incorreta.")
        return

    while True:
        print("\n========== Menu Administrador ==========")
        print("1. Visualizar solicitações de exclusão de conta")
        print("2. Listar todas as contas")
        print("3. Voltar ao menu principal")
        op = input("Opção: ")

        if op == "1":
            pending = bank.get_pending_deletion_requests()
            if not pending:
                print("Não há solicitações pendentes.")
            else:
                for acc in pending:
                    print("-------------------------------------")
                    print(f"Agência: {acc.agencia} | Conta: {acc.conta} | Titular: {acc.titular}")
                    print("-------------------------------------")
                    resp = input("Aprovar exclusão desta conta? (s/n): ")
                    if resp.lower() == "s":
                        bank.remove_account(acc)
                        print("Conta excluída.")
                    else:
                        acc.deletion_requested = False
                        print("Solicitação de exclusão cancelada para esta conta.")

        elif op == "2":
            if not bank.accounts:
                print("Nenhuma conta cadastrada.")
            else:
                print("\n----- Lista de Contas -----")
                for acc in bank.accounts:
                    print(f"Agência: {acc.agencia} | Conta: {acc.conta} | Titular: {acc.titular} | Saldo: R$ {acc.saldo:.2f}")
                print("---------------------------")

        elif op == "3":
            break

        else:
            print("Opção inválida. Tente novamente.")

def main():
    bank = Bank()
    while True:
        print("\n========== Bem-vindo ao Sistema Bancário ==========")
        print("1. Cliente")
        print("2. Administrador")
        print("3. Sair")
        opc = input("Opção: ")

        if opc == "1":
            client_menu(bank)
        elif opc == "2":
            admin_menu(bank)
        elif opc == "3":
            print("Saindo do sistema. Até logo!")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == "__main__":
    main()
