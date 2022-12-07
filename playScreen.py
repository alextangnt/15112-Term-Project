from cmu_graphics import *

from classes import *
from audioClass import Recording
from drawMethods import *
from gameMethods import *


def play_onScreenActivate(app):
    app.cloud=True
    app.starColors = [(230, 80, 123),(240, 178, 55),(199, 237, 47),(47, 237, 155),(177, 120, 240)]
    app.textColor = RGB(22,33,63)
    app.ingameColor = RGB(22,33,63)
    app.events = {'sunset':None,
                'dark':None,
                'sunrise':None,
                'day':None}
    app.currEvent = 'day'
    # time of day event
    app.time = 0
    app.paused = False
    app.lines = False
    app.onOff = 'on'
    app.pendingScreen = None
    #print('play screen')
    app.currScreen = 'play'
    app.currScore = 0
    app.scoreE = Element('play',7.5*app.width/10,1*app.height/15,'y')
    app.scoreE.goOff()
    app.currLives = 5
    app.livesE = Element('play',1*app.width/2,1*app.height/15,'y')
    app.livesE.goOff()
    app.infinite = False
    if not app.recorder.stream.is_active():
        app.recorder.start()
    app.gameOver = False
    app.overButton.goOn()
    app.homeButton.goOn()
    app.continueButton.goOn()
    app.birdAngle = 0
    app.speed = 1
    app.songOver = False
    Food.delay = 40
    #timer for food and clouds
    app.timer=0
    app.timerDelay=1
    Food.onScreenList = []
    Food.upcomingList = []
    if app.mode == 'easy':
        Food.delay = 40
    elif app.mode == 'medium':
        Food.delay = 32
        Food.ratio = 5
        app.speed = 2
    elif app.mode == 'hard':
        Food.delay = 15
        Food.ratio = 3
        app.speed = 3
    if not app.mode == 'sing':
        Food.delay = 20
        Food.makeFoodList(app)
    else:
        Food.delay = 20
        app.speed = 2
        Food.makeTwinkle(app)
    Food.onScreenList.append(Food.upcomingList.pop(0))
    app.conway.reset()

def play_onKeyPress(app,key):
    checkPause(key)
    if key == 'l':
        app.lines = not app.lines
        #print('lines')
    elif key == 'r':
        setActiveScreen('play')
    elif key == 's':
        app.mode = 'sing'
        setActiveScreen('play')
    elif key == 'f':
        app.infinite = not app.infinite

def play_onMousePress(app,mouseX,mouseY):
    checkButtonPress(app,mouseX,mouseY)

def play_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)

def play_redrawAll(app):
    
    drawBackground(app)
    drawConway(app)
    drawCloud(app)

    if app.lines or app.mode == 'sing':
        drawLines(app)
    drawBird(app)
    drawFood(app)
    drawFilter(app)
    drawScore(app)

    if app.gameOver:
        drawRect(0,0,app.width,app.height,fill=RGB(219, 212, 197),opacity=30)
        #drawRect(app.width/10,app.height/9,8*app.width/10,6*app.height/9,fill = 'white',opacity=40)
        drawLabel('Game over!',app.width/2,app.height/2,font=app.font,size=50,fill=app.textColor,bold=True)
        drawLabel(f'Score: {app.currScore}  Highest Score: {max(app.scores)}',app.width/2,app.height*0.6,font=app.font,size=30,fill=app.textColor,bold=True)
        drawButtons(app)
    if app.paused:
        drawRect(0,0,app.width,app.height,fill='white',opacity=30)
        drawLabel('Paused Game',app.width/2,app.height/2,font=app.font,size=50,fill=app.textColor,bold=True)
        drawLabel('Tip: Press R to restart, F for infinite mode,',app.width/2,app.height/4,fill=app.textColor,
                font=app.font,size=20)
        drawLabel('and S for singing mode',app.width/2,app.height/4+30,fill=app.textColor,
                font=app.font,size=20)
        drawButtons(app)
    
def eventCheck(app):
    events = ['sunset','dark','sunrise','day']
    nextIndex = (events.index(app.currEvent)+1)%4
    event = events[nextIndex]
    #print(event,app.currEvent)
    if event == 'sunset' and app.currEvent == 'day':
        if app.events['day'] == None:
            time = 0
        else:
            time = app.events['day']
        if len(app.conway.liveCells) > 300 and app.time-time>100:
            app.events['sunset'] = app.time
            return event
        return app.currEvent
    elif event == 'dark' and app.currEvent == 'sunset':
        if len(app.conway.liveCells) > 500 and app.time-app.events['sunset']>100:
            app.events['dark'] = app.time
            return event
        return app.currEvent
    elif event == 'sunrise' and app.currEvent == 'dark':
        if len(app.conway.liveCells) < 200 and app.time-app.events['dark']>100:
            app.events['sunrise'] = app.time
            return event
        return app.currEvent
    elif event == 'day' and app.currEvent == 'sunrise':
        if len(app.conway.liveCells) < 100 and app.time-app.events['sunrise']>100:
            app.events['day'] = app.time
            return event
        return app.currEvent
    return app.currEvent

