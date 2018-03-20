import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import maya.app.general.createImageFormats as createImageFormats
import random
from functools import partial


#colorInputTarget
bgobjects=[]
rendercount = 1
targetpositions = []

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
    UI.targetMiddle = False
    UI.targetOffsetRange = 1

    UI.lightRot = (0.0, 0.0, 0.0)
    UI.lightIntensity = 0.8

    UI.exportTargetData = True
    UI.exportLightData = False
    UI.exportNoiseData = False
    

    #if mc.window('UIwindow', exists = True):
    #  mc.deleteUI(uiwindow)
    #  print('deleted previous window')
  
    uiwindow = mc.window('UIw2255342s32222222ndow', t = 'Training Scene Generator', widthHeight=(320,520), mnb = False, mxb = False, sizeable = False)

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

    #POSITION AND ORIENTATION AND SIZE
    mc.separator(6)
    mc.rowColumnLayout(numberOfRows =1)
    mc.checkBox('in_mid', v=UI.targetMiddle, cc=setTargetMidBool)
    mc.checkBox('rand_rot', cc=setRandomOrientation)

    mc.text('size: ')
    mc.intField('radiusIntField', w =30, v=2, cc=changeRadiusIntField)
    mc.text('offset: ')
    mc.intField('offsetIntField', w =30, maxValue=10, minValue = 0, v=UI.targetOffsetRange, cc=changeOffsetIntField)
    mc.separator(6)
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

    #--------------------------------------LIGHTS-----------------------------------------#
    mc.rowColumnLayout(numberOfRows = 1)
    mc.text('light rotation')
    mc.separator(w=120)
    mc.text('light intensity')
    mc.setParent('..')
    mc.rowColumnLayout(numberOfRows = 1)
    mc.separator(h=6)
    mc.floatField('lxr', w=40, cc=setLightRot)
    mc.floatField('lyr', w=40, cc=setLightRot)
    mc.floatField('lzr', w=40, cc=setLightRot)
    mc.separator(w=60)
    mc.floatField('lin', w=40, cc=setLightIntensity, v = 0.8)
    mc.setParent('..')
    #-----------------------------------END OF LIGHTS-------------------------------------#

    
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

    mc.rowColumnLayout( numberOfRows = 1)
    mc.text('Export   : ')
    mc.checkBox('target', v=UI.exportTargetData)
    mc.checkBox('light', v=UI.exportLightData)
    mc.checkBox('noise', v=UI.exportNoiseData)
    mc.setParent('..')


    
    mc.showWindow(uiwindow)
    
    #-----------------------------------END OF OUTPUT------------------------------------#


def init():
    UI()
    populateTargetPrim()
    Materials()

def changeOffsetIntField(*args):
    #normalized 0-1
    UI.targetOffsetRange = float(mc.intField('offsetIntField', q = True, v = True))/10.0

def setLightIntensity(*args):
    UI.lightIntensity = mc.floatField('lin',q = True ,v = True)

def setLightRot(*args):
     UI.lightRot = (mc.floatField('lxr',q = True ,v = True),
                    mc.floatField('lyr',q = True ,v = True),
                    mc.floatField('lzr',q = True ,v = True))
    #UI.lightRot[0]=mc.intField('lxr',q = True ,v = True)
     print(UI.lightRot)

    

def changeRadiusIntField(*args):
    UI.targetPrimSize = mc.intField('radiusIntField', query = True, v = True)
    print('new size is set to: '+str(UI.targetPrimSize))

def changeRenderpath(*args):
    global renderpath
    renderpath = mc.fileDialog2(fm=3, cap='open')
    print(renderpath)
      
    
def updateRenderCount(*args):
    print('render count updated')
    global rendercount
    rendercount = mc.intField('rendercountfield', q=True, v=True)

    
def deleteCamera(*args):
    mc.delete(makeCamera.cam)

def Materials():
    Materials.shader = mc.shadingNode('blinn',asShader=True)
    Materials.bgplaneshader = mc.shadingNode('blinn',asShader=True, )
    mc.setAttr(Materials.bgplaneshader+'.color', 1,1,1)

def setTargetMidBool(*args):
    UI.targetMid = mc.checkBox('in_mid', query = True, v = True)
    print(UI.targetMid)
    
