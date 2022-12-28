# Batch Export Selected
Provides batch export of selected objects in common formats. Currently only OBJs, but more are coming soon!

## Installation
Copy **BatchExportSelected.py** to your Blender addons directory.

Windows:      %APPDATA%\Blender Foundation\Blender\3.4\scripts\addons\  
Linux:        /home/$user/.blender/3.4/scripts/addons/  
From Blender: User Preferences > Add-ons > Install Add-on from File... > Select **BatchExportSelected.py**  

## Usage
File > Export > Batch Export Selected Objects as OBJ

## Known Limitations
1. Requires the project to be saved
2. Has several baked in settings that may not be desirable for your export needs

## Notes
The follow settings are currently used for OBJ exports:

    export_materials=False,
    export_uv=False,
    export_normals=False,
    apply_modifiers=True,
    export_eval_mode='DAG_EVAL_VIEWPORT'

I do plan on exposing these settings either through preferences or through a prompt so that it's more flexible and applicable to more situations, but I feel that this is a good start.