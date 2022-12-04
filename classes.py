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

# class Element():
#     def __init__(self,screenX,screenY):
#         self.screenX = screenX
#         self.screenY = screenY
#         # if xMove:
#         #     self.offX = -50
#         #     self.offY = screenY
#         # if yMove:
#         #     self.offY = -50
#         #     self.offX = screenY
        
#     def moveOff(self):


class Button(Element):
    butts = set()
    def __init__(self,screen,title,cx,cy,bw=100,bh=60,description='',active=True,fontSize=25):
        super().__init__(cx,cy)
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

