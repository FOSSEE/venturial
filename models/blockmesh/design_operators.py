from bpy.types import Operator
from bpy.props import BoolProperty, EnumProperty, IntProperty, StringProperty
import bpy, numpy as np, bmesh
from venturial.utils.custom_icon_object_generator import *

class VNT_OT_location_spawnner(Operator):
    """Click to see options for cell locations"""
    bl_label = "Click to see options for cell locations" 
    bl_idname = "vnt.location_spawnner"
    bl_description = " "

    options : EnumProperty(items = [("Grid", "Grid", "Generate cells in a grid."),
                                    ("3D Cursor", "3D Cursor", "Generate cells at the 3D cursor"),
                                    ("Center", "Center", "Generate cells at the center.")],
                           default = "Grid")
    
    x : IntProperty()
    y : IntProperty()
    
    def execute(self, context):   
        context.scene.spawn_type = self.options
        bpy.context.window.cursor_warp(0, 0)
        bpy.context.window.cursor_warp(self.x, self.y)
        
        return {'FINISHED'}
        
    def invoke(self, context, event):
        self.x = event.mouse_x
        self.y = event.mouse_y
        
        return self.execute(context)

class VNT_OT_add_to_viewport(Operator):
    """Add chosen number of cell shape units to the viewport"""
    bl_label = "Create Cells"
    bl_idname = "vnt.add_to_viewport"
    bl_description = "Add chosen number of cell shape units to the viewport" 
    
    # The __init__ method is understood by those who hate if-else statements and long-ass code.
    # This makes the operator run slower but systematically replicates the first step of block-composition-algorithm.  
    def __init__(self, spawn_locations=None, cs=None):
        """initialise all possible spawn locations"""
        self.cs = bpy.context.scene
        self.m = int(self.cs.cellShape_units ** 0.5)
        self.spawn_locations = {"Grid" : [(i % self.m, i // self.m, 0) for i in range(self.cs.cellShape_units)],
                                "3D Cursor" : [tuple(self.cs.cursor.location) for i in range(self.cs.cellShape_units)],
                                "Center" : [(0.0, 0.0, 0.0) for i in range(self.cs.cellShape_units)]}
        self.spawn_object = {"Hexahedron": "spawn_hexahedrons",
                             "Prism": "spawn_prisms"}
        
    def spawn_hexahedrons(self, context, loc):
        # bpy.ops.mesh.primitive_cube_add(size = 1.0, location=loc)
        
        scn = context.scene

        bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
        bpy.context.scene.tool_settings.use_snap = True

        # loc = [np.random.uniform(-i*2.0, i*2.0), np.random.uniform(-i*2.0, i*2.0), np.random.uniform(-i*2.0, i*2.0)]
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=loc)
        
        obj = bpy.context.object
        bpy.context.object.show_wire = True
        mat = obj.matrix_world

              
        LV_list = [[-0.5, -0.5, -0.5], 
                   [0.5, -0.5, -0.5],  
                   [0.5, 0.5, -0.5], 
                   [-0.5, 0.5, -0.5], 
                   [-0.5, -0.5, 0.5], 
                   [0.5, -0.5, 0.5], 
                   [0.5, 0.5, 0.5], 
                   [-0.5, 0.5, 0.5]]    
                   
        bpy.ops.object.mode_set(mode='EDIT')
        
        bm=bmesh.from_edit_mesh(obj.data)
        dml_order = [0, 0, 0, 0, 0, 0, 0, 0]
        v_order = [0, 4, 6, 2, 1, 5, 7, 3]
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        
        block_origin = []
        for v in bm.verts:
            print(f"v:{v}")
            if v.index == 0:
                block_origin = list(mat @ v.co)

            print(f"vertex: {np.array(list(v.co))}")
            for i in range(0, len(dml_order)):
                if list(np.around(np.array(list(v.co)), 4)) == LV_list[i]:
                    
                    dml_order[i] = list(mat @ v.co)
        
        for k in range(0, len(v_order)):
            
            item = scn.simblk.add()
            item.name = obj.name
            item.index = v_order[k]
            item.vertptx = dml_order[k][0]
            item.vertpty = dml_order[k][1]
            item.vertptz = dml_order[k][2]
            
        bpy.ops.object.mode_set(mode='OBJECT')
        scn.cnt += 1
        
        bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=block_origin, scale=(1, 1, 1))
        
        mt = bpy.context.active_object
        mt.parent = obj
        mt.parent_type = 'VERTEX'
        
        mt.parent_vertices[0] = 0
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        bpy.context.object.location[2] = 0
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
            
    def spawn_prisms(self, context, loc): #TODO: Fix the count of prisms
        scn = context.scene
        
        bpy.context.scene.tool_settings.snap_elements = {'VERTEX'}
        bpy.context.scene.tool_settings.use_snap = True
        
        
            # loc = [np.random.uniform(-i*2.0, i*2.0), np.random.uniform(-i*2.0, i*2.0), np.random.uniform(-i*2.0, i*2.0)]
        bpy.ops.mesh.primitive_cylinder_add(vertices=3, enter_editmode=False, align='WORLD', location=loc, scale=(1, 1, 1))
    
        obj = bpy.context.object
        #obj.name = "Prism"
        bpy.context.object.show_wire = True
        mat = obj.matrix_world

        bpy.ops.object.mode_set(mode='EDIT')
        
        bm=bmesh.from_edit_mesh(obj.data)
        bpy.context.tool_settings.mesh_select_mode = (False, False, True)
        
        for e in bm.faces:
            if e.index == 1:
                e.select = True
                
            else:
                e.select = False
        
        bpy.ops.transform.resize(value=(0.2, 1, 1), orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(True, False, False), mirror=True, use_proportional_edit=False, proportional_edit_falloff='SMOOTH', proportional_size=1, use_proportional_connected=False, use_proportional_projected=False)
        
        bpy.ops.object.mode_set(mode='OBJECT')
        
        #ordering of vertices for 6V block = 0, 3, 5, 1, 2, 4, 4, 2
        #Vertex number 2 and 4 are repeated
        LV_list = [[-0.1732, -0.5, -1.0], #4
                   [0.1732, -0.5, -1.0],  #2
                   [0.0, 1.0, -1.0],   #0
                   [0.0, 1.0, -1.0],  #0
                   [-0.1732, -0.5, 1.0],  #5
                   [0.1732, -0.5, 1.0],   #3
                   [0.0, 1.0, 1.0],   #1
                   [0.0, 1.0, 1.0]]  #1
                   
        bpy.ops.object.mode_set(mode='EDIT')
        
        bm=bmesh.from_edit_mesh(obj.data)
        dml_order = [0, 0, 0, 0, 0, 0, 0, 0]
        v_order = [4, 2, 0, 0, 5, 3, 1, 1]
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        
        block_origin = []
        for v in bm.verts:
            if v.index == 4:
                
                block_origin = list(mat @ v.co)
            for i in range(0, len(dml_order)):
                if list(np.around(np.array(list(v.co)), 4)) == LV_list[i]:
                    dml_order[i] = list(mat @ v.co)
        
        for k in range(0, len(v_order)):
            
            item = scn.simblk.add()
            item.name = obj.name
            item.index = v_order[k]
            item.vertptx = dml_order[k][0]
            item.vertpty = dml_order[k][1]
            item.vertptz = dml_order[k][2]
            
        bpy.ops.object.mode_set(mode='OBJECT')
        scn.cnt += 1
        
        bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=block_origin, scale=(1, 1, 1))
        
        mt = bpy.context.active_object
        mt.parent = obj
        mt.parent_type = 'VERTEX'
        
        mt.parent_vertices[0] = 4
        bpy.context.object.location[0] = 0
        bpy.context.object.location[1] = 0
        bpy.context.object.location[2] = 0
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.context.view_layer.objects.active = obj
        obj.select_set(True)
        
        for obj in bpy.context.scene.objects:
            obj.select_set(False)
            bpy.context.view_layer.objects.active = obj 
                
    
        #return {'RUNNING_MODAL'} 

    def draw(self, context):
        #layout.alignment doesn't work here: probable bug in blender.
        cs = context.scene
        layout = self.layout
        
        if cs.spawn_type != "Grid":
            split = layout.split(factor = 0.32)
            c1 = split.row()
            c2 = split.row().column().box()
            
            c1.template_icon(icon_value=custom_icons["warning_sign_1"]["warning_sign_1"].icon_id, scale=3)
            c2.label(text="          This will create multiple cells at " + cs.spawn_type + " ?")
            c2.label(text="Switch to grid mode to distribute multiple cells in a grid.")
            
        else:
            layout.label(text="                                                       Click OK to proceed.")
        
        row1 = layout.row()
        row1.alignment = "EXPAND"
        row1.operator(VNT_OT_location_spawnner.bl_idname, text="Grid", depress=True if cs.spawn_type == "Grid" else False).options = "Grid"
        row1.operator(VNT_OT_location_spawnner.bl_idname, text="3D Cursor", depress=True if cs.spawn_type == "3D Cursor" else False).options = "3D Cursor"
        row1.operator(VNT_OT_location_spawnner.bl_idname, text="Center", depress=True if cs.spawn_type == "Center" else False).options = "Center"
        
    
    def render_cellShapes(self, context):
        pass
    
    def execute(self, context):
        """The execute method renders the cell shapes into 3D view"""
        cs = context.scene
        for loc in self.spawn_locations[cs.spawn_type]:
            getattr(self, self.spawn_object[cs.cellShapes])(context, loc)
        
        return {'FINISHED'} 
    
    def invoke(self, context, event):
        # Raise warning dialog box if multiple cells are spawned using 3D cursor or Center spawn type. 
        if context.scene.cellShape_units > 1 and context.scene.spawn_type != "Grid":
            return context.window_manager.invoke_props_dialog(self, width=440)
        # Run execute if cells are drawn with the Grid method
        else:
            return self.execute(context)


