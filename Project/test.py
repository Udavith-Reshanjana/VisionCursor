import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)
mp_draw = mp.solutions.drawing_utils

# Screen size
screen_width, screen_height = pyautogui.size()

# Tip landmarks
tip_ids = [4, 8, 12, 16, 20]

# State flags
clicked = False
dragging = False
right_clicked = False

# Start camera
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        hand_landmarks = results.multi_hand_landmarks[0]
        lm_list = []
        for id, lm in enumerate(hand_landmarks.landmark):
            h, w = img.shape[:2]
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((id, cx, cy))

        if lm_list:
            # Move cursor with index finger
            _, x, y = lm_list[8]
            screen_x = int(x * screen_width / w)
            screen_y = int(y * screen_height / h)
            pyautogui.moveTo(screen_x, screen_y)

            # Finger detection
            fingers = []
            fingers.append(lm_list[4][1] > lm_list[3][1])  # Thumb
            for i in range(1, 5):
                fingers.append(lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2])
            total_fingers = fingers.count(True)

            # Left click (5 fingers)
            if total_fingers == 5:
                if not clicked:
                    pyautogui.click()
                    clicked = True
            else:
                clicked = False

            # Drag (2 fingers: index + middle)
            if total_fingers == 2 and fingers[1] and fingers[2]:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # Right click (3 fingers: index + middle + ring)
            if total_fingers == 3 and fingers[1] and fingers[2] and fingers[3]:
                if not right_clicked:
                    pyautogui.rightClick()
                    right_clicked = True
            else:
                right_clicked = False

        # Draw hand landmarks
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Mouse Control", img)
    if cv2.waitKey(1) & 0xFF == 27: # Escape key to exit
        break

cap.release()
cv2.destroyAllWindows()
