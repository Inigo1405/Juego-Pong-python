import pygame, sys
from ball import Ball
from player import Player

#Inicializar la librería
pygame.init()
pygame.display.set_caption('Pong Game')

#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)


ball = Ball(20)

#Crear ventana
large = 900
height = 500

windowSize = (900, 500)
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()


# Pelota
ball.get_ball_start(windowSize)



# Paletas
paleta_x = 10
"""Ancho de la paleta"""
paleta_y = 125
"""Altura de la paleta"""

#Pos inicial
P1_coord_y = (height / 2) - (paleta_y / 2)
P2_coord_y = (height / 2) - (paleta_y / 2)


player_right = Player()

# velocidad
speed_P1 = 0
# speed_P2 = 0



while True:
     #Registra todo lo de la ventana
     for event in pygame.event.get():
          #print(event)
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()


          #! Eventos teclado
          #Al presionar tecla
          if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_UP:
                    speed_P1 = -5

               if event.key == pygame.K_DOWN:
                    speed_P1 = 5
               
               # if event.key == pygame.K_w:
               #      speed_P2 = -5
               # if event.key == pygame.K_s:
               #      speed_P2 = 5


          #Al soltar tecla
          if event.type == pygame.KEYUP:
               if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    speed_P1 = 0

               # if event.key == pygame.K_w or event.key == pygame.K_s:
               #      speed_P2 = 0



     screen.fill(BLACK)

     # --- Zona de animación ---

     P1_coord_y += speed_P1
     # P2_coord_y += speed_P2
     

     #Mantiene jugadores en pantalla
     #Jugador 1
     if P1_coord_y > height-paleta_y:
          P1_coord_y = height-paleta_y

     if P1_coord_y < 0:
          P1_coord_y = 0
          
     #Jugador 2
     # if P2_coord_y > height-paleta_y:
     #      P2_coord_y = height-paleta_y
     
     # if P2_coord_y < 0:
     #      P2_coord_y = 0


     #Movimiento de la pelota
     ball.ball_movement(windowSize)
     

     # --- Zona de dibujo ---
     # Pelota
     pygame.draw.rect(screen, ball.color, ((ball.pos_x - ball.halfSize), (ball.pos_y - ball.halfSize), ball.sizeBall, ball.sizeBall))

     
     # Paletas
     pygame.draw.rect(screen, WHITE, (large-paleta_x, P1_coord_y, paleta_x, paleta_y))
     # pygame.draw.rect(screen, WHITE, (0, P2_coord_y, paleta_x, paleta_y))



     pygame.display.flip()
     clock.tick(60)