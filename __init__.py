#!/usr/bin/python
# -*- coding: utf-8 -*-

#  Author: Per Olsen / Joel Palmius

import bpy
from bpy.props      import BoolProperty, StringProperty, EnumProperty, IntProperty, CollectionProperty, FloatProperty
from bpy.utils  import register_class, unregister_class

from .makeshapes    import MHC_PT_MakeShapes_Panel
from .printshapetarget  import MHC_OT_PrintShapeTargetOperator
from .saveshapetarget   import MHC_OT_SaveShapeTargetOperator
from .loadshapetarget   import MHC_OT_LoadShapeTargetOperator
from .savefaceshapefile import  MHC_OT_SaveFaceshapeFileOperator

bl_info = {
    "name": "MakeShapes",
    "author": "Per Olsen based on MakeTarget2 by Joel Palmius",
    "version": (0,1,0),
    "blender": (2,80,0),
    "location": "View3D > UI > Make Target 2 > Make Shapes",
    "description": "Create MakeHuman Shapes from MH Targets, placed in MakeTarget2 panel",
    'wiki_url': "http://www.makehumancommunity.org/wiki/Documentation:MHBlenderTools:_MakeShapes",
    "category": "MakeHuman"}

MAKESHAPES_CLASSES = [
    MHC_OT_PrintShapeTargetOperator,
    MHC_OT_SaveShapeTargetOperator,
    MHC_OT_LoadShapeTargetOperator,
    MHC_OT_SaveFaceshapeFileOperator,
    MHC_PT_MakeShapes_Panel
]

__all__ = [
    "MHC_OT_PrintShapeTargetOperator",
    "MHC_OT_SaveShapeTargetOperator",
    "MHC_OT_LoadShapeTargetOperator",
    " MHC_OT_SaveFaceshapeFileOperator",
    "MHC_PT_MakeShapes_Panel",
    "MAKESHAPES_CLASSES"
]

def register():
    for cls in MAKESHAPES_CLASSES:
        register_class(cls)

def unregister():

    for cls in reversed(MAKESHAPES_CLASSES):
        unregister_class(cls)
        

if __name__ == "__main__":
    register()
    print("MakeShapes loaded")