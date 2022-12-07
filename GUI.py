from time import sleep
from tkinter import messagebox
from PIL import Image,ImageTk
from src.main import *
import subprocess
from src.spacenavigator import Space_call

# myargs = [
#     "C:/Users/itlab/Desktop/blender-3.3.1-windows-x64/blender",     # File Path for the Blender Executable
#     "Pictures/Dji-Tello.blend"        # The File Path for the Blend file
#     ]
if __name__ == "__main__":

    # defining class objects
    start = GUI_mate()
    joy = XboxController()
    space = Space_call()
    hand = HandDetection()
    face = FaceTracking()
    tello = Tello() 
    root = Tk()


    icon = ImageTk.PhotoImage(Image.open("Pictures\Icon.png"))      #type: ignore
    mate = ImageTk.PhotoImage(Image.open("Pictures\Logo.png"))      #type: ignore
    root.iconphoto(False, icon)     #type: ignore
    # Creating the camera Labels for the Drone
    lmain = Label(root)
    ldrone = Label(root)

    # Testing case to enable and disable the cameras
    cam_state = False
    cam_finger_track = False

    drone_state = False
    yaw, roll, pitch = 0, 0, 0
    # try:
    #     blend = subprocess.Popen(myargs, stdin=subprocess.PIPE, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    # except:
    #     messagebox.showerror(title="Blender not Found", message="Check if you set the correct filepath for Blender\nChange it if necessary in the GUI.py file")
    # Starting the Window

    start.init(root, False, tello)
    # setting the width and height for the Webcam
    width, height = 1980, 1080

    if cam_state == True:
        print('Init cap...')
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        print('Cap initialized!')

    if drone_state == True:
        tello.connect()

    cam_direction = 0

    fly_flag = IntVar(root, 0)
    cont_var = StringVar(root, "0")
    fcam_var = IntVar(root, 0)
    dcam_var = StringVar(root, "0")
    throt_var = IntVar(root, 70)
    # Variables used to read Drones Speed and Accleration
    speed_var = IntVar(root, 0)

    drone_var = IntVar(root, 0)

    battery_var =    StringVar(root, f'Battery:     {0}%')
    height_var =     StringVar(root, f'Height:      {0} cm')
    time_var =       StringVar(root, f'Flight Time: {0} s')
    temperatur_var = StringVar(root, f'Drone Temp:  {0} °C')
    barometer_var =  StringVar(root, f'Barometer:   {0} cm')

    face_distance_var = IntVar(root, 20)


    start.buttons(cont_var,throt_var, lmain, root, dcam_var, tello, speed_var, face_distance_var, battery_var,
        height_var, time_var, temperatur_var, barometer_var, drone_var, fcam_var, fly_flag) 


    xbox_flag = False
    space_flag = False
    flight_flag = True
    gesture_flag = False
    throttle_comp = 0
    print("starting loop")
    helper = 0
    countdown = 0
    time_minutes = 0
    while True:         # The Loop is used as an alternative for tkinter.mainloop
        if root.state() != 'normal':        # Forcefully closes everything, calls Attribute and Traceback Errors
            start.total_annihilation(dcam_var, tello,  root)
            break

        connection_stat = drone_var.get()
        if connection_stat == 1:
            if drone_state == False:
                tello.connect()
                tello.streamon()
                drone_state = True

        helper2 = fly_flag.get()
        if drone_state == True:
            pitch = tello.get_pitch()
            roll = tello.get_roll()
            yaw = tello.get_yaw()
            if helper2 == 1:
                try:
                    if helper == 0:
                        tello.takeoff()
                        helper = 1

                except:
                    fly_flag.set(0)

            if helper2 == 0:
                try:
                    if helper == 1:
                        tello.land()
                        helper = 0

                except:
                    helper = 0

            if countdown >= 10:
                speed_var.set(start.get_drone_speed(tello))

                time = tello.get_flight_time()
                if time >= 120:

                    time_minutes = time//60
                    time_seconds = time - 60*time_minutes
                    time_var.set(f'Flight Time: {time_minutes} min  {time_seconds} s')
                else:
                    time_var.set(f'Flight Time: {time} s')

                battery_var.set(f'Battery:     {tello.get_battery()}%')
                height_var.set(f'Height:      {tello.get_height()} cm')
                temperatur_var.set(f'Drone Temp:  {tello.get_temperature()} °C')
                barometer_var.set(f'Barometer:   {int(tello.get_barometer())} cm')
                countdown = 0

        with open("drone_data.txt", "w") as txt:
            txt.write(f'{pitch},{roll},{yaw}')

        # Requesting the Values from the Variables
        fcam_stream = fcam_var.get()       
        cam_stream = dcam_var.get()
        controller = cont_var.get()
        speed = throt_var.get()
        distance = face_distance_var.get()
        # responsible for either showing the cam or our addiction  
        if fcam_stream == 1:
            if cam_state == False:
                print('Init cap...')
                cap = cv2.VideoCapture(0)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
                print('Cap initialized!') 
                cam_state = True  
            else:         
                img = hand.tk_handflight(tello, cap, speed, gesture_flag)       #type: ignore
                start.Cam(lmain, img)    #type: ignore
        
        elif fcam_stream == 0:
            lmain.configure(image=mate)
        # Main Part for the Controlls
        if controller != "4":               # Needed so the Gesture controll doesnt always send Commands
            gesture_flag = False

        if controller == "1":               # Xbox Controll Mode with GTA Config
            speed = joy.define_speed_xbox(speed)
            throt_var.set(speed)

            try:
                try:
                    helper, cam_direction = joy.flight_xbox(tello, helper, speed, cam_direction)   

                except:
                    cont_var.set("0")
                    messagebox.showerror(title="Controller Error", message="The drone doesnt seem to be connected")
            except:
                cont_var.set("0")
                print("couldnt send command")
                messagebox.showerror(title="Controller Error", message="Couldnt Procced with controll Method \nCheck if your Xbox Controller is properly connected")    
            
        elif controller == "2":             # Space Mouse, not yet tested
            try:
                if space_flag == False:
                    dev = space.open(callback=None, button_callback=space.toggle_led)
                    space_flag = True

                elif space_flag == True:
                    helper = space.flight(tello, helper)
            except:
                cont_var.set("0")
                messagebox.showerror(title="Spacemouse Error", message="Couldnt Procced with controll Method \nCheck if your Spacemouse is properly connected")

        elif controller == "3":             # Face Tracking
            if drone_state == False:
                tello.connect()
                print("turning the drone stream on...")
                tello.streamoff()
                tello.streamon()
                print("Stream turned on")
                print("reading drone Frames...")
                drone_cam = tello.get_frame_read().frame
                print("frames read")                
                face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
                drone_state = True
            
            else:
                face.tk_facetrack(tello, distance, face_cascade)  #type: ignore
                cv2.destroyWindow("stream")

        elif controller == "4":             # Gesture Tracking
            if fcam_stream != 1:
                fcam_var.set(1)
            gesture_flag = True

        elif controller == "5":             # Xbox Controller with more classic Drone Controll
            speed = joy.define_speed_classic(speed)
            throt_var.set(speed)
            try:    
                try:
                    helper, cam_direction = joy.flight_xbox_classic(tello, helper, speed, cam_direction)
                except:
                    cont_var.set("0")
                    messagebox.showerror(title="Controller Error", message="The drone doesnt seem to be connected")
            except:
                cont_var.set("0")
                messagebox.showerror(title="Controller Error", message="The drone doesnt seem to be connected")

        # Drone Stream                
        if cam_stream == "1":
            try:
                start.drone_stream(tello, cam_direction)
            except:
                dcam_var.set("0")
                messagebox.showerror(title="Camera Error", message="Something went wrong with starting the Video Stream \nPlease try again or restart the Drone")
                pass

        # Helper variable to let the programm know if the Drone is currently in the Air
        if helper == 1:
            fly_flag.set(1)
        elif helper == 0:
            fly_flag.set(0)
        
        root.update()                       # Updates the UI, alternativ to tk.mainloop
        countdown += 1
        sleep(1/60)