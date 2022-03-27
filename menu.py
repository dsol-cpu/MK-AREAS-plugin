import bpy
import os

from sys import platform
if platform.startswith("linux"):
    # linux
    path = os.path.dirname(bpy.data.filepath)+"/"
if platform.startswith("darwin"):
    # OS X
    path = os.path.dirname(bpy.data.filepath)+"/"
if platform.startswith("cygwin") or platform.startswith("win32") or platform.startswith("Windows"):
    # Windows
    path = os.path.dirname(bpy.data.filepath)+"\\"
else:
    print("What are you on?")



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
    sample_string_list = write_kmp(lines)
    print(sample_string_list)
    return(sample_string_list)

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

#writes out the area into a much more readable format, return the list of list
def write_kmp(lines) :
    hash_count = 0
    area_sector_count = 0
    print("writing!")
    temp = []
    sample_string_list = []
    with open(path +'output.txt', 'w') as f:
        for line in lines:
            if "###############################################################################" in line:
                hash_count += 1          # Is this quadratic time? Yes, now hush
                #The area section is the 5th hash symbol line
            if hash_count == 5:
                f.write(line)
                if "#------------------------------------------------------------------------------" in line:
                    area_sector_count += 1
#                    print("working")
                    #2nd hash symbol with hyphens line
                if area_sector_count >= 2 and "#------------------------------------------------------------------------------" not in line:
                    #Grab elements from current line that are not >/spaces/empty/'/n'
                    splitted_line = line.split()
                    temp.append(','.join(splitted_line))
                    if len(temp) == 3 :
                        sample_string_list.append(temp)
                        temp = []
                    f.write(','.join(splitted_line)+'\n')
        print(sample_string_list)
        return(sample_string_list)

    #Now we want to parse from the AREA section and use each "#------" section
    #and then trim the > symbol and split the output into items

class AREA_Cube(bpy.types.Operator):
    bl_idname = "myops.add_area_cube"
    bl_label = "Add AREA cubes"
    def execute(self, context):
        sample_string_list = []
        print(sample_string_list)
        sample_string_list = import_kmp(context)
        create_cube(self, context, sample_string_list)
        return {'FINISHED'}

def create_cube(self, context, sample_string_list):
    print("work dammit")
    counter = 0
    current_index = 0
    position = []
    rotation = []
    scale = []
    print(sample_string_list)
    if not sample_string_list:
        return []
    else:
        pass #work here
                
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
