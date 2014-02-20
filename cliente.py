#coding:utf-8
import Pyro4
# use the URI that the server printed:
uri = raw_input("Enter the uri of the warehouse: ").strip()
p = Pyro4.Proxy(uri)
opcao=True

while opcao:
  #Menu
  print "*********************************************************************************************************************"
  print "Opções\t | 0 -> Sair | 1 -> Saldo | 2 -> A definir"
  print "---------------------------------------------------------------------------------------------------------------------"
  option=int(raw_input("Opção: "))

  if option==0:
    print "Saindo"
    opcao = False

  elif option==1:
    n = raw_input("Nome: ")
    s = raw_input("Senha: ")
    print p.imprimir(n, s)

  elif option==2:
    n = raw_input("Nome: ")
    s = raw_input("Senha: ")
    v = input("Valor a ser depositado: ")
    print p.depositar(n, s, v)
    print p.imprimir(n, s)
