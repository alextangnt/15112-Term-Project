from cmu_graphics import *
from PIL import Image, ImageDraw

from classes import *


def drawScore(app):
    scx=app.scoreE.currX
    scy=app.scoreE.currY
    lcx=app.livesE.currX
    lcy=app.livesE.currY
    symbol = str(chr(0x2764))
    drawLabel(f'Score: {app.currScore}',scx,scy,font=app.font,fill=app.ingameColor,size=25,bold=True,align='left')
    if not app.infinite and not app.mode == 'sing':
        drawLabel(app.currLives*'<3',lcx,lcy,font=app.font,fill=app.ingameColor,size=25,align='left')


def drawButtons(app):
    for butt in Button.butts:
        if butt.screen == app.currScreen and not butt.invisible:
            if isinstance(butt,imgButton):
                imgW, imgH = getImageSize(butt.img)
                drawImage(butt.img, butt.currX, butt.currY, align='center',
                width=imgW*butt.scale/100,height=imgH*butt.scale/100)
            else:
                if butt.active == False:
                    drawLabel(butt.title,butt.currX,butt.currY,size=butt.fontSize*butt.scale/100,font=app.font,bold=True,fill=app.textColor,opacity=50)
                else:
                    if butt.hovered:
                        drawLabel(butt.title.upper(),butt.currX,butt.currY,size=butt.fontSize*butt.scale/100,font=app.font,bold=True,fill=app.hoverColor)
                    else:
                        drawLabel(butt.title,butt.currX,butt.currY,size=butt.fontSize*butt.scale/100,font=app.font,bold=True,fill=app.textColor)
            

def drawTweater(app):
    cx=app.tweaterE.currX
    cy=app.tweaterE.currY
    drawImage(app.tweater1, cx, cy, align='center')
    

def drawPause(app):
    cx=app.pausex
    cy=4*app.height/5
    drawImage(app.playButton, cx, cy, align='center')

def drawblack(app):
    cx=app.width/2
    cy=4*app.height/5
    drawRect(cx-50,cy-60,100,120,fill='black')

    
def drawBackground(app):
    cx=app.width/2
    cy=app.height/2
    #drawImage(app.bg['base'], cx, cy, align='center',width=app.width,height=app.height)
    #drawRect(0,0,app.width,app.height,fill=RGB(14, 28, 48),opacity = min(100,0.01*app.time))
    if app.currEvent == 'sunset':
        interval = app.time-app.events['sunset']
        drawImage(app.bg['sunset'], cx, cy,width=app.width,height=app.height, align='center',opacity = min(100,interval),)
        drawImage(app.bg['base'], cx, cy,width=app.width,height=app.height, align='center',opacity = max(0,100-interval))
    elif app.currEvent == 'dark':
        interval = app.time-app.events['dark']
        drawImage(app.bg['sunset'], cx, cy, align='center',width=app.width,height=app.height,opacity = max(0,100-interval))
        drawImage(app.bg['dark'], cx, cy, align='center',width=app.width,height=app.height,opacity = min(100,interval))
    elif app.currEvent == 'sunrise':
        interval = app.time-app.events['sunrise']
        drawImage(app.bg['dark'], cx, cy, align='center',width=app.width,height=app.height,opacity = max(0,100-interval))
        drawImage(app.bg['sunset'], cx, cy, align='center',width=app.width,height=app.height,opacity = min(100,interval))
    elif app.currEvent == 'day':
        if app.events['day'] != None:
            interval = app.time-app.events['day']
            drawImage(app.bg['sunset'], cx, cy, align='center',width=app.width,height=app.height,opacity = max(0,100-interval))
            drawImage(app.bg['base'], cx, cy, align='center',width=app.width,height=app.height,opacity = min(100,interval))
        else:
            drawImage(app.bg['base'], cx, cy, align='center',width=app.width,height=app.height)


def drawConway(app):
    conwayDraw = Image.new('RGBA', (app.width, app.height),None)
    conwayDraw = CMUImage(conwayDraw)
    pilImage = conwayDraw.image

    # Create the ImageDraw object
    draw = ImageDraw.Draw(pilImage)
    
    for cell in app.conway.prevCells:
        x,y = cell[0],cell[1]
        if app.currEvent == 'dark':
            draw.ellipse((x-1, y-1, x+1, y+1), fill = app.starColors[int(app.time/5)%5])
    for cell in app.conway.liveCells:
        x,y = cell[0],cell[1]
        if app.currEvent == 'dark':
            draw.ellipse((x-1, y-1, x+1, y+1), fill = (219, 209, 200),outline=1)
        else:
            draw.ellipse((x-1, y-1, x+1, y+1), fill = (219, 209, 200),)
   
    # Store the updated CMUImage
    conwayDraw = CMUImage(pilImage)
    if app.currEvent == 'dark':
        drawImage(conwayDraw, app.width/2, app.height/2,align='center',
                width=pilImage.width,
                height=pilImage.height,opacity=80)
    else:
        drawImage(conwayDraw, app.width/2, app.height/2,align='center',
                width=pilImage.width,
                height=pilImage.height)

