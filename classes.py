import cmu_graphics
import random
import copy

# Food and cloud classes initially made by zilyuj

class Food:
    onScreenList = [ ]
    upcomingList=[]
    delay = 40
    ratio = 8
    def __init__(self, parameter, row, timeDelay,song=False):
        self.parameter = parameter #the location of the food item on screen 
        self.row = row #the number of row that the food is in 
        self.timeDelay = timeDelay #amount of time delay before an item is added to the on-screen list
        if song:
            self.fast=False
        else:
            self.fast = bool(random.getrandbits(1))
        self.evil = False
        self.boost = False
        if not song:
            evil = random.randint(1,Food.ratio)
            if evil == 1:
                self.evil = True
                return
            boost = random.randint(1,Food.ratio)
            if boost == 1:
                self.boost = True

    @classmethod   
    def onStep(cls, app):
        
        if app.started == True and Food.upcomingList != [ ]:#if the upcomming list is not empty
            delay = Food.upcomingList[0].timeDelay #get the needed amount of time delay 
            app.timer += 1
            
            if app.timer == delay:#if the delay is reached
                app.timer = 0#refresh the timer
                Food.onScreenList.append(Food.upcomingList.pop(0))#add the first food of the upcoming list to the on screen list
    
    def makeFood(app):
        row=random.randrange(1,9)
        timeDelay=random.randint(int(Food.delay),int(Food.delay*2))
        parameter=[app.width,(row*(app.height-app.topBar)/9)+app.topBar]
        
        return Food(parameter,row,timeDelay)

    def makeFoodList(app):
        L=[]
        for i in range(25):
            stuff=Food.makeFood(app)
            L.append(stuff)
        Food.upcomingList.extend(L)

    def makeTwinkle(app):
        song = []
        notes = [0,1,1,5,5,6,6,5,0,4,4,3,3,2,2,1,0,5,5,4,4,3,3,2,0,5,5,4,4,3,3,2,0,1,1,5,5,6,6,5,0,4,4,3,3,2,2,1]
        for note in range(1,len(notes)):
            row = 9-notes[note]
            parameter=[app.width,(row*(app.height-app.topBar)/9)+app.topBar]
            if notes[note-1] == 0:
                song.append(Food(parameter,row,int(Food.delay+20),song=True))
            elif notes[note] == 0:
                continue
            else:
                song.append(Food(parameter,row,int(Food.delay),song=True))
        Food.upcomingList.extend(song)
    
    def __repr__(self):
        return f'Food at {self.parameter}'

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
                Cloud.onScreenList.append(Cloud.upcomingList.pop(0))

    @staticmethod
    def CloudGen(app):
        cloudType=random.randint(0,3)
        cx=app.width+250
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
    def __init__(self,screen,title,cx,cy,bw=120,bh=40,description='',active=True,fontSize=25):
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
        self.hovered = False
        self.fontSize = fontSize
        self.invisible = False
        Button.butts.add(self)
    
    def __repr__(self):
        return '<' + self.title + '>'
 
class imgButton(Button):
    def __init__(self,screen,title,cx,cy,img,bw=100,bh=30,description=''):
        super().__init__(screen,title,cx,cy,bw,bh,description)
        self.img = img

class Conway():
    #star generator based on Conway's Game of Life
    def __init__(self,width,height):
        self.width = width
        self.height = height
        self.liveCells = set()
        self.prevCells = set()
        self.prevCells2 = set()
        self.generation = 0
        self.tenGens = set()
        self.cellToCount = Conway.step2(self)
    
    
    def step2(self):
        cellToCount = dict()
        for cell in self.liveCells:
            cellX, cellY = cell[0],cell[1]
            for x in [-2,-1,0,1,2]:
                for y in [-2,-1,0,1,2]:
                    if (not (x==0 and y==0) and
                        0 <= cellX+x < self.width and
                        0 <= cellY+y < self.height):
                        newCell = (cellX+x,cellY+y)
                        cellToCount[newCell] = cellToCount.get(newCell,0)+1
        return cellToCount
        
    
    def step(self):
        self.generation+=1
        nextGen = set()
        reduce = False
        if len(self.liveCells)>1500:
            reduce = True
        for cell in self.cellToCount:
            if cell in self.liveCells:
                if self.cellToCount[cell] in [4]:
                    if reduce:
                        if bool(random.getrandbits(1)):
                            nextGen.add(cell)
                    else:
                        nextGen.add(cell)
            else:
                if self.cellToCount[cell] in [4]:
                    if reduce:
                        if bool(random.getrandbits(1)):
                            nextGen.add(cell)
                    else:
                        nextGen.add(cell)
        self.tenGens = self.tenGens & self.liveCells
        self.prevCells2 = copy.copy(self.prevCells)
        self.prevCells = copy.copy(self.liveCells)
        self.liveCells = nextGen
        if self.generation%10 == 0:
            self.liveCells = nextGen-self.tenGens
            self.tenGens = self.liveCells
        self.cellToCount = Conway.step2(self)

    def generateCells(self):
        num = 30
        for i in range(5):

            seedx = random.randrange(num,self.width-num)
            seedy = random.randrange(num,self.height-num)
            for i in range(10):
                x = random.randrange(-int(self.width/num),int(self.width/num))
                y = random.randrange(-int(self.height/num),int(self.height/num))
                if 0 < seedx+x < self.width and 0 < seedy+y < self.height:
                    cell = (seedx+x,seedy+y)
                    self.liveCells.add((cell))
        self.cellToCount = Conway.step2(self)

    def generateLocation(self,seedx,seedy,magnum):
        seedx = int(seedx)
        seedy = int(seedy)
        for i in range(magnum):
            x = random.randrange(-5,5)
            y = random.randrange(-5,5)
            if 0 < seedx+x < self.width and 0 < seedy+y < self.height:
                cell = (seedx+x,seedy+y)
                #print(cell)
                self.liveCells.add((cell))
        self.cellToCount = Conway.step2(self)
    
    def reset(self):
        self.liveCells = set()
        self.prevCells = set()
        self.prevCells2 = set()
        self.generation = 0
        self.tenGens = set()
        self.cellToCount = Conway.step2(self)
