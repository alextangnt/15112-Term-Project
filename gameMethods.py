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

def checkButtonPress(app,mouseX,mouseY):
    for butt in Button.butts:
        if (butt.active == True and
        butt.cx-butt.bw/2<mouseX<butt.cx+butt.bw/2 and 
        butt.cy-butt.bh/2<mouseY<butt.cy+butt.bh/2 and
        butt.screen == app.currScreen):
            pressButton(app,butt)
            #print(f'pressed {butt} button')

def buttonHover(app,mouseX,mouseY):
    for butt in Button.butts:
        if (butt.active == True and
            butt.cx-butt.bw/2<mouseX<butt.cx+butt.bw/2 and 
            butt.cy-butt.bh/2<mouseY<butt.cy+butt.bh/2):
            #pressButton(app,button)
            butt.hovered = True
            butt.scale = 110
            if butt.title == 'Easy':
                app.message = 'No obstacles, slow notes!'
            elif butt.title == 'Medium':
                app.message = 'Some obstacles, faster notes!'
            elif butt.title == 'Hard':
                app.message = 'Faster and even more danger!'
            elif butt.title == 'Infinite':
                app.message = 'No dying. Not in real life, though.'
            elif butt.title == 'Sing Mode!':
                app.message = 'Sing your heart out!'
            else:
                app.message = None
        else:
            butt.scale = 100
            butt.hovered = False


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
    if key == 'p' or key == 'esc':
        app.paused = not app.paused
        if app.paused:
            if app.recorder.stream.is_active():
                app.recorder.pause
        else:
            if not app.recorder.stream.is_active():
                app.recorder.start

def distance(l1,l2,c1,c2):

    return math.sqrt((l1-c1)**2+(l2-c2)**2)


def openImages(app):
    # bird and bug gifs animated by Zen Jitsajjappong (Andrew ID pjitsajj)
    # All other images are mine
    app.birdClosedGif=loadAnimatedGif(app, 'images/bird_closed.gif')
    app.birdOpenGif=loadAnimatedGif(app, 'images/bird_open.gif')
    app.bugGif=loadAnimatedGif(app, 'images/bug.gif')
    app.bugGifFast=app.bugGif

    app.birdClosedGif2=loadAnimatedGif(app, 'images/bird_closed.gif','blue')
    app.birdOpenGif2=loadAnimatedGif(app, 'images/bird_open.gif','blue')
    app.bugGif2=loadAnimatedGif(app, 'images/bug.gif','blue')
    app.evilBugGif=loadAnimatedGif(app, 'images/bug.gif','evil')
    app.boostBugGif=loadAnimatedGif(app, 'images/bug.gif','boost')

    #keeping track of gif frames
    app.count0=0
    app.count1=0
    app.count2=0
    app.count3=0
    
    app.cloudImages=[]
    for image in ['images/cloud1.png','images/cloud2.png','images/cloud3.png','images/cloud4.png']:
        cloudDict = dict()
        cloudDict['base'] = Image.open(image)
        cloudDict['sunset'] = editImage(cloudDict['base'],'set')
        cloudDict['dark'] = editImage(cloudDict['base'],'blue')
        cloudDict['base'] = CMUImage(cloudDict['base'])
        cloudDict['sunset'] = CMUImage(cloudDict['sunset'])
        cloudDict['dark'] = CMUImage(cloudDict['dark'])
        app.cloudImages.append(cloudDict)


    app.bg = dict()
    app.bg['base']=Image.open('images/sky.png')
    app.bg['sunset'] = editImage(app.bg['base'],'sunset')
    app.bg['dark'] = editImage(app.bg['base'],'dark')
    app.bg['base'] = CMUImage(app.bg['base'])
    app.bg['sunset'] = CMUImage(app.bg['sunset'])
    app.bg['dark'] = CMUImage(app.bg['dark'])


    app.playButton=CMUImage(Image.open('images/play.png'))
    app.tweater1=CMUImage(Image.open('images/tweater.png'))
    app.tweaterE = Element('home',app.width/2,app.height/3,'x')

