#!/usr/bin/python
# -*- coding: utf-8 -*-

import bpy, bpy_extras, os, re
from bpy_extras.io_utils import ExportHelper
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty

class MHC_OT_SaveShapeTargetOperator(bpy.types.Operator, ExportHelper):
    """Save the required shape key to a file (i.e export a target)"""
    bl_idname = "mh_community.save_shape_target"
    bl_label = "Save Shape(s) as target(s)"

    filter_glob : StringProperty(default='*.target', options={'HIDDEN'})
    filename_ext = ".target"

    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            if not hasattr(context.active_object, "MhObjectType"):
                return False
            if context.active_object.select_get():
                if context.active_object.MhObjectType == "Basemesh":
                    if context.active_object.data.shape_keys and context.active_object.data.shape_keys.key_blocks and "Basis" in context.active_object.data.shape_keys.key_blocks:
                        return True
        return False

    def execute(self, context):

        scaleFactor = 10.0
        scaleMode = str(bpy.context.scene.MhScaleMode)

        if scaleMode == "DECIMETER":
            scaleFactor = 1.0

        if scaleMode == "CENTIMETER":
            scaleFactor = 0.1

        obj = context.active_object
        sks = obj.data.shape_keys
        idx = context.object.active_shape_key_index
        nt  = obj.data.shape_keys.key_blocks[idx].name
        bt = sks.key_blocks["Basis"]
        pt = sks.key_blocks[idx] # var PrimaryKey

        filename, extension = os.path.splitext(self.filepath)
        dirName = os.path.dirname(filename)
        self.filepath = dirName + "\\" + nt + ".target"

        if context.scene.do_save_all_targets:
            x = 0 # Do not handle index 0, Basis 
            for pt in sks.key_blocks: 
                if x > 0:  
                    self.save_shape_file(str(pt.name + ".target"), dirName, obj, context, scaleFactor, bt, pt)
                else:    
                    x = x + 1 
        else:
            self.save_shape_file(str(nt + ".target"), dirName, obj, context, scaleFactor, bt, pt)

        self.report({'INFO'}, "Target saved")
        return {'FINISHED'}

    def save_shape_file(self, file, dirName, obj, context, scaleFactor, bt, pt):
        # print("Save file:" + dirName + "\\" + file )
        with open(dirName + "\\" + file,"w") as f:
            f.write("# This is a target file for MakeHuman , shape key: " + file + ".  \n")
            f.write("# It was written by MakeShapes2, which is a part of the MakeHuman Community addons for Blender.\n#\n")
            f.write("# basemesh hm08\n")
            numverts = len(bt.data)
            i = 0
            while i < numverts:
                btvco = bt.data[i].co
                ptvco = pt.data[i].co
                if btvco != ptvco:
                    diffco = ptvco - btvco
                    x = str(diffco[0] * scaleFactor)
                    y = str(-diffco[1] * scaleFactor)
                    z = str(diffco[2] * scaleFactor)
                    f.write(str(i) + " " + x + " " + z + " " + y + "\n")
                i = i + 1
        return