"""Create SELENE, a detailed static cyborg portrait. Run with Blender --background --python create_robot.py."""
import bpy, math, os, random
from mathutils import Vector
random.seed(17)
ROOT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.object.select_all(action='SELECT'); bpy.ops.object.delete(use_global=False)
def mat(name,color,metal=0,rough=.35,emission=0):
 m=bpy.data.materials.new(name); m.diffuse_color=(*color,1); m.use_nodes=True
 p=m.node_tree.nodes.get('Principled BSDF'); p.inputs['Base Color'].default_value=(*color,1); p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
 if emission: p.inputs['Emission Color'].default_value=(*color,1); p.inputs['Emission Strength'].default_value=emission
 return m
ivory=mat('Pearl ceramic titanium',(.72,.78,.79),.65,.25)
dark=mat('Graphite titanium',(.025,.038,.048),.85,.28)
steel=mat('Machined brushed steel',(.23,.30,.34),.92,.23)
gold=mat('Champagne brass',(.52,.31,.12),.8,.26)
skin=mat('Porcelain synthetic skin',(.82,.61,.49),0,.43)
p=skin.node_tree.nodes.get('Principled BSDF'); p.inputs['Subsurface Weight'].default_value=.09
lip=mat('Natural lips',(.38,.13,.12),0,.42)
cyan=mat('Ice blue status emitters',(.035,.6,.85),.35,.2,4)
white=mat('Eye sclera',(.85,.88,.86),0,.2)
iris=mat('Blue gray iris',(.055,.19,.24),.25,.18)
black=mat('Pupil and rubber seals',(.006,.009,.012),.1,.35)
def finish(o,name,material):
 o.name=name; o.data.materials.append(material)
 if o.type=='MESH':
  for f in o.data.polygons:f.use_smooth=True
 return o
def uv(name,loc,scale,material,segments=48):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=segments,ring_count=32,location=loc); o=bpy.context.object; o.scale=scale; return finish(o,name,material)
def cube(name,loc,scale,material,bevel=.04):
 bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=bpy.context.object;o.scale=scale;bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 if bevel:mod=o.modifiers.new('Manufactured edge radii','BEVEL');mod.width=bevel;mod.segments=3
 o.modifiers.new('Weighted normals','WEIGHTED_NORMAL');return finish(o,name,material)
def rod(name,a,b,r,material,r2=None):
 a,b=Vector(a),Vector(b); d=b-a
 bpy.ops.mesh.primitive_cone_add(vertices=32,radius1=r,radius2=r if r2 is None else r2,depth=d.length,location=(a+b)/2)
 o=bpy.context.object;o.rotation_euler=d.to_track_quat('Z','Y').to_euler();return finish(o,name,material)
def ring(name,loc,major,minor,material,rot=(0,0,0)):
 bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=12,location=loc,major_radius=major,minor_radius=minor,rotation=rot);return finish(bpy.context.object,name,material)
def wire(name,points,r,material):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3;s=c.splines.new('BEZIER');s.bezier_points.add(len(points)-1)
 for b,pt in zip(s.bezier_points,points):b.co=pt;b.handle_left_type='AUTO';b.handle_right_type='AUTO'
 o=bpy.data.objects.new(name,c);bpy.context.collection.objects.link(o);o.data.materials.append(material);return o
def bolt(name,loc,r=.022):
 r*=.40
 o=rod(name,(loc[0],loc[1]-.012,loc[2]),(loc[0],loc[1]+.012,loc[2]),r,gold)
 cube(name+' socket',(loc[0],loc[1]-.014,loc[2]),(r*.65,.004,r*.65),black,.002)
def panel(name,loc,scale):
 o=uv(name,loc,scale,ivory)
 for dx in [-.65,.65]:
  for dz in [-.65,.65]:bolt(name+' captive screw',(loc[0]+dx*scale[0],loc[1]-scale[1]*.72,loc[2]+dz*scale[2]),.018)
 return o
