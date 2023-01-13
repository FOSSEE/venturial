class get_boundaries:
    def draw(self, ptr, context):
        scn = context.scene
        ptr.scale_y = 1.4
        ptr.template_list("CUSTOM_UL_faces", "", scn, "fcustom", scn, "fcustom_index", rows=2)