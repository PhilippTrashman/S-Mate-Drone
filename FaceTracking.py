import cv2
from djitellopy import Tello


tello = Tello()
tello.connect()
tello.streamon()
#tello.turn_motor_on()

face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")



while True:
    frame = tello.get_frame_read().frame
    gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detected_faces = face_cascade.detectMultiScale(gray_image, 1.1, 4)
    print(detected_faces)
    for (x, y, w, h) in detected_faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0))

    cv2.imshow("Detection", frame)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
tello.streamoff()
#tello.turn_motor_off()
frame.release()