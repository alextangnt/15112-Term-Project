from cmu_graphics import *
from PIL import Image

from classes import *
#from audioClass import Recording
from drawMethods import *
from gameMethods import *



#def home_onAppStart(app):

    

def home_onScreenActivate(app):
    app.paused = False
    app.onOff = 'on'
    app.pendingScreen = None
    app.currScreen = 'home'
    print('home screen')
    app.cloud = True

#####################Loading image################


############
# play screen
############


def home_redrawAll(app):
    drawBackground(app)
    drawCloud(app)
    drawTweater(app)
    drawButtons(app)
    #drawBird(app)
    #drawFood(app)

    
def splitScreen(app):
    app.Introx-=15
    for butt in app.butts:
        if butt.screen == app.currScreen:
            butt.cx+=15



            

def home_onMousePress(app,mouseX,mouseY):
    if app.currScreen == 'home':
        checkButtonPress(app,mouseX,mouseY)

def home_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)



def home_onKeyPress(app,key):
    checkPause(key)
    if key=="w":
        if Bird.rail>1: 
            Bird.rail-=1
            app.bird.targetRrail=False
            app.cy=(Bird.rail)*app.height/14-app.height/28
            
    elif key=="s":
        if Bird.rail<14: 
            Bird.rail+=1
            app.bird.targetRrail=False
            app.cy=(Bird.rail)*app.height/14-app.height/28
    elif key == 'q':
        #print("*** done recording")
        app.stream.stop_stream()
        app.stream.close()
        app.p.terminate()
        app.quit()

def home_onStep(app):
    if not app.paused:
        if app.pendingScreen == 'home':
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
