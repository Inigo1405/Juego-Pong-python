import cv2
import mediapipe as mp
import time

# Inicializar MediaPipe Hands
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# Variables para almacenar la posición de la mano y detectar agitación
prev_x = None
prev_time = None
prev_direction = None  # Dirección previa: None, 'izquierda' o 'derecha'
movement_threshold = 0.05  # Ajustado para definir el umbral de movimiento lateral
wave_detected = False
direction_changes = 0  # Contador de cambios de dirección
min_speed = 0.03  # Mínima velocidad para contar el gesto de agitar

def detectar_agitar_mano(landmarks):
    global prev_x, prev_time, prev_direction, direction_changes, wave_detected

    # Obtener la coordenada X de la muñeca (landmark 0)
    current_x = landmarks[0].x
    current_time = time.time()

    # Si es la primera vez, inicializar la posición anterior y el tiempo
    if prev_x is None:
        prev_x = current_x
        prev_time = current_time
        return False

    # Calcular la distancia movida y la velocidad de la mano
    distance = abs(current_x - prev_x)
    time_elapsed = current_time - prev_time
    speed = distance / time_elapsed if time_elapsed > 0 else 0

    # Verificar si el movimiento es suficientemente rápido
    if speed < min_speed:
        return False

    # Determinar la dirección del movimiento
    if current_x - prev_x > movement_threshold:
        current_direction = 'derecha'
    elif prev_x - current_x > movement_threshold:
        current_direction = 'izquierda'
    else:
        current_direction = prev_direction

    # Si la dirección ha cambiado y es rápido
    if current_direction != prev_direction and current_direction is not None:
        direction_changes += 1
        prev_direction = current_direction

    # Actualizar la posición y el tiempo previos
    prev_x = current_x
    prev_time = current_time

    # Detectar agitación de la mano
    if direction_changes >= 4:
        wave_detected = True
        direction_changes = 0
        return True

    return False

# Captura de video
cap = cv2.VideoCapture(0)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    # Convertir imagen de BGR a RGB
    image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Procesar la imagen con MediaPipe
    result = hands.process(image_rgb)

    # Si se detectan manos
    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Detectar si la mano se está agitando de lado a lado
            if detectar_agitar_mano(hand_landmarks.landmark):
                cv2.putText(frame, 'Saludando!', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
                print('Hola! :D')

    cv2.imshow('Agitar la mano de lado a lado con MediaPipe', frame)

    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()