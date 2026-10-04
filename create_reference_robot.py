"""Reference-inspired white humanoid, neutral standing pose. No external assets."""
import bpy, math, os
from mathutils import Vector
ROOT=os.path.dirname(os.path.abspath(__file__))
# Reuse modeling primitives only; the original scene and render pipeline are not executed.
with open(os.path.join(ROOT,'create_robot.py'),encoding='utf-8') as f:
 exec(f.read().split('# Coordinates:')[0])
ceramic=mat('Reference satin white polymer',(.80,.82,.84),.18,.32)
face_mat=mat('White synthetic facial dermis',(.69,.71,.73),.04,.48)
black_m=mat('Reference carbon mechanism',(.012,.016,.020),.68,.34)
rubber=mat('Matte joint bellows',(.009,.012,.014),.05,.55)
def loft(name,rows,material,deform=None):
 verts=[];faces=[];n=96
 for j,(z,cx,cy,rx,ry) in enumerate(rows):
  for i in range(n):
   a=i*2*math.pi/n;x=cx+rx*math.sin(a);y=cy-ry*math.cos(a);zz=z
   if deform:x,y,zz=deform(x,y,z,a,j)
   verts.append((x,y,zz))
 for j in range(len(rows)-1):
  for i in range(n):a=j*n+i;b=j*n+(i+1)%n;faces.append((a,b,b+n,a+n))
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);bpy.context.collection.objects.link(o);finish(o,name,material)
 sub=o.modifiers.new('Continuous shaped surface','SUBSURF');sub.levels=2;sub.render_levels=2
 sol=o.modifiers.new('Real shell wall thickness','SOLIDIFY');sol.thickness=.004
 return o
def small_screw(x,y,z):
 rod('Recessed black fastener',(x,y-.001,z),(x,y+.002,z),.004,black_m)
def front_joint(name,x,z,r):
 uv(name,(x,0,z),(r,r,r),black_m)
 ring(name+' bearing',(x,-r*.83,z),r*.64,.005,steel,(math.pi/2,0,0))
 rod(name+' hub',(x,-r*.92,z),(x,-r,z),r*.39,black_m)
# Long slim legs, asymmetrically shaped thigh shells and exposed hip joints.
for s in [-1,1]:
 x=s*.125
 front_joint('Hip universal joint',x,.91,.088)
 rod('Femur carbon load beam',(x,0,.91),(s*.135,0,.53),.034,black_m)
 rows=[(.555,s*.136,0,.035,.041),(.575,s*.135,0,.045,.055),(.64,s*.134,.008,.060,.069),(.74,s*.13,.012,.072,.081),(.83,s*.125,.012,.077,.078),(.875,s*.125,.008,.065,.059)]
 loft('Contoured thigh shell',rows,ceramic)
 # Long black service recess on inner thigh, kept flush to the shell.
 uv('Thigh inner service recess',(s*.086,-.052,.767),(.027,.022,.103),black_m)
 for j in range(3):rod('Thigh exposed tendon',(s*(.084+j*.012),-.072,.70),(s*(.084+j*.012),-.066,.835),.003,steel)
 for z in [.61,.83]:small_screw(s*.163,-.050,z)
 front_joint('Knee spherical bearing',s*.135,.52,.053)
 loft('Knee outer shield',[(.49,s*.15,-.023,.029,.030),(.51,s*.15,-.024,.035,.031),(.54,s*.15,-.025,.030,.027)],ceramic)
 rod('Tibia structural member',(s*.135,0,.50),(s*.136,0,.125),.025,black_m)
 loft('Tapered shin armor',[(.13,s*.136,0,.029,.029),(.17,s*.136,-.008,.034,.038),(.27,s*.137,-.008,.049,.049),(.36,s*.136,0,.055,.059),(.43,s*.135,.005,.043,.049),(.465,s*.135,.005,.034,.035)],ceramic)
 wire('Shin panel seam',[(s*.147,-.048,.40),(s*.151,-.055,.30),(s*.143,-.04,.19)],.0013,steel)
 rod('Rear shin polished actuator',(s*.136,.052,.18),(s*.136,.060,.42),.007,steel)
 front_joint('Ankle bearing',s*.136,.115,.030)
 uv('Foot upper shell',(s*.136,-.045,.060),(.054,.108,.037),ceramic)
 cube('Foot graphite sole',(s*.136,-.05,.029),(.105,.21,.025),rubber,.012)
 wire('Toe panel seam',[(s*.09,-.104,.069),(s*.136,-.124,.082),(s*.18,-.104,.069)],.002,black_m)
