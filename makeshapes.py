#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: Joel Palmius
#   - modified by Per Olsen
#
#   MakeShapes is to be ADDED  to the MakeTarget2 panel.. so we have the same class here? 

import bpy
from bpy.types import Operator
# 
bpy.types.Scene.do_load_all_targets = bpy.props.BoolProperty(
            name="Load all targets",
            description="Load all targets, not just the one you select!",
            default = True)

bpy.types.Scene.do_save_all_targets = bpy.props.BoolProperty(
            name="Save all targets",
            description="Save all targets, not just the one you select!",
            default = True)

bpy.types.Scene.do_save_faceshapes = bpy.props.BoolProperty(
            name="Save faceshapes to fil",
            description="Save all shape keys, as a file!",
            default = True)


class MHC_PT_MakeShapes_Panel(bpy.types.Panel):
    bl_label = "MakeShapes from MHTargets"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "MakeTarget2"

    def draw(self, context):
        layout = self.layout
        scn = context.scene

        shapeLoadBox = layout.box()
        shapeLoadBox.label(text="For Shape keys and targets", icon="MESH_DATA")
        shapeLoadBox.operator("mh_community.load_shape_target", text="Load shapes from targets")
        shapeLoadBox.prop(scn, "do_load_all_targets" )

        # shapeSaveBox = layout.box()
        # shapeSaveBox.label(text="Save Target", icon="MESH_DATA")
        shapeLoadBox.operator("mh_community.save_shape_target", text="Save target")
        shapeLoadBox.prop(scn, "do_save_all_targets" )

        shapePrintBox = layout.box()
        shapePrintBox.label(text="Output Shape Keys", icon="MESH_DATA")
        shapePrintBox.operator("mh_community.print_shape_target", text="Print shape key(s)")
        shapePrintBox.operator("mh_community.save_faceshape_file", text="Save your faceshape.mxa file")
        shapePrintBox.prop(scn, "do_save_faceshapes" )

