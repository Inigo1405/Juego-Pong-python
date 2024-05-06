import cv2
import numpy as np
import mediapipe as mp
# import tensorflow as tf


# Initialize mediapipe
mpHands = mp.solutions.hands
hands = mpHands.Hands(max_num_hands=2, min_detection_confidence=0.7)
mpDraw = mp.solutions.drawing_utils



# Initialize video capture
cap = cv2.VideoCapture(1)

position = ['left', 'right']

players = [
    {
        'name': 'Player 1',
        'position': 'left',
        'score': 0,
        'x': 0,
        'y': 0,
        'z': 0
    },
    {
        'name': 'Player 2',
        'position': 'right',
        'score': 0,
        'x': 0,
        'y': 0,
        'z': 0
    }
]


while True:
    ret, frame = cap.read()
    x, y, c = frame.shape
    # print(x, y, c)
    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Get hand landmark prediction
    result = hands.process(framergb)

    # post process the result
    if result.multi_hand_landmarks:
        print(len(result.multi_hand_landmarks))
        landmarks = []
        for count, hand_landmarks in enumerate(result.multi_hand_landmarks):
            # Get landmark 9
            point = hand_landmarks.landmark[mpHands.HandLandmark.MIDDLE_FINGER_MCP]

            # Access to cordenates
            players[count]['x'] = point.x
            players[count]['y'] = point.y
            players[count]['z'] = point.z

            # print(f'Coordenadas del dedo pulgar: x={point_x}, y={point_y}, z={point_z}')

            for lm in hand_landmarks.landmark:
                lmx = int(lm.x * x)
                lmy = int(lm.y * y)
                landmarks.append([lmx, lmy])

            # Drawing landmarks on frames
            mpDraw.draw_landmarks(frame, hand_landmarks,
                                  mpHands.HAND_CONNECTIONS)



    # Show the point position of player 1 on the frame (left)
    cv2.putText(frame, f"x={players[0]['x']}", (10, 100), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, f"y={players[0]['y']}", (10, 120), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 1, cv2.LINE_AA)
    cv2.putText(frame, f"z={players[0]['z']}", (10, 140), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 255, 0), 1, cv2.LINE_AA)
    
    # Show the point position of player 2 on the frame (right)
    cv2.putText(frame, f"x={players[1]['x']}", (y-100, 100), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f"y={players[1]['y']}", (y-100, 120), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, f"z={players[1]['z']}", (y-100, 140), cv2.FONT_HERSHEY_SIMPLEX,
                0.5, (0, 0, 255), 1, cv2.LINE_AA)
    

    # Draw a line in the middle of the frame
    cv2.line(frame, (int(y/2), 0), (int(y/2), x), (0, 0, 255), 2)

    cv2.line(frame, (int(y/2)-130, 0), (int(y/2)-130, x), (150, 150, 255), 2)
    cv2.line(frame, (int(y/2)+130, 0), (int(y/2)+130, x), (150, 150, 255), 2)

    # Draw a circle for each player
    cv2.circle(frame, (int(players[0]['x']*y), int(players[0]['y']*x)), 30, (0, 255, 0), -1)
    cv2.circle(frame, (int(players[1]['x']*y), int(players[1]['y']*x)), 30, (0, 0, 255), -1)



    # Show the final output
    cv2.imshow("Output", frame)

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