# Pelvic shell, with distinct rising hip rim and central V shape.
uv('Pelvic internal chassis',(0,.013,.945),(.161,.091,.087),black_m)
def pelvis_shape(x,y,z,a,j):
 return x,y,z+(.048*abs(math.sin(a)) if j==len(pelvis_rows)-1 else 0)
pelvis_rows=[(.892,0,-.003,.055,.056),(.905,0,-.009,.075,.065),(.941,0,-.003,.13,.085),(.976,0,.006,.162,.090),(.989,0,.010,.168,.083)]
loft('Sweeping pelvic white shell',pelvis_rows,ceramic,pelvis_shape)
for s in [-1,1]:small_screw(s*.13,-.054,1.010)
# Narrow exposed midriff, vertical ribbed dark column as in reference.
loft('Abdominal flexible black core',[(1.003,0,.010,.089,.068),(1.035,0,.010,.090,.068),(1.13,0,.008,.088,.065),(1.21,0,0,.112,.075),(1.24,0,0,.126,.079)],black_m)
for j in range(36):
 a=(j/36)*2*math.pi;x=.091*math.sin(a);y=.01-.069*math.cos(a)
 wire('Abdominal vertical rib',[(x,y,1.018),(x*.99,y,1.11),(x*1.18,y*1.08,1.19),(x*1.38,y*1.16,1.23)],.0018,steel)
for s in [-1,1]:rod('Waist lateral support',(s*.092,.025,1.02),(s*.116,.026,1.23),.007,black_m)
# Unified torso shell, chest relief integrated into the surface rather than separate spheres.
torso_rows=[(1.21,0,0,.107,.075),(1.225,0,0,.113,.078),(1.26,0,0,.132,.085),(1.31,0,0,.151,.091),(1.36,0,0,.164,.090),(1.41,0,0,.170,.087),(1.46,0,0,.175,.083),(1.51,0,0,.180,.080),(1.55,0,0,.182,.072),(1.58,0,0,.170,.067),(1.605,0,0,.128,.061),(1.624,0,0,.063,.051),(1.630,0,0,.049,.044)]
def chest_shape(x,y,z,a,j):
 front=max(0,math.cos(a))**1.5
 y-=front*.10*math.exp(-((abs(x)-.088)/.050)**2-((z-1.427)/.067)**2)
 if j<2:z+=.033*(abs(x)/.113)
 return x,y,z
