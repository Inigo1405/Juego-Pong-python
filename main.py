import pygame, sys
import random

from module.ball import Ball
from module.player import Player
from module.gameManager import GameManager
from module.pointsMarker import Points_marker


#Inicializar la librería
pygame.init()
pygame.display.set_caption('Pong Game')

#Definir colores
BLACK = (0,0,0)

#Crear ventana
windowSize = (900, 600)
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

#Definir objetos
ball = Ball(20)
p1 = Player(1)
p2 = Player(2)
game_manager = GameManager(p1, p2, ball, windowSize)

# Pelota
ball.get_ball_start(windowSize)

#Paletas jugadores
p1.get_player_start(windowSize)
p2.get_player_start(windowSize)


# Variables para mantener el seguimiento de las teclas presionadas
teclas_presionadas = set()


while True:
     screen.fill(BLACK)
     # Registra todo lo de la ventana
     for event in pygame.event.get():
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()

          #! Eventos teclado
          # Al presionar tecla
          if event.type == pygame.KEYDOWN:
               teclas_presionadas.add(event.key)
          # Al soltar tecla
          if event.type == pygame.KEYUP:
               teclas_presionadas.discard(event.key)

          #print(event)
     
     # Start
     # while start_button != True:
     #      for event in pygame.event.get():
     #           if event.type == pygame.QUIT:
     #                sys.exit()

     #           if event.type == pygame.KEYDOWN:
     #                if event.key == pygame.K_SPACE:
     #                     teclas_presionadas.add(event.key)
     #                     start_button = True
     
     game_manager.start_game()


     # Actualizar las velocidades en el bucle principal del juego
     p1.update_player_speed(teclas_presionadas)
     p2.update_player_speed(teclas_presionadas)

     
     # --- Zona de animación --- 
     #Mantiene jugadores en pantalla
     p1.player_movement(windowSize)
     p2.player_movement(windowSize)


     # Movimiento de la pelota
     game_manager.ball_restart()
     ball.ball_movement(windowSize)

     game_manager.collision_ball()


     # --- Zona de dibujo ---
     # Texto
     game_manager.player_points(screen)

     # Pelota
     pygame.draw.rect(screen, ball.color, ((ball.pos_x - ball.halfSize), (ball.pos_y - ball.halfSize), ball.sizeBall, ball.sizeBall))
     
     # Jugadores
     pygame.draw.rect(screen, p1.color, (p1.pos_x, (p1.pos_y - p1.halfHeight), p1.width, p1.height))
     pygame.draw.rect(screen, p2.color, (p2.pos_x, (p2.pos_y - p2.halfHeight), p2.width, p2.height))


     pygame.display.flip()
     clock.tick(60)