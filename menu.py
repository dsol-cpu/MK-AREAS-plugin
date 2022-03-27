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


class KMP_Import(bpy.types.Panel):
    """Creates a Panel in the Object properties window"""
    bl_label = "Kmp area plugin"
    bl_idname = "OBJ_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.operator("myops.add_area_cube")
        
        

class AREA_Cube(bpy.types.Operator):
    bl_idname = "myops.add_area_cube"
    bl_label = "Add AREA cubes"
    def execute(self, context):
        #Make a new collection, 
        #bpy.ops.outliner.collection_new(nested=False)
        sample_string_list = import_kmp(context)       
        Cube_Gen(sample_string_list)
        return {'FINISHED'}

    
def import_kmp(context):
    print("importing!")
    #Decode the KMP file and get the AREAS dataset 
    os.system("wkmpt DECODE " + path + "course.kmp")

    #Parse text file for all AREA objects
    file = open(path + "course.txt")
    lines = file.readlines()
    return(write_kmp(lines))

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
                    #2nd hash symbol with hyphens line
                if area_sector_count >= 2 and "#------------------------------------------------------------------------------" not in line:
                    #Grab elements from current line that are not >/spaces/empty/'/n'
                    splitted_line = line.split()
                    temp.append(','.join(splitted_line))
                    if len(temp) == 3 :
                        sample_string_list.append(temp)
                        temp = []
                    f.write(','.join(splitted_line)+'\n')
        return(sample_string_list)


def Cube_Gen(sample_string_list):
    current_index = 0
    position = []
    rotation = []
    scale = []
    
    
    
    if not sample_string_list:
        return []
    else:
        for element in sample_string_list:
            for i in range (0, 4):
                if i == 0:
                    position = element[i].split(",")[3:5]
                    #print("Position: " + position[0] + position[1] + position[2])
                elif i == 1:
                    rotation = element[i].split(",")[3:5]
                elif i == 2:
                    scale = element[i].split(",")[1:3]
                elif i == 3:
                    
                    bpy.ops.mesh.primitive_cube_add(1, location, rotation)
                    cube.name = 
                    cube.position = position
                    cube.rotation_mode = 'XYZ'
                    cube.rotation_euler = rotation
                    cube.scale = scale
                    cube.move_to_collection(current_index)
                    
                    current_index += 1

    
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