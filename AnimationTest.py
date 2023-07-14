import pygame, sys
from ball import Ball


#Definir colores
BLACK = (0,0,0)

#Inicializar la librería
pygame.init()


#Crear ventana
windowSize = (800, 500)
screen = pygame.display.set_mode(windowSize)

# Controla los FPS
clock = pygame.time.Clock()


#* Coordenadas del cuadrado
ball = Ball(30)

ball.get_ball_start(windowSize)


#*Correr juego
while True:
     #Registra todo lo de la ventana
     for event in pygame.event.get():
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()

     #Color fondo
     screen.fill(BLACK)
     
     
     #! --- Zona de animación ---
     #Para que rebote el cuadrado
     ball.ball_movement(windowSize)
          


     #! --- Zona de dibujo ---
     pygame.draw.rect(screen, ball.color, ((ball.pos_x - ball.halfSize), (ball.pos_y - ball.halfSize), ball.sizeBall, ball.sizeBall))

     #Actualizar pantalla
     pygame.display.flip()
     clock.tick(60)