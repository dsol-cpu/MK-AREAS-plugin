import bpy
import os

#i swear im so sorry
path = input("input the absolute path of the folder your kmp file is in pls and thx <3")

class KMP_Import(bpy.types.Panel):
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
        import_kmp(context)
          
    
def import_kmp(context):
    print("importing!")
    #Decode the KMP file and get the AREAS dataset 
    os.system("wkmpt DECODE " + path + "course.kmp")

    #Parse text file for all AREA objects
    file = open(path + "course.txt")
    lines = file.readlines()
    write_kmp(lines)
    '''
    #Make a new collection, 
    bpy.ops.outliner.collection_new(nested=False)
    
    current_index = 0
    #make a new cube with the information and link it to the new collection iteratively
    for i in range (0, len(lines)/16):
        for j in range(0, 16):
            #populate collection with cubes with their properties in their name     
            create_cube(current_index, lines)
        current_index+=1'''

'''
Note: I have the write_kmp function currently just write the existing kmp settings
This is to just to make things managable for debugging / coding.
I'll be working on the writing some sample stuff shortly hereafter, but this
should get you an idea of what's what. (Flashbacks to hashing in data structures)
'''
def write_kmp(lines) :
    hash_count = 0
    print("writing!")
    with open(path +'output.txt', 'w') as f:
        for line in lines:
            if "###############################################################################" in line:
                hash_count += 1          # Is this quadratic time? Yes, now hush
                print('hash!')
            if hash_count  == 5 :
                f.write(line)
    print(hash_count)


def create_cube(current_index, lines):
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
    
#def export_kmp(self, context):
#    #get collection with info and iterate through all cubes in order and export in the same format as kmp
#    self.report("kmp file exported!")    

_classes = [KMP_Import]
def register():
    for element in _classes:
        bpy.utils.register_class(element)


def unregister():
    for element in _classes:
        bpy.utils.unregister_class(element)


if __name__ == "__main__":
    register()
