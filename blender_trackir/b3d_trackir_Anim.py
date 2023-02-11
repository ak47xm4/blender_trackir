import bpy

class OBJECT_MT_OpenCVPanel(bpy.types.WorkSpaceTool):
    """Creates a Panel in the Object properties window"""
    bl_idname = "wm.OBJECT_MT_OpenCVPanel"
    bl_label = "OpenCV Animation"
    bl_space_type = 'VIEW_3D'
    bl_context_mode='OBJECT'
        
    #bl_region_type = 'TOOLS'
    bl_idname = "ui_plus.opencv"
    #bl_context = "object"
    bl_options = {}

    bl_icon = "ops.generic.select_circle"
    '''
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
        
    '''
        
    def draw_settings(context, layout, tool):
        sce = context.scene
        #props = tool.operator_properties("wm.opencv_operator")
        
        row = layout.row()
        op = row.operator("wm.opencv_operator", text="Capture", icon="OUTLINER_OB_CAMERA")
        
        
        #moving_mult = row1.prop(aaa,"wm.opencv_operator",'myprop', slider=True)
        layout.prop(sce, "moving_mult", slider=True)
        layout.prop(sce, "force_autokeyframe")
        
        #layout.template_ID(bpy.context.object,'xform_obj' ,new='', open='', unlink='', filter='ALL')
        row = layout.row()
        row.prop_search(sce, "xform_obj", sce, "objects")
        #row.prop(sce, "xform_obj")
        #props = tool.operator_properties("wm.opencv_operator")
        #layout.prop(props, "stop", text="Stop Capture")
        #layout.prop(tool.op, "stop", text="Stop Capture")
        

        

def register():
    #bpy.utils.register_class(OBJECfT_MT_OpenCVPanel)
    #bpy.types.VIEW3D_PT_tools_active.prepend(OBJECT_MT_OpenCVPanel.draw)  # << add menu above
    # bpy.utils.register_tool(OBJECT_MT_OpenCVPanel, separator=True, group=True)
    bpy.utils.register_tool(OBJECT_MT_OpenCVPanel)
    # print('test_register: OBJECT_MT_OpenCVPanel')
        
def unregister():
    #bpy.types.VIEW3D_PT_tools_active.remove(OBJECT_MT_OpenCVPanel.draw)
    #bpy.utils.unregister_class(OBJECT_MT_OpenCVPanel)
    bpy.utils.unregister_tool(OBJECT_MT_OpenCVPanel)
    # print('test_register: OBJECT_MT_OpenCVPanel')
    
'''
if __name__ == "__main__":
    register()
'''