import tkinter as tk
from tkinter import messagebox, scrolledtext
from tkinter import ttk
from datetime import datetime
from SistemaBancario import Bank, ContaCorrente, ContaPoupanca, Account

class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Sistema Bancário')
        self.geometry('800x600')
        self.configure(bg='#f0f0f0')
        # Estilos
        self.style = ttk.Style(self)
        self.style.theme_use('clam')
        self._setup_styles()
        # Backend
        self.bank = Bank()
        self.admin_ids = ['admin123']
        self._frame = None
        self.switch_frame(SelectionFrame)

    def _setup_styles(self):
        bg = '#f0f0f0'
        fg = '#333333'
        accent = '#005f73'
        font_header = ('Segoe UI', 20, 'bold')
        font_label = ('Segoe UI', 12)
        font_button = ('Segoe UI', 12)
        self.style.configure('TFrame', background=bg)
        self.style.configure('Header.TLabel', font=font_header, foreground=fg, background=bg)
        self.style.configure('TLabel', font=font_label, foreground=fg, background=bg)
        self.style.configure('TEntry', font=font_label)
        self.style.configure('Accent.TButton', font=font_button, foreground='#ffffff', background=accent)
        self.style.map('Accent.TButton', background=[('active', accent)], foreground=[('active', '#ffffff')])

    def switch_frame(self, frame_class, **kwargs):
        if self._frame:
            self._frame.destroy()
        frame = frame_class(self, **kwargs)
        frame.pack(fill='both', expand=True, padx=20, pady=20)
        self._frame = frame

class SelectionFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text='Bem-vindo ao Sistema Bancário', style='Header.TLabel').grid(row=0, column=0, pady=(0,30))
        ttk.Button(self, text='Login Cliente', style='Accent.TButton', command=lambda: master.switch_frame(ClientLoginFrame)).grid(row=1, column=0, pady=10, ipadx=20)
        ttk.Button(self, text='Cadastrar Cliente', style='Accent.TButton', command=lambda: master.switch_frame(ClientRegisterFrame)).grid(row=2, column=0, pady=10, ipadx=20)
        ttk.Button(self, text='Login Administrador', style='Accent.TButton', command=lambda: master.switch_frame(AdminLoginFrame)).grid(row=3, column=0, pady=10, ipadx=20)
        ttk.Button(self, text='Cadastrar Administrador', style='Accent.TButton', command=lambda: master.switch_frame(AdminRegisterFrame)).grid(row=4, column=0, pady=10, ipadx=20)

class ClientRegisterFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        fields = [
            ('Tipo (1-Corrente,2-Poupança):', '1'),
            ('Agência:', ''),
            ('Conta:', ''),
            ('Titular:', ''),
            ('Endereço:', ''),
            ('Saldo Inicial:', '0'),
        ]
        ttk.Label(self, text='Cadastro Cliente', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        self.entries = {}
        for i, (label, default) in enumerate(fields, start=1):
            ttk.Label(self, text=label).grid(row=i, column=0, sticky='w', pady=5)
            entry = ttk.Entry(self)
            entry.insert(0, default)
            entry.grid(row=i, column=1, sticky='ew', pady=5)
            self.entries[label] = entry
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Cadastrar', style='Accent.TButton', command=self.register).grid(row=7, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', command=lambda: master.switch_frame(SelectionFrame)).grid(row=8, column=0, columnspan=2)

    def register(self):
        try:
            tipo = self.entries['Tipo (1-Corrente,2-Poupança):'].get().strip()
            agencia = self.entries['Agência:'].get().strip()
            conta = self.entries['Conta:'].get().strip()
            nome = self.entries['Titular:'].get().strip()
            endereco = self.entries['Endereço:'].get().strip()
            saldo = float(self.entries['Saldo Inicial:'].get())
            if tipo == '1': acc = ContaCorrente(agencia, conta, nome, endereco, saldo)
            else: acc = ContaPoupanca(agencia, conta, nome, endereco, saldo)
            self.master.bank.add_account(acc)
            messagebox.showinfo('Sucesso', 'Cliente cadastrado com sucesso')
            self.master.switch_frame(ClientLoginFrame)
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class ClientLoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        ttk.Label(self, text='Login Cliente', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Agência:').grid(row=1, column=0, sticky='w', pady=5)
        self.ag = ttk.Entry(self); self.ag.grid(row=1, column=1, sticky='ew', pady=5)
        ttk.Label(self, text='Conta:').grid(row=2, column=0, sticky='w', pady=5)
        self.ct = ttk.Entry(self); self.ct.grid(row=2, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Entrar', style='Accent.TButton', command=self.login).grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', command=lambda: master.switch_frame(SelectionFrame)).grid(row=4, column=0, columnspan=2)

    def login(self):
        acc = self.master.bank.find_account(self.ag.get(), self.ct.get())
        if acc:
            self.master.switch_frame(ClientMainFrame, account=acc)
        else:
            messagebox.showerror('Erro', 'Agência ou conta não encontrada')

class AdminRegisterFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        ttk.Label(self, text='Cadastro Administrador', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Novo ID:').grid(row=1, column=0, sticky='w', pady=5)
        self.id_entry = ttk.Entry(self); self.id_entry.grid(row=1, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Cadastrar', style='Accent.TButton', command=self.register).grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', command=lambda: master.switch_frame(SelectionFrame)).grid(row=3, column=0, columnspan=2)

    def register(self):
        new = self.id_entry.get().strip()
        if not new:
            return messagebox.showerror('Erro','ID vazio')
        if new in self.master.admin_ids:
            return messagebox.showerror('Erro','ID já existe')
        self.master.admin_ids.append(new)
        messagebox.showinfo('Sucesso','Administrador cadastrado')
        self.master.switch_frame(AdminLoginFrame)

class AdminLoginFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        ttk.Label(self, text='Login Administrador', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='ID:').grid(row=1, column=0, sticky='w', pady=5)
        self.id_entry = ttk.Entry(self); self.id_entry.grid(row=1, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Entrar', style='Accent.TButton', command=self.login).grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', command=lambda: master.switch_frame(SelectionFrame)).grid(row=3, column=0, columnspan=2)

    def login(self):
        if self.id_entry.get() in self.master.admin_ids:
            self.master.switch_frame(AdminMainFrame)
        else:
            messagebox.showerror('Erro','ID inválido')

class ClientMainFrame(ttk.Frame):
    def __init__(self, master, account: Account):
        super().__init__(master)
        self.master = master
        self.account = account
        ttk.Label(self, text=f'Cliente: {account.titular}', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        actions = [
            ('Depósito', DepositFrame),
            ('Saque', WithdrawFrame),
            ('Transferência', TransferFrame),
            ('Extrato', ExtractFrame),
            ('Detalhes Conta', AccountDetailsFrame),
            ('Atualizar Endereço', UpdateAddressFrame),
        ]
        for i, (txt, frm) in enumerate(actions, start=1):
            ttk.Button(self, text=txt, style='Accent.TButton', command=lambda f=frm: master.switch_frame(f, account=account)).grid(row=i, column=0, pady=5, ipadx=20)
        ttk.Button(self, text='Solicitar Exclusão', style='Accent.TButton', command=self.request_deletion).grid(row=1, column=1, pady=5)
        ttk.Button(self, text='Logout', style='Accent.TButton', command=lambda: master.switch_frame(SelectionFrame)).grid(row=2, column=1, pady=5)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

    def request_deletion(self):
        self.account.deletion_requested = True
        messagebox.showinfo('Sucesso','Solicitação enviada')

class DepositFrame(ttk.Frame):
    def __init__(self, master, account: Account):
        super().__init__(master)
        self.master = master
        self.account = account
        ttk.Label(self, text='Depósito', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Valor:').grid(row=1, column=0, sticky='w', pady=5)
        self.val = ttk.Entry(self); self.val.grid(row=1, column=1, sticky='ew', pady=5)
        ttk.Label(self, text='Origem:').grid(row=2, column=0, sticky='w', pady=5)
        self.inf = ttk.Entry(self); self.inf.grid(row=2, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Confirmar', style='Accent.TButton', command=self.deposit).grid(row=3, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(ClientMainFrame, account=account)).grid(row=4, column=0, columnspan=2)

    def deposit(self):
        try:
            self.account.deposit(float(self.val.get()), self.inf.get())
            messagebox.showinfo('Sucesso','Depósito realizado')
            self.master.switch_frame(ClientMainFrame, account=self.account)
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class WithdrawFrame(ttk.Frame):
    def __init__(self, master, account: Account):
        super().__init__(master)
        self.master = master
        self.account = account
        ttk.Label(self, text='Saque', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Valor:').grid(row=1, column=0, sticky='w', pady=5)
        self.val = ttk.Entry(self); self.val.grid(row=1, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Confirmar', style='Accent.TButton', command=self.withdraw).grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(ClientMainFrame, account=account)).grid(row=3, column=0, columnspan=2)

    def withdraw(self):
        try:
            self.account.withdraw(float(self.val.get()))
            messagebox.showinfo('Sucesso','Saque realizado')
            self.master.switch_frame(ClientMainFrame, account=self.account)
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class TransferFrame(ttk.Frame):
    def __init__(self, master, account: Account):
        super().__init__(master)
        self.master = master
        self.account = account
        ttk.Label(self, text='Transferência', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Agência destino:').grid(row=1, column=0, sticky='w', pady=5)
        self.ag = ttk.Entry(self); self.ag.grid(row=1, column=1, sticky='ew', pady=5)
        ttk.Label(self, text='Conta destino:').grid(row=2, column=0, sticky='w', pady=5)
        self.ct = ttk.Entry(self); self.ct.grid(row=2, column=1, sticky='ew', pady=5)
        ttk.Label(self, text='Valor:').grid(row=3, column=0, sticky='w', pady=5)
        self.val = ttk.Entry(self); self.val.grid(row=3, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Confirmar', style='Accent.TButton', command=self.transfer).grid(row=4, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(ClientMainFrame, account=account)).grid(row=5, column=0, columnspan=2)

    def transfer(self):
        try:
            dest = self.master.bank.find_account(self.ag.get(), self.ct.get())
            if not dest:
                raise ValueError('Conta destino não encontrada')
            self.account.transfer(dest, float(self.val.get()))
            messagebox.showinfo('Sucesso','Transferência realizada')
            self.master.switch_frame(ClientMainFrame, account=self.account)
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class ExtractFrame(ttk.Frame):
    def __init__(self, master, account: Account):
        super().__init__(master)
        self.master = master
        self.account = account
        ttk.Label(self, text='Extrato', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Data início (dd/mm/aaaa):').grid(row=1, column=0, sticky='w', pady=5)
        self.start = ttk.Entry(self); self.start.grid(row=1, column=1, sticky='ew', pady=5)
        ttk.Label(self, text='Data fim (dd/mm/aaaa):').grid(row=2, column=0, sticky='w', pady=5)
        self.end = ttk.Entry(self); self.end.grid(row=2, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Gerar', style='Accent.TButton', command=self.generate).grid(row=3, column=0, columnspan=2, pady=20)
        self.text = scrolledtext.ScrolledText(self, height=10)
        self.text.grid(row=4, column=0, columnspan=2, sticky='nsew', pady=5)
        self.rowconfigure(4, weight=1)
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(ClientMainFrame, account=account)).grid(row=5, column=0, columnspan=2)

    def generate(self):
        self.text.delete('1.0', tk.END)
        try:
            inicio = datetime.strptime(self.start.get(), '%d/%m/%Y')
            fim = datetime.strptime(self.end.get(), '%d/%m/%Y')
            ops = self.account.get_extrato(inicio, fim)
            if not ops:
                self.text.insert(tk.END, 'Nenhuma operação neste período.')
            else:
                for t in ops:
                    self.text.insert(tk.END, str(t) + '\n')
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class AccountDetailsFrame(ttk.Frame):
    def __init__(self, master, account: Account):
        super().__init__(master)
        info = (
            f'Agência: {account.agencia}\n'
            f'Conta: {account.conta}\n'
            f'Titular: {account.titular}\n'
            f'Endereço: {account.endereco}\n'
            f'Saldo: R$ {account.saldo:.2f}\n'
        )
        if isinstance(account, ContaCorrente):
            info += f'Limite cheque especial: R$ {account.limite_cheque_especial:.2f}\n'
            info += f'Taxa manutenção: R$ {account.taxa_manutencao:.2f}'
        elif isinstance(account, ContaPoupanca):
            info += f'Rendimento mensal: {account.rendimento_mensal:.2%}'
        ttk.Label(self, text='Detalhes da Conta', style='Header.TLabel').pack(pady=(0,20))
        ttk.Label(self, text=info, justify='left').pack(padx=10)
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(ClientMainFrame, account=account)).pack(pady=10)

class UpdateAddressFrame(ttk.Frame):
    def __init__(self, master, account: Account):
        super().__init__(master)
        self.master = master
        self.account = account
        ttk.Label(self, text='Atualizar Endereço', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Novo endereço:').grid(row=1, column=0, sticky='w', pady=5)
        self.en = ttk.Entry(self)
        self.en.grid(row=1, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Salvar', style='Accent.TButton', command=self.update).grid(row=2, column=0, columnspan=2, pady=20)
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(ClientMainFrame, account=account)).grid(row=3, column=0, columnspan=2)

    def update(self):
        try:
            self.account.update_address(self.en.get())
            messagebox.showinfo('Sucesso','Endereço atualizado')
            self.master.switch_frame(ClientMainFrame, account=self.account)
        except Exception as e:
            messagebox.showerror('Erro', str(e))

class DeletionRequestsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        ttk.Label(self, text='Solicitações de Exclusão', style='Header.TLabel').pack(pady=(0,20))
        pendentes = self.master.bank.get_pending_deletion_requests()
        if not pendentes:
            ttk.Label(self, text='Nenhuma solicitação pendente.').pack()
        else:
            for acc in pendentes:
                frm = ttk.Frame(self, borderwidth=1, relief='solid')
                frm.pack(fill='x', pady=5)
                ttk.Label(frm, text=f'Ag: {acc.agencia} Cn: {acc.conta} Titular: {acc.titular}').pack(side='left', padx=5)
                ttk.Button(frm, text='Aprovar', style='Accent.TButton', command=lambda a=acc: self.process(a, True)).pack(side='right', padx=5)
                ttk.Button(frm, text='Recusar', style='Accent.TButton', command=lambda a=acc: self.process(a, False)).pack(side='right')
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(AdminMainFrame)).pack(pady=10)

    def process(self, acc, aprovar):
        if aprovar:
            self.master.bank.remove_account(acc)
        else:
            acc.deletion_requested = False
        messagebox.showinfo('Sucesso','Solicitação processada')
        self.master.switch_frame(DeletionRequestsFrame)

class ListAccountsFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        ttk.Label(self, text='Lista de Contas', style='Header.TLabel').pack(pady=(0,20))
        txt = scrolledtext.ScrolledText(self, height=15)
        txt.pack(fill='both', expand=True)
        if not self.master.bank.accounts:
            txt.insert(tk.END,'Nenhuma conta cadastrada.')
        else:
            for acc in self.master.bank.accounts:
                txt.insert(tk.END,f'Ag: {acc.agencia} Cn: {acc.conta} Titular: {acc.titular} Saldo: R$ {acc.saldo:.2f}\n')
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(AdminMainFrame)).pack(pady=10)

class SearchAccountFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        ttk.Label(self, text='Buscar Conta', style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=(0,20))
        ttk.Label(self, text='Agência:').grid(row=1, column=0, sticky='w', pady=5)
        self.ag = ttk.Entry(self); self.ag.grid(row=1, column=1, sticky='ew', pady=5)
        ttk.Label(self, text='Conta:').grid(row=2, column=0, sticky='w', pady=5)
        self.ct = ttk.Entry(self); self.ct.grid(row=2, column=1, sticky='ew', pady=5)
        self.columnconfigure(1, weight=1)
        ttk.Button(self, text='Buscar', style='Accent.TButton', command=self.search).grid(row=3, column=0, columnspan=2, pady=20)
        self.txt = scrolledtext.ScrolledText(self, height=10)
        self.txt.grid(row=4, column=0, columnspan=2, sticky='nsew', pady=5)
        self.rowconfigure(4, weight=1)
        ttk.Button(self, text='Voltar', style='Accent.TButton', command=lambda: master.switch_frame(AdminMainFrame)).grid(row=5, column=0, columnspan=2)

    def search(self):
        self.txt.delete('1.0', tk.END)
        acc = self.master.bank.find_account(self.ag.get(), self.ct.get())
        if not acc:
            self.txt.insert(tk.END, 'Conta não encontrada')
        else:
            info = (
                f'Ag: {acc.agencia}\n'
                f'Cn: {acc.conta}\n'
                f'Tit: {acc.titular}\n'
                f'End: {acc.endereco}\n'
                f'Saldo: R$ {acc.saldo:.2f}\n'
            )
            if isinstance(acc, ContaCorrente):
                info += f'Limite: R$ {acc.limite_cheque_especial:.2f}\nTaxa: R$ {acc.taxa_manutencao:.2f}'
            elif isinstance(acc, ContaPoupanca):
                info += f'Rend: {acc.rendimento_mensal:.2%}'
            self.txt.insert(tk.END, info)

class AdminMainFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.columnconfigure(0, weight=1)
        ttk.Label(self, text='Administrador', style='Header.TLabel').grid(row=0, column=0, pady=(0,30))
        ttk.Button(self, text='Solicitações de Exclusão', style='Accent.TButton', command=lambda: master.switch_frame(DeletionRequestsFrame)).grid(row=1, column=0, pady=10, ipadx=20)
        ttk.Button(self, text='Listar Contas', style='Accent.TButton', command=lambda: master.switch_frame(ListAccountsFrame)).grid(row=2, column=0, pady=10, ipadx=20)
        ttk.Button(self, text='Buscar Conta', style='Accent.TButton', command=lambda: master.switch_frame(SearchAccountFrame)).grid(row=3, column=0, pady=10, ipadx=20)
        ttk.Button(self, text='Logout', style='Accent.TButton', command=lambda: master.switch_frame(SelectionFrame)).grid(row=4, column=0, pady=10, ipadx=20)

if __name__ == '__main__':
    app = BankingApp()
    app.mainloop()
