#coding:utf8
import Pyro4
from pymongo import Connection
set = None

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


    def __init__(self):
        self.erro = "Login e/ou Senha incorreto(s)"

    def imprimir(self, n, s):
        if Pessoa.autentica(n , s) != False: return self.p['conta']['saldo'] #retorno do saldo
        else : return self.erro

    def depositar(self, n, s, valor):
        if Pessoa.autentica_deposito(n , s, valor) != False:
            return "Deposito Efetuado com sucesso"
  

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
p = Pessoa()

# ------ alternatively, using serveSimple -----
Pyro4.Daemon.serveSimple(
    {
        Pessoa(): None
    },
    ns=False, verbose=True)
