#File access
#Text file access
#KMP library
#Access a collection of cubes' properties
#custom ui blender library import

import bpy

class HelloWorldPanel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_options = {"DEFAULT_CLOSED"}


class HELLO_PT_World1(HelloWorldPanel, bpy.types.Panel):
    bl_idname = "HELLO_PT_World1"
    bl_label = "Panel 1"

    def draw(self, context):
        layout = self.layout
        layout.label(text="This is the main panel.")


class HELLO_PT_World2(HelloWorldPanel, bpy.types.Panel):
    bl_parent_id = "HELLO_PT_World1"
    bl_label = "Panel 2"

    def draw(self, context):
        layout = self.layout
        layout.label(text="First Sub Panel of Panel 1.")


class HELLO_PT_World3(HelloWorldPanel, bpy.types.Panel):
    bl_parent_id = "HELLO_PT_World1"
    bl_label = "Panel 3"

    def draw(self, context):
        layout = self.layout
        layout.label(text="Second Sub Panel of Panel 1.")