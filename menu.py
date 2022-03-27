import bpy
import os

path = os.path.dirname(bpy.data.filepath)+"\\"

sample_string_list = []
class KMP_Import(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Kmp area plugin"
    bl_idname = "OBJECT_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("myops.add_area_cube")
        
          
    
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
    area_sector_count = 0
#    print("writing!")
    with open(path +'output.txt', 'w') as f:
        for line in lines:
            if "###############################################################################" in line:
                hash_count += 1          # Is this quadratic time? Yes, now hush
#                print('hash!')
                #5th hash symbol line
            if hash_count == 5:
                f.write(line)
                if "#------------------------------------------------------------------------------" in line:
                    area_sector_count += 1
#                    print("working")
                    #2nd hash symbol with hyphens line
                if area_sector_count >= 2 and "#------------------------------------------------------------------------------" not in line:
                    #Grab elements from current line that are not >/spaces/empty/'/n'
                    sample_string_list = line.split()

    #Now we want to parse from the AREA section and use each "#------" section
    #and then trim the > symbol and split the output into items

class AREA_Cube(bpy.types.Operator):
    bl_idname = "myops.add_area_cube"
    bl_label = "Add AREA cubes"
    
    def execute(self, context):
        import_kmp(context)
        create_cube(self, context)
        return {'FINISHED'}

def create_cube(self, context):
    print("work dammit")
    counter = 0
    current_index = 0
    position = []
    rotation = []
    scale = []
    if not sample_string_list:
        return []
    else:
        for line in sample_string_list:
            if counter == 0: 
                position = [float(x) for x  in sample_string_list[3:5]] 
            elif counter == 1:
                rotation = [float(x) for x  in sample_string_list[3:5]]
            elif counter == 2:
                scale = [float(x) for x  in sample_string_list[1:3]] 
            elif counter == 3:
                counter = -1
                
                bpy.ops.primitive.primitive_cube_add(2,False,'World',position,scale)
    #            bpy.context.active_object.rotation_mode = 'XYZ'
    #            bpy.context.active_object.rotation_euler = rotation
                bpy.ops.object.move_to_collection(collection_index=current_index)
                cube = bpy.context.selected_objects[0]
                cube.name = line
                
                current_index += 1
            counter += 1
    
#def export_kmp(self, context):
#    #get collection with info and iterate through all cubes in order and export in the same format as kmp
#    print("kmp file exported!")    

_classes = [KMP_Import, AREA_Cube]
def register():
    for element in _classes:
        bpy.utils.register_class(element)


def unregister():
    for element in _classes:
        bpy.utils.unregister_class(element)


if __name__ == "__main__":
    register()
