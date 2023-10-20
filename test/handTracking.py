import mediapipe as mp
import sys
import cv2

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)



with mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=4,
    min_detection_confidence=0.5
    ) as hands:
    
    while True:
        ret, frame = cap.read()
        if ret == False:
            break
        
        height, width, _ = frame.shape
        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        results = hands.process(frame_rgb)
        # print(results)
        
        # print(results.multi_handedness)
        # print(dir(results))
        # ['__add__', '__class__', '__class_getitem__', '__contains__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__getnewargs__', '__getstate__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__iter__', '__le__', '__len__', '__lt__', '__match_args__', '__module__', '__mul__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__rmul__', '__setattr__', '__sizeof__', '__slots__', '__str__', '__subclasshook__', '_asdict', '_field_defaults', '_fields', '_make', '_replace', 'count', 'index', 'multi_hand_landmarks', 'multi_hand_world_landmarks', 'multi_handedness']
        
        # Dibujar las manos
        if results.multi_hand_landmarks is not None:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                # print(mp_hands.HAND_CONNECTIONS)
                # print(len(mp_hands.HAND_CONNECTIONS))
                
                # print(dir(mp_hands))
                # ['HAND_CONNECTIONS', 'HandLandmark', 'Hands', 'NamedTuple', 'SolutionBase', '_BINARYPB_FILE_PATH', '__builtins__', '__cached__', '__doc__', '__file__', '__loader__', '__name__', '__package__', '__spec__', 'association_calculator_pb2', 'constant_side_packet_calculator_pb2', 'detections_to_rects_calculator_pb2', 'enum', 'gate_calculator_pb2', 'image_to_tensor_calculator_pb2', 'inference_calculator_pb2', 'logic_calculator_pb2', 'non_max_suppression_calculator_pb2', 'np', 'rect_transformation_calculator_pb2', 'split_vector_calculator_pb2', 'ssd_anchors_calculator_pb2', 'tensors_to_classification_calculator_pb2', 'tensors_to_detections_calculator_pb2', 'tensors_to_landmarks_calculator_pb2', 'thresholding_calculator_pb2']

            # print(results.multi_hand_landmarks)
            # print(len(results.multi_hand_landmarks))
                
        # Pantalla
        cv2.imshow("Hand Tracking", frame)
        if cv2.waitKey(1) & 0xff == 27:
            break
        
cap.release()
cv2.destroyAllWindows()