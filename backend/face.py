import cv2
import mediapipe as mp
import os

# -----------------------------
# Create folder to save faces
# -----------------------------
SAVE_FOLDER = "face_data"
os.makedirs(SAVE_FOLDER, exist_ok=True)

# -----------------------------
# MediaPipe Module
# -----------------------------
mp_face = mp.solutions.face_detection


# -----------------------------
# Face Registration Function
# -----------------------------
def register_face(username):

    # Create detector when needed
    face_detector = mp_face.FaceDetection(
        model_selection=0,
        min_detection_confidence=0.7
    )

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    if not cap.isOpened():
        face_detector.close()
        raise Exception("Could not open camera")

    print("====================================")
    print(" AirCanvas Secure - Face Registration")
    print("====================================")
    print("S -> Save Face")
    print("Q -> Quit")
    print("====================================")

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        results = face_detector.process(rgb)

        face_detected = False

        if results.detections:

            h, w, _ = frame.shape

            for detection in results.detections:

                face_detected = True

                bbox = detection.location_data.relative_bounding_box

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                bw = int(bbox.width * w)
                bh = int(bbox.height * h)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + bw, y + bh),
                    (0, 255, 0),
                    3
                )

                cv2.putText(
                    frame,
                    "FACE DETECTED",
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.8,
                    (0, 255, 0),
                    2
                )

        else:

            cv2.putText(
                frame,
                "NO FACE DETECTED",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                (0, 0, 255),
                2
            )

        cv2.putText(
            frame,
            "S - Save Face",
            (20, 80),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Q - Quit",
            (20, 115),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255, 255, 255),
            2
        )

        cv2.imshow("AirCanvas Secure - Face", frame)

        key = cv2.waitKey(1) & 0xFF
        print("KEY =", key)

        # -----------------------------
        # Save Face
        # -----------------------------
        if key == ord("s") or key == ord("S"):

            if face_detected:

                filename = os.path.join(
                    SAVE_FOLDER,
                    f"{username}.jpg"
                )

                cv2.imwrite(filename, frame)

                print("\n==============================")
                print("✅ Face Saved Successfully")
                print(f"👤 Username : {username}")
                print(f"📷 Saved As : {filename}")
                print("==============================")

                cap.release()
                cv2.destroyAllWindows()
                face_detector.close()

                return filename

            else:

                print("⚠ No face detected. Cannot save.")

        # -----------------------------
        # Quit
        # -----------------------------
        elif key == ord("q") or key == ord("Q") or key == 27:

            print("Registration Cancelled")

            cap.release()
            cv2.destroyAllWindows()
            face_detector.close()

            raise Exception("Face registration cancelled")

    cap.release()
    cv2.destroyAllWindows()
    face_detector.close()

    raise Exception("Face registration failed")
if __name__== "__main__":
    print(register_face("test"))