def drawBird(app):
    cx=app.width/7
    cy=app.bird.cy
    closed = app.birdClosedGif[int(app.count0)]
    open = app.birdOpenGif[int(app.count1)]
    closeddark = app.birdClosedGif2[int(app.count0)]
    opendark = app.birdOpenGif2[int(app.count1)]
    if app.bird.mouthOpen==False and app.started==True:
        if app.currEvent == 'dark':
            interval = app.time-app.events['dark']
            drawImage(closeddark, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = min(100,interval))
            drawImage(closed, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = max(0,100-interval))
        elif app.currEvent == 'sunrise':
            interval = app.time-app.events['sunrise']
            drawImage(closed, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = min(100,interval))
            drawImage(closeddark, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = max(0,100-interval))
        else:
            drawImage(closed, cx, cy, align='center',rotateAngle=app.birdAngle)
        

    elif app.bird.mouthOpen==True and app.started==True:
        if app.currEvent == 'dark':
            interval = app.time-app.events['dark']
            drawImage(opendark, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = min(100,interval))
            drawImage(open, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = max(0,100-interval))
        elif app.currEvent == 'sunrise':
            interval = app.time-app.events['sunrise']
            drawImage(open, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = min(100,interval))
            drawImage(opendark, cx, cy, align='center',rotateAngle=app.birdAngle,opacity = max(0,100-interval))
        else:
            drawImage(open, cx, cy, align='center',rotateAngle=app.birdAngle)
       
        
    #drawRect(cx+20,cy-30,5,60,border='black',opacity=50)
        

def drawCloud(app):
    if Cloud.onScreenList!=[]:
        for each in Cloud.onScreenList:
            cx,cy=each.parameter
            image=app.cloudImages[each.cloudType]
            if app.currEvent == 'sunset':
                interval = app.time-app.events['sunset']
                drawImage(image['sunset'], cx, cy, align='center',opacity = min(100,interval))
                drawImage(image['base'], cx, cy, align='center',opacity = max(0,100-interval))
            elif app.currEvent == 'dark':
                interval = app.time-app.events['dark']
                drawImage(image['sunset'], cx, cy, align='center',opacity = max(0,100-interval))
                drawImage(image['dark'], cx, cy, align='center',opacity = min(80,interval))
            elif app.currEvent == 'sunrise':
                interval = app.time-app.events['sunrise']
                drawImage(image['dark'], cx, cy, align='center',opacity = max(0,100-interval))
                drawImage(image['sunset'], cx, cy, align='center',opacity = min(80,interval))
            elif app.currEvent == 'day':
                if app.events['day'] != None:
                    interval = app.time-app.events['day']
                    drawImage(image['sunset'], cx, cy, align='center',opacity = max(0,100-interval))
                    drawImage(image['base'], cx, cy, align='center',opacity = min(100,interval))
                else:
                    drawImage(image['base'], cx, cy, align='center')


def drawFood(app):
    if Food.onScreenList!=[]:
        for each in Food.onScreenList:
            cx,cy=each.parameter
            bug = app.bugGif[int(app.count2)]
            darkbug = app.bugGif2[int(app.count2)]
            fastbug = app.bugGifFast[int(app.count3)]
            darkfastbug = app.bugGif2[int(app.count3)]
            evilbug = app.evilBugGif[int(app.count3)]
            boostbug = app.boostBugGif[int(app.count2)]
            if each.evil:
                drawImage(evilbug, cx, cy, align='center')
            elif each.boost:
                drawImage(boostbug, cx, cy, align='center')
            elif each.fast:
                if app.currEvent == 'dark':
                    interval = app.time-app.events['dark']
                    drawImage(darkbug, cx, cy, align='center',opacity = min(100,interval))
                    drawImage(bug, cx, cy, align='center',opacity = max(0,100-interval))
                elif app.currEvent == 'sunrise':
                    interval = app.time-app.events['sunrise']
                    drawImage(bug, cx, cy, align='center',opacity = min(100,interval))
                    drawImage(darkbug, cx, cy, align='center',opacity = max(0,100-interval))
                else:
                    drawImage(bug, cx, cy, align='center')
                
            else:
                if app.currEvent == 'dark':
                    interval = app.time-app.events['dark']
                    drawImage(darkfastbug, cx, cy, align='center',opacity = min(100,interval))
                    drawImage(fastbug, cx, cy, align='center',opacity = max(0,100-interval))
                elif app.currEvent == 'sunrise':
                    interval = app.time-app.events['sunrise']
                    drawImage(fastbug, cx, cy, align='center',opacity = min(100,interval))
                    drawImage(darkfastbug, cx, cy, align='center',opacity = max(0,100-interval))
                else:
                    drawImage(fastbug, cx, cy, align='center')
                
            #drawRect(cx-40,cy-44,80,88,border='black',opacity=50)
                                                    

    
def drawLines(app):
    notes = ['G4','F4','E4','D4','C4','B3','A3','G3']
    for i in range(1,9):
        drawLine(0,(app.height-app.topBar)*(i/9)+app.topBar,app.width,(app.height-app.topBar)*(i/9)+app.topBar,fill=app.ingameColor,opacity=35)
        drawLabel(notes[i-1],30,(app.height-app.topBar)*(i/9)+app.topBar-13,fill=app.ingameColor,opacity=70,size=16,font=app.font,bold=True)

def drawFilter(app):
    if app.currEvent == 'sunset':
        interval = app.time-app.events['sunset']
        drawRect(0,0,app.width,app.height,fill=RGB(237, 133, 43),opacity = min(10,interval))
    elif app.currEvent == 'dark':
        interval = app.time-app.events['dark']
        drawRect(0,0,app.width,app.height,fill=RGB(237, 133, 43),opacity = max(0,20-interval))
        drawRect(0,0,app.width,app.height,fill=RGB(19, 36, 69),opacity = min(20,interval))
    elif app.currEvent == 'sunrise':
        interval = app.time-app.events['sunrise']
        drawRect(0,0,app.width,app.height,fill=RGB(19, 36, 69),opacity = max(0,20-interval))
        drawRect(0,0,app.width,app.height,fill=RGB(237, 133, 43),opacity = min(20,interval))
    elif app.currEvent == 'day':
        if app.events['day'] != None:
            interval = app.time-app.events['day']
            drawRect(0,0,app.width,app.height,fill=RGB(237, 133, 43),opacity = max(0,20-interval))
     