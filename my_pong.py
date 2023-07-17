import pygame, sys
from ball import Ball
from player import Player


def collision_ball(windowSize):
     width, height = windowSize
     ball_x1, ball_y1, ball_x2, ball_y2 = ball.hitBox

     if ball_x1 > width/2:
          player_x1, player_y1, player_x2, player_y2 = p2.hitBox
          
          if ball_x1 >= player_x2 and ball_y1 <= player_y2 and ball_y2 >= player_y1:
               ball.speed_x *= -1

     else:
          player_x1, player_y1, player_x2, player_y2 = p1.hitBox
          
          if ball_x2 <= player_x1 and ball_y1 <= player_y2 and ball_y2 >= player_y1:
               ball.speed_x *= -1


#Inicializar la librería
pygame.init()
pygame.display.set_caption('Pong Game')

#Definir colores
BLACK = (0,0,0)

ball = Ball(20)
p1 = Player(1)
p2 = Player(2)

#Crear ventana
windowSize = (900, 500)
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

# Pelota
ball.get_ball_start(windowSize)

#Paletas jugadores
p1.get_player_start(windowSize)
p2.get_player_start(windowSize)

# Cargar la fuente
font = pygame.font.Font("undertale.ttf", 50)

# Variables para mantener el seguimiento de las teclas presionadas
teclas_presionadas = set()
while True:
     screen.fill(BLACK)
     #Registra todo lo de la ventana
     for event in pygame.event.get():
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()

          #! Eventos teclado
          #Al presionar tecla
          if event.type == pygame.KEYDOWN:
               teclas_presionadas.add(event.key)
          #Al soltar tecla
          if event.type == pygame.KEYUP:
               teclas_presionadas.discard(event.key)

     
     # Actualizar las velocidades en el bucle principal del juego
     p1.update_player_speed(teclas_presionadas)
     p2.update_player_speed(teclas_presionadas)


     # --- Zona de animación --- 
     #Mantiene jugadores en pantalla
     p1.player_movement(windowSize)
     p2.player_movement(windowSize)

     # print("P2: ", p2.hitBox)


     #Movimiento de la pelota
     ball.ball_movement(windowSize)
     

     collision_ball(windowSize)


     # --- Zona de dibujo ---
     # Texto
     text = font.render(str(0), True, ball.color)
     text_rect = text.get_rect(center=(windowSize[0] // 2, windowSize[1] // 2))
     screen.blit(text, text_rect)

     # Pelota
     pygame.draw.rect(screen, ball.color, ((ball.pos_x - ball.halfSize), (ball.pos_y - ball.halfSize), ball.sizeBall, ball.sizeBall))
     

     # Jugadores
     pygame.draw.rect(screen, p1.color, (p1.pos_x, (p1.pos_y - p1.halfHeight), p1.width, p1.height))
     pygame.draw.rect(screen, p2.color, (p2.pos_x, (p2.pos_y - p2.halfHeight), p2.width, p2.height))


     pygame.display.flip()
     clock.tick(60)