from cmu_graphics import *

from classes import *
from audioClass import Recording
from drawMethods import *
from gameMethods import *


def play_onScreenActivate(app):
    app.textColor = RGB(22,33,63)
    app.timestamp = None
    app.events = {'sunset':None,
                'dark':None,
                'sunrise':None,
                'day':None}
    app.time = 0
    app.paused = False
    app.lines = False
    app.onOff = 'on'
    app.pendingScreen = None
    print('play screen')
    app.currScreen = 'play'
    app.currScore = 0
    app.scoreE = Element('play',7.5*app.width/10,1*app.height/15,'y')
    app.scoreE.goOff()
    app.currLives = 5
    app.livesE = Element('play',6*app.width/10,1*app.height/15,'y')
    app.livesE.goOff()
    app.infinite = False
    if not app.recorder.stream.is_active():
        app.recorder.start()
    app.gameOver = False
    app.overButton.goOn()
    app.homeButton.goOn()
    app.birdAngle = 0
    Food.onScreenList = []
    Food.makeFoodList(app)
    Food.onScreenList.append(Food.upcomingList.pop(0))

def play_onKeyPress(app,key):
    checkPause(key)
    if key == 'l':
        app.lines = not app.lines
        print('lines')
    elif key == 'r':
        setActiveScreen('play')
    elif key == 'f':
        app.infinite = not app.infinite

def play_onMousePress(app,mouseX,mouseY):
    checkButtonPress(app,mouseX,mouseY)
    #print('setup click')

def play_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)

def play_redrawAll(app):
    
    drawBackground(app)
    #drawSky(app)
    #drawConway(app)
    drawCloud(app)
    
    drawBird(app)
    drawFood(app)
    #drawFilter(app)
    drawScore(app)
    if app.lines:
        drawLines(app)
    if app.gameOver:
        drawRect(0,0,app.width,app.height,fill='white',opacity=30)
        #drawRect(app.width/10,app.height/9,8*app.width/10,6*app.height/9,fill = 'white',opacity=40)
        drawLabel('YOU LOST SUCKERRRRRRR',app.width/2,app.height/2,font=app.font,size=50,fill=app.textColor,bold=True)
        drawButtons(app)
    if app.paused:
        drawRect(0,0,app.width,app.height,fill='white',opacity=30)
        drawLabel('Paused Game',app.width/2,app.height/2,font=app.font,size=50,fill=app.textColor,bold=True)
        drawButtons(app)
    


def play_onStep(app):
    if app.gameOver:
        app.currScreen = 'end'
        #app.overButton.goOn()
        #app.homeButton.goOn()
        movingStep(app)
    if app.paused:
        app.currScreen = 'end'
        #app.overButton.goOn()
        #app.homeButton.goOn()
        movingStep(app)
    if not app.paused and not app.gameOver:
        app.time += 1
        if app.conway.liveCells == set() or len(app.conway.liveCells)<50:
            app.conway.generateCells()
        app.conway.step()
        if app.timestamp == None and len(app.conway.liveCells) >300:
            app.timestamp = app.time
        if app.timestamp != None:
            interval = app.time-app.timestamp
            #print(interval)
            app.textColor = RGB(min(180,22+interval*2),min(200,33+interval*2),min(210,63+interval*2))
            #app.textcolor = RGB(200,60,150)
            #if len(app.conway.liveCells) <300:

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
            app.recorder.makeFft(4)
        if app.recorder.mag >= Recording.noiseMag:
            app.bird.openMouth()
        else:
            app.bird.closeMouth()
        
        #moveRail(app)
        for food in Food.onScreenList:
            food.parameter[0]-=4
            if food.parameter[0]+44<0:
                Food.onScreenList.remove(food)
                if not app.infinite:
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

def moveSmooth(app):
    target = app.height-app.recorder.getCastFreq()
    if target < 50:
        target = 50
    elif target > app.height-50:
        target = app.height-50
    for i in range(5):
        app.bird.cy += (target-app.bird.cy)/5

def eat(app):
    
    birdx=app.width/7+20
    birdy=app.bird.cy
    if Food.onScreenList!=[] and app.bird.mouthOpen == True:
        for each in Food.onScreenList:
            x,y=each.parameter
            x0,x1 = x-40,x+40
            y0,y1 = y-44,y+44
            #(y0<birdy-30<y1 or y0<birdy+30<y1)
            if x0<birdx<x1 and y0<birdy<y1:
                Food.onScreenList.remove(each)
                app.currScore+=1
            # if abs(birdx-x0)<50:
            #     if abs(birdy-y1)<50:
            #         Food.onScreenList.remove(each)
                    
def loseLife(app):
    app.birdAngle = (app.birdAngle+60)%720
