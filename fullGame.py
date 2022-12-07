from cmu_graphics import *

from classes import *

from setupScreen import *
from homeScreen import *
from playScreen import *
from drawMethods import *
from gameMethods import *

def onAppStart(app):
    app.time = 0
    app.timestamp = None
    app.setMaxShapeCount(3000)
    app.topBar = 30
    app.font = 'monospace'
    app.textColor = RGB(22,33,63)
    app.hoverColor = RGB(186, 65, 48)
    app.currScreen = 'start'
    app.scores = [0]

    app.started=False
    app.paused = False
    app.timer=0
    app.timerDelay=1
    app.stepsPerSecond=44
    
    openImages(app)
    

    app.butts = set()
    app.settings = Button('home','Set Up',5*app.width/7,4.1*app.height/5)
    app.settings = Button('home','Modes',5*app.width/7,3.6*app.height/5)
    app.tutorial = Button('home','Tutorial',2*app.width/7,4*app.height/5)
    #app.play = Button('home','home')
    app.butts.add(app.settings)
    app.butts.add(app.tutorial)
    app.butts.add(imgButton('home','play',app.width/2,4*app.height/5,app.playButton,100,100))
    app.overButton = Button('end','Restart',app.width/2,3.5*app.height/5)
    app.homeButton = Button('end','Home',app.width/2,3.9*app.height/5)
    app.continueButton = Button('end','Continue',app.width/2,3.1*app.height/5)

    app.timerC=0
    app.cloud=True
    #app.Introx=app.width/2
    #app.pausex=app.width/2


    app.bird=Bird(app.height/5)

    app.recorder = Recording(app.height-app.topBar)
    app.recorder.pause()
    app.conway = Conway(app.width,app.height)

    app.events = {'sunset':None,
                'dark':None,
                'sunrise':None,
                'day':None}
    app.currEvent = 'day'


def main():
    runAppWithScreens(initialScreen='home', width=800,height=500)
main()