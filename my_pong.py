import pygame, sys

#Inicializar la librería
pygame.init()
pygame.display.set_caption('Pong Game')

#Definir colores
BLACK = (0,0,0)
WHITE = (255,255,255)


#Crear ventana
large = 900
height = 500

size = (large, height)
screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()


# Pelota
side = 20
org_ballPos_x = ball_coord_x = (large / 2) - (side / 2)
org_ballPos_y = ball_coord_y = (height / 2) - (side / 2)


# Paletas
paleta_x = 10
"""Ancho de la paleta"""
paleta_y = 160
"""Altura de la paleta"""

#Pos inicial
P1_coord_y = (height / 2) - (paleta_y / 2)
P2_coord_y = (height / 2) - (paleta_y / 2)


#velocidad
speed_ball = 10
speed_P1 = 0
speed_P2 = 0




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
               
               if event.key == pygame.K_w:
                    speed_P2 = -5
               if event.key == pygame.K_s:
                    speed_P2 = 5



          #Al soltar tecla
          if event.type == pygame.KEYUP:
               if event.key == pygame.K_UP:
                    speed_P1 = 0
               if event.key == pygame.K_DOWN:
                    speed_P1 = 0

               if event.key == pygame.K_w:
                    speed_P2 = 0
               if event.key == pygame.K_s:
                    speed_P2 = 0



     screen.fill(BLACK)
     
     # --- Zona de animación ---
     ball_coord_y += speed_ball

     P1_coord_y += speed_P1
     P2_coord_y += speed_P2
     

     #Mantiene jugadores en pantalla
     #Jugador 1
     if P1_coord_y > height-paleta_y:
          P1_coord_y = height-paleta_y

     if P1_coord_y < 0:
          P1_coord_y = 0
          
     #Jugador 2
     if P2_coord_y > height-paleta_y:
          P2_coord_y = height-paleta_y
     
     if P2_coord_y < 0:
          P2_coord_y = 0

     

     #Regresa a su posición original al salir
     if ball_coord_x >= large - (side/2) or ball_coord_x <= 0 - (side/2):
          ball_coord_x = org_ballPos_x
          ball_coord_y = org_ballPos_y

     
     if ball_coord_y > height-side or ball_coord_y < 0:
          speed_ball *= -1


     # Rebote en paleta


     # --- Zona de dibujo ---
     # Pelota
     pygame.draw.rect(screen, WHITE, (ball_coord_x, ball_coord_y, side, side))

     
     # Paletas
     pygame.draw.rect(screen, WHITE, (large-paleta_x, P1_coord_y, paleta_x, paleta_y))
     pygame.draw.rect(screen, WHITE, (0, P2_coord_y, paleta_x, paleta_y))



     pygame.display.flip()
     clock.tick(60)