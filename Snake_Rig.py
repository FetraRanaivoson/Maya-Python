import maya.cmds as cmds
import maya.mel
import re

sel = cmds.ls(os=1, fl=1)
obj = cmds.ls(o=1, sl=1)
num = []
out = []
edges = []
joints = []
steps = 2
	
for one in sel:
	split = one.split('.')
	num.append(split[1][2:-1])

size = len(num)

if(size):
	if size == 1:
		edges = cmds.polySelect(er=(int(num[0])),ns = 1) #get the edge ring (not loop)
	if size == 2:
		edges = cmds.polySelect(erp=( int(num[0]), int(num[1]) ), ns = 1) #get shortest path btw 2 exact edge rings
			#print('%s' %(edges))
	if size > 2:
		edges = num
	#for one in edges:
	for i in reversed(range(0, len(edges))):
		if i%steps == 0:
			cmds.select(obj)
			#cmds.polySelect(elb=int(one)) #if one edge selected, the ring generated will cycle through each loop/border
			cmds.polySelect(elb = int(edges[i]))
			clust = cmds.cluster(n='clus#')
			cmds.select(cl=1)
			posi = cmds.getAttr(clust[0]+'HandleShape.origin')
			joints.append(cmds.joint(p = [posi[0][0], posi[0][1], posi[0][2]]))
			cmds.delete(clust[0])
			print(edges[i])
	cmds.select(cl=1)
	#for i in reversed(range(1,len(edges))):
	for i in reversed(range(1,len(joints))):
		cmds.parent(joints[i], joints[i-1])
	cmds.joint(joints[0], e=1, oj= 'xyz', sao= 'zup', ch=1, zso=1)
	cmds.joint(joints[-1], e=1, o=(0,0,0))
	out.append(joints[0])
	cmds.select(out)	
			
else:
	print("Nothing is selected")
	
# Skin
skinClust = cmds.skinCluster(joints[len(joints)-1], obj[0], sm = 1, nw = 1, wd = 1, mi=4)
cmds.geomBind(skinClust, bindMethod=3 )
		
# Rig
ik = cmds.ikHandle(sj= joints[0], ee= joints[len(joints)-1], solver = 'ikSplineSolver', pcv= 0, scv = 0)
crv = ik[2]
# number of CVs = degree + spans:
degs = cmds.getAttr( '%s.degree'%(crv))
spans = cmds.getAttr( '%s.spans'%(crv))
cvCount = degs+spans

# Create controls
ctrls = []
for i in range(0, cvCount-1):
	ct = cmds.circle(n='cv#_ctrl',ch = 0, r = 15)
	ctrls.append(ct)
	# Move the controller to the position of the current CV
	pos = cmds.getAttr('%s.cv[%s]' % (crv,i));
	cmds.move(pos[0][0], pos[0][1], pos[0][2], ct, ws = True)
	# Freeze transform the controller
	cmds.makeIdentity(ct, a=1, t=1, r=1, s=1)
	#cmds.matchTransform('ctrls[%s]'%(i),'joints[%s]'%(i),rot = 1)
	
# Create clusters: exception: first two and last two cvs are bound both to one cluster
clusters = []
cmds.select('%s.cv[0]'%(crv))
cmds.select('%s.cv[1]'%(crv), add = 1)
clust = cmds.cluster(n='clus#')
cmds.parent(clust,ctrls[0])
clusters.append(clust)
cmds.select(cl=1)

cmds.select('%s.cv[%s]'%(crv,cvCount-2))
cmds.select('%s.cv[%s]'%(crv,cvCount-1), add = 1)
clust = cmds.cluster(n='clus#')
cmds.parent(clust,ctrls[len(ctrls)-1])
clusters.append(clust)
cmds.select(cl=1)

currentCv = 2
for i in range(1, cvCount - 2):
	cmds.select('%s.cv[%s]'%(crv,currentCv))
	clust = cmds.cluster(n='clus#')
	cmds.parent(clust,ctrls[i])
	clusters.append(clust)
	cmds.select(cl=1)
	currentCv += 1
	
cmds.select(cl=1)
# Add the sine deformer to all curves
for ctrl in ctrls:
	cmds.select(ctrl,add=1)
cmds.select(crv,add=1)
sineDef = cmds.nonLinear(type='sine')

# Tweak sine deformer
mel.eval('setAttr "%s.rotateX" 90'%(sineDef[1]))
mel.eval('setAttr "%s.amplitude" 0.2'%(sineDef[0]))
mel.eval('setAttr "%s.wavelength" 1.5'%(sineDef[0]))
mel.eval('setAttr "%s.offset" -10'%(sineDef[0]))
#for ground snake vines to restrict root from moving
#mel.eval('setAttr "%s.dropoff" -1'%(sineDef[0])) 
#for C shape vines to restrict root from moving
#mel.eval('setAttr "%s.highBound" 0.0'%(sineDef[0]));

# Create keyframes
maxFrame = 1500
mel.eval('currentTime 0 ')
mel.eval('setKeyframe "%s.off"'%(sineDef[0]))
mel.eval('currentTime %s'%(maxFrame))
mel.eval('setAttr "%s.offset" 10'%(sineDef[0]))
mel.eval('currentTime 0 ')
	
	
	
	
	
	
	
	
	
	
	
	


# Group the tipCtrl
tipGrp = cmds.group (tipCtrl, n = 'tip_Grp');
#cmds.matchTransform(tipGrp, 'joint10');
cmds.matchTransform(tipGrp, jointList[len(jointList)-1]);
cmds.makeIdentity(tipGrp, a=1, t=1, r=1, s=1);

# The animation
#cmds.setKeyframe(ik, attribute = 'ty', value=0, time=1)
#cmds.setKeyframe(ik, attribute = 'ty', value=10, time=20)
#cmds.setKeyframe(ik, attribute = 'ty', value=0, time=40)
