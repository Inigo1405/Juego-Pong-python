import cv2
import mediapipe as mp
import numpy as np
import pygame
import threading
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
pressed_key = set()
game_manager = GameManager(p1, p2, ball, windowSize, screen, pressed_key)

# Ball
ball.get_ball_start(windowSize)

# Players
p1.get_player_start(windowSize)
p2.get_player_start(windowSize)


# Inicializar la captura de video con OpenCV
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Configurar el tamaño deseado para la pantalla
desired_width = 100
desired_height = 100
cap.set(3, desired_width)
cap.set(4, desired_height)

# Inicializar mediapipe para el seguimiento de manos
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.6
)


def hand_tracking_thread():
     while True:
          ret, frame = cap.read()
          if not ret:
               break

          height, width, _ = frame.shape
          frame = cv2.flip(frame, 1)
          frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

          # Procesar las manos
          results = hands.process(frame_rgb)

          # Dibujar las manos
          if results.multi_hand_landmarks is not None:
               for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                         frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    )

          # Convertir el frame de OpenCV a formato Pygame
          frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          frame = np.rot90(frame)
          frame = pygame.surfarray.make_surface(frame)
          frame = pygame.transform.flip(frame, True, False)

          # Mostrar el frame en la ventana de Pygame
          screen.blit(frame, (0, 0))
          pygame.display.update()
          

# Create the hand tracking thread
hand_tracking_thread = threading.Thread(target=hand_tracking_thread)
hand_tracking_thread.start()


first_round = True
start_button = False
while True:
     screen.fill(BLACK)
     # Registra todo lo de la ventana
     for event in pygame.event.get():
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               sys.exit()

          #* Eventos teclado
          # Al presionar tecla
          if event.type == pygame.KEYDOWN:
               pressed_key.add(event.key)
          # Al soltar tecla
          if event.type == pygame.KEYUP:
               pressed_key.discard(event.key)


     if not start_button:
          start_button = game_manager.start_game(start_button, clock)


     if first_round:
          # Permite eventos mientras sacan
          time_elapsed = 0
          screen.fill(BLACK)

          while time_elapsed < 1200: # 1000 milisegundos (1 segundo)
               game_manager.draw_game()
               game_manager.get_event()
               pygame.display.update()
               time_elapsed += clock.tick(60)
          first_round = False

          
     # Music
     if pygame.K_v in pressed_key: 
          pygame.mixer.music.load("module/resource/Veo en ti la luz.mp3")
          pygame.mixer.music.play(-1)
     
     
     #* --- Zona de animación --- 
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


     #* --- Zona de dibujo ---
     game_manager.draw_game()


     # Actualizar la pantalla completa
     pygame.display.flip()
     # Frames
     clock.tick(60)