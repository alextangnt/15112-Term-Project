from cmu_graphics import *

from classes import *
from audioClass import Recording
from drawMethods import *
from gameMethods import *


def play_onScreenActivate(app):
    app.onOff = 'on'
    app.pendingScreen = None
    print('play screen')
    app.currScreen = 'play'
    app.currScore = 0
    app.scoreE = Element('play',7.5*app.width/10,1*app.height/10,'y')
    app.scoreE.goOff()
    app.currLives = 5
    app.livesE = Element('play',6*app.width/10,1*app.height/10,'y')
    app.livesE.goOff()
    if not app.recorder.stream.is_active():
        app.recorder.start()
    app.gameOver = False
    app.overButton.goOff()
    app.birdAngle = 0
    Food.onScreenList = []
    Food.makeFoodList(app)
    Food.onScreenList.append(Food.upcomingList.pop(0))

def play_onMousePress(app,mouseX,mouseY):
    checkButtonPress(app,mouseX,mouseY)
    #print('setup click')

def play_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)

def play_redrawAll(app):
    #drawLine(app)
    drawBackground(app)
    drawCloud(app)
    
    drawBird(app)
    drawFood(app)
    drawScore(app)
    if app.gameOver:
        #drawRect(app.width/10,app.height/9,8*app.width/10,6*app.height/9,fill = 'white',opacity=40)
        drawLabel('YOU LOST SUCKERRRRRRR',app.width/2,app.height/2,font=app.font,size=50,fill=app.textColor,bold=True)
    drawButtons(app)

def play_onStep(app):
    if app.gameOver:
        app.currScreen = 'end'
        app.overButton.goOn()
    if not app.paused and not app.gameOver:
        if app.birdAngle!=0:
            loseLife(app)
        if app.pendingScreen == 'play':
            Element.allOff(app.currScreen)
            app.pendingScreen = None
        movingStep(app)
        Cloud.onStep(app)
        if app.currLives == 0:
            app.gameOver = True
        for cloud in Cloud.onScreenList:
                cloud.parameter[0]-=1
                if cloud.parameter[0]<-200:
                    Cloud.onScreenList.remove(cloud)
        if app.cloud==True:
            L=Cloud.CloudListGen(app)
            app.cloud=False 
            Cloud.upcomingList=L
            Cloud.onScreenList.append(Cloud.upcomingList.pop(0))
        if Food.upcomingList == []:
            Food.makeFoodList(app)
        eat(app)
        app.recorder.processAudio()
        if app.recorder.frames>=4:
            app.recorder.makeFft()
        if app.recorder.mag >= Recording.noiseMag:
            app.bird.openMouth()
        else:
            app.bird.closeMouth()
        
        #moveRail(app)
        for food in Food.onScreenList:
            food.parameter[0]-=4
            food.parameter[2]-=4
            if food.parameter[2]<-30:
                Food.onScreenList.remove(food)
                app.currLives-=1
                loseLife(app)

        Food.onStep(app)
        

        app.count0= (0.5 + app.count0) % len(app.birdClosedGif)
        app.count1= (0.5 + app.count1) % len(app.birdOpenGif)
        app.count2= (0.25 + app.count2) % len(app.bugGif)
        app.count3= (0.5 + app.count3) % len(app.bugGifFast)
        

        #app.bird.cy = app.height-app.recorder.getCastFreq()
        moveSmooth(app)
        #print(app.recorder.pitchList[-1])
        # cy = app.recorder.pitchList[-1]
        # if cy<180:
        #     app.bird.targetRrail=14
        # elif cy>430:
        #     app.bird.targetRrail=1
        # else:
        #     app.bird.targetRrail=int(14-(((cy-180)/(app.height/14))+1))
        
        #put this in the audioClass
        if len(app.recorder.pitchList)>10:
            app.recorder.pitchList = app.recorder.pitchList[-9:]

def play_onKeyPress(app,key):
    checkPause(key)