loft('Continuous anatomical chest cuirass',torso_rows,ceramic,chest_shape)
wire('Chest lower chevron seam',[(-.135,-.060,1.29),(-.07,-.084,1.312),(0,-.090,1.33),(.07,-.084,1.312),(.135,-.060,1.29)],.0015,steel)
wire('Collar seam',[(-.13,-.045,1.604),(0,-.060,1.595),(.13,-.045,1.604)],.0012,steel)
# Graceful hanging arms; dark gimbals, long white tubular armor, slim hands.
for s in [-1,1]:
 shoulder=(s*.206,0,1.558);elbow=(s*.247,-.006,1.286);wrist=(s*.265,-.018,1.046)
 front_joint('Shoulder recessed gimbal',s*.202,1.555,.049)
 rod('Upper arm internal spar',shoulder,elbow,.018,black_m)
 loft('Upper arm white shell',[(1.305,s*.245,0,.028,.032),(1.34,s*.24,0,.031,.035),(1.43,s*.225,0,.035,.039),(1.52,s*.211,0,.036,.039),(1.545,s*.209,0,.030,.033)],ceramic)
 front_joint('Elbow rotary joint',s*.248,1.286,.035)
 rod('Forearm internal spar',elbow,wrist,.015,black_m)
 loft('Forearm white shell',[(1.065,s*.264,-.015,.020,.024),(1.09,s*.263,-.012,.023,.027),(1.17,s*.259,-.005,.030,.034),(1.23,s*.254,-.003,.031,.034),(1.255,s*.251,-.004,.028,.028)],ceramic)
 small_screw(s*.256,-.038,1.22)
 front_joint('Wrist joint',s*.266,1.044,.022)
 cube('Palm dark mechanics',(s*.268,-.017,.999),(.063,.035,.068),black_m,.010)
 uv('Palm white dorsal cover',(s*.268,.001,1.003),(.034,.016,.036),ceramic)
 for f in range(4):
  x=s*(.245+f*.015);length=[.065,.079,.074,.059][f]
  for j in range(3):
   z=.967-j*length/3
   uv('Finger joint',(x,-.019-j*.002,z),(.006,.006,.006),black_m,24)
   rod('Finger white phalanx',(x,-.019-j*.002,z-.004),(x,-.021-j*.002,z-length/3+.002),.005,ceramic)
 rod('Thumb proximal',(s*.236,-.018,1.015),(s*.218,-.025,.986),.007,ceramic)
 uv('Thumb bearing',(s*.218,-.025,.986),(.007,.007,.007),black_m,24)
 rod('Thumb tip',(s*.218,-.025,.986),(s*.222,-.030,.966),.006,ceramic)
# Ribbed neck with no helmet.
rod('Black cervical column',(0,0,1.625),(0,0,1.744),.035,black_m)
for j in range(14):ring('Cervical fine bellows',(0,0,1.644+j*.006),.037,.0015,steel)
for s in [-1,1]:rod('Neck posterior tendon',(s*.027,.028,1.635),(s*.028,.025,1.735),.004,black_m)
# Anatomical white face with shaped jaw, cheekbones, nose, forehead and skull.
head_rows=[(1.726,0,-.012,.020,.025),(1.738,0,-.008,.037,.036),(1.756,0,-.001,.052,.047),(1.778,0,.003,.062,.057),(1.804,0,.006,.069,.064),(1.833,0,.009,.074,.069),(1.862,0,.010,.077,.072),(1.888,0,.012,.078,.076),(1.916,0,.016,.077,.078),(1.941,0,.020,.072,.076),(1.962,0,.024,.061,.067),(1.981,0,.025,.042,.046),(1.993,0,.025,.012,.015)]
def face_shape(x,y,z,a,j):
 f=max(0,math.cos(a))**10
 nose=.031*math.exp(-(x/.012)**2-((z-1.832)/.027)**2)
 bridge=.011*math.exp(-(x/.011)**2-((z-1.866)/.034)**2)
 nose_wing=.008*math.exp(-((abs(x)-.012)/.007)**2-((z-1.821)/.008)**2)
 brow=.008*math.exp(-((abs(x)-.029)/.020)**2-((z-1.884)/.013)**2)
 socket=.008*math.exp(-((abs(x)-.029)/.015)**2-((z-1.870)/.011)**2)
 cheek=.010*math.exp(-((abs(x)-.040)/.019)**2-((z-1.842)/.024)**2)
 muzzle=.007*math.exp(-(x/.026)**2-((z-1.796)/.013)**2)
 y-=f*(nose+bridge+nose_wing+brow+cheek+muzzle-socket)
 return x,y,z
