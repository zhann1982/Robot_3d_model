"""Read-only verification for SELENE_REFERENCE.blend."""
import bpy, json
names=['Unhelmeted anatomical synthetic head','Continuous anatomical chest cuirass','Sweeping pelvic white shell','Seamless curved studio']
for n in names:assert bpy.data.objects.get(n),n
assert not any('Helmet' in o.name or 'helmet' in o.name and o.name!='Unhelmeted anatomical synthetic head' for o in bpy.data.objects)
assert bpy.context.scene.camera
assert len([o for o in bpy.data.objects if o.name.startswith('Finger white phalanx')])==24
print(json.dumps({'objects':len(bpy.data.objects),'base_vertices':sum(len(m.vertices) for m in bpy.data.meshes),'shells':sum(any(m.type=='SOLIDIFY' for m in o.modifiers) for o in bpy.data.objects),'camera':bpy.context.scene.camera.name},indent=2))
