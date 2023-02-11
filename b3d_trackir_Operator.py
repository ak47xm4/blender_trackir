'''
feature request:
    1. ani auto keyframe #OK
    2. smooth good to use 
        . del #OK
        shift+C #OK
    3. moving speed ctrl  #OK
    4. auto active trackir #OK
        but can't auto close py4Trackir for NOW
    
        
not support:
    viewport gizmo


update:
    ctrl+z undo is OK 


the original code from:
https://github.com/jkirsons/FacialMotionCapture_v2
https://github.com/johnflux/python_trackir

'''

import bpy
import time
import numpy
import math
import mathutils
#from bpy.props import FloatProperty

import subprocess
import sys

class OpenCVAnimOperator(bpy.types.Operator):
    """Operator which runs its self from a timer"""
    bl_idname = "wm.opencv_operator"
    bl_label = "OpenCV Animation Operator"
    bl_options = {'REGISTER','UNDO'}
    
    _timer = None
    _cap  = None
    
    stop :bpy.props.BoolProperty()
    
    # define a python 3 with tk
    py4Trackir = "C:\\Users\\Administrator\\AppData\\Local\\Programs\\Python\\Python310\\python.exe"

    # define trackir_log_to_txt.py
    py_log_to_csv= 'C:\\Users\\Administrator\\Documents\GitHub\\blender_trackir\\trackir_log_to_txt.py'



    # event type define
    evt_def = dict()
    evt_def['all_evt'] = []
    evt_def['TIMER'] =           ['TIMER']
    evt_def['vp_ctrl'] =         ['TIMER1','MIDDLEMOUSE' , 'WHEELUPMOUSE' ,'WHEELDOWNMOUSE','ACCENT_GRAVE','NUMPAD_PERIOD','LEFT_CTRL']
    evt_def['vp_force_detect'] = ['MOUSEMOVE','NONE']
    evt_def['ctrl'] =            ['LEFT_CTRL']

    for i in evt_def:
        if i != 'all_evt':
            evt_def['all_evt'].extend(evt_def[i])
        
    #print( evt_def )

    #all_fuck_type = ['NONE', 'LEFTMOUSE', 'MIDDLEMOUSE', 'RIGHTMOUSE', 'BUTTON4MOUSE', 'BUTTON5MOUSE', 'BUTTON6MOUSE', 'BUTTON7MOUSE', 'PEN', 'ERASER', 'MOUSEMOVE', 'INBETWEEN_MOUSEMOVE', 'TRACKPADPAN', 'TRACKPADZOOM', 'MOUSEROTATE', 'MOUSESMARTZOOM', 'WHEELUPMOUSE', 'WHEELDOWNMOUSE', 'WHEELINMOUSE', 'WHEELOUTMOUSE', 'EVT_TWEAK_L', 'EVT_TWEAK_M', 'EVT_TWEAK_R', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'ZERO', 'ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'LEFT_CTRL', 'LEFT_ALT', 'LEFT_SHIFT', 'RIGHT_ALT', 'RIGHT_CTRL', 'RIGHT_SHIFT', 'OSKEY', 'APP', 'GRLESS', 'ESC', 'TAB', 'RET', 'SPACE', 'LINE_FEED', 'BACK_SPACE', 'DEL', 'SEMI_COLON', 'PERIOD', 'COMMA', 'QUOTE', 'ACCENT_GRAVE', 'MINUS', 'PLUS', 'SLASH', 'BACK_SLASH', 'EQUAL', 'LEFT_BRACKET', 'RIGHT_BRACKET', 'LEFT_ARROW', 'DOWN_ARROW', 'RIGHT_ARROW', 'UP_ARROW', 'NUMPAD_2', 'NUMPAD_4', 'NUMPAD_6', 'NUMPAD_8', 'NUMPAD_1', 'NUMPAD_3', 'NUMPAD_5', 'NUMPAD_7', 'NUMPAD_9', 'NUMPAD_PERIOD', 'NUMPAD_SLASH', 'NUMPAD_ASTERIX', 'NUMPAD_0', 'NUMPAD_MINUS', 'NUMPAD_ENTER', 'NUMPAD_PLUS', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'F13', 'F14', 'F15', 'F16', 'F17', 'F18', 'F19', 'F20', 'F21', 'F22', 'F23', 'F24', 'PAUSE', 'INSERT', 'HOME', 'PAGE_UP', 'PAGE_DOWN', 'END', 'MEDIA_PLAY', 'MEDIA_STOP', 'MEDIA_FIRST', 'MEDIA_LAST', 'TEXTINPUT', 'WINDOW_DEACTIVATE', 'TIMER', 'TIMER0', 'TIMER1', 'TIMER2', 'TIMER_JOBS', 'TIMER_AUTOSAVE', 'TIMER_REPORT', 'TIMERREGION', 'NDOF_MOTION', 'NDOF_BUTTON_MENU', 'NDOF_BUTTON_FIT', 'NDOF_BUTTON_TOP', 'NDOF_BUTTON_BOTTOM', 'NDOF_BUTTON_LEFT', 'NDOF_BUTTON_RIGHT', 'NDOF_BUTTON_FRONT', 'NDOF_BUTTON_BACK', 'NDOF_BUTTON_ISO1', 'NDOF_BUTTON_ISO2', 'NDOF_BUTTON_ROLL_CW', 'NDOF_BUTTON_ROLL_CCW', 'NDOF_BUTTON_SPIN_CW', 'NDOF_BUTTON_SPIN_CCW', 'NDOF_BUTTON_TILT_CW', 'NDOF_BUTTON_TILT_CCW', 'NDOF_BUTTON_ROTATE', 'NDOF_BUTTON_PANZOOM', 'NDOF_BUTTON_DOMINANT', 'NDOF_BUTTON_PLUS', 'NDOF_BUTTON_MINUS', 'NDOF_BUTTON_ESC', 'NDOF_BUTTON_ALT', 'NDOF_BUTTON_SHIFT', 'NDOF_BUTTON_CTRL', 'NDOF_BUTTON_1', 'NDOF_BUTTON_2', 'NDOF_BUTTON_3', 'NDOF_BUTTON_4', 'NDOF_BUTTON_5', 'NDOF_BUTTON_6', 'NDOF_BUTTON_7', 'NDOF_BUTTON_8', 'NDOF_BUTTON_9', 'NDOF_BUTTON_10', 'NDOF_BUTTON_A', 'NDOF_BUTTON_B', 'NDOF_BUTTON_C', 'ACTIONZONE_AREA', 'ACTIONZONE_REGION', 'ACTIONZONE_FULLSCREEN', 'XR_ACTION']

    def get_trackir_data(trackir_data_dict):
        f = open('C:/tmp/trackir_data_test.txt', 'r')
        #print(f.read())
        lines = f.readlines()
        if len(lines) >0:
            #print(float(lines[0]))
            trackir_data_dict['roll'] = float(lines[0])
            trackir_data_dict['pitch'] = float(lines[1])
            trackir_data_dict['yaw'] = float(lines[2])
            trackir_data_dict['x'] = float(lines[3])
            trackir_data_dict['y'] = float(lines[4])
            trackir_data_dict['z'] = float(lines[5])
    
    def __init__(self):
        
        self.scene = bpy.context.scene # get the scene

        self.trackir_data = dict()
        self.trackir_data = {'roll':0,'pitch':0,'yaw':0,'x':0,'y':0,'z':0}

        self.trackir_data_rest = dict()
        self.trackir_data_rest = {'roll':0,'pitch':0,'yaw':0,'x':0,'y':0,'z':0}

        self.cam = bpy.data.objects[bpy.context.scene.xform_obj]

        self.cam_rest = dict()
        self.cam_rest = {'rx':0,'ry':0,'rz':0,'tx':0,'ty':0,'tz':0}

        self.eee = 1 # enable
        self.eee2 = 0 # enable 2
        
        self.temp_mmm = bpy.context.scene.moving_mult
        
        # NEW 20220904
        self.inv = self.cam.matrix_world.copy()
        
        # NEW 20220909
        self.ctrl = False
        self.p = subprocess.Popen([py4Trackir,py_log_to_csv], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    
        
        
    def modal(self, context, event):
        # protect undo
        self.scene =  bpy.context.scene
        self.cam = self.cam = bpy.data.objects[bpy.context.scene.xform_obj]
        
        if (event.type in {'ESC'}) or self.stop == True: #{ 'RIGHTMOUSE','ESC'}
            #self.cancel(context)
            self.cancel(context)
            return {'CANCELLED'}
        
        # protect undo
        if ( event.type in evt_def['ctrl'] and ( event.value == 'PRESS' ) ) :
            self.ctrl = True
        elif ( event.type in evt_def['ctrl'] and ( event.value == 'RELEASE' ) ) :
            self.ctrl = False
        
        
        if (event.type in evt_def['all_evt'] ) and ( self.ctrl==False ): 
            #print(event.type)
            if (event.type in  evt_def['TIMER'] ): 
                get_trackir_data(self.trackir_data)
                
                if self.eee ==1 :
                    temp_xxx = self.trackir_data['x']-self.trackir_data_rest['x']
                    temp_yyy = self.trackir_data['y']-self.trackir_data_rest['y']
                    temp_zzz = self.trackir_data['z']-self.trackir_data_rest['z']
                    
                    # to local move
                    vec = mathutils.Vector(( temp_xxx , temp_yyy , temp_zzz ))
                    self.inv = self.cam.matrix_world.copy()
                    self.inv.invert()
                    vec_rot = vec @ self.inv
                    
                    # assign rot
                    temp_pitch = self.trackir_data['pitch']-self.trackir_data_rest['pitch']
                    temp_roll  = self.trackir_data['roll']-self.trackir_data_rest['roll']
                    temp_yaw   = self.trackir_data['yaw']-self.trackir_data_rest['yaw']
                    
                    self.cam.rotation_euler[0] = self.cam_rest['rx']+temp_pitch / (360/(math.pi*2))
                    self.cam.rotation_euler[1] = self.cam_rest['ry']+temp_roll / (360/(math.pi*2))
                    self.cam.rotation_euler[2] = self.cam_rest['rz']-temp_yaw / (360/(math.pi*2))
                    
                    # local move
                    self.cam.location[0] = self.cam_rest['tx']+vec_rot[0] * self.temp_mmm
                    self.cam.location[1] = self.cam_rest['ty']+vec_rot[1] * self.temp_mmm
                    self.cam.location[2] = self.cam_rest['tz']+vec_rot[2] * self.temp_mmm
                    
                    
                    
                    if self.scene.force_autokeyframe:
                        self.cam.keyframe_insert('location')
                        self.cam.keyframe_insert('rotation_euler')
                    
            elif (event.type not in evt_def['TIMER'] ):
                if (event.type in evt_def['vp_ctrl'] ): 
                    self.eee = 0
                    self.eee2 = 0
                    
                    self.trackir_data_rest = dict(self.trackir_data) # IMPORTANT
                    
                elif (event.type in evt_def['vp_force_detect'] ):
                    if self.eee2 <= 0:
                        self.eee = 0
                        
                        self.cam =  bpy.data.objects[bpy.context.scene.xform_obj]
                        self.cam_rest['rx'] = self.cam.rotation_euler[0]
                        self.cam_rest['ry'] = self.cam.rotation_euler[1]
                        self.cam_rest['rz'] = self.cam.rotation_euler[2]
                        self.cam_rest['tx'] = self.cam.location[0]
                        self.cam_rest['ty'] = self.cam.location[1]
                        self.cam_rest['tz'] = self.cam.location[2]
                        
                    else:
                        self.eee = 1
                    self.eee2 += 1
            
        return {'PASS_THROUGH'}
    
    def execute(self, context):
        
        self.cam_rest['rx'] = self.cam.rotation_euler[0]
        self.cam_rest['ry'] = self.cam.rotation_euler[1]
        self.cam_rest['rz'] = self.cam.rotation_euler[2]
        self.cam_rest['tx'] = self.cam.location[0]
        self.cam_rest['ty'] = self.cam.location[1]
        self.cam_rest['tz'] = self.cam.location[2]
        
        get_trackir_data(self.trackir_data)
        self.trackir_data_rest = dict(self.trackir_data)
        
        wm = context.window_manager
        self._timer = wm.event_timer_add(1/120.0, window=context.window)
        wm.modal_handler_add(self)
        print('trackir_START~~~~~~~~~~~~~~~~~~~~~~~~~')
        return {'RUNNING_MODAL'}
        
        
    def cancel(self, context):
        wm = context.window_manager
        wm.event_timer_remove(self._timer)
        #self._cap.release()
        self._cap = None
        print('trackir_CANCELLED ~~~~~~~~~~~~~~~~~~~~~')


def register():
    bpy.utils.register_class(OpenCVAnimOperator)

def unregister():
    bpy.utils.unregister_class(OpenCVAnimOperator)
    
    
'''
if __name__ == "__main__":
    register()

    # test call
    #bpy.ops.wm.opencv_operator()



'''