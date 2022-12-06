from cmu_graphics import *
from PIL import Image

from classes import *


def drawScore(app):
    scx=app.scoreE.currX
    scy=app.scoreE.currY
    lcx=app.livesE.currX
    lcy=app.livesE.currY
    symbol = str(chr(0x2764))
    drawLabel(f'Score: {app.currScore}',scx,scy,font=app.font,fill=app.textColor,size=25,bold=True,align='left')
    if not app.infinite:
        drawLabel(app.currLives*symbol,lcx,lcy,font='symbols',fill=app.textColor,size=25,align='left')
    #drawLabel('Score:',cx-90,cy,fill=app.textColor,size=25,bold=True,font=app.font)
  

def drawButtons(app):
    for butt in Button.butts:
        if butt.screen == app.currScreen:
            if isinstance(butt,imgButton):
                imgW, imgH = getImageSize(butt.img)
                drawImage(butt.img, butt.currX, butt.currY, align='center',
                width=imgW*butt.scale/100,height=imgH*butt.scale/100)
            else:
                if butt.active == False:
                    drawLabel(butt.title,butt.currX,butt.currY,size=butt.fontSize*butt.scale/100,font=app.font,bold=True,fill=app.textColor,opacity=50)
                else:
                    
                    #drawRect(butt.cx,butt.cy,butt.bw,butt.bh,align='center',fill=RGB(236,234,226))
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
    drawImage(app.bg['base'], cx, cy, align='center',width=app.width,height=app.height)
    #drawRect(0,0,app.width,app.height,fill=RGB(14, 28, 48),opacity = min(100,0.01*app.time))
    if app.timestamp != None:
        interval = app.time-app.timestamp
        if interval < 200:
            drawImage(app.bg['sunset'], cx, cy, align='center',opacity = min(100,interval))
            drawImage(app.bg['base'], cx, cy, align='center',opacity = max(0,100-interval))
        else:
            drawImage(app.bg['sunset'], cx, cy, align='center',opacity = max(10,300-interval))
            drawImage(app.bg['dark'], cx, cy, align='center',opacity = min(100,interval-200))
    else:
        drawImage(app.bg['base'], cx, cy, align='center')



def drawSky(app):
    if app.timestamp != None:
        interval = app.time-app.timestamp
        drawRect(0,0,app.width,app.height,fill=RGB(int(max(40,214-interval/2)),int(max(28,117-interval/3)),(min(48,15+interval/10))),opacity = min(80,interval/2))

        # if interval < 50:
        #     drawRect(0,0,app.width,app.height,fill=RGB(14, 28, 48),opacity = min(100,interval))
        # elif interval <100:
        #     drawRect(0,0,app.width,app.height,fill=RGB(14, 28, 48),opacity = max(100,100-interval))
        
    # if len(app.conway.liveCells) >300:
    #     #app.timestamp = app.time
    #     drawRect(0,0,app.width,app.height,fill=RGB(14, 28, 48),opacity = min(100,app.time-app.timestamp))

        #drawRect(0,0,app.width,app.height,fill=RGB(14, 28, 48),opacity = min(100,len(app.conway.liveCells)*0.05))

def drawConway(app):
    # for cell in app.conway.prevCells2:
    #     drawRect(cell[0]*2,cell[1]*2,2,2,fill=RGB(92, 141, 189),border = None)
    #if app.timestamp!= None:
    # for cell in app.conway.prevCells:
    #     drawCircle(cell[0]*2,cell[1]*2,3,fill=RGB(107, 214, 161),border = None,opacity=50)
    for cell in app.conway.liveCells:
        #print(app.conway.prevCellToCount)
        
        drawCircle(cell[0]*2,cell[1]*2,2,
                fill=RGB(247, 239, 218),border = None,opacity=30)


def drawBird(app):
    #rail=Bird.rail
    cx=app.width/7
    cy=app.bird.cy
    
    r=30
    photoImage0 = app.birdClosedGif2[int(app.count0)]
    photoImage1 = app.birdOpenGif2[int(app.count1)]
    if app.bird.mouthOpen==False and app.started==True:
        drawImage(photoImage0, cx, cy, align='center',rotateAngle=app.birdAngle)
        

    elif app.bird.mouthOpen==True and app.started==True:
        cy=app.bird.cy
        drawImage(photoImage1, cx, cy, align='center',rotateAngle=app.birdAngle)
    #drawRect(cx+20,cy-30,5,60,border='black',opacity=50)
        

def drawCloud(app):
    if Cloud.onScreenList!=[]:
        for each in Cloud.onScreenList:
            cx,cy=each.parameter
            image=app.cloudImages[each.cloudType]
            if app.timestamp != None:
                interval = app.time-app.timestamp
                if interval < 300:
                    drawImage(image['sunset'], cx, cy, align='center',opacity = min(100,interval))
                    drawImage(image['base'], cx, cy, align='center',opacity = max(0,100-interval))
                else:
                    drawImage(image['sunset'], cx, cy, align='center',opacity = max(10,400-interval))
                    drawImage(image['dark'], cx, cy, align='center',opacity = min(30,interval-300))
            else:
                drawImage(image['base'], cx, cy, align='center')


def drawFood(app):
    if Food.onScreenList!=[]:
        for each in Food.onScreenList:
            cx,cy=each.parameter
            photoImage2 = app.bugGif[int(app.count2)]
            photoImage3 = app.bugGifFast[int(app.count3)]
            
            if each.fast:
                #canvas.create_image(cx,cy-20,image=photoImage2)
                drawImage(photoImage3, cx, cy, align='center')
            else:
                #canvas.create_image(cx,cy-20,image=photoImage3)
                drawImage(photoImage2, cx, cy, align='center')
            #drawRect(cx-40,cy-44,80,88,border='black',opacity=50)
                                                    

    
def drawLines(app):
    for i in range(1,8):
        drawLine(0,(app.height-app.topBar)*(i/8)+app.topBar,app.width,(app.height-app.topBar)*(i/8)+app.topBar,fill=app.textColor,opacity=50)

def drawFilter(app):
    if app.timestamp != None:
        interval = app.time-app.timestamp
        if interval < 200:
            drawRect(0,0,app.width,app.height,fill=RGB(237, 133, 43),opacity = min(20,interval))
        else:
            newInterval = interval-200
            drawRect(0,0,app.width,app.height,fill=RGB(237, 133, 43),opacity = max(0,20-newInterval))
            drawRect(0,0,app.width,app.height,fill=RGB(19, 36, 69),opacity = min(40,newInterval))
        
        