from tkinter import *
from tkinter import messagebox
from spacenavigator import *
from xbox_controller import *
import PIL.Image, PIL.ImageTk
import time  
from tello_control_ui import *

def connect():
    tello = Tello()
    tello.connect

def controll(controll):

    print(controll)

def controll_selection():
    root = Tk()
    root.geometry('250x150')

    label = LabelFrame(root, text='Choose your input method') 
    label.pack(expand = "yes", fill="both")

    btn_confirm = Button(label,text= "confirm", command=root.quit)
    btn_confirm.place(x = 30, y = 10) 

    xbox_con = Checkbutton(label, text = "Xbox Controller", onvalue=1, offvalue=0, command=controll("xbox"))
    xbox_con.place(x=30,y=50)
    space = Checkbutton(label, text = "Space Mouse", command = controll("spacemouse"))
    space.place(x=30, y=80)

    mainloop()

def xbox():
    print("xbox controlls")
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
    file_menu.add_command(label='Settings', command=controll_selection) 
    file_menu.add_separator() 
    file_menu.add_command(label='Exit', command=win.quit) 
    help_menu = Menu(mn) 
    mn.add_cascade(label='Help', menu=help_menu) 
    help_menu.add_command(label='Feedback') 
    help_menu.add_command(label='Contact') 

def scale (window):
    sc1= Scale(window, from_=100, to=10, sliderlength= 50, length= 250, width= 25) 
    sc1.pack() # Must implement speed controll with drone (set_speed(x))

def throttle(val):
    val = int(val)
    tello = Tello()
    tello.set_speed(val)
    print(val)

if __name__ == "__main__":
    window =  TelloUI
    win = Tk()
    # Name
    win.title("S-Mate Drone :)")
    # Window size
    win.geometry('1080x720')
    # Icon
    pic = PhotoImage(file= "icon.png")
    win.iconphoto(False, pic)

    # Button Options an their placements on the windows
    # btn=Button(win,text="Camera on", width=10,height=2,command=cam_on)
    btn2 = Button(win, text = "Xbox", width=10, height=2, command=xbox)
    btn_con = Button(win, text="connect", width=10, height=2, command=connect())
    btn_exit = Button(win, text="Exit", width=10, height=2, command=win.quit, background= "red")

    menus(win)
    sca = Scale(win, from_=100, to=10, sliderlength= 50, length= 250, width= 25, command = throttle)


    # btn.place(x=10,y=20)
    btn_con.pack(side= 'top', anchor=W, pady= 2, padx= 4)
    btn2.pack(side= 'top', anchor=W, pady= 2, padx= 4)
    btn_exit.pack(side='bottom',anchor=E, pady= 2, padx= 4)
    sca.pack(side='top',anchor=E, fill=Y)



    win.mainloop()