import pygame, sys

#Inicializar la librería
pygame.init()


#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)


#Crear ventana
size = (800, 500)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


while True:
     #Registra todo lo de la ventana
     for event in pygame.event.get():
          print(event)
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()

     screen.fill(BLACK)

     

     pygame.display.flip()
     clock.tick(60)