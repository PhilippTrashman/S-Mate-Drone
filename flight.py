from spacenavigator import *
from xbox_controller import *
from djitellopy import Tello

# im trying my best to implement a toggable camera, but cant use the drone ;-;

def flight(controll_mode: str):#supported controll modes are currently spacemouse and xbox
    cam = False
    _cam_on()
    img = tello.get_frame_read().frame
    if controll_mode == "xbox":

        cont = XboxController()
        while True:

            print(cont.read())
            if cont.read()[15] == 1:
                easygui.msgbox("Press 'Ok' to engage throw takeoff",title="Info")
                tello.initiate_throw_takeoff()
                help += 1
            elif cont.read()[14] == 1 and help == 0:
                tello.takeoff()
                help += 1
                print("Takeoff")
            elif cont.read()[14] == 1 and help != 0:
                tello.land()
                break

            elif cont.read()[9] == 1:
                tello.flip("b")

            elif cont.read()[8] == -1:
                tello.flip("l")

            elif cont.read()[9] == -1:
                tello.flip("f")

            elif cont.read()[8] == 1:
                tello.flip("r")
            
            elif cont.read()[7] == 1 and cam == True:
                cam = False

            elif cont.read()[6] == 1 and cam == False:
                cam = True
            

            if cam == True:
                cv2.imshow("LiveStream", img)
                cv2.waitKey(1)

            tello.send_rc_control(int(cont.read()[0]*100), int(cont.read()[1]*100), int(cont.read()[16]*100), int(cont.read()[3]*100))
 
        
    elif controll_mode == "Spacemouse":
        print("Devices found:\n\t%s" % "\n\t".join(list_devices()))
        dev = open(callback=None, button_callback=toggle_led)
        help = 0

        while True:

            a = read()
            print(a)
            sleep(0.1)
            if a[7][1] == 1 and a[7][0] == 1:
                easygui.msgbox("Press 'Ok' to engage throw takeoff",title="Info")
                tello.initiate_throw_takeoff()
                help += 1
            elif a[7][1] == 1 and help == 0:
                tello.takeoff()
                help += 1
                print("Takeoff")
            elif a[7][1] == 1 and help != 0:
                tello.land()
                break
            elif a[7][0] == 1 and help != 0:
                tello.flip("r")
            tello.send_rc_control(int(a[4]*100), int(a[5]*100), int(a[3]*100), int(a[6]*100))

def _cam_on():
    Tello().streamon()
    Tello().set_video_resolution(Tello.RESOLUTION_720P)
    Tello().set_video_fps(Tello.FPS_30)

        
            