class VNT_OT_compose(Operator):
    """Select Blocks to Join and merge All Overlapping Vertices, Faces and Edges to build Geometry. 
    Perform this action only after Blocks are assembled. This action cannot be undone"""
    bl_label = "Merge all Selected Blocks"
    bl_description = "Select Blocks to Join and merge All Overlapping Vertices, Faces and Edges to build Geometry. Perform this action only after Blocks are assembled. This action cannot be undone"
    bl_idname = "vnt.compose"
    
    update_VC: BoolProperty(default=False,
                            name="Update Vertices after Geometry Completion")
                            
    @classmethod
    def poll(cls, context):
        return bool(context.scene.simblk)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)
    
    def execute(self, context):
        scn = context.scene
        sel_obj = bpy.context.selected_objects
        
        #print("Merge Blocks--------------------------------------------------------------")
        if len(sel_obj) != 0:    
            for i in range(0, len(scn.simblk)):
                    
                for obj in sel_obj:
                    if obj.type == "MESH":
                        mat = obj.matrix_world
                        if scn.simblk[i].name == obj.name:
                            bpy.ops.object.mode_set(mode='EDIT')
                        
                            bm=bmesh.from_edit_mesh(obj.data)
                                
                            for v in bm.verts:
                                    
                                if scn.simblk[i].index == v.index:
                                    scn.simblk[i].vertptx = list(mat @ v.co)[0]
                                    scn.simblk[i].vertpty = list(mat @ v.co)[1]
                                    scn.simblk[i].vertptz = list(mat @ v.co)[2]
                                    
            bpy.ops.object.mode_set(mode='OBJECT')
            
            lap = [] #local axis global position
            lar = [] #local axis rotation 
            for obj in sel_obj:
                if obj.type == "MESH":
                    mat = obj.matrix_world
                    bpy.ops.object.mode_set(mode='EDIT')
                    bm=bmesh.from_edit_mesh(obj.data)
                    
                    if obj.name.startswith('Cube'):
                        for v in bm.verts:
                            if v.index == 0:
                                lap.append([obj.name, list(mat @ v.co)])
                    
                    else:
                        for v in bm.verts:
                            if v.index == 4:
                                lap.append([obj.name, list(mat @ v.co)])
                        

                    for i in range(0, len(obj.children)):
                        m = [bpy.data.objects[obj.children[i].name].rotation_euler[th] for th in range(0, 3)]
                
                    lar.append(m)
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            for obj in bpy.context.scene.objects:
                if obj.type == "EMPTY":
                    obj.select_set(True)   
                else:
                    obj.select_set(False)  
            bpy.ops.object.delete()
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            self.update_VC = True
                  
        else:
            self.report({'INFO'}, "Selection is Empty.")
            self.update_VC = False
            
        if self.update_VC == True:
            
            for obj in bpy.context.scene.objects:
                if obj in sel_obj:
                    obj.select_set(True)
                    
            merge_threshold = 0.1
            bpy.ops.object.join()
            
            bpy.ops.object.mode_set(mode = 'EDIT') 
            bpy.ops.mesh.select_mode(type="VERT")
            bpy.ops.mesh.select_all(action = 'SELECT')
            bpy.ops.mesh.remove_doubles(threshold = merge_threshold)
            bpy.ops.object.mode_set(mode = 'OBJECT')
            
            geo = bpy.context.active_object
            bpy.ops.object.mode_set(mode='EDIT')
            bm=bmesh.from_edit_mesh(geo.data)
            geomat = geo.matrix_world
            
        
            lap_geo = []#local axis position wrt geometry
            for i in range(0, len(lap)):
                for v in bm.verts:
                    if list(np.around(np.array(lap[i][1]), 2)) == list(np.around(np.array(list(geomat @ v.co)), 2)):
                        lap_geo.append([list(v.co), v.index])
            
            print("\n\nlap_geo\n")    
            print(lap_geo)
            print("Length of lap_geo:", len(lap_geo))
            
            bpy.ops.object.mode_set(mode='OBJECT')
            
            for i in range(0, len(lap_geo)):
                bpy.ops.object.empty_add(type='ARROWS', align='WORLD', location=lap[i][1], rotation=lar[i], scale=(1, 1, 1))
                mt = bpy.context.active_object
                bpy.context.object.rotation_euler = lar[i]

            for obj in bpy.context.scene.objects:
                obj.select_set(True)
                bpy.context.view_layer.objects.active = obj
                
                bpy.context.object.lock_rotation[0] = True
                bpy.context.object.lock_rotation[1] = True
                bpy.context.object.lock_rotation[2] = True
                
                bpy.context.object.lock_location[0] = True
                bpy.context.object.lock_location[1] = True
                bpy.context.object.lock_location[2] = True
                
            bpy.context.view_layer.objects.active = None
            for obj  in bpy.context.scene.objects:
                if obj.type == "MESH":
                    obj.select_set(True)
                    bpy.context.view_layer.objects.active = obj
                
                else:
                    obj.select_set(False)
            
            final_geo = bpy.context.active_object       
            bpy.ops.object.mode_set(mode='EDIT')
            mat = final_geo.matrix_world
            bm=bmesh.from_edit_mesh(final_geo.data)
                
            fovl = []           
            for v in bm.verts:        
                fovl.append([list(mat @ v.co), v.index])
         
            for y in range(0, len(scn.simblk)):
                for x in fovl:
                    m = [scn.simblk[y].vertptx, scn.simblk[y].vertpty, scn.simblk[y].vertptz]
                    if list(np.around(np.array(m), 4)) == list(np.around(np.array(x[0]), 4)):
                        scn.simblk[y].index = x[1]
            
            bpy.ops.object.mode_set(mode='OBJECT')
        else:
            self.report({'INFO'}, "Select at least 2 Blocks.")   
            
         
        return {'FINISHED'}  
    

