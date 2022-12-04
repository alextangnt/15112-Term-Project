from cmu_graphics import *
import random
from PIL import Image
import math

from classes import *
from audioClass import Recording
#############################################################


########################################################################
# SCREENS: setup/ play/ end

def onAppStart(app):
    app.font = 'monospace'
    app.textColor = RGB(22,33,63)
    app.currScreen = 'start'
    app.scores = []

def setup_onAppStart(app):
    app.setupButts = {Button('setup','Noise',app.width/5,app.height/2-20),
            Button('setup','Reset Noise Level',app.width/5,app.height/2+20,fontSize=15,bh=30),
            Button('setup','Lowest',4*app.width/5,30+app.height/2),
            Button('setup','Highest',4*app.width/5,app.height/2-30),
            Button('setup','Done',app.width/2,3.5*app.height/5)}
    app.bW,app.bH = 60,30


def setup_onScreenActivate(app):

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
    drawBackgroud(app)
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

def checkButtonPress(app,mouseX,mouseY):
    for butt in Button.butts:
        if (butt.active == True and
        butt.cx-butt.bw/2<mouseX<butt.cx+butt.bw/2 and 
        butt.cy-butt.bh/2<mouseY<butt.cy+butt.bh/2 and
        butt.screen == app.currScreen):
            pressButton(app,butt)
            print(f'pressed {butt} button')

def setup_onMousePress(app,mouseX,mouseY):
    checkButtonPress(app,mouseX,mouseY)
    #print('setup click')

def setup_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)


def setup_onStep(app):
    if not app.paused:
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
    if key == 's':
        setActiveScreen('play')


######## setup screen

def almostEqual(a,b):
    if abs(a-b)<=10:
        return True
    return False


def play_onAppStart(app):
    app.currScore = 0
    app.started=False
    app.paused = False
    app.timer=0
    app.timerDelay=1
    app.stepsPerSecond=44
    
    openImages(app)
    

    app.butts = set()
    app.settings = Button('play','Set Up',5*app.width/7,4*app.height/5)
    app.tutorial = Button('play','Tutorial',2*app.width/7,4*app.height/5)
    #app.play = Button('play','Play')
    app.butts.add(app.settings)
    app.butts.add(app.tutorial)
    app.butts.add(imgButton('play','Play',app.width/2,4*app.height/5,app.playButton,100,100))
    
    app.timerC=0
    app.cloud=True
    app.Introx=app.width/2
    #app.pausex=app.width/2


    app.bird=Bird(app.height/2)

    app.recorder = Recording(app.height-50)
    app.recorder.pause()

def play_onScreenActivate(app):
    app.currScreen = 'play'
    print('play screen')

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
    app.cloudImage=[app.cloud1,app.cloud2,app.cloud3,app.cloud4]

#####################Loading image################
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

############
# play screen
############


def play_redrawAll(app):
    
    drawLine(app)
    drawBackgroud(app)
    drawCloud(app)
    drawTweater(app)
    #drawPause(app)
    drawButtons(app)
    drawBird(app)
    drawFood(app)
    drawLabel(app.currScore,9*app.width/10,1*app.height/10,font=app.font,fill=app.textColor,size=25,bold=True)
    #drawblack(app)

def splitScreen(app):
    
    app.Introx-=15
    for butt in app.butts:
        if butt.screen == app.currScreen:
            butt.cx+=15

def moveElement(app):
    tempcx = 0
    tempcy = 0

def deactivateButtons(app,title):
    for butt in Button.butts:
        if butt.title != title and butt.screen == app.currScreen:
            butt.active = False

def activateButtons(app):
    for butt in Button.butts:
        if butt.screen == app.currScreen:
            butt.active = True

def pressButton(app,which):
    if which.title == 'Set Up':
        setActiveScreen('setup')
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
        Recording.noiseMag = 0.001
        app.message = 'Noise magnitude has been reset.'
        app.message2 = None
    elif which.title == 'Done':
        setActiveScreen('play')
        deactivateButtons(app,'Done')
        activateButtons(app)
    elif which.title == 'Play':
        app.started=True
        if not app.recorder.stream.is_active():
                app.recorder.start()
        Food.makeFoodList(app)
        Food.onScreenList.append(Food.upcomingList.pop(0))
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

def play_onMousePress(app,mouseX,mouseY):
    if app.currScreen == 'play':
        checkButtonPress(app,mouseX,mouseY)

def play_onMouseMove(app,mouseX,mouseY):
    buttonHover(app,mouseX,mouseY)