# Coordinates: face and front surfaces point toward negative Y. Height approximately 2.2 m.
uv('Pelvic chassis',(0,0,1.03),(.245,.15,.16),dark)
panel('Pelvic front shield',(0,-.135,1.045),(.15,.052,.125))
for s in [-1,1]:
 panel('Iliac crest armor',(s*.205,-.01,1.11),(.095,.16,.12))
 uv('Hip spherical bearing',(s*.18,0,.94),(.105,.105,.105),steel)
 a=(s*.18,0,.93);k=(s*.20,-.015,.57);ank=(s*.21,.015,.16)
 rod('Femur structural beam',a,k,.065,dark)
 panel('Thigh ceramic shell',(s*.20,-.045,.77),(.105,.085,.215))
 panel('Thigh lateral panel',(s*.285,.02,.79),(.043,.07,.16))
 for j in range(6):
  z=.65+j*.037;cube('Thigh cooling fin',(s*.28,-.008,z),(.08,.12,.011),steel,.003)
 rod('Thigh exposed piston',(s*.14,.08,.90),(s*.14,.08,.65),.021,steel)
 rod('Thigh actuator sleeve',(s*.14,.08,.90),(s*.14,.08,.77),.035,dark)
 uv('Knee ball',(s*.20,-.015,.55),(.079,.08,.074),steel)
 ring('Knee bearing rim',(s*.20,-.085,.55),.055,.013,gold,(math.pi/2,0,0))
 panel('Patella shield',(s*.20,-.11,.56),(.065,.025,.07))
 rod('Tibia carbon spine',k,ank,.048,dark)
 panel('Shin armor',(s*.21,-.035,.34),(.079,.073,.19))
 for x in [-.045,.045]:
  rod('Calf polished piston',(s*.21+x,.07,.48),(s*.21+x,.06,.19),.012,steel)
 for j in range(9):cube('Shin side ventilation',(s*.275,-.018,.24+j*.022),(.013,.074,.009),black,.002)
 uv('Ankle bearing',ank,(.059,.064,.052),gold)
 cube('Foot rubber sole',(s*.21,-.06,.055),(.16,.32,.055),black,.02)
 panel('Armored foot',(s*.21,-.065,.105),(.078,.155,.052))
 for j in range(4):cube('Toe articulation',(s*.21,-.17+j*.022,.11),(.135,.014,.035),steel,.005)
# Thorax and visibly open abdominal engine.
uv('Thorax structural cage',(0,.015,1.48),(.25,.145,.25),dark)
panel('Sternum',(0,-.14,1.53),(.075,.042,.17))
for s in [-1,1]:
 panel('Pectoral sculpted armor',(s*.125,-.095,1.55),(.13,.115,.13))
 panel('Clavicle plate',(s*.14,-.07,1.695),(.145,.058,.045))
 for j in range(5):
  z=1.37+j*.035;wire('Rib exoskeleton',[(s*.055,-.135,z),(s*.19,-.09,z-.015),(s*.235,.015,z+.02),(s*.17,.13,z+.025)],.013,steel)
 rod('Waist suspension',(s*.16,.02,1.18),(s*.18,.015,1.40),.018,steel)
 rod('Waist piston housing',(s*.16,.02,1.18),(s*.17,.017,1.28),.035,dark)
 for j in range(5):
  x=s*(.07+j*.012);wire('Abdominal braided conduit',[(x,-.06,1.39),(x+s*.025,-.105,1.27),(x,-.08,1.16)],.005,gold if j%2 else black)
for j in range(7):
 z=1.18+j*.029;cube('Abdominal vertebra',(0,0,z),(.095,.10,.024),steel,.009);cube('Abdominal floating shield',(0,-.105,z),(.09,.035,.021),ivory,.006)
