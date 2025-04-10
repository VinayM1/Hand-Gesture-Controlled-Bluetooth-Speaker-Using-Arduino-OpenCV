import cv2
import mediapipe as mp
import serial
import time
import keyboard  # system-wide keypress control

# Setup Serial Communication
try:
    arduino = serial.Serial('COM9', 9600)  # Change COM port as needed
    time.sleep(2)
    print("✅ Arduino connected")
except:
    arduino = None
    print("⚠️ Arduino not connected")

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

# Webcam
cap = cv2.VideoCapture(0)
prev_gesture = None

# Gesture logic
def is_hand_open(landmarks):
    tips = [8, 12, 16, 20]  # Finger tips: index to pinky
    open_fingers = 0
    for tip in tips:
        if landmarks[tip].y < landmarks[tip - 2].y:
            open_fingers += 1
    return open_fingers >= 3

# Main loop
while True:
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(frame_rgb)

    gesture = None

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            if is_hand_open(hand_landmarks.landmark):
                gesture = "OPEN"
            else:
                gesture = "FIST"

            if gesture != prev_gesture:
                if gesture == "OPEN":
                    keyboard.press_and_release("play/pause media")
                    if arduino:
                        arduino.write(b'P')
                    print("🖐️ Gesture: OPEN → Play/Pause")
                elif gesture == "FIST":
                    keyboard.press_and_release("next track")
                    if arduino:
                        arduino.write(b'N')
                    print("✊ Gesture: FIST → Next Track")
                prev_gesture = gesture
    else:
        prev_gesture = None

    # Show current gesture
    cv2.putText(frame, f"Gesture: {gesture}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
