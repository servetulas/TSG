import maya.cmds as mc
import pymel.core as pm
import maya.mel as mel
import maya.app.general.createImageFormats as createImageFormats
import random
from functools import partial

#github
#colorInputTarget
bgobjects=[]
rendercount = 1
bggroup = mc.group( em=True, name='bggroup' )
renderpath = mc.internalVar(upd=True)+"SG Output/"

def UI():  
    #function attributes that will be used for getting final settings from the UI
    UI.targetPrim = 'Cube'
    UI.population = 0
    UI.resolution = 512

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
      # print('deleted previous window')
  
    uiwindow = mc.window('UIw22342ggfg422433g4fi4442ndow', t = 'Training Scene Generator', widthHeight=(320,520), mnb = False, mxb = False, sizeable = False)

    #main layout
    mainLayout = mc.columnLayout(w=320, h=520, co=('left',10))

    #logo
    mc.separator(12)
    imagePath = mc.internalVar(upd=True)+"icons/SG2000Logo.png"
    mc.image(w=320, h=93, image = imagePath)
    
    mc.separator(h=12)   
   #mc.text("Pick target primitive")
    mc.separator(h=6)
    #commit
    #dropdown for target object
    targetDropdownMenu = mc.optionMenu('targetDropdownMenu',w=280, label = 'Target Primitive Geometry: ', cc = partial(updateTargetPrim))
    
    #mc.checkBox(label='color', onc = partial(widgetColorOn), ofc = partial(widgetColorOff))
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

    mc.separator(6)
    mc.rowColumnLayout( numberOfRows =1)
    mc.checkBox('place_in_mid', v=True, cc=setTargetMidBool)
    mc.checkBox('rand_rotation', cc=setRandomOrientation)
    mc.setParent('..')
    mc.rowColumnLayout( numberOfRows =1)
    mc.button(label='CREATE', c=partial(createTargetPrim))
    mc.button(label='DELETE', c=partial(deleteTargetPrim))
    mc.setParent('..')
    
    mc.separator(h=18)
    mc.text('Background Population Density')
    mc.rowColumnLayout( numberOfRows = 1)
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
    UI.targetMid = mc.checkBox('place_in_mid', query = True, v = True)
    print(UI.targetMid)
    
def setRandomOrientation(*args):

    UI.randomOrientation = mc.checkBox('rand_rotation', query=True, v=True)
    
    if UI.randomOrientation == True:
        UI.targetOrientation = (random.randint(0,360), random.randint(0,360), random.randint(0,360))
        print('randoming')
    else:
       UI.targetOrientation = (0,0,0)
       
    print(UI.targetOrientation)
    
def setTargetRGB(*args):
    UI.targetR = mc.floatSlider('targetRSlider', query =True, value=True)/mc.floatSlider('targetRSlider', query = True, max = True)
    UI.targetG = mc.floatSlider('targetGSlider', query =True, value=True)/mc.floatSlider('targetGSlider', query = True, max = True)
    UI.targetB = mc.floatSlider('targetBSlider', query =True, value=True)/mc.floatSlider('targetBSlider', query = True, max = True)

    mc.setAttr(Materials.shader+'.color', UI.targetR, UI.targetG, UI.targetB)

def deleteTargetPrim(*args):
    if createTargetPrim.targetprim!=0:
        mc.delete(createTargetPrim.targetprim)
    #print(createTargetPrim.targetprim)

def createTargetPrim(*args):
    #delete existing target primitive
    #deleteTargetPrim()
    
    createTargetPrim.targetprim = 0
    
    if UI.targetPrim == 'Cube':
        createTargetPrim.targetprim = mc.polyCube(sx=1, sy=1, sz=1)
        mc.hyperShade( assign = Materials.shader)
        #mc.polyColorPerVertex( rgb=(UI.targetR, UI.targetG, UI.targetB), cdo = True )
        #if UI.randomOrientation != False:
        #mc.select(targetprim)
        mc.rotate(UI.targetOrientation[0], UI.targetOrientation[1], UI.targetOrientation[2], a = True)

        if UI.targetMiddle != True:
            mc.move(random.randint(-10, 10), random.randint(-10, 10), 35)
        else:
            mc.move(0, 0, 35)
        
    if UI.targetPrim == 'Sphere':
        mc.polySphere(sx=24, sy=24, r=1)
        mc.hyperShade( assign = Materials.shader)
        #mc.polyColorPerVertex( rgb=(UI.targetR, UI.targetG, UI.targetB), cdo = True )
        if UI.targetMiddle != True:
            mc.move(random.randint(-10, 10), random.randint(-10, 10), 35)
        
    if UI.targetPrim == 'Cylinder':
        mc.polyCylinder(sx=24, sy=2, sz=2)
        mc.hyperShade( assign = Materials.shader)
        #mc.polyColorPerVertex( rgb=(UI.targetR, UI.targetG, UI.targetB), cdo = True )
        if UI.targetMiddle != True:
            mc.move(random.randint(-10, 10), random.randint(-10, 10), 35)
        
    if UI.targetPrim == 'Torus':
        mc.polyTorus(n='target',sx=24, sy=16, r=2, sr=1)
        mc.hyperShade( assign = Materials.shader)
        #mc.polyColorPerVertex( rgb=(UI.targetR, UI.targetG, UI.targetB), cdo = True )
        if UI.targetMiddle != True:
            mc.move(random.randint(-10, 10), random.randint(-10, 10), 35)
        
    if UI.targetPrim == 'Cone':
        mc.polyCone(sx=1, sy=1, sz=1)
        mc.hyperShade( assign = Materials.shader)
        #mc.polyColorPerVertex( rgb=(UI.targetR, UI.targetG, UI.targetB), cdo = True )
        if UI.targetMiddle != True:
            mc.move(random.randint(-10, 10), random.randint(-10, 10), 35)
  
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

    #dir light
    pm.directionalLight(intensity=0.8)
    
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
    
def BackgroundPlane():
    plane = mc.polyPlane(w=90, h=80, ax=[0,0,1])
    bgobjects.append(plane)
    mc.hyperShade( assign = Materials.bgplaneshader)
    mc.move(0,0,-30)


UI()
populateTargetPrim()
Materials()
#BackgroundPlane()



 
