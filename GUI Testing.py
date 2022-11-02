from tkinter import *
from tkinter import messagebox
from spacenavigator import *
from xbox_controller import *
import PIL.Image, PIL.ImageTk
import time

class MyVideoCapture:
    def __init__(self, video_source=0):

        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError("Unable to open video_source", video_source)
        
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)
    
    def get_frame(self):
        if self.vid.isOpend():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BAYER_BG2RGB))
            else:
                return (ret, None)
        
        else:
            return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

class App:
    def __init__(self, window, window_title, video_source=0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        # open video source (by default this will try to open the computer webcam)
        self.vid = MyVideoCapture(self.video_source)

        # Create a canvas that can fit the above video source size
        self.canvas = Canvas(window, width = self.vid.width, height = self.vid.height)
        self.canvas.pack()  

        # Button that lets the user take a snapshot
        self.btn_snapshot=Button(window, text="Snapshot", width=50, command=self.snapshot)
        self.btn_snapshot.pack(anchor=CENTER, expand=True)  

        # After it is called once, the update method will be automatically called every delay milliseconds
        self.delay = 15
        self.update()   
        self.window.mainloop() 

    def snapshot(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()   
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)) 
    def update(self):
        # Get a frame from the video source
        ret, frame = self.vid.get_frame()   
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW) 
        self.window.after(self.delay, self.update)
    

def cam_on(window):
    tello = Tello()
    tello.streamon()
    tello.set_video_resolution(Tello.RESOLUTION_720P)
    tello.set_video_fps(Tello.FPS_30)
    App(window, "TKinter and OpenCV")
    
def xbox():

    flight_xbox()

def btn_e(wind):
    btn_exit = Button(wind, text="Exit", width=10, height=2, command=wind.quit)
    return btn_exit

def menu_buttons():
    mb =  Menubutton ( win, text = 'Menu') 
    mb.grid() 
    mb.menu  =  Menu ( mb, tearoff = 0 ) 
    mb['menu']  =  mb.menu
    var1 = IntVar() 
    var2 = IntVar() 
    var3 = IntVar()
    mb.menu.add_checkbutton ( label ='Settings', variable = var1 ) 
    mb.menu.add_checkbutton ( label = 'Profile', variable = var2 ) 
    mb.menu.add_checkbutton ( label = 'Sign Out', variable = var3 ) 
    mb.pack() 

def menus(window):
    mn = Menu(window) 
    window.config(menu=mn) 
    file_menu = Menu(mn) 
    mn.add_cascade(label='File', menu=file_menu) 
    file_menu.add_command(label='New') 
    file_menu.add_command(label='Open...') 
    file_menu.add_command(label='Save') 
    file_menu.add_separator() 
    file_menu.add_command(label='About') 
    file_menu.add_separator() 
    file_menu.add_command(label='Exit', command=win.quit) 
    help_menu = Menu(mn) 
    mn.add_cascade(label='Help', menu=help_menu) 
    help_menu.add_command(label='Feedback') 
    help_menu.add_command(label='Contact') 

def scale (window):
    sc1= Scale(window, from_=100, to=10, sliderlength= 50, length= 250, width= 25) 
    sc1.pack() 

def video_stream():
    tl = Toplevel()


if __name__ == "__main__":

    win = Tk()
    # Name
    win.title("S-Mate Drone :)")
    # Window size
    win.geometry('1080x720')
    # Button Options an their placements on the windows
    btn=Button(win,text="Camera on", width=10,height=2,command=cam_on)
    btn2 = Button(win, text = "Xbox", width=10, height=2, command=xbox)

    btn_exit = Button(win, text="Exit", width=10, height=2, command=win.quit)

    menus(win)
    sca = Scale(win, from_=100, to=10, sliderlength= 50, length= 250, width= 25) 


    btn.place(x=10,y=20)
    btn2.place(x=10, y=70)
    btn_exit.place(x=990, y= 400)
    sca.place(x = 990, y = 20)

    # # Canvas for image placements
    # canvas = Canvas(win, width = 300, height = 300)  
    # canvas.pack()  
    # img = PhotoImage("my_reaction.jpeg")  
    # canvas.create_image(20, 20, anchor=NW, image=img)

    win.mainloop()