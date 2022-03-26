import bpy

class kmp_import(bpy.types.PropertyGroup):
    """Object Array"""
    bl_idname = ""
    bl_label = "Import KMP AREAS"
    bl_options = {'REGISTER', 'UNDO'}        
    
    def invoke (self, context):
        
        import_kmp(self)
   
        return {'FINISHED'}
    
def import_kmp(self, context):
    print("importing!")
    
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

class HelloWorldPanel(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Kmp area plugin"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        obj = context.object

        row = layout.row()
        row.label(text="Hello world!", icon='WORLD_DATA')

        row = layout.row()
        row.label(text="Active object is: " + obj.name)
        row = layout.row()
        row.prop(obj, "name")

        row = layout.row()
        row.operator("mesh.primitive_cube_add")


def register():
    bpy.utils.register_class(HelloWorldPanel, kmp_import, import_kmp, export_kmp)


def unregister():
    bpy.utils.unregister_class(HelloWorldPanel)


if __name__ == "__main__":
    register()