def buttonHover(app,mouseX,mouseY):
    for butt in Button.butts:
        if (butt.active == True and
            butt.cx-butt.bw/2<mouseX<butt.cx+butt.bw/2 and 
            butt.cy-butt.bh/2<mouseY<butt.cy+butt.bh/2):
            #pressButton(app,button)
            butt.scale = 110
        else:
            butt.scale = 100

def play_onKeyPress(app,key):
    
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
    
    elif key == 'p':
        app.paused = not app.paused
        if app.paused:
            app.recorder.pause
        else:
            app.recorder.start
    elif key == 'q':
        print("*** done recording")
        app.stream.stop_stream()
        app.stream.close()
        app.p.terminate()
        app.quit()

def play_onStep(app):
    if not app.paused:
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
        if Food.upcomingList == []:
            Food.makeFoodList(app)

        if app.started:
            if app.Introx>-500:
                splitScreen(app)
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
                if food.parameter[2]<-200:
                    Food.onScreenList.remove(food)

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
    for i in range(5):
        app.bird.cy += (target-app.bird.cy)/5



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
            # if abs(birdx-x0)<50:
            #     if abs(birdy-y1)<50:
            #         Food.onScreenList.remove(each)
                    
                
def drawButtons(app):
    for butt in Button.butts:
        if butt.screen == app.currScreen:
            if isinstance(butt,imgButton):
                imgW, imgH = getImageSize(butt.img)
                drawImage(butt.img, butt.cx, butt.cy, align='center',
                width=imgW*butt.scale/100,height=imgH*butt.scale/100)
            else:
                if butt.active == False:
                    drawLabel(butt.title,butt.cx,butt.cy,size=butt.fontSize*butt.scale/100,font=app.font,bold=True,fill=app.textColor,opacity=50)
                else:
                    
                    #drawRect(butt.cx,butt.cy,butt.bw,butt.bh,align='center',fill=RGB(236,234,226))
                    drawLabel(butt.title,butt.cx,butt.cy,size=butt.fontSize*butt.scale/100,font=app.font,bold=True,fill=app.textColor)
            

def drawTweater(app):
    cx=app.Introx
    cy=app.height/3
    #canvas.create_image(cx,cy,image=ImageTk.PhotoImage(app.tweater1))
    drawImage(app.tweater1, cx, cy, align='center')
    

def drawPause(app):
    cx=app.pausex
    cy=4*app.height/5
    drawImage(app.playButton, cx, cy, align='center')

def drawblack(app):
    cx=app.width/2
    cy=4*app.height/5
    drawRect(cx-50,cy-60,100,120,fill='black')

    
def drawBackgroud(app):
    cx=app.width/2
    cy=app.height/2
    drawImage(app.bg, cx, cy, align='center',width=app.width,height=app.height)         

def drawBird(app):
    #rail=Bird.rail
    cx=app.width/7
    cy=app.bird.cy
    
    r=30
    photoImage0 = app.birdClosedGif[int(app.count0)]
    photoImage1 = app.birdOpenGif[int(app.count1)]
    if app.bird.mouthOpen==False and app.started==True:
        drawImage(photoImage0, cx, cy, align='center')
        

    elif app.bird.mouthOpen==True and app.started==True:
        cy=app.bird.cy
        drawImage(photoImage1, cx, cy, align='center')
        

def drawCloud(app):
    if Cloud.onScreenList!=[]:
        for each in Cloud.onScreenList:
            cx,cy=each.parameter
            image=app.cloudImage[each.cloudType]
            drawImage(image, cx, cy, align='center')
            
            
        
    
def drawFood(app):
    if Food.onScreenList!=[]:
        for each in Food.onScreenList:
            x0,y0,x1,y1=each.parameter
            cx=((x1-x0)/2+x1)
            cy=((y1-y0)/2+y1)
            photoImage2 = app.bugGif[int(app.count2)]
            photoImage3 = app.bugGifFast[int(app.count3)]
            
            if each.fast:
                #canvas.create_image(cx,cy-20,image=photoImage2)
                drawImage(photoImage3, cx, cy, align='center')
            else:
                #canvas.create_image(cx,cy-20,image=photoImage3)
                drawImage(photoImage2, cx, cy, align='center')
                                                    

    
def drawLine(app):
    for i in range(7):
        #canvas.create_rectangle(0,app.height*(i/7),app.width,app.height*((i+1)/7),
                                #fill="white",outline="black")
        drawRect(0,app.height*(i/7),app.width,app.height*((i+1)/7),
                                fill="white",border="black")




############
# end screen
############


def main():
    runAppWithScreens(initialScreen='play', width=800,height=500)
main()

    

