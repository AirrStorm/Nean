import cv2
import mediapipe as mp
import serial
import time


SERIAL_PORT = 'COM3'     
BAUD_RATE = 9600

ser = serial.Serial(SERIAL_PORT, BAUD_RATE)
time.sleep(2) 

#MEDIAPIPE SETUP
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# CAMERA 
cap = cv2.VideoCapture(0)

def hand_is_open(landmarks):

    fingers = []

    # Thumb 
    fingers.append(landmarks[4].x < landmarks[3].x)

    # Other fingers
    finger_tips = [8, 12, 16, 20]
    finger_pips = [6, 10, 14, 18]

    for tip, pip in zip(finger_tips, finger_pips):
        fingers.append(landmarks[tip].y < landmarks[pip].y)

    return fingers.count(True) >= 3  # 3+ fingers = OPEN


last_state = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if hand_is_open(hand_landmarks.landmark):
                state = 'O'
                cv2.putText(frame, "OPEN", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            else:
                state = 'C'
                cv2.putText(frame, "CLOSED", (20, 50),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

            # Send only if state changes
            if state != last_state:
                ser.write(state.encode())
                last_state = state

    cv2.imshow("Robotic Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to quit
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
