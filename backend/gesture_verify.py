import cv2
import mediapipe as mp
import json
import os
import math

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SAVE_FOLDER = os.path.join(BASE_DIR, "gesture_data")
os.makedirs(SAVE_FOLDER, exist_ok=True)

# MediaPipe objects will be initialized later
mp_hands = None
hands = None
mp_draw = None

DOT_RADIUS = 35


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

            distance = math.sqrt(
                (x - dx) ** 2 +
                (y - dy) ** 2
            )

            if distance < DOT_RADIUS:
                return dot

            dot += 1

    return None


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

        color = (255, 255, 255)

        if i in current_pattern:
            color = (0, 255, 0)

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


def verify_gesture(username):

    global mp_hands, hands, mp_draw

    # Initialize MediaPipe AFTER taking username input
    mp_hands = mp.solutions.hands

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )

    mp_draw = mp.solutions.drawing_utils

    filename = os.path.join(
    SAVE_FOLDER,
    f"{username}.json"
    )

    print("================================")
    print("Username :", username)
    print("Looking For :", filename)
    print("Exists :", os.path.exists(filename))
    print("================================")

    print("Checking file:", filename)

    if not os.path.exists(filename):
        print("❌ Gesture not registered.")
        return False

    with open(filename, "r") as f:
        registered_pattern = json.load(f)

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    recording = False

    pattern = []

    print("===================================")
    print(" Gesture Verification")
    print("Press S to Start")
    print("Press E to Verify")
    print("===================================")

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

                x = int(
                    hand_landmarks.landmark[8].x * w
                )

                y = int(
                    hand_landmarks.landmark[8].y * h
                )

                cv2.circle(
                    frame,
                    (x, y),
                    10,
                    (0, 255, 0),
                    -1
                )

                if recording:

                    dot = get_selected_dot(
                        x,
                        y,
                        frame
                    )

                    if dot is not None:

                        if len(pattern) == 0 or pattern[-1] != dot:

                            pattern.append(dot)

        cv2.putText(
            frame,
            f"Pattern : {pattern}",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 255),
            2
        )

        cv2.imshow(
            "Gesture Verification",
            frame
        )

        key = cv2.waitKey(1) & 0xFF

        if key == ord("s"):

            recording = True
            pattern = []

            print("Recording Started")

        elif key == ord("e"):

            recording = False

            cap.release()
            cv2.destroyAllWindows()

            print("Registered :", registered_pattern)
            print("Entered    :", pattern)

            if pattern == registered_pattern:

                print("Gesture Verified")

                return True

            else:

                print("Gesture Verification Failed")

                return False

        elif key == ord("q"):

            break

    cap.release()
    cv2.destroyAllWindows()

    return False


if __name__ == "__main__":

    print("===================================")
    print(" AirCanvas Secure")
    print(" Gesture Verification")
    print("===================================")

    username = input("\nEnter Username: ").strip()

    if username == "":
        print("❌ Username cannot be empty.")
        exit()

    print(f"\nUsername: {username}")

    if verify_gesture(username):
        print("\n✅ ACCESS GRANTED")
    else:
        print("\n❌ ACCESS DENIED")