ring('Core illuminated reactor',(0,-.137,1.435),.037,.006,cyan,(math.pi/2,0,0))
for j in range(12):
 z=1.15+j*.044;cube('Dorsal spinal module',(0,.16,z),(.09,.065,.032),steel,.008)
 for s in [-1,1]:uv('Dorsal fastener',(s*.027,.20,z),(.009,.009,.009),gold,24)
for s in [-1,1]:wire('Dorsal power trunk',[(s*.11,.12,1.13),(s*.12,.20,1.42),(s*.10,.13,1.69)],.012,black)
# Arms, fingers, joints, piston groups.
for s in [-1,1]:
 shoulder=(s*.29,0,1.65); elbow=(s*.37,-.025,1.34); wrist=(s*.40,-.065,1.07)
 uv('Shoulder gimbal',shoulder,(.085,.09,.09),steel)
 panel('Shoulder cap',(s*.31,.005,1.70),(.12,.105,.075))
 ring('Shoulder bearing',(s*.30,-.085,1.65),.063,.011,gold,(math.pi/2,0,0))
 rod('Humerus spine',shoulder,elbow,.035,dark)
 panel('Upper arm shell',(s*.345,-.005,1.49),(.065,.072,.14))
 rod('Biceps actuator',(s*.31,-.063,1.60),(s*.37,-.077,1.38),.013,steel)
 uv('Elbow joint',elbow,(.056,.055,.055),dark)
 ring('Elbow ring',(s*.37,-.076,1.34),.038,.008,gold,(math.pi/2,0,0))
 rod('Forearm strut',elbow,wrist,.031,steel)
 panel('Forearm plate',(s*.39,-.062,1.21),(.060,.045,.115))
 for j in range(6):cube('Forearm heat sink',(s*.435,-.015,1.15+j*.023),(.025,.062,.01),steel,.003)
 for j in range(3):wire('Arm control cable',[(s*(.29+j*.013),.05,1.63),(s*(.40+j*.008),.06,1.34),(s*(.40+j*.009),0,1.09)],.004,black)
 uv('Wrist bearing',wrist,(.038,.037,.033),gold)
 panel('Hand metacarpal shield',(s*.405,-.068,1.015),(.047,.03,.06))
 for f in range(4):
  x=s*(.370+f*.024);z=.982;length=[.082,.105,.098,.078][f]
  for seg in range(3):
   za=z-seg*length/3;zb=za-length/3+.004
   rod('Finger titanium phalanx',(x,-.075,za),(x,-.084,zb),.009,ivory)
   uv('Finger micro knuckle',(x,-.076,za),(.010,.011,.009),steel,24)
  wire('Finger tendon',[(x,-.055,.99),(x,-.060,.95),(x,-.069,z-length)],.0025,gold)
 rod('Thumb proximal',(s*.365,-.07,1.03),(s*.344,-.09,.99),.012,ivory)
 rod('Thumb distal',(s*.344,-.09,.99),(s*.348,-.105,.963),.011,ivory)
# Neck spindle and concentric collars.
rod('Cervical column',(0,0,1.69),(0,0,1.86),.046,dark)
for j in range(5):ring('Neck articulated collar',(0,0,1.72+j*.025),.054,.009,steel)
for s in [-1,1]:rod('Neck support tendon',(s*.085,.02,1.70),(s*.060,.01,1.85),.009,gold)
# Continuous custom facial surface: elliptical cross sections with localized anatomical relief.
verts=[];faces=[];nz=72;nt=112
for j in range(nz+1):
 t=j/nz; z=1.83+t*.36; w=.105*math.sin(math.pi*t)**.48*(.79+.21*t);depth=.09*math.sin(math.pi*t)**.48
 for i in range(nt):
  a=2*math.pi*i/nt;x=w*math.sin(a);y=-depth*math.cos(a)
  front=max(0,math.cos(a))**14
  nose=.036*math.exp(-(x/.019)**2-((z-2.003)/.043)**2)
  cheeks=.009*math.exp(-((abs(x)-.054)/.025)**2-((z-1.993)/.038)**2)
  chin=.010*math.exp(-(x/.041)**2-((z-1.870)/.025)**2)
  sockets=.008*math.exp(-((abs(x)-.044)/.023)**2-((z-2.057)/.019)**2)
  y-=front*(nose+cheeks+chin-sockets);verts.append((x,y,z))
