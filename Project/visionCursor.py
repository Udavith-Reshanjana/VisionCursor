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

    if results.multi_hand_landmarks and results.multi_handedness:
        hand_landmarks = results.multi_hand_landmarks[0]
        hand_label = results.multi_handedness[0].classification[0].label  # 'Left' or 'Right'

        lm_list = []
        h, w = img.shape[:2]
        for id, lm in enumerate(hand_landmarks.landmark):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append((id, cx, cy))

        if lm_list:
            # Move mouse with index finger
            x, y = lm_list[8][1], lm_list[8][2]
            screen_x = int(x * screen_width / w)
            screen_y = int(y * screen_height / h)
            pyautogui.moveTo(screen_x, screen_y)

            # Detect fingers
            fingers = []

            # Thumb
            if hand_label == "Right":
                fingers.append(lm_list[4][1] > lm_list[3][1])  # Thumb right of joint
            else:  # Left
                fingers.append(lm_list[4][1] < lm_list[3][1])  # Thumb left of joint

            # Other fingers
            for i in range(1, 5):
                fingers.append(lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2])

            total_fingers = fingers.count(True)

            # Left click (5 fingers up)
            if total_fingers == 5:
                if not clicked:
                    pyautogui.click()
                    clicked = True
            else:
                clicked = False

            # Drag (index + middle)
            if fingers[1] and fingers[2] and total_fingers == 2:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # Right click (index + middle + ring)
            if fingers[1] and fingers[2] and fingers[3] and total_fingers == 3:
                if not right_clicked:
                    pyautogui.rightClick()
                    right_clicked = True
            else:
                right_clicked = False

        # Draw hand landmarks
        mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Gesture Mouse Control", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
