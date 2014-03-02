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
            val = p['conta']['saldo'] + val #acréscimo do valor depositado a saldo
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
            if(tipo == "Deposito"):
                saldo_atual = p['conta']['saldo'] + valor
            else:
                saldo_atual = p['conta']['saldo'] - valor
            db.log_transacoes.insert( { "id_cliente": idobj, "tipo": tipo, "valor": valor, "Data" : data, "saldo_atual" : saldo_atual } )
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
        Pessoa.registrar_log("Deposito", valor, n, s)
        if Pessoa.autentica_deposito(n , s, valor) != False:
            return "Deposito Efetuado com sucesso"

    def sacar(self, n, s, valor):
        Pessoa.registrar_log("Saque", valor, n, s)
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

# ------ Código padrão encontrado na documentação da biblioteca ------
daemon = Pyro4.Daemon('192.168.43.5', 5000) #instancia que contém a lógica do lado do servidor e distribui os métodos remotos e as chamadas recebidas para os objetos apropriados. A instancia é contruída passando o IP e a porta para execução do sistema.
uri = daemon.register(Pessoa())#Registra um objeto Pyro com o identificador fornecido. O objeto é agora conhecido apenas dentro deste daemon, não está automaticamente disponível em um servidor de nomes. Este método retorna uma URI para o objeto registrado.
print "uri=",uri
daemon.requestLoop()#loop para atender as solicitações de entrada.

Pyro4.Daemon.serveSimple( # inicia um servidor Daemon com a classe Pessoa
    {
        Pessoa(): None
    },
    ns=False, verbose=True)