for j in range(nz):
 for i in range(nt):a=j*nt+i;b=j*nt+(i+1)%nt;faces.append((a,b,b+nt,a+nt))
mesh=bpy.data.meshes.new('Sculpted facial topology');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Synthetic human face',mesh);bpy.context.collection.objects.link(o);finish(o,o.name,skin)
sub=o.modifiers.new('Facial subdivision','SUBSURF');sub.levels=1;sub.render_levels=2
for s in [-1,1]:
 uv('Eye',(s*.043,-.078,2.056),(.022,.011,.009),white)
 uv('Iris',(s*.043,-.089,2.056),(.007,.002,.007),iris)
 uv('Pupil',(s*.043,-.091,2.056),(.0032,.001,.0036),black)
 uv('Eye catchlight',(s*.040,-.092,2.059),(.0012,.001,.0012),white,24)
 for upper in [True,False]:
  wire('Sculpted eyelid',[(s*.021,-.082,2.055),(s*.043,-.090,2.063 if upper else 2.049),(s*.064,-.080,2.055)],.0035,skin)
 wire('Eyebrow',[(s*.021,-.081,2.080),(s*.044,-.085,2.085),(s*.068,-.073,2.080)],.0025,dark)
 uv('Nostril',(s*.010,-.115,1.992),(.004,.002,.0023),lip,24)
 wire('Cheek interface seam',[(s*.084,-.045,2.04),(s*.079,-.061,1.984),(s*.062,-.056,1.931)],.0015,gold)
wire('Upper lip',[(-.026,-.080,1.943),(-.011,-.088,1.946),(0,-.089,1.943),(.011,-.088,1.946),(.026,-.080,1.943)],.0032,lip)
wire('Lower lip',[(-.025,-.080,1.941),(0,-.090,1.936),(.025,-.080,1.941)],.0036,lip)
wire('Mouth line',[(-.023,-.083,1.942),(0,-.092,1.941),(.023,-.083,1.942)],.0009,black)
# Open helmet: skull cap, ear sensor hubs, crown rails and gadgets.
uv('Helmet rear carapace',(0,.045,2.055),(.116,.093,.15),dark)
panel('Crown ceramic shell',(0,.020,2.164),(.112,.10,.056))
wire('Brow armored rim',[(-.098,-.028,2.08),(-.082,-.072,2.14),(0,-.073,2.177),(.082,-.072,2.14),(.098,-.028,2.08)],.012,ivory)
for s in [-1,1]:
 uv('Temple interface',(s*.101,.004,2.048),(.027,.057,.069),steel)
 ring('Temple sensor gold bearing',(s*.126,.004,2.055),.039,.008,gold,(0,math.pi/2,0))
 rod('Ear sensor hub',(s*.119,.004,2.055),(s*.138,.004,2.055),.031,dark)
 rod('Ear sensor light',(s*.138,.004,2.055),(s*.140,.004,2.055),.020,cyan)
 panel('Helmet side armor',(s*.092,.045,2.14),(.041,.068,.05))
 for j in range(5):cube('Helmet thermal vent',(s*.09,.092,2.06+j*.019),(.024,.020,.008),steel,.002)
 wire('Mandibular helmet rail',[(s*.102,.01,2.045),(s*.105,.005,1.955),(s*.066,-.04,1.885)],.010,ivory)
 for j in range(3):uv('Temple rivet',(s*.094,-.048,2.107+j*.013),(.006,.006,.006),gold,24)
 wire('Helmet braided harness',[(s*.06,.10,2.15),(s*.075,.14,2.03),(s*.054,.08,1.85)],.009,black)
