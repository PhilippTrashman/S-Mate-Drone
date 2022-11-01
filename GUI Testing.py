from tkinter import *
from tkinter import messagebox
from spacenavigator import *


def cam_on():
    tello = Tello()
    tello.streamon()
    tello.set_video_resolution(Tello.RESOLUTION_720P)
    tello.set_video_fps(Tello.FPS_30)
    while True:
        img = tello.get_frame_read().frame
        cv2.imshow("LiveStream", img)
        cv2.waitKey(1)

    flight()
    
def cam_off():
    flight()

def btn_e(wind):
    btn_exit = Button(win, text="Exit", width=10, height=2, command=win.quit)
    return btn_exit

if __name__ == "__main__":

    win = Tk()
    # Name
    win.title("S-Mate Drone :)")
    # Window size
    win.geometry('900x720')
    # Button Options an their placements on the windows
    btn=Button(win,text="Camera on", width=10,height=2,command=cam_on)
    btn2 = Button(win, text = "Camera off", width=10, height=2, command=cam_off)
    btn_exit = Button(win, text="Exit", width=10, height=2, command=win.quit)

    btn.place(x=10,y=20)
    btn2.place(x=10, y=70)
    btn_exit.place(x=10, y= 130)

    # Canvas for image placements
    canvas = Canvas(win, width = 300, height = 300)  
    canvas.pack()  
    img = PhotoImage("my_reaction.jpeg")  
    canvas.create_image(20, 20, anchor=NW, image=img) 

    win.mainloop()