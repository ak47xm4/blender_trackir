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
    bpy.types.Scene.moving_mult = bpy.props.FloatProperty(name="moving_mult", 
        description="test", default=0.025, min=0, max=1.0, soft_min=0.0, soft_max=1.0, 
        step=1, precision=4, unit='NONE', update=None, get=None, set=None)

    bpy.types.Scene.force_autokeyframe = bpy.props.BoolProperty(
        name="force_autokeyframe",
        description="force autokeyframe",
        default = False)
            
    bpy.types.Scene.xform_obj = bpy.props.StringProperty(
        name = "xform_obj",
        maxlen = 1000,
        default = ""
        )
        
    b3d_trackir_Anim.register()
    b3d_trackir_Operator.register()
    # print('test_register:')
    
def unregister():
    b3d_trackir_Anim.unregister()
    b3d_trackir_Operator.unregister()
    # print('test_unregister:')