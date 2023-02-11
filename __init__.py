bl_info = {
    "name": "trackir mijo",
    "blender": (3, 40, 1),
    "category": "3D View",
    "author": "mijo",
    "location": "View3D > right-side panel > ",
    "description":"",
    "warning": "",
    "wiki_url":"",
    "tracker_url": "",
    "version":(0,2,0)
}

# from . import b3d_trackir_Operator , b3d_trackir_Anim

from . import b3d_trackir_Operator , b3d_trackir_Anim

import bpy
# from bpy.app.handlers import persistent
classes = [
    b3d_trackir_Operator,
    b3d_trackir_Anim,
]

def scene_update_post_handler(dummy):
    pass

def register():
    for c in classes:
        c.register()
    
def unregister():
    for c in classes:
        c.unregister()