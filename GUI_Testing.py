from time import sleep
from tkinter import messagebox
from main import *
import threading

if __name__ == "__main__":

    # defining class objects
    start = GUI_mate()
    joy = XboxController()
    space = Space_call()
    hand = HandDetection()
    face = FaceTracking()
    tello = Tello()
    root = Tk()

    # Creating the camera Labels for the Drone
    lmain = Label(root)
    ldrone = Label(root)

    # Testing case to enable and disable the cameras
    cam_state = False
    cam_finger_track = False

    drone_state = True
    d_cam_state = True

    # Starting the Window

    start.init(root, False, tello)
    # setting the width and height for the Webcam
    width, height = 1920, 1080

    if cam_state == True:
        print('Init cap...')
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        print('Cap initialized!')

    if drone_state == True:
        tello.connect()
        
        if d_cam_state == True:

            print("turning the drone stream on...")
            tello.streamoff()
            tello.streamon()
            print("Stream turned on")
            

            face_cascade = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

    cam_direction = 0
    cont_var = StringVar(root, "0")
    dcam_var = StringVar(root, "0")
    throt_var = IntVar(root, 70)
    # Variables used to read Drones Speed and Accleration
    speed_var = IntVar(root, 0)


    battery_var =    StringVar(root, f'Battery:     {0}%')
    height_var =     StringVar(root, f'Height:      {0} cm')
    time_var =       StringVar(root, f'Flight Time: {0} s')
    temperatur_var = StringVar(root, f'Drone Temp:  {0} °C')
    barometer_var =  StringVar(root, f'Barometer:   {0} cm')

    face_distance_var = IntVar(root, 20)


    start.buttons(cont_var,throt_var, lmain, root, dcam_var, tello, speed_var, face_distance_var, battery_var,
        height_var, time_var, temperatur_var, barometer_var) 


    xbox_flag = False
    space_flag = False
    flight_flag = True
    throttle_comp = 0
    print("starting loop")
    helper = 0
    countdown = 0
    time_minutes = 0
    while True:         # The Loop is used as an alternative for tkinter.mainloop
        if root.state() != 'normal':        # Forcefully closes everything, calls Attribute and Traceback Errors
            start.total_annihilation(dcam_var, tello,  root)

        if countdown == 10 and drone_state == True:
            speed_var.set(start.get_drone_speed(tello))

            time = tello.get_flight_time()
            if time >= 120:
                
                time_minutes = time//60
                time_seconds = time - 60*time_minutes
                time_var.set(f'Flight Time: {time_minutes} min  {time_seconds} s')
            else:
                time_var.set(f'Flight Time: {time}')
            
            battery_var.set(f'Battery:     {tello.get_battery()}%')
            height_var.set(f'Height:      {tello.get_height()} cm')
            temperatur_var.set(f'Drone Temp:  {tello.get_temperature()} °C')
            barometer_var.set(f'Barometer:   {int(tello.get_barometer())} cm')
            countdown = 0

        if cam_state == True:               # If the cam has been enabled hand tracking will also start, not sure if this can be implemented to only start if enabled in the GUI
            start.Cam(lmain, cap)    #type: ignore
       
        cam_stream = dcam_var.get()
        controller = cont_var.get()
        speed = throt_var.get()
        distance = face_distance_var.get()
        
        if controller == "1":               # Xbox Controll Mode with GTA Config
            try:
                speed = joy.define_speed_xbox(speed)
                throt_var.set(speed)
                if drone_state == True:
                    helper, cam_direction = joy.flight_xbox(tello, helper, speed, cam_direction)   

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
                    space.flight(tello, help)
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
            if cam_finger_track == True:
                hand.tk_handflight(tello, cap, speed)    #type: ignore
            
            else:
                print('Init cap...')
                cap = cv2.VideoCapture(0)
                cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
                cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

                cam_state = True           
                print('Cap initialized!')  

        elif controller == "5":             # Xbox Controller with more classic Drone Controll
            speed = joy.define_speed_classic(speed)
            throt_var.set(speed)
            if drone_state == True:
                helper, cam_direction = joy.flight_xbox_classic(tello, helper, speed, cam_direction)
                
        if cam_stream == "1":               # Drone Stream
            start.drone_stream(tello, cam_direction)


        root.update()                       # Updates the UI, alternativ to mainloop
        countdown += 1
        sleep(1/60)


    # root.after(1, xbox)

    # root.mainloop()