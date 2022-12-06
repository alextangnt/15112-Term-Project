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

#####################Loading image################


############
# play screen
############


def home_redrawAll(app):
    
    #drawLine(app)
    drawBackground(app)
    drawCloud(app)
    drawTweater(app)
    #drawPause(app)
    drawButtons(app)
    #drawBird(app)
    #drawFood(app)
    #drawblack(app)

    
def splitScreen(app):
    app.Introx-=15
    for butt in app.butts:
        if butt.screen == app.currScreen:
            butt.cx+=15


#def pending()

            

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
        print("*** done recording")
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


        # if app.started:
        #     if app.Introx>-500:
        #         splitScreen(app)
        #     eat(app)
        #     app.recorder.processAudio()
        #     if app.recorder.frames>=4:
        #         app.recorder.makeFft()
        #     if app.recorder.mag >= Recording.noiseMag:
        #         app.bird.openMouth()
        #     else:
        #         app.bird.closeMouth()
            
        #     #moveRail(app)
        #     for food in Food.onScreenList:
        #         food.parameter[0]-=4
        #         food.parameter[2]-=4
        #         if food.parameter[2]<-200:
        #             Food.onScreenList.remove(food)

        #     Food.onStep(app)
            

        #     app.count0= (0.5 + app.count0) % len(app.birdClosedGif)
        #     app.count1= (0.5 + app.count1) % len(app.birdOpenGif)
        #     app.count2= (0.25 + app.count2) % len(app.bugGif)
        #     app.count3= (0.5 + app.count3) % len(app.bugGifFast)
            

        #     #app.bird.cy = app.height-app.recorder.getCastFreq()
        #     moveSmooth(app)
        #     #print(app.recorder.pitchList[-1])
        #     # cy = app.recorder.pitchList[-1]
        #     # if cy<180:
        #     #     app.bird.targetRrail=14
        #     # elif cy>430:
        #     #     app.bird.targetRrail=1
        #     # else:
        #     #     app.bird.targetRrail=int(14-(((cy-180)/(app.height/14))+1))
            
        #     #put this in the audioClass
        #     if len(app.recorder.pitchList)>10:
        #         app.recorder.pitchList = app.recorder.pitchList[-9:]

