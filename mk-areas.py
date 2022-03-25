#File access
#Text file access
#KMP library
#Access a collection of cubes' properties
#custom ui blender library import


bl_info = {
    "name": "Import KMP AREAS",
    "blender": (2, 80, 0),
    "category": "Object",
}

import bpy
import os

class kmp_import(bpy.types.PropertyGroup):
    """Object Cursor Array"""
    bl_idname = ""
    bl_label = "Import KMP AREAS"
    bl_options = {'REGISTER', 'UNDO'}        
    
    def execute (self, context):
        scene = context.scene
        #Decode the KMP file and get the AREAS dataset 
        os.system("wkmpt DECODE course.kmp")

        #Parse text file for all AREA objects
        file = open("course.txt")
        lines = file.readlines().split("")        
        
        #Make a new collection, make a new cube with the information and link it to the new collection iteratively
        bpy.ops.outliner.collection_new(nested=False)      
        
        #arr = [[0]*cols]*rows

        #create new collection for AREA cubes
        areas_collection = bpy.data.collections.new("AREA Collection")  
        
        #populate collection with cubes with their properties in their name        
        
        return {'FINISHED'}
    
    #def save():
    
#    def  
#        bpy.ops.primitive.primitive_cube_add(2,False,'World',(),()
    

def register():
    bpy.utils.register_class(KMP_Import)


def unregister():
    bpy.utils.unregister_class(KMP_Import)


if __name__ == "__main__":
    register()