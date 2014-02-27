#coding:utf8
import Pyro4
from pymongo import Connection
import time

class Pessoa(object):

    @classmethod
    def autentica(self, n, s):
        con = Connection('localhost')
        db = con['Banco']
        self.db = db
        if(db.pessoa.find({"name": n, "senha": s}).count() > 0 ):
            users = db.pessoa.find({"name": n})
            self.p = users[0]
            return users[0]
        else:
            return False

    @classmethod
    def autentica_deposito(self, n, s, val): #to do
        con = Connection('localhost')
        db = con['Banco']
        self.db = db
        if(db.pessoa.find({"name": n, "senha": s}).count() > 0 ): #verifica se existe
            users = db.pessoa.find({"name": n}) #resultado json em user
            p = users[0] #linha encontrada passada para p. p = {"Chave":"valor"...}
            idobj = p['_id']
            val = val + p['conta']['saldo'] #acréscimo do valor depositado a saldo
            db.pessoa.update({ "_id" : idobj},  {"$set":{ "conta" : {"saldo": val}}}) #atualização do valor no banco
            return users[0]
        else:
            return False

    @classmethod
    def autentica_saque(self, n, s, val): #to do
        con = Connection('localhost')
        db = con['Banco']
        self.db = db
        if(db.pessoa.find({"name": n, "senha": s}).count() > 0 ): #verifica se existe
            users = db.pessoa.find({"name": n}) #resultado json em user
            p = users[0] #linha encontrada passada para p. p = {"Chave":"valor"...}
            idobj = p['_id']
            val = p['conta']['saldo'] - val #acréscimo do valor depositado a saldo
            db.pessoa.update({ "_id" : idobj},  {"$set":{ "conta" : {"saldo": val}}}) #atualização do valor no banco
            return users[0]
        else:
            return False

    @classmethod
    def registrar_log(self, tipo, valor, n, s):
        con = Connection('localhost')
        db = con['Banco']
        if(db.pessoa.find({"name": n, "senha": s}).count() > 0 ): #verifica se existe
            users = db.pessoa.find({"name": n}) #resultado json em user
            p = users[0] #linha encontrada passada para p. p = {"Chave":"valor"...}
            idobj = p['_id']
            data = time.strftime("%Y-%m-%d %H:%M:%S")
            db.log_transacoes.insert( { "id_cliente": idobj, "tipo": tipo, "valor": valor, "Data" : data} )
            return "!"
        else:
            return "!Falha de registro de extrato"






    def __init__(self):
        self.erro = "Login e/ou Senha incorreto(s)"

    def imprimir(self, n, s):
        if Pessoa.autentica(n , s) != False:
            return self.p['conta']['saldo'] #retorno do saldo
        else : return self.erro

    def depositar(self, n, s, valor):
        extrato = Pessoa.registrar_log("Deposito", valor, n, s)
        if Pessoa.autentica_deposito(n , s, valor) != False:
            return "Deposito Efetuado com sucesso"

    def sacar(self, n, s, valor):
        if Pessoa.autentica_saque(n , s, valor) != False:
            return "Saque efetuado com sucesso"
    
    def gerar_extrato(self, n, s):
        con = Connection('localhost')
        db = con['Banco']
        self.db = db
        if Pessoa.autentica(n , s) != False:
            id_cli = self.p['_id'] #retorno do saldo
            users = db.log_transacoes.find({"id_cliente": id_cli})
            b = []
            for a in users:
                b.append(a)
            return b
        else : return self.erro

class Conta(object):

    def __init__(self, name, senha):
        con = Connection('localhost')
        db = con['SCTI']
        users = db.alunos.find()
        self.a = users[0]['nome']
        return users[0]['nome']

    def m(self):
        return "Deu certo"

    def g(self):
        return "asd - "+self.a

# ------ normal code ------
daemon = Pyro4.Daemon()
uri = daemon.register(Pessoa())
print "uri=",uri
daemon.requestLoop()
#p = Pessoa()

# ------ alternatively, using serveSimple -----
Pyro4.Daemon.serveSimple(
    {
        Pessoa(): None
    },
    ns=False, verbose=True)