class VNT_OT_get_blocks(Operator):
    """Obtain ordered list of vertices belonging to a block"""
    bl_idname = "vnt.get_blocks"
    bl_label = "Get Blocks"
    bl_description = "Automatically assign block vertices based on vertex ordering i.e. right-handed cyclic about Z axis of block"
    #bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.simblk)
    
    def calc_vertices(self, context):
        pass

    def execute(self, context):
        
        scn = context.scene
        obj = bpy.context.active_object
        
        if obj:
           
            BN = [] #Block Names
            for i in scn.simblk:
                BN.append(i.name)
        
            seen = set()
            result = []
            for item in BN:
                if item not in seen:
                    seen.add(item)
                    result.append(item)
            
            BV = [] #Block Vertices
            for j in result:
                m = []
                for i in range(0, len(scn.simblk)):
                    if scn.simblk[i].name == j:
                        m.append(scn.simblk[i].index)
                        
                BV.append(m)
                
            for i in range(0, len(BV)):
                data = scn.bcustom.add()
                data.b_name = result[i]
                data.name = "hex ("+ ' '.join(str(e) for e in BV[i]) + ")"
                data.grading = "simpleGrading (1 1 1)"
                data.setcellx = scn.cell_x
                data.setcelly = scn.cell_y
                data.setcellz = scn.cell_z
 
        else:
            self.report({'INFO'}, "Select a Geometry.")
            
        return{'FINISHED'}
    