def setRandomOrientation(*args):

    UI.randomOrientation = mc.checkBox('rand_rot', query=True, v=True)
    
    if UI.randomOrientation == True:
        UI.targetOrientation = (random.randint(0,360), random.randint(0,360), random.randint(0,360))
        print('random rotation')
    else:
       UI.targetOrientation = (0,0,0)
       
    print(UI.targetOrientation)
    
def setTargetRGB(*args):
    #normalized 0-1
    UI.targetR = mc.floatSlider('targetRSlider', query =True, value=True)/mc.floatSlider('targetRSlider', query = True, max = True)
    UI.targetG = mc.floatSlider('targetGSlider', query =True, value=True)/mc.floatSlider('targetGSlider', query = True, max = True)
    UI.targetB = mc.floatSlider('targetBSlider', query =True, value=True)/mc.floatSlider('targetBSlider', query = True, max = True)

    mc.setAttr(Materials.shader+'.color', UI.targetR, UI.targetG, UI.targetB)

def deleteTargetPrim(*args):
    if createTargetPrim.targetprim!=0:
        mc.delete(createTargetPrim.targetprim)
    #print(createTargetPrim.targetprim)

def assignMatAndPlaceInScene(obj, *args):

    setRandomOrientation()
    
    mc.select(obj)
    mc.scale(UI.targetPrimSize, UI.targetPrimSize, UI.targetPrimSize)
    mc.hyperShade( assign = Materials.shader)
    mc.rotate(UI.targetOrientation[0], UI.targetOrientation[1], UI.targetOrientation[2], a = True)

    if UI.targetMiddle != True:
        mc.move(random.uniform(-UI.targetOffsetRange, UI.targetOffsetRange),
        random.uniform(-UI.targetOffsetRange, UI.targetOffsetRange),
        35)
        print(UI.targetOffsetRange)
    else:
        mc.move(0, 0, 35)

def createTargetPrim(*args):
    #delete existing target primitive
    #deleteTargetPrim()
    
    createTargetPrim.targetprim = 0
    
    if UI.targetPrim == 'Cube':
        createTargetPrim.targetprim = mc.polyCube(sx=1, sy =1, sz =1)
        assignMatAndPlaceInScene(createTargetPrim.targetprim[0])
        
    if UI.targetPrim == 'Sphere':
        createTargetPrim.targetprim = mc.polySphere(sx=24, sy=24, r=1)
        assignMatAndPlaceInScene(createTargetPrim.targetprim[0])
        
        
    if UI.targetPrim == 'Cylinder':
        createTargetPrim.targetprim = mc.polyCylinder(sx=24, sy=2, sz=2)
        assignMatAndPlaceInScene(createTargetPrim.targetprim[0])
        
    if UI.targetPrim == 'Torus':
        createTargetPrim.targetprim = mc.polyTorus(n='target',sx=24, sy=16, r=2, sr=1)
        assignMatAndPlaceInScene(createTargetPrim.targetprim[0])
        
    if UI.targetPrim == 'Cone':
        createTargetPrim.targetprim = mc.polyCone(sx=1, sy=1, sz=1)
        assignMatAndPlaceInScene(createTargetPrim.targetprim[0])
  
def populateTargetPrim():
    targetPrimList = ('Cube', 'Cylinder', 'Torus', 'Cone', 'Sphere')
    for prim in targetPrimList:
        mc.menuItem(label=prim, parent ='targetDropdownMenu')

def widgetColorOn(*args):
    if mc.colorInputWidgetGrp('colorInputTarget', exists = True):
        print('ALREADY EXISTS')
    else:
        colorInputTarget = mc.colorInputWidgetGrp('colorInputTarget',label = 'Color', rgb =(1, 0 ,0), w=280)
        print('ON')

def widgetColorOff(*args):
    if mc.colorInputWidgetGrp('colorInputTarget', exists = True):
        mc.deleteUI('colorInputTarget', control=True)
        print('OFF') 

def updateTargetPrim(*args):
    selectedTarget = mc.optionMenu('targetDropdownMenu', query = True, value = True)
    UI.targetPrim = selectedTarget
    print('selected target primitive is a '+UI.targetPrim)

