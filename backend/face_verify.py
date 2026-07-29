import cv2
import os

SAVE_FOLDER = "face_data"

orb = cv2.ORB_create(nfeatures=1000)
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)


def verify_face(username):

    registered_path = os.path.join(
        SAVE_FOLDER,
        f"{username}.jpg"
    )

    if not os.path.exists(registered_path):
        print("❌ Registered face not found.")
        return False

    registered = cv2.imread(registered_path)

    registered_gray = cv2.cvtColor(
        registered,
        cv2.COLOR_BGR2GRAY
    )

    kp1, des1 = orb.detectAndCompute(
        registered_gray,
        None
    )

    if des1 is None:
        print("❌ Could not extract features from registered face.")
        return False

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    print("=================================")
    print(" FACE VERIFICATION")
    print("Look at the Camera")
    print("Verifying Automatically...")
    print("=================================")

    frame_count = 0

    while True:

        ret, frame = cap.read()

        if not ret:
            break

        frame = cv2.flip(frame, 1)

        frame_count += 1

        cv2.putText(
            frame,
            "Look at the Camera...",
            (20, 40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (0, 255, 0),
            2
        )

        cv2.imshow(
            "Face Verification",
            frame
        )

        cv2.waitKey(1)

        # Verify after approximately 3 seconds
        if frame_count >= 90:

            gray = cv2.cvtColor(
                frame,
                cv2.COLOR_BGR2GRAY
            )

            kp2, des2 = orb.detectAndCompute(
                gray,
                None
            )

            if des2 is None:
                print("❌ No face features detected.")
                cap.release()
                cv2.destroyAllWindows()
                return False

            matches = bf.match(des1, des2)

            matches = sorted(
                matches,
                key=lambda x: x.distance
            )

            good_matches = [
                m for m in matches
                if m.distance < 45
            ]

            print(f"Good Matches: {len(good_matches)}")

            cap.release()
            cv2.destroyAllWindows()

            if len(good_matches) > 35:
                print("✅ Face Verified")
                return True
            else:
                print("❌ Face Verification Failed")
                return False

    cap.release()
    cv2.destroyAllWindows()

    return False


if __name__ == "__main__":

    username = input("Enter Username: ").strip()

    if verify_face(username):
        print("\n✅ ACCESS GRANTED")
    else:
        print("\n❌ ACCESS DENIED")