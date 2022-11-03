from djitellopy import Tello
from FaceTracking import *

if __name__ == "__main__":
    tello = Tello()
    tello.connect()
    battery = tello.get_battery()
    print(battery)
    tello.streamoff()
    tello.streamon()
    sleep(1)
    tello.takeoff()
    tello.move_up(140)
    
    #Integer refers to distance(small numbers large distance / big numbers small distance). Rec. between 2 and 9
    face_track_fly(tello, 9)
    
    tello.streamoff()
    tello.land()