#!/usr/bin/python
# -*- coding: utf-8 -*-
# Re-work to dump the entire thing into MH2X format! 
import bpy, os

from bpy_extras.io_utils import ExportHelper

from bpy.props import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty

class MHC_OT_SaveFaceshapeFileOperator(bpy.types.Operator, ExportHelper):
    """Save  all differing vertices in Faceshape.mxa format """
    bl_idname = "mh_community.save_faceshape_file"
    bl_label = "Save Shape keys in Faceshape file "
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob : StringProperty(default='*.mxa', options={'HIDDEN'})
    filename_ext = ".mxa"

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
        if not context.scene.do_save_faceshapes: 
            # print("Save faceshapes ... not in progress")
            self.report({'INFO'}, ".. but do you REALLY want to save?"  )
            return {'FINISHED'}
        
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
        # pt = sks.key_blocks[idx] # var PrimaryKey

        numverts = len(bt.data)
        print("******* Here we go... << Eye catcher")

                
        filename, extension = os.path.splitext(self.filepath)
        dirName = os.path.dirname(filename)

        # We process the faceshape_BASE file and add our own... ;-) 
        with open(dirName + "\\Faceshapes.mxa","w") as f:
            #f.write("# This is a faceshape file for MakeHuman HMX2 importer, for shape keys.\n")
            #f.write("# It was written by MakeShapes, which is a part of the MakeHuman Community addons for Blender.\n#\n")
            #f.write("# basemesh hm08\n")

            with open(dirName + "\\Faceshapes_BASE.mxa","r") as fb:
                for line in fb:
                    lineStrip = line.strip()
                    if line and not line.startswith("<faceshape>"):
                        f.write(line)
                    else:
                        
                        notBasis = False
                        # Process all ShapeKeys, but not 'Basis'
                        for pt in sks.key_blocks: 
                            nt = pt.name
                            iv = 0
                            i = 0
                            targettext = '  ,\n      "' + nt + '" : [' 
                            print("... processing: " + nt )
                            if notBasis: 
                                iv = 0
                                i = 0
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
                                        targettext = targettext + " [" + str(i) + ", [" +  x + "," + z + "," + y + " ]] " 

                                    i = i + 1
                                
                                f.write(targettext + "]")
                                print("... written (" + str(iv) + " verts )")
                            else:
                                notBasis = True

                            #f.write(targettext)

        print("Selected Shape Key '" + nt + "' printed to console, #" + str(iv) + " verts ")
        self.report({'INFO'}, "Selected Shape Key printed to console, #" + str(iv) + " verts "  )
        return {'FINISHED'}

