import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import maya.app.general.createImageFormats as createImageFormats
import random
from functools import partial


#colorInputTarget
bgobjects=[]
rendercount = 1

#unused group for background objects
bggroup = mc.group( em=True, name='bggroup' )

#create a folder callsed SG Output in dir.
renderpath = mc.internalVar(upd=True)+"SG Output/"

def UI():  
    #function attributes that will be used for getting final settings from the UI
    UI.targetPrim = 'Cube'
    UI.population = 0
    UI.resolution = 256
    #default radius/size 
    UI.targetPrimSize = 2

    #target color
    UI.targetR = 1
    UI.targetG = 1
    UI.targetB = 1

    #target rotation
    UI.targetOrientation = (0, 0, 0)
    UI.randomOrientation = False;

    #target in middle/random
    UI.targetMiddle = True

    #if mc.window('UIwindow', exists = True):
    #  mc.deleteUI(uiwindow)
    #  print('deleted previous window')
  
    uiwindow = mc.window('UIw22342ggfg422433g4fi4442ndow', t = 'Training Scene Generator', widthHeight=(320,520), mnb = False, mxb = False, sizeable = False)

    #main layout 
    mainLayout = mc.columnLayout(w=320, h=520, co=('left',10))

    #header image
    mc.separator(12)
    imagePath = mc.internalVar(upd=True)+"icons/SG2000Logo.png"
    mc.image(w=320, h=93, image = imagePath)
    mc.separator(h=18)   


    #-------------------------------------TARGET PRIM-------------------------------------#
    #dropdown for target object
    targetDropdownMenu = mc.optionMenu('targetDropdownMenu',w=280, label = 'Target Primitive Geometry: ', cc = partial(updateTargetPrim))

    #RGB sliders
    mc.separator(h=6)
    mc.text("Target Primitive Color RGB")
    mc.separator(h=6)

    mc.rowColumnLayout( numberOfRows = 1, rowSpacing = (10, 10))
    mc.text('R:')
    mc.floatSlider('targetRSlider', min=0, max=30, value=0, step=1, cc=setTargetRGB, bgc=(.6,0.2,0.2))
    mc.text('G:')
    mc.floatSlider('targetGSlider', min=0, max=30, value=0, step=1, cc=setTargetRGB, bgc=(.2,.6,.2))
    mc.text('B:')
    mc.floatSlider('targetBSlider', min=0, max=30, value=0, step=1, cc=setTargetRGB, bgc=(0.4,0.4,.8))
    mc.setParent('..')

    #POSITION AND ORIENTATION 
    mc.separator(6)
    mc.rowColumnLayout(numberOfRows =1)
    mc.checkBox('place_in_mid', v=True, cc=setTargetMidBool)
    mc.checkBox('rand_rotation', cc=setRandomOrientation)
    mc.setParent('..')

    #CREATE OR DELETE PRIM
    mc.rowColumnLayout(numberOfRows =1)
    mc.button(label='CREATE', c=partial(createTargetPrim))
    mc.button(label='DELETE', c=partial(deleteTargetPrim))
    mc.setParent('..')
    #---------------------------------END OF TARGET PRIM---------------------------------#

    #---------------------------------BACKGROUND OBJECTS---------------------------------#
    mc.separator(h=18)
    mc.text('Background Population Density')
    mc.rowColumnLayout(numberOfRows = 1)
    mc.separator(h=12)
    mc.text('few')
    mc.intSlider('popSlider', min=0, max=400, value=0, step=1, cc=setPopulation)
    mc.text('many objects in the background')
    mc.setParent('..')

   # mc.text('Background Population Variety')
   # mc.rowColumnLayout( numberOfRows = 1)
   # mc.separator(h=6)
   # mc.text('few')
   # mc.intSlider('popSlider', min=0, max=400, value=0, step=80, cc=setPopulation)
   # mc.text('many types of primitives')
    mc.setParent('..')
    mc.rowColumnLayout(numberOfRows = 1)
    mc.separator(h=6)
    mc.button(label='BUILD', c=partial(buildBackground))
    mc.button(label='DELETE', c=partial(deleteBackground))
    mc.setParent('..')

    #-----------------------------END OF BACKGROUND OBJECTS-------------------------------#

    #--------------------------------------OUTPUT-----------------------------------------#
    mc.separator(h=12)
    mc.text('Rendering')
    mc.separator(h=6)

    mc.rowColumnLayout( numberOfRows = 1)
    mc.button('change save directory', bgc=(.2,.6,.2), c=changeRenderpath)
    mc.separator(h=6)
    mc.setParent('..')
    
    mc.rowColumnLayout( numberOfRows = 1)
    mc.button(label='CAMERA', c=partial(makeCamera))
    mc.button(label='X', c=partial(deleteCamera), bgc=(.8,.2,.2))
    mc.button(label='RENDER', c=partial(RenderScenes))
    mc.intField('rendercountfield', w=40, minValue = 1, maxValue = 4000, cc=updateRenderCount)
    mc.text('times with these settings')
    mc.setParent('..')

    mc.showWindow(uiwindow)
    
    #-----------------------------------END OF OUTPUT------------------------------------#



 