def loadAnimatedGif(app,path,setting=None):
    pilImages = Image.open(path)
    if pilImages.format != 'GIF':
        raise Exception(f'{path} is not an animated image!')
    if not pilImages.is_animated:
        raise Exception(f'{path} is not an animated image!')
    cmuImages = [ ]
    for frame in range(pilImages.n_frames):
        pilImages.seek(frame)
        pilImage = pilImages.copy()
        if setting == None:
            cmuImages.append(CMUImage(pilImage))
        else:
            pilImage = editImage(pilImage,setting)
            cmuImages.append(CMUImage(pilImage))
    return cmuImages

#from editing pixels demo         
def editImage(sourceImage,setting):
    # First, get the RGB version of the image so getpixel returns r,g,b values:
    rgbImage = sourceImage.convert('RGBA')

    # Now, a new image in the 'RGB' mode with same dimensions as app.image
    newImage = Image.new(mode='RGBA', size=rgbImage.size)
    for x in range(newImage.width):
        for y in range(newImage.height):
            r,g,b,a = rgbImage.getpixel((x,y))
            #print(rgbImage.getpixel((0,0)))
            if setting == 'set':
                if [r,g,b,a] == [0,0,0,0]:
                    newImage.putpixel((x,y),(0,0,0,0))
                else:
                    newImage.putpixel((x,y),(int(r/2),int(g/8),int(b/10),0))
            if setting == 'sunset':
                if [r,g,b,a] == [0,0,0,0]:
                    newImage.putpixel((x,y),(0,0,0,0))
                else:
                    newImage.putpixel((x,y),(int(r*1.4),int(g*0.7),int(b*0.4),a))
            elif setting == 'blue':
                if [r,g,b,a] == [0,0,0,0]:
                    newImage.putpixel((x,y),(0,0,0,0))
                else:
                    if r > 100 + g:
                        newImage.putpixel((x,y),(int(r),int(g*0.9),min(255,b+20),a))
                    else:
                        newImage.putpixel((x,y),(int(r*0.5),int(g*0.9),min(255,b+20),a))
            elif setting == 'dark':
                if [r,g,b,a] == [0,0,0,0]:
                    newImage.putpixel((x,y),(0,0,0,0))
                else:
                    newImage.putpixel((x,y),(int(r*0.4*(r-b)/25),int(g*0.2*(g-b)/13),int(b*0.3),a))
            elif setting == 'evil':
                if [r,g,b,a] == [0,0,0,0]:
                    newImage.putpixel((x,y),(0,0,0,0))
                else:
                    newImage.putpixel((x,y),(min(255,int(r*3)),int(g*0.4),int(b*0.3),a))
            elif setting == 'boost':
                if [r,g,b,a] == [0,0,0,0]:
                    newImage.putpixel((x,y),(0,0,0,0))
                else:
                    if r > 160 and b > 160 and g > 160:
                        newImage.putpixel((x,y),(r,g,b,a))
                    else:
                        
                        newImage.putpixel((x,y),(int(r*0.8),int(g*1.2),int(b*0.5),a))
                
    return newImage

def pressButton(app,which):
    if which.title == 'Modes':
        app.onOff = 'off'
        app.pendingScreen = 'modes'
    elif which.title == 'Easy':
        app.mode = 'easy'
        #app.message = 'No obstacles, slow notes!'
        app.message2 = 'Easy mode selected'
    elif which.title == 'Medium':
        app.mode = 'medium'
        #app.message = 'Some obstacles, faster notes!'
        app.message2 = 'Medium mode selected'
    elif which.title == 'Hard':
        app.mode = 'hard'
        #app.message = 'Faster and even more danger!'
        app.message2 = 'Hard mode selected'
    elif which.title == 'Infinite':
        app.mode = 'infinite'
        #app.message = 'No dying. Not in real life, though.'
        app.message2 = 'Infinite selected'
    elif which.title == 'Sing Mode!':
        app.mode = 'sing'
        #app.message = 'Sing your heart out!'
        app.message2 = 'Sing mode selected'
    elif which.title == 'Set Up':
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
    elif which.title == 'Done' or which.title == 'Home':
        app.onOff = 'off'
        app.pendingScreen = 'home'
        
    elif which.title == 'continue':
        app.paused = not app.paused
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
