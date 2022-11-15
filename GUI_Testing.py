from time import sleep

from main import *

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

    # Starting the Window
    start.init(root, False)

    # Testing case to enable and disable the cameras
    cam_state = True

    drone_state = True
    d_cam_state = True

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


    cont_var = StringVar(root, "0")
    dcam_var = StringVar(root, "0")
    throt_var = IntVar(root, 70)


    start.buttons(cont_var,throt_var, lmain, root, dcam_var, tello) 


    xbox_flag = False
    space_flag = False
    flight_flag = True
    print("starting loop")
    while True:
        if root.state() != 'normal':        # Forcefully closes everything, calles Attribute and Traceback Errors
            start.total_annihilation(dcam_var, tello,  root)

        if cam_state == True:               # If the cam has been enabled hand tracking will also start, not sure if this can be implemented to only start if enabled in the GUI
            start.Cam(lmain, cap)    #type: ignore
       
        cam_stream = dcam_var.get()
        controller = cont_var.get()
        throttle = throt_var.get()

        if controller == "1":               # Enters Xbox Controll Mode
            joy.flight_xbox(tello)
            print(joy.read())

        elif controller == "2":             # Should work with a Space Mouse, not yet tested
            if space_flag == False:
                dev = space.open(callback=None, button_callback=space.toggle_led)
                space_flag = True

            elif space_flag == True:
                space.flight(tello, help)

        elif controller == "3":             # used to controll the drone via face tracking
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
                face.tk_facetrack(tello, 20, face_cascade)  #type: ignore

        elif controller == "4":             #Is the Gesture Tracking

            hand.tk_handflight(tello, cap, throttle)
                

        if cam_stream == "1":
            start.drone_stream(tello)

        root.update()
        sleep(1/60)



    # root.after(1, xbox)

    # root.mainloop()