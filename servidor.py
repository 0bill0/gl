import Pyro4
from pymongo import Connection

class Pessoa(object):

    @classmethod
    def autentica(self, n, s):
        con = Connection('localhost')
        db = con['SCTI']
        if(db.alunos.find({"nome": n})): 
            users = db.alunos.find({"nome": n})
            self.pessoa = users[0]
            #return self.pessoa['nome']
        #else:
         #   return False

    def __init__(self):
        self.a = "a"

    def imprimir(self, n, s):
        a = 1
        if Pessoa.autentica(n , s):
            return self.pessoa['nome']


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
