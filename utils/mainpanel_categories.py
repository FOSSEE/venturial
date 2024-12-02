from bpy.props import (
    IntProperty,
    FloatProperty,
    FloatVectorProperty,
    BoolProperty,
    StringProperty,
    PointerProperty,
    CollectionProperty,
    EnumProperty,
)


def mainpanel_properties_chooser():
    def_items = EnumProperty(
        name="MainPanel_Items",
        items=[
            ("Explore", "Explore", ""),
            ("Geometry", "Geometry", ""),
            ("Edges", "Edges", ""),
            ("Step Controls", "Steps Controls", ""),
            ("Boundary", "Boundary", "")
            ("Visualize", "Visualize", ""),
            ("Run", "Run", ""),
        ],
        default="Explore",
    )

    


