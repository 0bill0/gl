
import pygame, sys, time
from pygame.locals import *
title = "Testando o inicio do comeco do fim..."
width = 640
height = 400
pygame.init()
screen = pygame.display.set_mode((width, height))
parada = True
pygame.display.set_caption(title)

def contagem(a):
 print("Inicio")
 ini = None
 while (pygame.key.get_pressed() != [K_ESCAPE]): 
  if ini == None:
   print("Antes de chamar o for.")
   ini=time.time()
  for event in pygame.event.get():
   p = pygame.key.get_pressed()
   if p[K_ESCAPE]:
    print ("fim")
    pygame.quit()
    sys.exit()
   else:
    print(a)
    if a == "Apertou":
     a = "Soltou"
     fim = time.time()
    else:
     a = "Apertou"
     fim = time.time()
     print "Tempo Inicial: ", ini, "Tempo Final: ", fim
#  if(pygame.key.get_pressed() == [K_ESCAPE]):
#   print 

contagem("Soltou")
#t = timeit.Timer("contagem", "from __main__ import contagem")
#print t.repeat()
  
#	print("Depois de chamar o for.")
	#print "Tempo", fim-ini
