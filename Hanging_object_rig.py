import maya.cmds as cmds
import maya.mel
import re
from functools import partial

def Skin(joints, object):
	skinClust = cmds.skinCluster(joints[0], object[0], sm = 1, nw = 1, wd = 1, mi=4);
	cmds.geomBind(skinClust, bindMethod=3 )

object = cmds.ls(o = 1, sl=1)
sel = cmds.ls(os = 1, fl =1)
edges = []
joints = []

#	Select the three extremity edges: 2 for the rope extremities and one for the end of the object
for e in sel:
	split = e.split('.')
	edges.append(split[1][2:-1])

#	Get the loop
for i in range(0,len(edges)):
	cmds.select(object)
	cmds.polySelect(elb=int(edges[i]))
	#	Create clusters
	clust = cmds.cluster(n='clus#')
	cmds.select(cl=1)
	posi = cmds.getAttr(clust[0]+'HandleShape.origin')
	#	Create the joints
	joints.append(cmds.joint(n = '{}_joint_#'.format(object[0]) ,p = [posi[0][0], posi[0][1], posi[0][2]]))
	#	delete clusters
	cmds.delete(clust[0])

#	Set up the joint hierarchy
for i in reversed(range(1,len(edges))):
	cmds.parent(joints[i], joints[i-1])

#	Select first and last joints
cmds.select(cl=1)
cmds.select(joints[0])
cmds.select(joints[-1],add=1)

# curve dynamic??

#	Make joints dynamic
mel.eval('bt_makeJointsDynamicUI')

#	Skin to mesh but wait for selection changed
cmds.scriptJob(runOnce = 1, event =("SelectionChanged", partial(Skin, joints, object)))

#	Post-Tweak: Nucleus1: Set air density to 10, wind speed to 7
hairId = 17
mel.eval('currentTime 1')
mel.eval('playbackOptions -e -playbackSpeed 0 -maxPlaybackSpeed 1');
#mel.eval('setAttr "nucleus1.timeScale" 3.6')
#mel.eval('setAttr "nucleus1.spaceScale" 0.125')
#mel.eval('setAttr "nucleus1.airDensity" 0')
#mel.eval('setAttr "nucleus1.windNoise" 25')
#mel.eval('setAttr "nucleus1.airDensity" 10')
#mel.eval('setAttr "nucleus1.airDensity" 0')
#mel.eval('setAttr "nucleus1.windSpeed" 100')
#mel.eval('setAttr "nucleus1.windNoise" 5')
mel.eval('setAttr "hairSystemShape%s.stretchResistance" 200'%(hairId))
mel.eval('setAttr "hairSystemShape%s.compressionResistance" 200'%(hairId))
mel.eval('setAttr "hairSystemShape%s.bendResistance" 200'%(hairId))
mel.eval('setAttr "hairSystemShape%s.stiffnessScale[2].stiffnessScale_Position" 0.035'%(hairId))
mel.eval('setAttr "hairSystemShape%s.stiffnessScale[2].stiffnessScale_FloatValue" 0.08'%(hairId))
#cmds.PlaybackForward()

#	Post baking
mel.eval('bakeResults -simulation true -t "0:600" -hierarchy below -sampleBy 1 -oversamplingRate 1 -disableImplicitControl true -preserveOutsideKeys false -sparseAnimCurveBake false -removeBakedAttributeFromLayer false -removeBakedAnimFromLayer false -bakeOnOverrideLayer false -minimizeRotation true -controlPoints false -shape true {}'.format(joints[0]))

