import textwrap
from venturial.models.tutorials_menu_operators import VNT_OT_tutorial_viewer

class layout_control_functions:
    
    def wrapText(self, context, text, frm):
        """Wrap text function for word wrapping of panel text"""
        wrapped_lines = textwrap.TextWrapper(width=int(context.region.width/13.5)).wrap(text=text.TUT_name)
        scn = context.scene
        split = frm.row().split(factor=0.01)
        c1 = split.column()
        c2 = split.column()
        
        c2row = c2.row().split(factor = 0.035)
        
        c2rowc1 = c2row.column()
        c2rowc2 = c2row.column()
        
        c2rowc2row = c2rowc2.row().split(factor = 0.84)
        c2rowc2rowc1 = c2rowc2row.column()
        c2rowc2rowc2 = c2rowc2row.column()
        
        c1.label(icon="KEYTYPE_BREAKDOWN_VEC" if text.TUT_progress == 100 else "KEYTYPE_MOVING_HOLD_VEC" if 0 < text.TUT_progress < 100 else "HANDLETYPE_AUTO_CLAMP_VEC")
        c1.scale_y = 2.5
        for i in wrapped_lines:
            c2rowc2rowc1.label(text=i)
            c2rowc2rowc1.scale_y = 1.72
        
        c2rowc2rowc2row = c2rowc2rowc2.row().split(factor = 0.5)
        c2rowc2rowc2rowc1 = c2rowc2rowc2row.column()
        c2rowc2rowc2rowc2 = c2rowc2rowc2row.column()
        
        c2rowc2rowc2rowc1.operator(VNT_OT_tutorial_viewer.bl_idname, text="", icon="FULLSCREEN_ENTER").tut_index_id = text.TUT_index
        c2rowc2rowc2rowc2.prop(text, "TUT_bookmark", icon="SOLO_ON" if text.TUT_bookmark is True else "SOLO_OFF", icon_only=True, emboss = True)
        
        c2rowc2rowc2rowc1.scale_y = 2.5
        c2rowc2rowc2rowc2.scale_y = 2.5