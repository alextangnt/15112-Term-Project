from cmu_graphics import *
from PIL import Image

from classes import *
from audioClass import Recording
from drawMethods import *
from gameMethods import *


def modes_onAppStart(app):
    app.modesButts = {Button('modes','Sing Mode!',app.width/5,app.height/2-20),
            Button('modes','Hard',4*app.width/5,30+app.height/2),
            Button('modes','Medium',4*app.width/5,app.height/2-30),
            Button('modes','Easy',4*app.width/5,app.height/2-90),
            Button('modes','Infinite',app.width/2,app.height/2),
            Button('modes','Done',app.width/2,3.7*app.height/5)}
    print(Button.butts)
    app.bW,app.bH = 60,30


def modes_onScreenActivate(app):
    app.paused = False
    app.onOff = 'on'
    #app.pendingScreen = None
    app.currScreen = 'modes'
    app.message = None
    app.message2 = None
    
def modes_redrawAll(app):
    drawBackground(app)
    drawCloud(app)
    #drawRect(app.width/10,app.height/9,8*app.width/10,6*app.height/9,fill = 'white',opacity=40)
    drawLabel('Pick your poison...', app.width/2,app.height/5,size=20,font=app.font,fill=app.textColor,bold=True)
    drawButtons(app)
    if app.message != None:
        drawLabel(app.message,app.width/2,6*app.height/7 + 30,size=17,font=app.font,fill=app.textColor)
    if app.message2 != None:
        drawLabel(app.message2,app.width/2,4*app.height/5 + 30,size=20,font=app.font,fill=app.textColor,bold=True)

def modes_onMousePress(app,mouseX,mouseY):
    checkButtonPress(app,mouseX,mouseY)
    #print('setup click')

def modes_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)


def modes_onStep(app):
    if not app.paused:
        if app.pendingScreen == 'modes':
            Element.allOff(app.currScreen)
            app.pendingScreen = None
        movingStep(app)
        Cloud.onStep(app)
        for cloud in Cloud.onScreenList:
                cloud.parameter[0]-=1
                if cloud.parameter[0]<-200:
                    Cloud.onScreenList.remove(cloud)
        if app.cloud==True:
            L=Cloud.CloudListGen(app)
            app.cloud=False 
            Cloud.upcomingList=L
            Cloud.onScreenList.append(Cloud.upcomingList.pop(0))
   

        

def modes_onKeyPress(app, key):
    checkPause(key)
    if key == 'h':
        setActiveScreen('home')