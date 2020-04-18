#!/usr/bin/python
# -*- coding: utf-8 -*-
#
#  After  the file dialog is closed we process files in the entire directory 

import bpy, bpy_extras, os, re
from bpy_extras.io_utils import ImportHelper
from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty

class MHC_OT_LoadShapeTargetOperator(bpy.types.Operator, ImportHelper):
    """Load required shape keys from file (i.e load targets)"""
    bl_idname = "mh_community.load_shape_target"
    bl_label = "Process ALL Targts in directory!"

    #filter_glob : StringProperty(default='*.target', options={'HIDDEN'})

    def execute(self, context):
        filename, extension = os.path.splitext(self.filepath)
        #bn = os.path.basename(filename)
        dirName = os.path.dirname(filename)
        
        scaleFactor = 0.1
        scaleMode = str(bpy.context.scene.MhScaleMode)

        if scaleMode == "DECIMETER":
           scaleFactor = 1.0

        if scaleMode == "CENTIMETER":
            scaleFactor = 10.0
        
        obj = context.active_object
        if not context.active_object.data.shape_keys:          
            basis = obj.shape_key_add(name="Basis", from_mix=False)

        # self.print_target_file(dirName)

        #print(str(context.scene.do_load_all_targets))

        #if bpy.types.Scene.do_load_all_targets:
        if context.scene.do_load_all_targets:
            for file in os.listdir(dirName):
                filename, extension = os.path.splitext(file)
                if extension == ".target":
                    self.load_target_file(file, dirName, obj , context, scaleFactor)
                else:
                    print(" ... is not a target:" + extension)      
        else:
            bn = os.path.basename(filename)
            self.load_target_file(bn + ".target", dirName, obj, context, scaleFactor)

#      for file in os.listdir(dirName):
#      filename, extension = os.path.splitext(dirName + "\\" + file)
        
        self.report({'INFO'}, "Target loaded")
        #shapeTarget.value = 0.0
        return {'FINISHED'}

     
 
    def load_target_file(self, file, dirName, obj, context, scaleFactor):
        filename, extension = os.path.splitext(dirName + "\\" + file)
        bn = os.path.basename(filename)
     
        shapeTarget = obj.shape_key_add(name=bn, from_mix=True)

        idx = context.active_object.data.shape_keys.key_blocks.find(bn)
        context.active_object.active_shape_key_index = idx

        sks = obj.data.shape_keys
     

        pname = sks.key_blocks  
        pt = sks.key_blocks[bn]  
        # print("Making " + context.active_object.name + "(" + str(idx) + ") " + bn )
        
        #with open(self.filepath,'r') as f:
        with open(dirName + "\\" + file,'r') as f:
        #with open(file,'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = re.compile(r"\s+").split(line.strip())
                        index = int(parts[0])
                        x = float(parts[1]) * scaleFactor
                        z = float(parts[2]) * scaleFactor
                        y = -float(parts[3]) * scaleFactor

                        #print(str(index) + " " + str(x) + " " + str(y) + " " + str(z))

                        pt.data[index].co[0] = pt.data[index].co[0] + x
                        pt.data[index].co[1] = pt.data[index].co[1] + y
                        pt.data[index].co[2] = pt.data[index].co[2] + z
            
        shapeTarget.value = 0.0
        # print("...done")
        return

    # Poll deterimin, True/False, if a button is active! 
    # This is, here, done via the context 
    @classmethod
    def poll(self, context):
        if context.active_object is not None:
            #if not hasattr(context.active_object, "MhObjectType"):
            #    print("NOT MhObjectType:" + str(context.active_object))
            #    return False
            if context.active_object.select_get():
                if context.active_object.MhObjectType == "Basemesh":
                #    if not context.active_object.data.shape_keys:
                #    print("OK ObjectType:" + str(context.active_object.MhObjectType))
                    return True
                else:
                    print("ObjectType:" + str(context.active_object.MhObjectType))
                    parts = context.active_object.name.split(":")
                    #print("Name      :" + str(context.active_object.name))
                    #print("Part0     :" + str(parts[0]))
                    #print("Part1     :" + str(parts[1]))
                    #print("Part2     :" + str(parts[2]))
                    if context.active_object.name == "Averagedude_base:Body":
                        return True
                    else:
                        return False
        return False
