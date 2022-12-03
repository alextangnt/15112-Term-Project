from cmu_graphics import *
import random
from PIL import Image
import math

from classes import Bird, Food, Cloud
from audioClass import Recording
#############################################################


########################################################################
# SCREENS: splash/ play/ end

def splash_onScreenStart(app):
    app.stepsPerSecond = 44
    app.bW,app.bH = 60,30
    app.buttons = {'Noise':(app.width/5,app.height/2),
                    'Lowest':(4*app.width/5,20+app.height/2),
                    'Highest':(4*app.width/5,app.height/2-20),
                    'Start':(app.width/2,3*app.height/5)}
    app.message = None
    app.message2 = None
    app.loading = False
    app.loadCount = 0
    app.measureNoise = False
    app.measureHigh = False
    app.measureLow = False

    app.recorder = Recording()
    app.recorder.pause()


def splash_redrawAll(app):
    drawRect(0,0,app.width,app.height,fill = 'turquoise')
    drawLabel('Welcome! Let\'s do some setup.', app.width/2,app.height/5,size=20)
    for button in app.buttons:
        drawRect(*app.buttons[button],app.bW,app.bH,align='center',fill='white')
        drawLabel(button,*app.buttons[button],size=16)
    if app.loading == True:
        drawRect(app.width/2-50,5*app.height/6,100,10)
        if app.loadCount>0:
            drawRect(app.width/2-50,5*app.height/6,app.loadCount*20,10,fill='white')
    if app.message != None:
        drawLabel(app.message,app.width/2,5*app.height/6 + 30)
    if app.message2 != None:
        drawLabel(app.message2,app.width/2,4*app.height/5 + 30,size=16)

def splash_onMousePress(app,mouseX,mouseY):
    for button in app.buttons:
        buttonX = app.buttons[button][0]
        buttonY = app.buttons[button][1]
        if (buttonX-app.bW/2<mouseX<buttonX+app.bW/2 and 
            buttonY-app.bH/2<mouseY<buttonY+app.bH/2):
            pressButton(app,button)

def pressButton(app,which):
    if which == 'Noise':
        app.loading = True
        app.message = 'Recording 3 seconds of background noise...'
        print('recording')
        app.recorder.start()
        app.measureNoise = True
    #if which == 'Highest':
    elif which == 'Start':
        setActiveScreen('main')
        app.recorder.end()
    elif which == 'Highest':
        app.message2 = 'Sing the highest note you can! Press Highest again to save.'
        app.measureHigh = not app.measureHigh
        if app.measureHigh:
            app.recorder.start()
        else:
            app.recorder.pause()
    elif which == 'Lowest':
        app.message2 = 'Sing the lowest note you can! Press Lowest again to save.'
        app.measureLow = not app.measureLow
        if app.measureLow:
            app.recorder.start()
        else:
            app.recorder.pause()

def splash_onStep(app):
    if app.measureNoise == True:
        if 2 * app.recorder.samplerate > len(app.recorder.temp):
            app.loadCount = int(5*len(app.recorder.temp)/(2 * app.recorder.samplerate))
            #print(len(app.temp))
            app.recorder.processAudio()
        else:
            app.loading = False
            app.loadCount = 0
            app.measureNoise = False
            bgMag = abs(sum((app.recorder.temp)))/len(app.recorder.temp)
            app.message = f'Your background noise is {bgMag} of some unit'
            #print(bgMag)
            #print("*** done recording")
            app.recorder.updateNoise(bgMag)
            app.recorder.pause()
    if app.measureHigh == True:
        app.recorder.processAudio()
        if app.recorder.frames==4:
            app.recorder.makeFft()
            if len(app.recorder.pitchList)!=1:
                highest = app.recorder.pitchList[-1]
                app.message = f'Your highest pitch is {highest} Hz'
                app.recorder.updateMaxPitch(highest)
    if app.measureLow == True:
        app.recorder.processAudio()
        if app.recorder.frames==4:
            app.recorder.makeFft()
            if len(app.recorder.pitchList)!=1:
                lowest = app.recorder.pitchList[-1]
                app.message = f'Your lowest pitch is {lowest} Hz'
                app.recorder.updateMinPitch(lowest)

        

def splash_onKeyPress(app, key):
    if key == 's':
        setActiveScreen('main')


######## splash screen

def almostEqual(a,b):
    if abs(a-b)<=10:
        return True
    return False


def main_onScreenStart(app):
    app.stepsPerSecond = 20
    app.started=False
    app.paused = False
    app.timer=0
    app.timerDelay=1
    app.stepsPerSecond=44

    # bird and bug gifs animated by Zen Jitsajjappong (Andrew ID pjitsajj)
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
    #app.cy=(Bird.rail)*app.height/14-app.height/28
    app.cloudImage=[app.cloud1,app.cloud2,app.cloud3,app.cloud4]
    app.timerC=0
    app.cloud=True
    app.Introx=app.width/2
    app.pausex=app.width/2
    #app.open=False

    app.bird=Bird(app.height/2)
    #app.bird.bHeight = 

    app.recorder2 = Recording(app.height-50)
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

############player interface#############


############
# main screen
############


def main_redrawAll(app):
    
    drawLine(app)
    drawBackgroud(app)
    drawCloud(app)
    drawTweater(app)
    drawPause(app)
    drawBird(app)
    drawFood(app)
    #drawblack(app)

def splitScreen(app):
    
    app.Introx-=15
    app.pausex+=15
        
def main_onMousePress(app,mouseX,mouseY):
    cx=app.width/2
    cy=4*app.height/5
    
    if app.started == False:
        if cx-50<mouseX<cx+50 and cy-60<mouseY<cy+60:
            app.started=True
            Food.makeFoodList(app)
            Food.onScreenList.append(Food.upcomingList.pop(0))
            

def main_onKeyPress(app,key):
    
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
    elif key == 'q':
        print("*** done recording")
        app.stream.stop_stream()
        app.stream.close()
        app.p.terminate()
        app.quit()

def main_onStep(app):
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
            app.recorder2.processAudio()
            if app.recorder2.frames==4:
                app.recorder2.makeFft()
            if app.recorder2.mag >= Recording.noiseMag:
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
            

            #app.bird.cy = app.height-app.recorder2.getCastFreq()
            moveSmooth(app)
            #print(app.recorder2.pitchList[-1])
            # cy = app.recorder2.pitchList[-1]
            # if cy<180:
            #     app.bird.targetRrail=14
            # elif cy>430:
            #     app.bird.targetRrail=1
            # else:
            #     app.bird.targetRrail=int(14-(((cy-180)/(app.height/14))+1))
            
            #put this in the audioClass
            if len(app.recorder2.pitchList)>10:
                app.recorder2.pitchList = app.recorder2.pitchList[-9:]
        

def moveSmooth(app):
    target = app.height-app.recorder2.getCastFreq()
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
                    
                
                
def drawTweater(app):
    cx=app.Introx
    cy=2*app.height/5
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
    runAppWithScreens(initialScreen='main', width=800,height=500)
main()

    

