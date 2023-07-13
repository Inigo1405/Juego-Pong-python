import pygame, sys

#Inicializar la librería
pygame.init()

#Definir colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


large = 800
height = 500

#Crear ventana
size = (large, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)


#cuadrado
side = 30


while True:
     #Registra todo lo de la ventana
     for event in pygame.event.get():
          if event.type == pygame.QUIT:
               sys.exit()

     # Obtener ubicación del mouse
     mouse_pos = pygame.mouse.get_pos() 
     pos_x = mouse_pos[0] - (side/2)
     pos_y = mouse_pos[1] - (side/2)

     screen.fill(BLACK)



     pygame.draw.rect(screen, WHITE, (pos_x, pos_y, side, side))
     

     pygame.display.flip()
     clock.tick(60)
