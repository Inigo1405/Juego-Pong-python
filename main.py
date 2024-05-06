import cv2
import mediapipe as mp
import numpy as np
import pygame
import queue
import sys
import threading

from module.ball import Ball
from module.gameManager import GameManager
from module.player import Player


# Inicializar la librería
pygame.init()
pygame.display.set_caption('Pong Game')

# Definir colores
BLACK = (0,0,0)

# Crear ventana
windowSize = (900, 600)
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

# Definir objetos
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

# Detect players variables
position = ['left', 'right']

players = [
    {
        'name': 'Player 1',
        'position': 'left',
        'x': 0,
        'y': 0,
        'z': 0
    },
    {
        'name': 'Player 2',
        'position': 'right',
        'x': 0,
        'y': 0,
        'z': 0
    }
]


# Configurar el tamaño deseado para la pantalla
desired_width = 100
desired_height = 100
cap.set(3, desired_width)
cap.set(4, desired_height)

# Inicializar mediapipe para el seguimiento de manos
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
     min_detection_confidence=0.5,
     static_image_mode=False,
     max_num_hands=2,
)

hand_pos_queue = queue.Queue()
def hand_tracking_thread():
     global hand_pos_queue
     while True:
          ret, frame = cap.read()
          x, y, c = frame.shape
          
          if not ret:
               break

          height, width, _ = frame.shape
          frame = cv2.flip(frame, 1)
          frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

          # Procesar las manos
          result = hands.process(frame_rgb)

          # Dibujar las manos
          if result.multi_hand_landmarks:
               # print(len(result.multi_hand_landmarks))
               landmarks = []
               for hand_landmarks in result.multi_hand_landmarks:
                    # Drawing landmarks on frames
                    # mp_drawing.draw_landmarks(
                    #      frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    # )
                    
                    # Get landmark 9
                    point = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    
                    # Draw a circle for each player
                    cv2.circle(frame, (int(point.x*y), int(point.y*x)), 5, (0, 255, 0), -1)
                    cv2.circle(frame, (int(point.x*y), int(point.y*x)), 5, (0, 0, 255), -1)
                    
                    # Access to cordenates
                    if int(point.x * windowSize[0]) >= 450:
                         players[1]['x'] = int(point.x * windowSize[0])
                         players[1]['y'] = int(point.y * windowSize[1])
                         players[1]['z'] = point.z
                    else:
                         players[0]['x'] = int(point.x * windowSize[0])
                         players[0]['y'] = int(point.y * windowSize[1])
                         players[0]['z'] = point.z
                    
                    # hand_pos_y = int(point.y * windowSize[0])
                    hand_pos_queue.put(players)

          # Draw a line in the middle of the frame
          cv2.line(frame, (int(y/2), 0), (int(y/2), x), (0, 0, 255), 2)

          cv2.line(frame, (int(y/2)-130, 0), (int(y/2)-130, x), (150, 150, 255), 2)
          cv2.line(frame, (int(y/2)+130, 0), (int(y/2)+130, x), (150, 150, 255), 2)


          # Convertir el frame de OpenCV a formato Pygame
          frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          frame = np.rot90(frame)
          
          frame = pygame.surfarray.make_surface(frame)
          frame = pygame.transform.flip(frame, True, False)
          frame_center_x = (900 - frame.get_width()) // 2

          # Mostrar el frame en la ventana de Pygame
          screen.blit(frame, (frame_center_x, 0))
          # screen.blit(frame, (0, 0))
          pygame.display.update()
          
 
 

first_round = True
start_button = False
while True:
     # Pinta la pantalla
     pygame.draw.rect(screen, BLACK, (0, 120, 900, 600))
     pygame.draw.rect(screen, BLACK, (0, 0, 370, 120))
     pygame.draw.rect(screen, BLACK, (530, 0, 370, 120))
     
     # Registra todo lo de la ventana
     for event in pygame.event.get():
          #Saldrá al cerrar ventana
          if event.type == pygame.QUIT:
               cap.release()
               cv2.destroyAllWindows()
               pygame.quit()
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
          # Create the hand tracking thread
          hand_tracking_thread = threading.Thread(target=hand_tracking_thread)
          hand_tracking_thread.start()


     if first_round:
          # Permite eventos mientras sacan
          time_elapsed = 0
          screen.fill(BLACK)

          while time_elapsed < 3000: # 1000 milisegundos (1 segundo)
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
     
     # Movimiento del jugador
     try:
          # Movimiento con las manos
          hand_pos_y = hand_pos_queue.get_nowait()
          p1.update_player_speed(pressed_key, hand_pos_y[0]['y'])
          p2.update_player_speed(pressed_key, hand_pos_y[1]['y'])
          
     except:
          # Movimiento con teclas
          # p1.update_player_speed(pressed_key)
          # p2.update_player_speed(pressed_key)
          pass
        

     # Mantiene jugadores en pantalla
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
     clock.tick(70)