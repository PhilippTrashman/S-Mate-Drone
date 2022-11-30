from time import sleep

import bpy
blender = bpy

def set_location(name, xyz):
    bpy.data.objects[name].location = xyz

def set_euler_rotation(name, xyz):
    bpy.data.objects[name].rotation_euler = xyz

def set_scale(name, xyz):
    bpy.data.objects[name].scale = xyz

x = 3.1415 * 0.5 
y = 3.1415 * 0.5
z = 3.1415 * 0.5

for obj in bpy.data.objects:
    print(obj.name)

