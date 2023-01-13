from venturial.models.edges_panel_operators import *
                                            
class edges_panel:
    
    def draw(self, ptr, context):
        row = ptr
        scn = context.scene
        
        sec1 = ptr.row(align=True)
        sec1.scale_y = 1.4
        sec1.ui_units_y = 1.50
        sec1.prop(scn, "geo_design_options", expand=True)
           
        col = ptr.column().box()
        
        row = col.split(factor=0.12)
        row.label(text="Edge Type:")
        row = row.split(factor=0.2)
        row.prop(scn, "edgelist")
        row = row.split(factor=0.16)
        row.prop(scn, "ipcnt")
        
        row = row.split(factor=0.60)
        row.active_default = True
        row.operator(edgeactions.bl_idname, icon='LINENUMBERS_ON', text="Add Edges").action = 'ADD'
        row.active_default = False
        
        row.alert = True
        row.operator(clear_currentedge.bl_idname, icon="CANCEL", text="Clear Current")
        row.alert = False
        
        col = ptr.column()
        
        row = col.split(align=True)
        row.operator(edgeactions.bl_idname, icon='REMOVE', text="").action = 'REMOVE'
        row.alert=True
        row.operator(ClearAllEdges.bl_idname, icon="TRASH", text="")
        row.alert=False
        row.operator(show_curvededge.bl_idname, icon="CON_TRACKTO", text="")
        row.operator(SelectUnselectEdges.bl_idname, icon="STICKY_UVS_LOC", text="").select_all = True
        row.operator(SelectUnselectEdges.bl_idname, icon="STICKY_UVS_DISABLE", text="").select_all = False
        row = col.split(align=True).box()
        rows = 2
            
        if scn.edgelist == 'arc':  
            row.template_list("CUSTOM_UL_edges", "", scn, "acustom", scn, "acustom_index", rows=rows)
        
        if scn.edgelist == 'polyLine':
            row.template_list("CUSTOM_UL_edges", "", scn, "pcustom", scn, "pcustom_index", rows=rows)
        
        if scn.edgelist == 'spline':
            row.template_list("CUSTOM_UL_edges", "", scn, "scustom", scn, "scustom_index", rows=rows)
        
        if scn.edgelist == 'BSpline':
            row.template_list("CUSTOM_UL_edges", "", scn, "bscustom", scn, "bscustom_index", rows=rows)
