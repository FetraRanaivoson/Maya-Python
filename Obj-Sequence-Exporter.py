import maya.cmds as cmds
import maya.mel as mel
import sys
import re

fileIndex = 1
frame = 1
sel = cmds.ls (sl=1)
maxFrame = 70

while frame <= maxFrame:
	if frame == 1:
		mel.eval('file -force -options "groups=1;ptgroups=1;materials=1;smoothing=1;normals=1" -typ "FBX export" -pr -es "E:/Titan1Studio/Events-At-Unity-VR/Animation/ObjCache/fbx_{}.fbx"'.format(fileIndex))
	else:
		mel.eval('file -force -options "groups=1;ptgroups=1;materials=0;smoothing=1;normals=1" -typ "FBX export" -pr -es "E:/Titan1Studio/Events-At-Unity-VR/Animation/ObjCache/fbx_{}.fbx"'.format(fileIndex))
	fileIndex +=1
	frame += 1
	cmds.currentTime(frame)