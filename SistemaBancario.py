from datetime import datetime

class Transaction:
    """
    Representa uma transação realizada na conta.
    """
    def __init__(self, tipo, valor, data, info=""):
        self.tipo = tipo
        self.valor = valor
        self.data = data
        self.info = info

    def __str__(self):
        sign = "-" if self.valor < 0 else ""
        return f"{self.data.strftime('%d/%m/%Y %H:%M:%S')} - {self.tipo}: {sign}R$ {abs(self.valor):.2f} ({self.info})"


class Account:
    """
    Classe base para contas bancárias.
    """
    def __init__(self, agencia, conta, titular, endereco, saldo=0.0):
        self.agencia = agencia
        self.conta = conta
        self.titular = titular
        self.endereco = endereco
        self.saldo = saldo
        self.transactions = []
        self.deletion_requested = False

    def deposit(self, amount, origem=""):
        if amount <= 0:
            raise ValueError("O valor do depósito deve ser positivo.")
        self.saldo += amount
        t = Transaction("Depósito", amount, datetime.now(), origem)
        self.transactions.append(t)
        return t

    def withdraw(self, amount):  # método abstrato
        raise NotImplementedError

    def transfer(self, destino, amount):  # método abstrato
        raise NotImplementedError

    def get_extrato(self, start_date, end_date):
        return [t for t in self.transactions if start_date <= t.data <= end_date]

    def update_address(self, novo_endereco):
        self.endereco = novo_endereco
        return novo_endereco


class ContaCorrente(Account):
    """
    Conta corrente com cheque especial e taxa de manutenção.
    """
    def __init__(self, agencia, conta, titular, endereco,
                 saldo=0.0, limite_cheque_especial=1000.0, taxa_manutencao=10.0):
        super().__init__(agencia, conta, titular, endereco, saldo)
        self.limite_cheque_especial = limite_cheque_especial
        self.taxa_manutencao = taxa_manutencao

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if self.saldo - amount < -self.limite_cheque_especial:
            raise ValueError("Saldo insuficiente: ultrapassa limite de cheque especial.")
        self.saldo -= amount
        t = Transaction("Saque", -amount, datetime.now(), "Saque realizado")
        self.transactions.append(t)
        return t

    def transfer(self, destino, amount):
        if amount <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if self.saldo - amount < -self.limite_cheque_especial:
            raise ValueError("Saldo insuficiente para transferência.")
        self.saldo -= amount
        t1 = Transaction("Transferência - Enviada", -amount,
                         datetime.now(), f"Para conta {destino.conta}")
        self.transactions.append(t1)
        destino.saldo += amount
        t2 = Transaction("Transferência - Recebida", amount,
                         datetime.now(), f"De conta {self.conta}")
        destino.transactions.append(t2)
        return t1, t2


class ContaPoupanca(Account):
    """
    Conta poupança sem saldo negativo e rendimento mensal.
    """
    def __init__(self, agencia, conta, titular, endereco,
                 saldo=0.0, rendimento_mensal=0.01):
        super().__init__(agencia, conta, titular, endereco, saldo)
        self.rendimento_mensal = rendimento_mensal

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("O valor do saque deve ser positivo.")
        if self.saldo - amount < 0:
            raise ValueError("Saldo insuficiente: não permite saldo negativo.")
        self.saldo -= amount
        t = Transaction("Saque", -amount, datetime.now(), "Saque realizado")
        self.transactions.append(t)
        return t

    def transfer(self, destino, amount):
        if amount <= 0:
            raise ValueError("O valor da transferência deve ser positivo.")
        if self.saldo - amount < 0:
            raise ValueError("Saldo insuficiente para transferência.")
        self.saldo -= amount
        t1 = Transaction("Transferência - Enviada", -amount,
                         datetime.now(), f"Para conta {destino.conta}")
        self.transactions.append(t1)
        destino.saldo += amount
        t2 = Transaction("Transferência - Recebida", amount,
                         datetime.now(), f"De conta {self.conta}")
        destino.transactions.append(t2)
        return t1, t2

    def aplicar_rendimento(self):
        rendimento = self.saldo * self.rendimento_mensal
        self.saldo += rendimento
        t = Transaction("Rendimento", rendimento,
                        datetime.now(), "Aplicação de rendimento")
        self.transactions.append(t)
        return t


class Bank:
    """
    Gerencia as contas do sistema.
    """
    def __init__(self):
        self.accounts = []

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
