import cv2
import mediapipe as mp
import json
import os
import math

# =====================================
# Create Gesture Folder
# =====================================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(BASE_DIR, "gesture_data")
os.makedirs(SAVE_FOLDER, exist_ok=True)
os.makedirs(SAVE_FOLDER, exist_ok=True)

DOT_RADIUS = 35


# =====================================
# Grid Selection Function
# =====================================

def get_selected_dot(x, y, frame):

    h, w = frame.shape[:2]

    center_x = w // 2
    center_y = h // 2

    spacing = 100

    dot = 1

    for row in range(-1, 2):

        for col in range(-1, 2):

            dx = center_x + col * spacing
            dy = center_y + row * spacing

            distance = math.sqrt((x - dx) ** 2 + (y - dy) ** 2)

            if distance < DOT_RADIUS:
                return dot

            dot += 1

    return None


# =====================================
# Draw Grid Function
# =====================================

def draw_grid(frame, current_pattern):

    h, w = frame.shape[:2]

    center_x = w // 2
    center_y = h // 2

    spacing = 100

    positions = []

    for row in range(-1, 2):

        for col in range(-1, 2):

            x = center_x + col * spacing
            y = center_y + row * spacing

            positions.append((x, y))

    for i, (x, y) in enumerate(positions, start=1):

        if i in current_pattern:
            color = (0, 255, 0)
        else:
            color = (255, 255, 255)

        cv2.circle(frame, (x, y), 18, color, -1)
        cv2.circle(frame, (x, y), 20, (0, 0, 0), 2)

        cv2.putText(
            frame,
            str(i),
            (x - 8, y - 28),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 255),
            2
        )


# =====================================
# Gesture Registration Function
# =====================================

def register_gesture(username):

    # Initialize MediaPipe INSIDE function
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    mp_draw = mp.solutions.drawing_utils

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        hands.close()
        raise Exception("Could not open camera")

    print("===========================================")
    print(" AirCanvas Secure - Pattern Registration")
    print("===========================================")
    print("S -> Start Recording Pattern")
    print("E -> Stop Recording & Save Pattern")
    print("Q -> Quit")
    print("===========================================")

    recording = False
    gesture_points = []
    pattern = []

    while True:

        success, frame = cap.read()

        if not success:
            break

        frame = cv2.flip(frame, 1)

        draw_grid(frame, pattern)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = hands.process(rgb)

        if results.multi_hand_landmarks:

            for hand_landmarks in results.multi_hand_landmarks:

                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS
                )

                h, w, _ = frame.shape

                x = int(hand_landmarks.landmark[8].x * w)
                y = int(hand_landmarks.landmark[8].y * h)

                cv2.circle(
                    frame,
                    (x, y),
                    10,
                    (0, 255, 0),
                    -1
                )

                if recording:

                    gesture_points.append([x, y])

                    selected = get_selected_dot(x, y, frame)

                    if selected is not None:

                        if not pattern or pattern[-1] != selected:

                            pattern.append(selected)

        # Draw Gesture Path
        if len(gesture_points) > 1:

            for i in range(1, len(gesture_points)):

                cv2.line(
                    frame,
                    tuple(gesture_points[i - 1]),
                    tuple(gesture_points[i]),
                    (255, 0, 255),
                    3
                )

        # Status
        if recording:
            status = "RECORDING PATTERN"
            status_color = (0, 0, 255)
        else:
            status = "READY"
            status_color = (0, 255, 0)

        cv2.putText(
            frame,
            f"Status : {status}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            status_color,
            2
        )

        cv2.putText(
            frame,
            f"Pattern : {pattern}",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 0),
            2
        )

        cv2.putText(
            frame,
            "S - Start | E - Save | Q - Quit",
            (20, 120),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow(
            "AirCanvas Secure - Pattern Registration",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        # =====================================
        # Start Recording
        # =====================================
        if key == ord("s") or key == ord("S"):

            recording = True
            gesture_points = []
            pattern = []

            print("\n================================")
            print("✅ Pattern Recording Started")
            print("================================")

        # =====================================
        # Stop Recording & Save Pattern
        # =====================================
        elif key == ord("e") or key == ord("E"):

            if recording:

                recording = False

                if not pattern:

                    print("⚠ No pattern detected.")
                    continue

                filename = os.path.join(
                    SAVE_FOLDER,
                    f"{username}.json"
                )

                with open(filename, "w") as file:

                    json.dump(pattern, file)

                print("\n================================")
                print("✅ Pattern Saved Successfully")
                print(f"👤 Username : {username}")
                print(f"🔢 Pattern : {pattern}")
                print(f"💾 Saved As : {filename}")
                print("================================")

                cap.release()
                cv2.destroyAllWindows()
                hands.close()

                return pattern

        # =====================================
        # Quit
        # =====================================
        elif key == ord("q") or key == ord("Q") or key == 27:

            cap.release()
            cv2.destroyAllWindows()
            hands.close()

            raise Exception("Gesture registration cancelled")

    cap.release()
    cv2.destroyAllWindows()
    hands.close()

    raise Exception("Gesture registration failed")

if __name__ == "__main__":

    print("===================================")
    print(" AirCanvas Secure")
    print(" Gesture Registration")
    print("===================================")

    username = input("Enter Username: ").strip()

    if username == "":
        print("Username cannot be empty.")
        exit()

    pattern = register_gesture(username)

    print("\nSaved Pattern:", pattern)