cube('Optical targeting module',(.077,-.066,2.158),(.046,.049,.036),dark,.007)
uv('Optical lens',(.077,-.095,2.158),(.013,.004,.013),cyan)
rod('Antenna mast',(-.097,.043,2.16),(-.12,.05,2.27),.004,steel)
uv('Antenna tip',(-.12,.05,2.27),(.008,.008,.008),cyan,24)
for j in range(7):cube('Crown segmented spine',(0,.012+j*.015,2.210-j*.007),(.023,.012,.008),gold,.002)
# Surface microengineering details, shoulder decals, cable clamps.
for s in [-1,1]:
 for j in range(4):
  cube('Clavicle status indicator',(s*(.095+j*.019),-.128,1.70),(.011,.005,.008),cyan,.002)
 for j in range(5):bolt('Torso peripheral fastener',(s*.221,-.064,1.43+j*.040),.009)
 for j in range(6):cube('Thigh luminous inset',(s*.211,-.129,.69+j*.029),(.009,.004,.017),cyan,.002)
def text_obj(body,loc,size,material):
 c=bpy.data.curves.new('Laser etched '+body,'FONT');c.body=body;c.size=size;c.extrude=.0001;o=bpy.data.objects.new(c.name,c);bpy.context.collection.objects.link(o);o.location=loc;o.rotation_euler=(math.pi/2,0,0);o.data.materials.append(material)
text_obj('S E L E N E',( -.060,-.185,1.625),.013,dark)
text_obj('S-07',(.176,-.130,.795),.018,dark)
# Presentation platform and studio.
rod('Exhibition plinth',(0,0,-.07),(0,0,.016),.58,dark)
ring('Plinth illuminated perimeter',(0,0,-.005),.565,.006,cyan)
floor=mat('Studio charcoal',(.026,.034,.043),.15,.55)
cube('Infinite studio floor',(0,0,-.095),(200,200,.035),floor,.005)
cube('Studio backdrop',(0,8,5),(200,.1,12),floor,.01)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=64;scene.cycles.use_denoising=True
scene.world.color=(.12,.12,.12)
def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def light(name,loc,power,color,size,target):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=color;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;aim(o,target)
light('Large soft portrait key',(-3,-4,5),650,(.80,.91,1),4,(0,0,1.3))
light('Warm rim',(2,2,3.4),850,(1,.64,.34),3,(0,0,1.4))
light('Cool edge',(-2,1,2.5),650,(.27,.65,1),2,(0,0,1.4))
light('Face beauty fill',(0,-3,2.5),120,(1,.86,.76),2,(0,0,2))
d=bpy.data.cameras.new('Portrait camera');cam=bpy.data.objects.new('Portrait camera',d);bpy.context.collection.objects.link(cam);scene.camera=cam
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.resolution_percentage=100
os.makedirs(os.path.join(ROOT,'renders'),exist_ok=True)
def camera(loc,target,lens,w,h):cam.location=loc;aim(cam,target);d.lens=lens;scene.render.resolution_x=w;scene.render.resolution_y=h
camera((3,-6,2.75),(0,0,1.13),68,1100,1500)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'SELENE.blend'))
for name,loc,target,lens,w,h in [
 ('01_full_body',(3,-6,2.75),(0,0,1.13),68,1100,1500),
 ('02_portrait',(.75,-2.5,2.18),(0,0,1.96),100,1200,1200),
 ('03_back_mechanics',(-3,5,2.65),(0,0,1.15),65,1100,1500)]:
 camera(loc,target,lens,w,h);scene.render.filepath=os.path.join(ROOT,'renders',name+'.png');bpy.ops.render.render(write_still=True)
camera((3,-6,2.75),(0,0,1.13),68,1100,1500)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'SELENE.blend'))
print('SELENE COMPLETE',len(bpy.data.objects),'objects')
