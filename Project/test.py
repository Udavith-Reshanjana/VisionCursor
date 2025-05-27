import cv2
import mediapipe as mp
import pyautogui

# Initialize MediaPipe and PyAutoGUI
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils
screen_width, screen_height = pyautogui.size()

# Landmark indices for finger tips and lower joints
tip_ids = [4, 8, 12, 16, 20]

# Start video capture
cap = cv2.VideoCapture(0)
clicked = False
dragging = False

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                h, w = img.shape[:2]
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                # Move mouse with index finger tip
                _, x, y = lm_list[8]
                screen_x = int(x * screen_width / w)
                screen_y = int(y * screen_height / h)
                pyautogui.moveTo(screen_x, screen_y)

                # Detect fingers up
                fingers = []
                # Thumb (check x direction)
                fingers.append(lm_list[4][1] > lm_list[3][1])
                # Other fingers (check y direction)
                for i in range(1, 5):
                    fingers.append(lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2])

                total_fingers = fingers.count(True)

                # Click if all 5 fingers are up
                if total_fingers == 5:
                    if not clicked:
                        pyautogui.click()
                        clicked = True
                else:
                    clicked = False

                # Drag if only index and middle fingers are up
                if fingers[1] and fingers[2] and not fingers[3] and not fingers[4]:
                    if not dragging:
                        pyautogui.mouseDown()
                        dragging = True
                else:
                    if dragging:
                        pyautogui.mouseUp()
                        dragging = False

            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow("Hand Mouse Control", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
