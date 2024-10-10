import cv2
import mediapipe as mp
import numpy as np
import pygame
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
windowSize = (900, 600) # W, H
screen = pygame.display.set_mode(windowSize)
clock = pygame.time.Clock()

# Inicializar la captura de video con OpenCV
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW) #* Laptop Cam
# cap = cv2.VideoCapture(1, cv2.CAP_DSHOW) #* Web Cam

# Definir objetos
ball = Ball(20)
p1 = Player(1)
p2 = Player(2)
pressed_key = set()
game_manager = GameManager(p1, p2, ball, windowSize, screen, pressed_key, cap)

# Ball
ball.get_ball_start(windowSize)

# Players
p1.get_player_start(windowSize)
p2.get_player_start(windowSize)


# Configurar el tamaño deseado para la camara
desired_width = 160
desired_height = 120

cap.set(cv2.CAP_PROP_FRAME_WIDTH, desired_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, desired_height)


# Inicializar mediapipe para el seguimiento de manos
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
     min_detection_confidence=0.65,
     static_image_mode=False,
     max_num_hands=2,
)


# Detect players variables
position = ['left', 'right']
players = [
    {'name': 'Player 1','position': 'left', 'x': 423,'y': windowSize[1]/2,'z': 0},
    {'name': 'Player 2','position': 'right','x': 474,'y': windowSize[1]/2,'z': 0}
]

def hand_tracking_thread():
     # global players
     while True:
          ret, frame = cap.read()
          # x, y, c = frame.shape
          
          if not ret:
               break
          
          frame = cv2.resize(frame, (desired_width, desired_height))
          height, width, c = frame.shape
          
          # Voltear el frame horizontalmente
          frame = cv2.flip(frame, 1)
          frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

          # Procesar las manos
          result = hands.process(frame_rgb)

          # Dibujar las manos
          if result.multi_hand_landmarks:
               for hand_landmarks in result.multi_hand_landmarks:
                    # Drawing landmarks on frames
                    # mp_drawing.draw_landmarks(
                    #      frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                    # )
                    
                    # Get landmark 9
                    point = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
                    
                    # Draw a circle for each player
                    color = (0, 255, 0) if point.x * windowSize[0] >= 450 else (226, 96, 255) # Color player
                    cv2.circle(frame, (int(point.x * desired_width), int(point.y * desired_height)), 5, color, -1)
                    
                    # Decide al jugador respecto al eje 'x'
                    player_index = 1 if int(point.x * windowSize[0]) >= 450 else 0
    
                    # Actualizar las coordenadas del jugador correspondiente
                    players[player_index]['x'] = int(point.x * windowSize[0])
                    players[player_index]['y'] = int(point.y * windowSize[1])
                    players[player_index]['z'] = point.z
                    

          # Draw a line in the middle of the frame
          cv2.line(frame, (desired_width // 2, 0), (desired_width // 2, desired_height), (0, 0, 255), 2)


          # Convertir el frame de OpenCV a formato Pygame
          frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
          frame = np.rot90(frame)
          
          frame = pygame.surfarray.make_surface(frame)
          frame = pygame.transform.flip(frame, True, False)
          frame_center_x = (900 - frame.get_width()) // 2

          # Mostrar el frame en la ventana de Pygame
          screen.blit(frame, (frame_center_x, 0))
          pygame.display.update()
          
          
 
# Musics
sound_v = pygame.mixer.Sound("module/resource/Veo en ti la luz.mp3")
sound_1 = pygame.mixer.Sound("module/resource/lv-3-65586.mp3")
 
# Variables
first_round = True
start_button = False
while True:
     # Pinta la pantalla al rededor de la camara
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


     # Start game
     if not start_button:
          start_button = game_manager.start_game(start_button, clock)
          pygame.mixer.music.stop()
          
          # Create the hand tracking thread
          hand_tracking_thread = threading.Thread(target=hand_tracking_thread)
          hand_tracking_thread.start()


     if first_round:
          # Permite eventos mientras sacan
          screen.fill(BLACK)
          channel1 = sound_1.play(-1)
          channel1.set_volume(1.0)

          time_elapsed = 0
          while time_elapsed < 3000: # 1000 milisegundos (1 segundo)
               game_manager.draw_game()
               game_manager.get_event()
               pygame.display.update()
               time_elapsed += clock.tick(60)
               
          first_round = False

          
     # Sorpresa Vianny
     if pygame.K_v in pressed_key: 
          sound_1.stop()
          pygame.mixer.music.play(-1)
          pygame.mixer.music.set_volume(1.0)
     
     
     #* --- Zona de animación --- 
     # Movimiento con las manos
     # if not hand_pos_queue.empty():
     #      players = hand_pos_queue.get_nowait()
     
     
     # Movimientos de los jugadores con vision por computadora y teclas
     # p1.update_player_speed(pressed_key, players[0]['y'])
     # p2.update_player_speed(pressed_key, players[1]['y'])
     
     p1.player_movement_hands(windowSize, players[0]['y'])
     p2.player_movement_hands(windowSize, players[1]['y'])
     

     # Movimiento con teclas
     # p1.update_player_speed(pressed_key)
     # p2.update_player_speed(pressed_key)
     
     # # Mantiene jugadores en pantalla
     # p1.player_movement(windowSize)
     # p2.player_movement(windowSize) 


     # Movimiento de la pelota
     game_manager.ball_restart(clock, players)
     ball.ball_movement(windowSize)

     # Golpeo de pelota
     game_manager.collision_ball()

     #* --- Zona de dibujo ---
     game_manager.draw_game()

     # Actualizar la pantalla completa
     pygame.display.flip()
     clock.tick(75) # Frames por segundo