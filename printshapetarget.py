#!/usr/bin/python
# -*- coding: utf-8 -*-
# Re-work to dump the entire thing into MH2X format! 
import bpy

from bpy_extras.io_utils import ExportHelper

from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty

class MHC_OT_PrintShapeTargetOperator(bpy.types.Operator):
    """Print all differing vertices to console"""
    bl_idname = "mh_community.print_shape_target"
    bl_label = "Print selected Shape key as target"
    bl_options = {'REGISTER', 'UNDO'}

    
    # If BaseMesh and there is a "Basis" shape key - then enable print
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
        #if context.scene.do_save_faceshapes: 
        #    print("Save faceshapes ... not in progress")
        #    self.report({'INFO'}, "Selected Shape Key not printet"  )
        #    return {'FINISHED'}
        
        # Scale factor may be important? 
        scaleFactor = 10.0
        scaleMode = str(bpy.context.scene.MhScaleMode)

        if scaleMode == "DECIMETER":
            scaleFactor = 1.0

        if scaleMode == "CENTIMETER":
            scaleFactor = 0.1

        obj = context.active_object
        sks = obj.data.shape_keys
        
        #kt = obj.data.shape_keys.name
        #nt  = obj.data.shape_keys.key_blocks[idx].name
        #st = context.active_object.select_get()
        
        # Get the selected Shape key, index, name and pointer...
        idx = context.object.active_shape_key_index
        nt  = obj.data.shape_keys.key_blocks[idx].name
        bt = sks.key_blocks["Basis"]
        pt = sks.key_blocks[idx] # var PrimaryKey

        numverts = len(bt.data)
        iv = 0
        i = 0
        targettext = '     "' + nt + '" : [' 
        print("******* Here we go... << Eye catcher")

        while i < numverts:
            btvco = bt.data[i].co
            ptvco = pt.data[i].co
            if btvco != ptvco:
                if iv > 0:
                   targettext = targettext + ","      
                iv = iv + 1 
                diffco = ptvco - btvco
                x = str(diffco[0] * scaleFactor)
                y = str(-diffco[1] * scaleFactor)
                z = str(diffco[2] * scaleFactor)
                
                #print(str(i) + " " + str(diffco))
                #tex = str(diffco)[+9:-2]
                #texX, texZ, texY = tex.split(sep=",")

                targettext = targettext + " [" + str(i) + ", [" +  x + "," + z + "," + y + " ]] " 

            i = i + 1
        
        #tex = str(diffco)[+9:-2]
        #tex1, tex2, tex3 = tex.split(sep=",")

        print( targettext + " ] " )
         
        print("Selected Shape Key '" + nt + "' printed to console, #" + str(iv) + " verts ")
        self.report({'INFO'}, "Selected Shape Key printed to console, #" + str(iv) + " verts "  )
        return {'FINISHED'}
