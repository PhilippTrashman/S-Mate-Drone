# VW-DJI-tello (S_Mate Drohne)
## A project about controlling the DJI Tello drone through a script. -->

To start the script first install the requirements and run GUI.py

## Controll Methods include:
 - an Xbox Controller (Two controll settings)
 - 3D Spacemouse
 - Facetracking
 - Gesture Tracking

The Drone Camera can be turned on by clicking the corresponding Button

### Blender:
An additional feature is seeing the drone's rotation in Blender, you only need to set your Blender executable, a modell of the Drone is included in the Pictures folder and is set as the standard.

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
