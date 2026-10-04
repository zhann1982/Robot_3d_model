import bpy, os
from mathutils import Vector
s=bpy.context.scene;c=s.camera;c.location=(-1.4,2.8,2.0);c.rotation_euler=(Vector((0,0,1.02))-c.location).to_track_quat('-Z','Y').to_euler();c.data.lens=43
s.render.resolution_x=1100;s.render.resolution_y=1500
s.render.filepath=os.path.join(os.path.dirname(os.path.abspath(__file__)),'renders_reference','03_back.png')
bpy.ops.render.render(write_still=True)
