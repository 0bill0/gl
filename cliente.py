#coding:utf-8
import Pyro4
import collections 
# Mensagem na tela para entrar com a URI, use a URI impressa no servidor
uri = raw_input("Entre com a uri: ").strip()
p = Pyro4.Proxy(uri) #instancia que cria proxies para os objetos da URImotos
opcao=True

while opcao:
  #Menu
  print "****************************************************************************************"
  print "|Opções\t| 0 -> Sair | 1 -> Saldo | 2 -> Depositar | 3 -> Sacar | 4 -> Imprimir Extrato |" 
  print "****************************************************************************************"
  option=int(raw_input("Opção: "))

  if option==0:
    print "Saindo"
    opcao = False

  elif option==1:
    n = raw_input("Nome: ")
    s = raw_input("Senha: ")
    print p.imprimir(n, s) #Proxie atuando com classe Pessoa, podendo invocar os métodos nos objetos remotos

  elif option==2:
    n = raw_input("Nome: ")
    s = raw_input("Senha: ")
    v = input("Valor a ser depositado: ")
    print p.depositar(n, s, v)#Proxie atuando com classe Pessoa, podendo invocar os métodos nos objetos remotos
    print p.imprimir(n, s)#Proxie atuando com classe Pessoa, podendo invocar os métodos nos objetos remotos

  elif option==3:
    n = raw_input("Nome: ")
    s = raw_input("Senha: ")
    v = input("Valor do saque: ")
    print p.sacar(n, s, v)#Proxie atuando com classe Pessoa, podendo invocar os métodos nos objetos remotos
    print p.imprimir(n, s)#Proxie atuando com classe Pessoa, podendo invocar os métodos nos objetos remotos

  elif option==4:
    n = raw_input("Nome: ")
    s = raw_input("Senha: ")
    print "*************************************************************************"
    print "|Data Movim.     \t| Histórico\t| Valor  \t| Saldo       \t|" 
    for x in p.gerar_extrato(n, s):
      print "|",x['Data'],"\t| ",x['tipo'],"\t| ",x['valor'],"  \t| ",x['saldo_atual'],"\t| " 

    print"*************************************************************************"
