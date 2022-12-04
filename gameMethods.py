import math
from cmu_graphics import *
from PIL import Image
from classes import *
from gameMethods import *
from audioClass import Recording

def almostEqual(a,b):
    if abs(a-b)<=10:
        return True
    return False

def loadAnimatedGif(app,path):
    pilImages = Image.open(path)
    if pilImages.format != 'GIF':
        raise Exception(f'{path} is not an animated image!')
    if not pilImages.is_animated:
        raise Exception(f'{path} is not an animated image!')
    cmuImages = [ ]
    for frame in range(pilImages.n_frames):
        pilImages.seek(frame)
        pilImage = pilImages.copy()
        cmuImages.append(CMUImage(pilImage))
    return cmuImages

def checkButtonPress(app,mouseX,mouseY):
    for butt in Button.butts:
        if (butt.active == True and
        butt.cx-butt.bw/2<mouseX<butt.cx+butt.bw/2 and 
        butt.cy-butt.bh/2<mouseY<butt.cy+butt.bh/2 and
        butt.screen == app.currScreen):
            pressButton(app,butt)
            print(f'pressed {butt} button')

def buttonHover(app,mouseX,mouseY):
    for butt in Button.butts:
        if (butt.active == True and
            butt.cx-butt.bw/2<mouseX<butt.cx+butt.bw/2 and 
            butt.cy-butt.bh/2<mouseY<butt.cy+butt.bh/2):
            #pressButton(app,button)
            butt.scale = 110
        else:
            butt.scale = 100



def moveSmooth(app):
    target = app.height-app.recorder.getCastFreq()
    for i in range(5):
        app.bird.cy += (target-app.bird.cy)/5


def movingStep(app):
    if app.onOff!= None:
        if app.onOff == 'off':
            if Element.moveOffStep(app.currScreen):
                app.onOff = None
                if app.pendingScreen != None:
                    setActiveScreen(app.pendingScreen)
        if app.onOff == 'on':
            if Element.moveOnStep(app.currScreen):
                app.onOff = None
                # if app.pendingScreen != None:
                #     setActiveScreen(app.pendingScreen)

def checkPause(key):
    if key == 'p':
        app.paused = not app.paused
        if app.paused:
            if app.recorder.stream.is_active():
                app.recorder.pause
        else:
            if not app.recorder.stream.is_active():
                app.recorder.start

def distance(l1,l2,c1,c2):

    return math.sqrt((l1-c1)**2+(l2-c2)**2)

def eat(app):
    
    birdx=app.width/7-90
    birdy=app.bird.cy-90
    if Food.onScreenList!=[] and app.bird.mouthOpen == True:
        for each in Food.onScreenList:
            x0,y0,x1,y1=each.parameter

            if x0<birdx<x1 and y0<birdy<y1:
                Food.onScreenList.remove(each)
                app.currScore+=1
            # if abs(birdx-x0)<50:
            #     if abs(birdy-y1)<50:
            #         Food.onScreenList.remove(each)
                    
def loseLife(app):
    app.birdAngle = (app.birdAngle+60)%720

def openImages(app):
    # bird and bug gifs animated by Zen Jitsajjappong (Andrew ID pjitsajj)
    # All other images are mine
    app.birdClosedGif=loadAnimatedGif(app, 'images/bird_closed.gif')
    app.birdOpenGif=loadAnimatedGif(app, 'images/bird_open.gif')
    app.bugGif=loadAnimatedGif(app, 'images/bug.gif')
    app.bugGifFast=app.bugGif
    app.count0=0
    app.count1=0
    app.count2=0
    app.count3=0
    app.cloud1=CMUImage(Image.open('images/cloud1.png'))
    app.cloud2=CMUImage(Image.open('images/cloud2.png'))
    app.cloud3=CMUImage(Image.open('images/cloud3.png'))
    app.cloud4=CMUImage(Image.open('images/cloud4.png'))
    app.bg=CMUImage(Image.open('images/sky.png'))
    app.playButton=CMUImage(Image.open('images/play.png'))
    app.tweater1=CMUImage(Image.open('images/tweater.png'))
    app.tweaterE = Element('home',app.width/2,app.height/3,'x')
    app.cloudImage=[app.cloud1,app.cloud2,app.cloud3,app.cloud4]

def pressButton(app,which):
    if which.title == 'Set Up':
        app.onOff = 'off'
        app.pendingScreen = 'setup'
    elif which.title == 'Noise':
        deactivateButtons(app,'Noise')
        app.recorder.magList = []
        app.loading = True
        app.message2 = None
        app.message = 'Recording 3 seconds of background noise...'
        print('recording')
        if not app.recorder.stream.is_active():
                app.recorder.start()
        app.measureNoise = True
    elif which.title == 'Reset Noise Level':
        Recording.noiseMag = 0.003
        app.message = 'Noise magnitude has been reset.'
        app.message2 = None
    elif which.title == 'Done':
        app.onOff = 'off'
        app.pendingScreen = 'home'

    elif which.title == 'play':
        app.started=True
        if not app.recorder.stream.is_active():
            app.recorder.start()
        app.onOff = 'off'
        app.pendingScreen = 'play'
    elif which.title == 'Restart':
        setActiveScreen('play')
    elif which.title == 'Highest':
        app.message = f'Your highest pitch is {int(Recording.maxPitch)} Hz'
        app.message2 = 'Sing the highest note you can! Press Highest again to save.'
        app.measureHigh = not app.measureHigh
        print(app.measureHigh)
        if app.measureHigh:
            deactivateButtons(app,'Highest')
            if not app.recorder.stream.is_active():
                app.recorder.start()
        else:
            if app.recorder.stream.is_active():
                activateButtons(app)
                app.recorder.pause()
                app.message = 'Saved new highest note'
                app.message2 = None
                #which.title += ':' + str(int(Recording.maxPitch))
    elif which.title == 'Lowest':
        app.message = f'Your lowest pitch is {int(Recording.minPitch)} Hz'
        app.message2 = 'Sing the lowest note you can! Press Lowest again to save.'
        app.measureLow = not app.measureLow
        if app.measureLow:
            deactivateButtons(app,'Lowest')
            if not app.recorder.stream.is_active():
                app.recorder.start()
        else:
            if app.recorder.stream.is_active():
                activateButtons(app)
                app.recorder.pause()
                app.message = 'Saved new lowest note'
                app.message2 = None
                #which.title += ':' + str(int(Recording.minPitch))

def deactivateButtons(app,title):
    for butt in Button.butts:
        if butt.title != title and butt.screen == app.currScreen:
            butt.active = False

def activateButtons(app):
    for butt in Button.butts:
        if butt.screen == app.currScreen:
            butt.active = True