class VNT_OT_remove_blocks(Operator):
    bl_label = "Remove from Viewport"
    bl_description = "Remove selected Blocks from Geometry"
    bl_idname = "vnt.removeblocks"
    
    @classmethod
    def poll(cls, context):
        return bool(context.scene.simblk)
    
    def execute(self, context):
        scn = context.scene
        
        for obj in bpy.context.selected_objects:
            obj.select_set(True)
            cnt = 0
            for i in range(0, len(scn.simblk)):
                if scn.simblk[i].name == obj.name:
                    print(scn.simblk[i].name)
                    cnt += 1            
            
            idx = 0
            for i in range(0, len(scn.simblk)):
                if scn.simblk[i].name == obj.name:
                    idx = i
                    break
                
            for p in range(0, cnt):
                scn.simblk.remove(idx)
                
            for child in obj.children:
                child.select_set(True)
                
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.delete()
        
        print("NEW------------------------------------------")
        for i in range(0, len(scn.simblk)):
            print(scn.simblk[i].name)
            
        return {'FINISHED'}
        
class VNT_OT_remove_all_blocks(Operator):
    bl_label = "Remove All Blocks from Geometry and Memory?"
    bl_description = "Remove All Blocks from Geometry and Memory\nDeleting a Block from the Viewport without using this Button will not remove it from memory"
    bl_idname = "vnt.removeallblocks"
    
    @classmethod
    def poll(cls, context):
        return bool(context.scene.simblk)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        
        for o in bpy.context.scene.objects:
            o.select_set(True)
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.delete()
        
        if bool(context.scene.simblk):
            context.scene.simblk.clear()
            self.report({'INFO'}, "All Blocks Removed from Geometry and Memory")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}
    
