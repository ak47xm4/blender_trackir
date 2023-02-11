bl_info = {
    "name": "trackir mijo",
    "blender": (3, 0, 40),
    "category": "3D View",
    "author": "mijo",
    "location": "View3D > left-side panel >  ",
    "description":"",
    "warning": "",
    "wiki_url":"",
    "tracker_url": "",
    "version":(0,2,0)
}

# from . import b3d_trackir_Operator , b3d_trackir_Anim

from . import b3d_trackir_Operator , b3d_trackir_Anim

import bpy

def register():
    b3d_trackir_Anim.register()
    b3d_trackir_Operator.register()
    # print('test_register:')
    
def unregister():
    b3d_trackir_Anim.unregister()
    b3d_trackir_Operator.unregister()
    # print('test_unregister:')