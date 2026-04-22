import serial
import time

#Uncomment if on Wayland
# import os
# os.environ["QT_QPA_PLATFORM"] = "xcb"


## Import stuff
import cv2 as cv
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from math import sqrt


ser = serial.Serial('/dev/ttyACM0', 115200)

cam = cv.VideoCapture(0)
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
HandResult = mp.tasks.vision.HandLandmarkerResult
VisionRunningMode = mp.tasks.vision.RunningMode


latest_result = None
latest_hand = None
latest_frame = None


def print_result(result: HandResult, output_image: mp.Image, timestamp_ms: int): # type: ignore
    global latest_result
    latest_result = result

def draw_landmarks(frame, result):
    if result is None:
        return frame

    h, w, _ = frame.shape

    for hand in result.hand_landmarks:

        points = []

        for lm in hand:
            x = int(lm.x * w)
            y = int(lm.y * h)

            points.append((x, y))
            cv.circle(frame, (x, y), 5, (255, 255, 0), -1)

        connections = [
            (0,1),(1,2),(2,3),(3,4),
            (0,5),(5,6),(6,7),(7,8),
            (5,9),(9,10),(10,11),(11,12),
            (9,13),(13,14),(14,15),(15,16),
            (13,17),(17,18),(18,19),(19,20),
            (0,17)
        ]

        for c in connections:
            cv.line(frame, points[c[0]], points[c[1]], (0, 165, 255), 3)

    return frame

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='hand_landmarker.task'),
    running_mode=VisionRunningMode.LIVE_STREAM,
    result_callback=print_result)

def get_pixel(part_name):
    global latest_hand, latest_frame

    if latest_hand is None or latest_frame is None:
        return None

    landmarks = {
        "wrist": 0,

        "thumb_mcp": 2,
        "thumb_ip": 3,
        "thumb_tip": 4,

        "index_mcp": 5,
        "index_pip": 6,
        "index_dip": 7,
        "index_tip": 8,

        "middle_mcp": 9,
        "middle_pip": 10,
        "middle_dip": 11,
        "middle_tip": 12,

        "ring_mcp": 13,
        "ring_pip": 14,
        "ring_dip": 15,
        "ring_tip": 16,

        "pinky_mcp": 17,
        "pinky_pip": 18,
        "pinky_dip": 19,
        "pinky_tip": 20,
    }

    idx = landmarks[part_name]
    lm = latest_hand[idx]

    h, w, _ = latest_frame.shape

    x = int(lm.x * w)
    y = int(lm.y * h)

    magnitude = sqrt(x**2 + y**2)

    return magnitude

timestamp = 0

with HandLandmarker.create_from_options(options) as landmarker:


    while True:

        ret, frame = cam.read()

        if not ret:
            print("Camera not working")
            break


        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=frame
        )

        frame_rgb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        timestamp += 1

        land = landmarker.detect_async(mp_image,timestamp)

            
        latest_frame = frame

        if latest_result and latest_result.hand_landmarks:
            latest_hand = latest_result.hand_landmarks[0]
        

        finger_map = {
            "thumb": ("thumb_tip", "thumb_ip"),
            "index": ("index_tip", "index_pip"),
            "middle": ("middle_tip", "middle_pip"),
            "ring": ("ring_tip", "ring_pip"),
            "pinky": ("pinky_tip", "pinky_pip"),
        }

        finger_states = {}

        for finger, (tip_name, pip_name) in finger_map.items():

            tip = get_pixel(tip_name)
            pip = get_pixel(pip_name)

            if tip is None or pip is None:
                continue

            # Thumb uses X axis
            if finger == "thumb":
                if tip > pip:  # Adjust direction if needed
                    finger_states[finger] = "open"
                else:
                    finger_states[finger] = "closed"

            # Other fingers use Y axis
            else:
                if tip < pip:
                    finger_states[finger] = "open"
                else:
                    finger_states[finger] = "closed"

        print(finger_states)
        # Convert to Arduino string
        # Default state if no hand detected
        default_state = 'open'  
        arduino_fingers = ['thumb','index', 'middle', 'ring', 'pinky']

        # Fill in missing fingers with default
        for f in arduino_fingers:
            if f not in finger_states:
                finger_states[f] = default_state

        arduino_string = ",".join(f"{f}:{finger_states[f]}" for f in arduino_fingers) + "\n"
        print(arduino_string)

        ser.write(arduino_string.encode())

        annotated = draw_landmarks(frame, latest_result)

        cv.imshow("deez", annotated)

        key = cv.waitKey(1)

        if key == ord('q'):
            break

cam.release()
cv.destroyAllWindows()