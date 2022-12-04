import cmu_graphics
import random

# Classes and original rail mechanic made by zilyuj, largely being restructured by me

class Food:
    onScreenList = [ ]
    upcomingList=[]
    def __init__(self, parameter, row, timeDelay):
        self.parameter = parameter #the location of the food item on screen 
        self.row = row #the number of row that the food is in 
        self.timeDelay = timeDelay #amount of time delay before an item is added to the on-screen list
        self.fast = bool(random.getrandbits(1))

    @classmethod   
    def onStep(cls, app):
        if app.started == True and Food.upcomingList != [ ]:#if the upcomming list is not empty
            delay = Food.upcomingList[0].timeDelay #get the needed amount of time delay 
            app.timer += 1
            
            if app.timer == delay:#if the delay is reached
                app.timer = 0#refresh the timer
                Food.onScreenList.append(Food.upcomingList.pop(0))#add the first food of the upcoming list to the on screen list
    
    def makeFood(app):

        row=random.randint(1,7)
        timeDelay=random.randint(20,40)
        parameter=[app.width,(row-1)*(app.height/7),app.width+77,
                (row-1)*(app.height/7)+88]
        
        return Food(parameter,row,timeDelay)

    def makeFoodList(app):
        L=[]
        for i in range(25):
            stuff=Food.makeFood(app)
            L.append(stuff)
        Food.upcomingList.extend(L)


class Cloud:
    onScreenList=[]
    upcomingList=[]
    
    def __init__(self,parameter,cloudType,timeDelay):
        self.parameter= parameter
        self.timeDelay=timeDelay
        self.cloudType=cloudType
    

    @classmethod   
    def onStep(cls, app):
        if Cloud.upcomingList != [ ]:#if the upcomming list is not empty
            delay = Cloud.upcomingList[0].timeDelay #get the needed amount of time delay 
            app.timerC += 1
            if app.timerC == delay:#if the delay is reached
                app.timerC = 0#refresh the timer
                Cloud.onScreenList.append(Cloud.upcomingList.pop(0))#add the first food of the upcomming list to the on screen list
    #make list of corn?

    @staticmethod
    def CloudGen(app):
        cloudType=random.randint(0,3)
        cx=app.width+200
        cy=random.randint(50,app.height)
        parameter=[cx,cy]
        timerDelay=random.randint(300,400)
        return Cloud(parameter,cloudType,timerDelay)
    
    @staticmethod
    def CloudListGen(app):
        L=[]
        for i in range(75):
            cloud=Cloud.CloudGen(app)
            L.append(cloud)
        return L
    
    
class Bird:
    rail = 14
    def __init__(self,cy):
        self.cy = cy
        self.mouthOpen = False
        self.targetRrail=False
    
    def openMouth(self):
        self.mouthOpen = True

    def closeMouth(self):
        self.mouthOpen = False

    def __repr__(self):
        return f'bird on rail {self.currentRail}, mouth open is {self.mouthOpen}'

class Element():
    offAmount = -300
    elements = dict()
    def __init__(self,screen,screenX,screenY,direction):
        #self.screen = screen
        self.screenX = screenX
        self.screenY = screenY
        self.currX = self.screenX
        self.currY = self.screenY
        self.direction = direction # x or y
        Element.elements[screen] = Element.elements.get(screen,set()).union({self})

    def moveOffStep(screen):
        allOff = True
        for element in Element.elements[screen]:
            if element.direction == 'x':
                if element.currX >= Element.offAmount:
                    element.currX -=20
                    allOff = False
            elif element.direction == 'y':
                if element.currY >= Element.offAmount:
                    element.currY -=20
                    allOff = False
        return allOff

    def moveOnStep(screen):
        allOn = True
        for element in Element.elements[screen]:
            if element.direction == 'x':
                if element.currX <= element.screenX:
                    element.currX +=20
                    allOn = False
            elif element.direction == 'y':
                if element.currY <= element.screenY:
                    element.currY +=20
                    allOn = False
        return allOn

    def allOff(screen):
        for element in Element.elements[screen]:
            Element.goOff(element)
    
    def allOn(screen):
        for element in Element.elements[screen]:
            Element.goOn(element)

    def goOff(self):
        if self.direction == 'x':
            self.currX = Element.offAmount
        elif self.direction == 'y':
            self.currY = Element.offAmount

    def goOn(self):
        if self.direction == 'x':
            self.currX = self.screenX
        elif self.direction == 'y':
            self.currY = self.screenY

    def changeDir(self,dir):
        self.direction = dir


class Button(Element):
    butts = set()
    def __init__(self,screen,title,cx,cy,bw=100,bh=60,description='',active=True,fontSize=25):
        super().__init__(screen,cx,cy,'x')
        self.screen = screen
        self.title = title
        self.cx = cx
        self.cy = cy
        self.bw = bw
        self.bh = bh
        self.desc = description
        self.scale = 100
        self.active = active
        self.fontSize = fontSize
        Button.butts.add(self)
    
    def __repr__(self):
        return '<' + self.title + ' button>'
    
    
    # def labelStr(self):
    #     #return f'self.cx,self.cy,self.bw,self.bh'
    #     return "butt.title,butt.cx,butt.cy,size=25,font='monospace',bold=True,fill=RGB(22,33,63)"

class imgButton(Button):
    def __init__(self,screen,title,cx,cy,img,bw=100,bh=30,description=''):
        super().__init__(screen,title,cx,cy,bw,bh,description)
        self.img = img

