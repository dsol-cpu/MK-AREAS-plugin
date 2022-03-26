#File access
#Text file access
#KMP library
#Access a collection of cubes' properties
#custom ui blender library import
import os
import bpy


bl_info = {
    "name": "Import KMP AREAS",
    "blender": (2, 93, 0),
    "category": "Object",
}

class kmp_import(bpy.types.PropertyGroup):
    """Object Array"""
    bl_idname = ""
    bl_label = "Import KMP AREAS"
    bl_options = {'REGISTER', 'UNDO'}        
    
    def execute (self, context):
        
        import_kmp(self)
   
        return {'FINISHED'}
    
def import_kmp(self, context):
    
    #Decode the KMP file and get the AREAS dataset 
    os.system("wkmpt DECODE course.kmp")
    self.report({'INFO'}, 'Printing report to Info window.')

    #Parse text file for all AREA objects
    file = open("course.txt")
    lines = file.readlines().split("")
    print(lines)
    
    #Make a new collection, 
    bpy.ops.outliner.collection_new(nested=False)
    
    current_index = 0
    #make a new cube with the information and link it to the new collection iteratively
    for i in range (0, len(lines)/16):
        for j in range(0, 16):
            #populate collection with cubes with their properties in their name     
            create_cube(current_index, lines)
        current_index+=1
    
def export_kmp(self, context):
    #get collection with info and iterate through all cubes in order and export in the same format as kmp
    self.report("kmp file exported!")
        
def create_cube(self, context, current_index, lines):
    place_in_file = current_index * 16
    location = lines[5+place_in_file:7+place_in_file]
    rotation = lines[8+place_in_file:10+place_in_file]
    scale = lines[11+place_in_file:13+place_in_file]

    bpy.ops.primitive.primitive_cube_add(2,False,'World',location,scale)
    bpy.context.active_object.rotation_mode = 'XYZ'
    bpy.context.active_object.rotation_euler = rotation
    bpy.ops.object.move_to_collection(collection_index=current_index)
    cube = bpy.context.selected_objects[0]
    cube.name = lines	


def register():
    bpy.utils.register_class(kmp_import)


def unregister():
    
    bpy.utils.unregister_class(kmp_import)


if __name__ == "__main__":
    register()