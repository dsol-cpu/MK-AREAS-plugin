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
    bl_label = "KMP Area plugin"
    bl_idname = "OBJ_PT_hello"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "object"
    def draw(self, context):
        scene = context.scene
        layout = self.layout
        
#        row = layout.row()
#        row.prop(scene, "myops.scale_view")

        row = layout.row()
        row.operator("myops.add_area_cube")
        row = layout.row()
        row.operator("myops.export_kmp")


class AREA_Cube(bpy.types.Operator):
    bl_idname = "myops.add_area_cube"
    bl_label = "Add AREA cubes"
    def execute(self, context):
        #Make a new collection, 
        #bpy.ops.outliner.collection_new(nested=False)
        sample_string_list = Import_KMP(context)       
        Cube_Gen(sample_string_list)
        return {'FINISHED'}
    
class Export_KMP(bpy.types.Operator):
    bl_idname = "myops.export_kmp"
    bl_label = "Export KMP"
    def execute(self, context):
        export_kmp(self, context)
        return {'FINISHED'}

class Scale_View(bpy.types.Operator):
    bl_idname = "myops.scale_view"
    bl_label = "Scale_View"
    bl_context = "object"
    def draw(self, context):
        return {'FINISHED'}

    
def Import_KMP(context):
    print("importing!")
    #Decode the KMP file and get the AREAS dataset 
    os.system("wkmpt DECODE " + path + "course.kmp")

    #Parse text file for all AREA objects
    file = open(path + "course.txt")
    lines = file.readlines()
    return(Write_KMP(lines))


#writes out the area into a much more readable format, return the list of list
def Write_KMP(lines) :
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
        print(sample_string_list)
        return(sample_string_list)


def Cube_Gen(sample_string_list):
    current_index = 0
    position = []
    rotation = []
    scale = []
#    collection = bpy.context.blend_data.collections.new(name='Area')
#    bpy.context.collection.children.link(collection)

    if bpy.data.collections.get('Area'):
        cubes_collection = bpy.data.collections['Area']
    else:
        cubes_collection = bpy.data.collections.new('Area')
        bpy.context.scene.collection.children.link(cubes_collection)

    bpy.context.view_layer.active_layer_collection = bpy.context.view_layer.layer_collection.children['Area']
    
    if not sample_string_list:
        return []
    else:
        for element in sample_string_list:
            for i in range (0, 4):
                if i == 0:
                    position = [float(x) for x in element[i].split(",")[3:6]]
                    #print("Position: " + position[0] + position[1] + position[2])
                elif i == 1:
                    rotation = [float(x) for x in element[i].split(",")[3:6]]
                elif i == 2:
                    scale = [float(x) for x in element[i].split(",")[1:4]]
                    print(scale)
                elif i == 3:
                    
                    bpy.ops.mesh.primitive_cube_add()
                    cube = bpy.context.selected_objects[0]
                    bpy.context.active_object.location = position
                    bpy.context.active_object.rotation_euler = rotation
                    bpy.context.active_object.scale = scale
                    bpy.context.active_object.name = "".join(element)
                    #collection.objects.link(bpy.context.active_object)                   

                    current_index += 1

    # Possable todo: make it so duplacates don't show up agan when you press the button.


def export_kmp(self, context):
    #get collection with info and iterate through all cubes in order and export in the same format as kmp

    #Write to the start of the area section
    file = open(path + "course.txt")
    lines = file.readlines()
    hash_count = 0
    print("writing!")
    sample_string_list = []
    with open(path +'output_kmp.txt', 'w') as f:
        for line in lines:
            if "###############################################################################" in line:
                hash_count += 1          # Is this quadratic time? Yes, now hush
                #The area section is the 5th hash symbol line
            if hash_count < 5:
                f.write(line)
    
    
    for collection in bpy.data.collections:
        if collection.name != "Area" :
            pass
        else:
            for obj in collection.all_objects:
                print("obj: ", obj.name)



_classes = [KMP_Import, AREA_Cube, Scale_View, Export_KMP]
def register():
    for element in _classes:
        bpy.utils.register_class(element)


def unregister():
    for element in _classes:
        bpy.utils.unregister_class(element)


if __name__ == "__main__":
    register()