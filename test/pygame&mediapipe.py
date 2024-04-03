import cv2
import pygame
import numpy as np
import mediapipe as mp
import sys
from pygame.locals import QUIT

# Inicializar Pygame
pygame.init()

# Configurar la ventana de Pygame
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hand Tracking with Pygame")

# Inicializar la captura de video con OpenCV
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

# Configurar el tamaño deseado para la pantalla
desired_width = 640
desired_height = 480
cap.set(3, desired_width)
cap.set(4, desired_height)

# Inicializar mediapipe para el seguimiento de manos
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5
)

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

    # Calcular las coordenadas para centrar el frame en la ventana de Pygame
    frame_center_x = (screen_width - frame.get_width()) // 2
    frame_center_y = (screen_height - frame.get_height()) // 2

    # Mostrar el frame centrado en la ventana de Pygame
    screen.blit(frame, (frame_center_x, frame_center_y))
    pygame.display.update()

    # Manejar eventos de Pygame
    for event in pygame.event.get():
        if event.type == QUIT:
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            sys.exit()