class VNT_OT_clearblocks(Operator):
    """Clear all items of the list"""
    bl_idname = "vnt.clear_blocks"
    bl_label = ""
    bl_description = "Clear all Blocks from the List."
    bl_options = {'INTERNAL'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.bcustom)

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

    def execute(self, context):
        if bool(context.scene.bcustom):
            context.scene.bcustom.clear()
            self.report({'INFO'}, "All items removed")
        else:
            self.report({'INFO'}, "Nothing to remove")
        return{'FINISHED'}
    
    
class VNT_OT_blocksdatacontrol(Operator):
    bl_idname = "vnt.blocksdatacontrol"
    bl_label = ""
    bl_description = "Add/Remove Blocks from blockmeshdict"
    bl_options = {'REGISTER'}

    action: bpy.props.EnumProperty(
        items=(('REMOVE', "Remove", ""),
               ('ADD', "Add", "")))

    def invoke(self, context, event):
        scn = context.scene
        print(type(context.scene))
        idx = scn.bcustom_index

        try:
            item = scn.bcustom[idx]
        except IndexError:
            pass
        else:

            if self.action == 'REMOVE':
                self.report({'INFO'}, "Feature in development. Use delete all for now.")

        if self.action == 'ADD':
            
            obj = context.active_object
            hex = []
            sel_vert = []
            
            if obj:
                
                if obj.mode == 'EDIT':
                    bm = bmesh.from_edit_mesh(obj.data) 
                    verts = bm.verts   
                    
                    sel_vert = [elem.index for elem in bm.select_history if isinstance(elem, bmesh.types.BMVert)]
                    hex = [v for v in sel_vert]
                    
                    if 3 < len(hex) < 9:
                        str1 = "(" + ' '.join(str(e) for e in hex) + ")"
                        
                        item = scn.bcustom.add()
                        item.name = "hex " + str1
                        item.set_cells = "(" + str(scn.cell_x) + " " + str(scn.cell_y) + " " + str(scn.cell_z) + ")"
                        item.grading = "simpleGrading (1 1 1)"
                        
                        scn.bcustom_index = len(scn.bcustom)-1
                        
                        info = '"%s" added to list' % (item.name)
                        self.report({'INFO'}, info)
                        
                    else: 
                        self.report({'INFO'}, "Block has " + str(len(hex)) + " vertices.")
                        
                else:
                    self.report({'INFO'}, "Enter Edit Mode.")
            
            else:
                self.report({'INFO'}, "Select a Block/Geometry.")
        return {"FINISHED"}

        
