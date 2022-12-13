import bpy
from mathutils import Euler
import math
import pathlib
loca = pathlib.Path(__file__).parent.resolve()
loca = str(loca)
loca = loca.replace("\\Dji-Tello.blend", "\\drone_data.txt")

class ModalTimerOperator(bpy.types.Operator):
    """Operator which runs itself from a timer"""
    bl_idname = "wm.modal_timer_operator"
    bl_label = "Modal Timer Operator"

    _timer = None

    def modal(self, context, event):
        if event.type in {'RIGHTMOUSE', 'ESC'}:
            self.cancel(context)
            return {'CANCELLED'}

        if event.type == 'TIMER':


            # calls data from a written txt
            with open(loca) as file:
                x = (0,0,0)
                for line in file:
                    x = line.split(",")
                pitch_y = int(x[0])
                pitch_y = pitch_y * -1
                roll_x = int(x[2])
                roll_x *= -1
                yaw_x = int(x[1])
                bpy.context.active_object.rotation_euler[0] = math.radians(yaw_x)  # x
                bpy.context.active_object.rotation_euler[1] = math.radians(pitch_y)  # y
                bpy.context.active_object.rotation_euler[2] = math.radians(roll_x)  # z
                
                                        
        return {'PASS_THROUGH'}

    def execute(self, context):
        wm = context.window_manager
        self._timer = wm.event_timer_add(0.1, window=context.window)
        wm.modal_handler_add(self)
        return {'RUNNING_MODAL'}

    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)


def menu_func(self, context):
    self.layout.operator(ModalTimerOperator.bl_idname, text=ModalTimerOperator.bl_label)


def register():
    bpy.utils.register_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.append(menu_func)


# Register and add to the "view" menu (required to also use F3 search "Modal Timer Operator" for quick access).
def unregister():
    bpy.utils.unregister_class(ModalTimerOperator)
    bpy.types.VIEW3D_MT_view.remove(menu_func)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.wm.modal_timer_operator()