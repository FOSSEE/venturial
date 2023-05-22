class snappyhexmesh_menu:

    def layout(self, tools, context):

        cs = context.scene

        row1 = tools.row(align=True)
        split = row1.split(factor = 0.18, align=True)
        
        row1c1 = split.row(align=True)
        row1c1.alignment = 'RIGHT'
        row1c1.label(text="Snappy Tools:")