loft('Unhelmeted anatomical synthetic head',head_rows,face_mat,face_shape)
mouth_mat=mat('Subtle gray lip tone',(.42,.43,.44),.02,.49)
eye_mat=mat('Neutral silver gray iris',(.12,.14,.15),.10,.30)
for s in [-1,1]:
 uv('Synthetic ear',(s*.077,.012,1.857),(.014,.010,.026),face_mat)
 uv('Ear interface',(s*.084,.008,1.858),(.006,.011,.015),black_m,32)
 uv('Inset ocular globe',(s*.029,-.058,1.870),(.017,.009,.0075),white)
 uv('Iris',(s*.029,-.066,1.870),(.005,.0016,.005),eye_mat)
 uv('Pupil',(s*.029,-.0675,1.870),(.0022,.001,.0024),black)
 for top in [True,False]:wire('Anatomical eyelid',[(s*.013,-.062,1.870),(s*.029,-.067,1.876 if top else 1.865),(s*.045,-.057,1.870)],.0024,face_mat)
 wire('Subtle brow',[(s*.014,-.067,1.888),(s*.031,-.067,1.891),(s*.046,-.059,1.885)],.0013,mouth_mat)
 uv('Nostril shadow',(s*.009,-.089,1.821),(.0025,.001,.0012),mouth_mat,24)
wire('Upper sculpted lip',[(-.020,-.061,1.798),(-.008,-.069,1.801),(0,-.070,1.799),(.008,-.069,1.801),(.020,-.061,1.798)],.0022,mouth_mat)
wire('Lower sculpted lip',[(-.020,-.061,1.797),(0,-.070,1.793),(.020,-.061,1.797)],.0024,face_mat)
wire('Mouth fine crease',[(-.018,-.063,1.797),(0,-.071,1.797),(.018,-.063,1.797)],.0007,mouth_mat)
# Clean white seamless studio using a curved cyclorama.
studio=mat('Seamless white studio',(.83,.83,.83),0,.75)
profiles=[(-15,0),(2,0)]+[(2+3*math.sin(i*math.pi/40),3-3*math.cos(i*math.pi/40)) for i in range(1,21)]+[(5,10)]
vs=[];fs=[]
for y,z in profiles:vs.extend([(-30,y,z),(30,y,z)])
for j in range(len(profiles)-1):fs.append((j*2,j*2+1,j*2+3,j*2+2))
me=bpy.data.meshes.new('Cyclorama');me.from_pydata(vs,[],fs);me.update();o=bpy.data.objects.new('Seamless curved studio',me);bpy.context.collection.objects.link(o);finish(o,o.name,studio)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.world.use_nodes=True;scene.world.node_tree.nodes['Background'].inputs[0].default_value=(.8,.8,.8,1);scene.world.node_tree.nodes['Background'].inputs[1].default_value=.18
def aim(o,target):o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
def area(name,loc,power,size):
 d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;o=bpy.data.objects.new(name,d);bpy.context.collection.objects.link(o);o.location=loc;aim(o,(0,0,1.1))
area('Portrait softbox',(-3,-2,4),500,2.5);area('Right fill',(3,-2,3),65,3);area('Top rim',(0,2,4),450,3)
d=bpy.data.cameras.new('Reference portrait camera');cam=bpy.data.objects.new(d.name,d);bpy.context.collection.objects.link(cam);scene.camera=cam
scene.view_settings.view_transform='AgX';scene.render.image_settings.file_format='PNG';scene.render.resolution_percentage=100
output=os.path.join(ROOT,'renders_reference');os.makedirs(output,exist_ok=True)
shots=[('01_full_body',(2.6,-6,2.6),(0,0,1.02),78,1100,1500),('02_face',(.5,-2.6,1.99),(0,0,1.82),105,1200,1200),('03_back',(-1.4,2.8,2.0),(0,0,1.02),43,1100,1500)]
def shot(v):
 name,loc,target,lens,w,h=v;cam.location=loc;aim(cam,target);d.lens=lens;scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.filepath=os.path.join(output,name+'.png')
shot(shots[0]);bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'SELENE_REFERENCE.blend'))
for v in shots:shot(v);bpy.ops.render.render(write_still=True)
shot(shots[0]);bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'SELENE_REFERENCE.blend'))
print('REFERENCE COMPLETE',len(bpy.data.objects),'objects')
