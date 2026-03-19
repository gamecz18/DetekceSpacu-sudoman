import cv2
import time
from dataclasses import dataclass


@dataclass
class State:
    lastEyeTime: float
    bustedSaved: bool


def saveBusted(frame):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    cv2.putText(frame, "BUSTED!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    cv2.putText(frame, timestamp, (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)


    filename = f"BUSTED_{int(time.time())}.jpg"
    cv2.imwrite(filename, frame)
    print(f"Snímek uložen: {filename}")
    return True


def processFaceEye(frame, gray, state, faceCascade, eyeCascade):
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
    pocetBdelich = 0

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        roiHalfH = int(h / 2)
        roiGray = gray[y:y + roiHalfH, x:x + w]
        roiColor = frame[y:y + roiHalfH, x:x + w]

        minEyeSize = (int(w / 10), int(h / 10))

        eyes = eyeCascade.detectMultiScale(
            roiGray,
            scaleFactor=1.1,
            minNeighbors=12,
            minSize=minEyeSize
        )

        if len(eyes) > 0:
            state.lastEyeTime = time.time()
            state.bustedSaved = False

            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(roiColor, (ex, ey), (ex + ew, ey + eh), (0, 165, 255), 2)

        timeSinceEyes = time.time() - state.lastEyeTime
        pocetBdelich += 1
        print(f"Nevidím oči: {timeSinceEyes:.1f} sekund")


        if timeSinceEyes > 5 and not state.bustedSaved:
            state.bustedSaved = saveBusted(frame)
            pocetBdelich -= 1


    cv2.putText(frame, "Pocet bdelich: " + str(pocetBdelich), (100, 600), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)
    return frame, state


def main(videoPath="video.mp4"):
    cap = cv2.VideoCapture(videoPath)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    eyeCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_eye.xml")

    state = State(lastEyeTime=time.time(), bustedSaved=False)

    while True:
        ret, frame = cap.read()

        if not ret:
            print("Konec videa nebo nelze načíst kameru.")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame, state = processFaceEye(frame, gray, state, faceCascade, eyeCascade)

        cv2.imshow("Okno", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    return 0


if __name__ == '__main__':
    print("Starting the program...")
    """main(0)  # Pro webkameru """
    main("video4.mp4")