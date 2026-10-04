"""Read-only sanity check: blender --background SELENE.blend --python inspect_scene.py."""
import bpy, json
s=bpy.context.scene
assert s.camera is not None
assert len(bpy.data.objects)>600
assert bpy.data.objects.get('Synthetic human face') is not None
assert bpy.data.objects.get('Studio backdrop') is not None
assert s.render.engine=='CYCLES'
print(json.dumps({'objects':len(bpy.data.objects),'meshes':len(bpy.data.meshes),'materials':len(bpy.data.materials),'vertices':sum(len(m.vertices) for m in bpy.data.meshes),'camera':s.camera.name,'render_engine':s.render.engine},indent=2))