# Operator to select one block or select all blocks
class VNT_OT_showselectedblocks(Operator):
    """Select Items in the Viewport"""
    bl_idname = "vnt.show_select_blocks"
    bl_label = "Display selected blocks in 3D view"
    bl_description = "Show Selected Block in Viewport"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        return bool(context.scene.bcustom)

    def execute(self, context):
        
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.context.tool_settings.mesh_select_mode = (True, False, False)
        
        scn = context.scene
        idx = scn.bcustom_index
        
        obj = bpy.context.active_object
        bm = bmesh.from_edit_mesh(obj.data)
        
        all_verts = [m for m in bm.verts]
          
        for i in range(0, len(scn.bcustom)):
            if scn.bcustom[i].enabled:
                item = scn.bcustom[i]            
                hex_vert = hex_strtolist(item.name)
            
                for v in all_verts:
                    if v.index in hex_vert:
                        v.select = True
                            
                    bmesh.update_edit_mesh(obj.data, True)
            
        self.report({'INFO'}, "Blocks Selected")
                
        return{'FINISHED'}


class VNT_OT_select_unselect_allblocks(Operator):
    bl_idname = "vnt.select_unselect_allblocks"
    bl_label = "Select/Unselect all blocks"
    bl_description = "Select/Unselect all blocks from the list."
    bl_options = {'INTERNAL'}
    
    select_all: BoolProperty(
        default=False,
        name="Select all Items of List",
        options={'SKIP_SAVE'})
        
    @classmethod
    def poll(cls, context):
        return bool(context.scene.bcustom)

    def execute(self, context):
        scn = context.scene
        
        if self.select_all:
                        
            for i in range(0, len(scn.bcustom)):
                scn.bcustom[i].enabled = True
        
        else:
            for i in range(0, len(scn.bcustom)):
                scn.bcustom[i].enabled = False
              
        return{'FINISHED'} 