def play_onStep(app):
    if app.gameOver:
        app.currScreen = 'end'
        app.continueButton.invisible = True
        app.scores.append(app.currScore)
        app.currEvent = 'day'
        movingStep(app)
        
    if app.paused:
        app.currScreen = 'end'
        app.continueButton.invisible = False
        movingStep(app)
    if not app.paused and not app.gameOver:
        app.time += 1
        if not app.mode == 'sing':
            app.speed += 0.00001
            Food.delay = max(1,Food.delay-0.00001)
        app.conway.step()
        app.currEvent = eventCheck(app)
        if app.currEvent == 'dark':
            interval = app.time-app.events['dark']

            app.ingameColor = RGB(min(180,22+interval*2),min(200,33+interval*2),min(210,63+interval*2))

        elif app.currEvent == 'sunrise':
            interval = app.time-app.events['sunrise']
            app.ingameColor = RGB(max(22,180-interval*2),max(33,200-interval*2),max(63,210-interval*2))

        if app.birdAngle!=0:
            loseLife(app)
            app.speed*=1.07
        if app.pendingScreen == 'play':
            Element.allOff(app.currScreen)
            app.pendingScreen = None
        movingStep(app)
        Cloud.onStep(app)
        Food.onStep(app)
        if app.currLives == 0:
            app.gameOver = True
        for cloud in Cloud.onScreenList:
                cloud.parameter[0]-=1*app.speed
                if cloud.parameter[0]<-300:
                    Cloud.onScreenList.remove(cloud)
        if app.cloud==True:
            L=Cloud.CloudListGen(app)
            app.cloud=False 
            Cloud.upcomingList=L
            Cloud.onScreenList.append(Cloud.upcomingList.pop(0))
        if Food.upcomingList == []:
            if not app.mode == 'sing':
                Food.makeFoodList(app)
            if Food.onScreenList == [] and app.mode == 'sing':
                app.gameOver = True
        eat(app)
        app.recorder.processAudio()

        if app.recorder.frames>=4:
            app.recorder.makeFft(4)
        if app.recorder.mag >= Recording.noiseMag:
            app.bird.openMouth()
            magnum = int(app.recorder.mag*100)
            app.conway.generateLocation((app.recorder.mag/Recording.noiseMag)*app.width/50,app.bird.cy,magnum)
            #print((app.recorder.mag/Recording.noiseMag)*app.width/10)
        else:
            app.bird.closeMouth()
        #moveRail(app)
        for food in Food.onScreenList:
            if food.fast:
                food.parameter[0]-=0.5*app.speed
            food.parameter[0]-=4*app.speed
            if food.parameter[0]+44<0:
                Food.onScreenList.remove(food)
                if not app.infinite and not food.evil and not app.mode == 'sing':
                    app.currLives-=1
                    app.speed*=0.4
                    loseLife(app)


        

        app.count0= (0.5 + app.count0) % len(app.birdClosedGif)
        app.count1= (0.5 + app.count1) % len(app.birdOpenGif)
        app.count2= (0.25 + app.count2) % len(app.bugGif)
        app.count3= (0.5 + app.count3) % len(app.bugGifFast)
        

        moveSmooth(app)
     
        if len(app.recorder.pitchList)>10:
            app.recorder.pitchList = app.recorder.pitchList[-9:]

def moveSmooth(app):
    if app.mode == 'sing':
        target = app.height-app.recorder.getNoteFreq()
        #print('app ' + str((app.height-app.topBar)/9))
        #print(app.recorder.getNoteFreq())
    else:
        target = app.height-app.recorder.getCastFreq()+app.topBar
        if target < 50:
            target = 50
        elif target > app.height-50:
            target = app.height-50
    for i in range(5):
        app.bird.cy += (target-app.bird.cy)/5

def eat(app):
    
    birdx=app.width/7+20
    birdy=app.bird.cy
    if Food.onScreenList!=[]:
        for each in Food.onScreenList:
            x,y=each.parameter
            x0,x1 = x-40,x+40
            y0,y1 = y-44,y+44

            if x0<birdx<x1 and y0<birdy<y1:
                if each.evil:
                    if not app.infinite:
                        app.currLives-=1
                    Food.onScreenList.remove(each)
                    app.speed*=0.4
                    loseLife(app)
                elif app.bird.mouthOpen == True:
                    Food.onScreenList.remove(each)
                    if each.boost:
                        app.currScore+=5
                        app.speed*=1.4
                        if app.currLives<5:
                            app.currLives+=1
                    else:
                        app.currScore+=1
                        #if not app.mode == 'sing':
                            #app.speed*=1.05

                    
def loseLife(app):
    app.birdAngle = (app.birdAngle+60)%720
