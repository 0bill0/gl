#coding:utf-8
import Pyro4
# use the URI that the server printed:
uri = raw_input("Enter the uri of the warehouse: ").strip()
p = Pyro4.Proxy(uri)
opcao=True

while opcao:
  #Menu
  print "********************************************"
  print "Opção\t Ação"
  print "--------------------------------------------"
  print "0\tSair"
  print "1\tImprimir"
  print "2\tTotal de Paginas Impressas"
  print "3\tTotal de Paginas Impressas na Impressora"
  print "4\tListar Usuarios"
  print "5\tLog de Impressoes (Ultimas 10)"
  print "\n9\tTrocar de Usuario"
  print "--------------------------------------------"
  option=int(raw_input("Opção: "))

  if option==0:
    print "Saindo"
    opcao = False

  elif option==1:
    n = raw_input("Nome: ")
    s = raw_input("Senha: ")
    print p.imprimir(n, s)

  elif option==2:
    print p.c()
