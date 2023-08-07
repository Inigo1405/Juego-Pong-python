import pygame 
import sys

from module.gameManager import GameManager
from module.player import Player
from module.ball import Ball

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
game_manager = GameManager(p1, p2, ball, windowSize, screen)

# Ball
ball.get_ball_start(windowSize)

# Players
p1.get_player_start(windowSize)
p2.get_player_start(windowSize)

# Music
pygame.mixer.music.load("module/resource/Veo en ti la luz.mp3")
pygame.mixer.music.play(-1)


# Variables para mantener el seguimiento de las teclas presionadas
pressed_key = set()
start_button = False
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
               pressed_key.add(event.key)
          # Al soltar tecla
          if event.type == pygame.KEYUP:
               pressed_key.discard(event.key)


     if not start_button:
          start_button = game_manager.start_game(start_button, clock)

     
     # --- Zona de animación --- 
     # Actualizar las velocidades en el bucle principal del juego
     p1.update_player_speed(pressed_key)
     p2.update_player_speed(pressed_key)


     #Mantiene jugadores en pantalla
     p1.player_movement(windowSize)
     p2.player_movement(windowSize)


     # Movimiento de la pelota
     game_manager.ball_restart(clock)
     ball.ball_movement(windowSize)

     # Golpeo de pelota
     game_manager.collision_ball()


     # --- Zona de dibujo ---
     game_manager.draw_game()


     # Actualizar la pantalla completa
     pygame.display.flip()
     # Frames
     clock.tick(60)