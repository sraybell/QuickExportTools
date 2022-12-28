# Batch Export Selected
Provides batch export of selected objects in common formats. Currently only OBJs, but more are coming soon!

## Installation
Copy **BatchExportSelected.py** to your Blender addons directory.

Windows:      %APPDATA%\Blender Foundation\Blender\3.4\scripts\addons\  
Linux:        /home/$user/.blender/3.4/scripts/addons/  
From Blender: User Preferences > Add-ons > Install Add-on from File... > Select **BatchExportSelected.py**  

## Usage
File > Export > Batch Export Selected Objects as OBJ  
Batch Export panel under Item while in Object mode

## Known Limitations
1. Requires the project to be saved
2. Has some settings baked in, such as materials are not exported, and it currently only supports applying the viewport modifiers on export