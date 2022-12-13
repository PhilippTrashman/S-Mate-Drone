# **VW-DJI-tello (S_Mate Drohne)**
## A project about controlling the DJI Tello drone through a script. -->

To start the script first install the requirements and run GUI.py

You first need to connect the Drone by checking if you're connected to its WiFi connection and clicking the "On" button in the Upper left corner
## Controll Methods include:
 - an Xbox Controller (GTA inspired controll and more Classic Drone controll methods)
 - 3D Spacemouse
 - Facetracking
 - Gesture Tracking

The Drone Camera can be turned on by clicking the corresponding Button

The Throttle Slider can be used to adjust the Drones maximum speed, but going under 18 results in the drone not actually moving

### Blender:
An additional feature is seeing the drone's rotation in Blender, you only need to set your Blender executable, a model of the Drone is included in the Pictures folder and is set as the standard.

it works by writing the drone rotation to the drone_data.txt and the data then gets read by the Blender model

(Different models arent supported as a seperate script has to be included in the blender model, if needed it can be copied from the included file)

## Requirements:
To install all the necessary modules just run the following code in your terminal 

    pip install -r requirements.txt

## The modules supporting the Programm are:
 - tkinter
 - Pillow
 - OpenCV
 - mediapipe
 - Inputs (from Zeth)
 - PywinUSB
 - DJI Tello API
 - Spacenavigator API

### **Regarding Controller Support**

You can check if your controller is properly connected by running "available_devices.py" in Controller_Testing, your controller should show up as an Xbox 360 controller.