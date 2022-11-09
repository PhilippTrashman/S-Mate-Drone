from time import sleep

from main import *

if __name__ == "__main__":
    start = GUI_mate()
    tello = Tello()
    root = Tk()
    lmain = Label(root)

    start.init(root, False)

    cam_state = True
    width, height = 800, 600

    if cam_state == True:
        print('Init cap...')
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        print('Cap initialized!')
        start.hand_track(lmain, cap)


    cont_var = StringVar(root, "0")
    throt_var = IntVar(root, 100)

    start.buttons(cont_var,throt_var, lmain, root)

    joy = XboxController()
    space = Space_call()
    help = 0
    xbox_flag = False
    space_flag = False
    while True:
        if root.state() != 'normal':    # Forcefully closes everything, calles Attribute and Traceback Errors
            root.destroy()

        if cam_state == True:           # If the cam has been enabled hand tracking will also start, not sure if this can be implemented to only start if enabled in the GUI
            start.hand_track(lmain, cap)    #type: ignore
       
        controller = cont_var.get()

        if controller == "1":           # Enters Xbox Controll Mode
            joy.flight_xbox(tello, help)
            print(joy.read())

        elif controller == "2":         # Should work with a Space Mouse, not yet tested
            if space_flag == False:
                dev = space.open(callback=None, button_callback=space.toggle_led)
                space_flag = True

            elif space_flag == True:
                space.flight(tello, help)

        elif controller == "3":         # used to controll the drone via face tracking
            print("Face tracking")
        
        elif controller == "4":
            print("Gesture tracking")
        
        root.update()
        sleep(0.001)



    # root.after(1, xbox)

    # root.mainloop()