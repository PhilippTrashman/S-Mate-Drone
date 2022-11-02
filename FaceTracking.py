import cv2
from djitellopy import Tello

def resize(image):
    resized = cv2.resize(image, (600, 400), interpolation=cv2.INTER_LINEAR)
    return resized

def gray(image):
    gray_frame = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    return gray_frame

def controlling(faces):
    width_middle = 300
    height_middle = 200

    if faces[0] > width_middle:
        tello.rotate_clockwise(10)
    elif faces[0] < width_middle:
        tello.rotate_counter_clockwise(10)
    else:
        tello.send_keepalive()
    

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    tello.streamon()
    tello.takeoff()

    face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    while True:
        frame = tello.get_frame_read().frame
        frame = resize(frame)
        gray_image = gray(frame)
        detected_faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
        print(detected_faces)
        for (x, y, w, h) in detected_faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))

        cv2.imshow("Detection", frame)
        k = cv2.waitKey(30) & 0xff
        if k == 27:
            break
    tello.land()
    tello.streamoff()
    frame.release()