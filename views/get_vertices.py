from venturial.models.blockmesh.get_vertices_operators import *


class get_vertices:
    def draw(self, ptr, context):
        cs = context.scene
        spt = ptr.column().split()
        spt.ui_units_y = 1.25
        c1 = spt.row(align=True)
        c1.scale_y = 1.25
        c2 = spt.column(align=True).split(align=True)

        c1spt = c1.column().split(factor=0.8)
        c1a = c1spt.row()
        c1b = c1spt.column(align=True).split(align=True)

        # c1a.active_default = True
        # c1b.active_default = True
        c1a.operator(VNT_OT_add_update_verts.bl_idname, text="Get Vertices")
        c1b.operator(VNT_OT_vertactions.bl_idname, icon='ADD', text="").action = 'ADD'
        # c1b.operator(VNT_OT_vertactions.bl_idname, icon="ADD", text="")
        # c1a.active_default = False
        # c1b.active_default = False

        c2.operator(
            VNT_OT_select_unselect_allverts.bl_idname, icon="STICKY_UVS_LOC", text=None
        ).select_all = True
        c2.operator(
            VNT_OT_select_unselect_allverts.bl_idname,
            icon="STICKY_UVS_DISABLE",
            text=None,
        ).select_all = False

        c2.scale_y = 1.4
        c2.alert = True
        c2.operator(VNT_OT_vertactions.bl_idname, icon="REMOVE", text=None).action = (
            "REMOVE"
        )
        c2.operator(VNT_OT_clearverts.bl_idname, icon="TRASH", text="")
        c2.alert = False

        row = ptr.row()
        row.scale_y = 1.4
        row.template_list(
            "CUSTOM_UL_verts", "", cs, "vcustom", cs, "vcustom_index", rows=2
        )
