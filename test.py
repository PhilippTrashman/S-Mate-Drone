from djitellopy import Tello
from GestureandFaceTracking import *
from mediapipe import *

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    battery = tello.get_battery()
    print(battery)
    tello.streamoff()
    tello.streamon()
    sleep(1)
    tello.takeoff()
    tello.move_up(100)
    
    #Integer refers to distance(small numbers large distance / big numbers small distance). Rec. between 2 and 8
    face_track_fly(tello, 20)
    #hand_tracking()
    tello.streamoff()
    tello.land()
    tello.turn_motor_on()
    sleep(10)
    tello.turn_motor_off()