def setPopulation(*args):
    popValue = mc.intSlider('popSlider', query =True, value=True)
    UI.population = popValue
    print('background poopulation density is now set to '+ str(UI.population))


def buildBackground(*args):
    BackgroundPlane()
    if len(bgobjects)!=0:
        global bgobjects
        bgobjects=[]
        print('cleared bgobjects')
    
    for i in range(UI.population):   
        bgobj = mc.polySphere(sx=24, sy=24, r=2)
        mc.move(random.randint(-20,20), random.randint(-20,20), random.randint(-40,20))
        bgobjects.append(bgobj)
        #bggroup
        #print(bgobjects[i])

def deleteBackground(*args):
    for i in bgobjects:
        #mc.delete(bgobjects[i])
        mc.delete(i[0])
       
        print('bgobject is this long: '+str(len(bgobjects)))
            #mc.move(i[0],random.randint(-20,20), random.randint(-20,20), random.randint(-5,5))
        
    #bgobjects = []
    
    

def makeCamera(*args):
    #set render resolution
    mc.setAttr('defaultResolution.height', UI.resolution)
    mc.setAttr('defaultResolution.width', UI.resolution)
    #square image - 1/1 ratio for no distortion
    mc.setAttr('defaultResolution.deviceAspectRatio', 1)
    #makeCamera.cam
    makeCamera.cam = pm.camera(dof=True, ar=1, fd=10)
    #mc.setAttr(camera1.translateZ, 45);
    mel.eval('setAttr "camera1.translateZ" 45;')
    #print(len(UI.lightRot))
    #dir light
    #print(UI.lightRot)
    #print(str(UI.lightRot[0])+' '+str(UI.lightRot[1])+' '+str(UI.lightRot[2]))
    pm.directionalLight(intensity=UI.lightIntensity, rot = (UI.lightRot[0], UI.lightRot[1], UI.lightRot[1]))
    
    #mel.eval('renderWindowRender redoPreviousRender renderView')
    makeCamera.editor = 'renderView'

    #try to str(cam[0]) later instead of 'cameraShape1'
    mc.lookThru('perspView', 'cameraShape1')
    

def Render(k, *args):
    formatManager = createImageFormats.ImageFormats()
    formatManager.pushRenderGlobalsForDesc("JPEG")
              
    mc.render();
    global renderpath
    mc.renderWindowEditor(makeCamera.editor, crc = str(makeCamera.cam[0]), e=True, writeImage=str(renderpath[0]+'/testImage'+str(k)+'.jpg'))

    formatManager.popRenderGlobals()          


def RenderScenes(*args):

    #print(rendercount)
      
    i=1
    global rendercount
    while i<rendercount:
        getSceneData()
        print('rendered 1 frame')
        Render(i)
        i=i+1
            
        #REMAKE SCENE HERE
        deleteBackground()
        buildBackground()
        
        deleteTargetPrim()
        createTargetPrim()
        #END OF REMAKE
        
    print('rendered') 
    writeData()
    
def BackgroundPlane():
    plane = mc.polyPlane(w=90, h=80, ax=[0,0,1])
    bgobjects.append(plane)
    mc.hyperShade( assign = Materials.bgplaneshader)
    mc.move(0,0,-30)

def writeData():
    file=open('c:/users/servet/desktop/prims.txt', 'w+')
    #print(mc.getAttr(createTargetPrim.targetprim[0]+'.translate'))
    
    s='tgt\npos'+str(targetpositions)

    if UI.exportLightData:
        s = '\nlight\nrot'+str(UI.lightRot)
        s = '\n\pow'+str(UI.lightIntensity)
    if UI.exportNoiseData:
        s = '\nnoise\npos'+str(UI.lightRot)
        s = '\n\cols'+str(UI.lightIntensity)
    
    #s=s+str(mc.getAttr(createTargetPrim.targetprim[0]+'.translate'))+'\n'
    
    #while i<200:
    #    s = s+str(UI.target)+'\n'
    #    i=i+1

    file.write(s)
    file.close()

def getSceneData():
    global targetpositions
    targetpositions.append(mc.getAttr(createTargetPrim.targetprim[0]+'.translate'))
    print(targetpositions)
    






