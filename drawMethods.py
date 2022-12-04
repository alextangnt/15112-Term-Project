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
    drawImage(app.bg, cx, cy, align='center',width=app.width,height=app.height)         

def drawBird(app):
    #rail=Bird.rail
    cx=app.width/7
    cy=app.bird.cy
    
    r=30
    photoImage0 = app.birdClosedGif[int(app.count0)]
    photoImage1 = app.birdOpenGif[int(app.count1)]
    if app.bird.mouthOpen==False and app.started==True:
        drawImage(photoImage0, cx, cy, align='center',rotateAngle=app.birdAngle)
        

    elif app.bird.mouthOpen==True and app.started==True:
        cy=app.bird.cy
        drawImage(photoImage1, cx, cy, align='center',rotateAngle=app.birdAngle)
        

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


