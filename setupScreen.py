from cmu_graphics import *
from PIL import Image

from classes import *
from audioClass import Recording
from drawMethods import *
from gameMethods import *


def setup_onAppStart(app):
    app.setupButts = {Button('setup','Noise',app.width/5,app.height/2-20),
            Button('setup','Reset Noise Level',app.width/5,app.height/2+20,fontSize=15,bh=30),
            Button('setup','Lowest',4*app.width/5,30+app.height/2),
            Button('setup','Highest',4*app.width/5,app.height/2-30),
            Button('setup','Done',app.width/2,3.5*app.height/5)}
    app.bW,app.bH = 60,30


def setup_onScreenActivate(app):
    app.onOff = 'on'
    #app.pendingScreen = None
    app.currScreen = 'setup'
    app.message = None
    app.message2 = None
    app.loading = False
    app.loadCount = 0
    app.measureNoise = False
    app.measureHigh = False
    app.measureLow = False
    if app.recorder.stream.is_active():
        app.recorder.pause()

def setup_redrawAll(app):
    drawBackground(app)
    drawCloud(app)
    #drawRect(app.width/10,app.height/9,8*app.width/10,6*app.height/9,fill = 'white',opacity=40)
    drawLabel('Welcome! Let\'s do some setup.', app.width/2,app.height/5,size=20,font=app.font,fill=app.textColor,bold=True)
    drawButtons(app)
    if app.loading == True:
        drawRect(app.width/2-50,6*app.height/7,100,10,fill=app.textColor)
        if app.loadCount>0:
            drawRect(app.width/2-50,6*app.height/7,app.loadCount*20,10,fill='white')
    if app.message != None:
        drawLabel(app.message,app.width/2,6*app.height/7 + 30,size=17,font=app.font,fill=app.textColor)
    if app.message2 != None:
        drawLabel(app.message2,app.width/2,4*app.height/5 + 30,size=20,font=app.font,fill=app.textColor)

def setup_onMousePress(app,mouseX,mouseY):
    checkButtonPress(app,mouseX,mouseY)
    #print('setup click')

def setup_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)


def setup_onStep(app):
    if not app.paused:
        if app.pendingScreen == 'setup':
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
        if app.measureNoise == True:
            app.loadCount = 0
            if 2 * app.recorder.samplerate > len(app.recorder.temp):
                app.loadCount = int(5*len(app.recorder.temp)/(2 * app.recorder.samplerate))
                #print(len(app.temp))
                app.recorder.processAudio()
                app.recorder.magList.append(app.recorder.mag)
                #print(app.recorder.magList)
            else:
                app.loading = False
                app.loadCount = 0
                app.measureNoise = False
                bgMag = sum(app.recorder.magList)/len(app.recorder.magList)
                #print(bgMag)
                if bgMag >= Recording.noiseMag:
                    app.message = f'Your background noise is {pythonRound(bgMag,3)} of some unit'
                    Recording.updateNoise(bgMag)
                else:
                    app.message = 'No significant noise detected.'
                #print(bgMag)
                #print("*** done recording")
                app.recorder.temp = []
                if app.recorder.stream.is_active():
                    app.recorder.pause()
                activateButtons(app)
        elif app.measureHigh == True:
            app.recorder.processAudio()
            if app.recorder.frames>=4:
                app.recorder.makeFft()
                if len(app.recorder.pitchList)>=1:
                    highest = app.recorder.pitchList[-1]
                    app.message = f'Your highest pitch is {highest} Hz'
                    Recording.updateMaxPitch(highest)
        elif app.measureLow == True:
            app.recorder.processAudio()
            if app.recorder.frames>=4:
                app.recorder.makeFft()
                if len(app.recorder.pitchList)>=1:
                    lowest = app.recorder.pitchList[-1]
                    app.message = f'Your lowest pitch is {lowest} Hz'
                    Recording.updateMinPitch(lowest)

        

def setup_onKeyPress(app, key):
    checkPause(key)
    if key == 's':
        setActiveScreen('home')