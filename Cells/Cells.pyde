from random import *
from math import *

width = 1000
height = 750
def setup():
    global width,height
    size(width,height,P3D)
    frameRate(60)


class Food:
    def __init__(self,pos):
        self.r = 1
        self.pos = pos
        self.a = PI
    
    def update(self):
        fill(0,255,0)
        ellipse(self.pos.x,self.pos.y,self.r*2,self.r*2)

class Cell:
    def __init__(self,r,pos=None,w=None):
        global width, height, cell
        self.r = r
        self.a = PI*self.r**2
        self.angle = randint(0,359)
        self.pos = pos or PVector(randint(0,width),randint(0,height))
        self.maxSpeed = 50/self.r
        self.speed = 1
        self.maxRotSpeed = 5
        self.rotSpeed = 1
        self.weights = w or [[(random()*2)-1 for i in range(2)] for j in range(6)]
        #print(self.weights)
        self.outputs = [0,0,0]
        self.closestCell = None
        self.closestFood = None
        self.biggest = self
        
    def eat(self):
        global food
        for i in food:
            if dist(self.pos.x,self.pos.y,i.pos.x,i.pos.y)<(self.r+i.r/2.0):
                if self.r > i.r:
                   self.r = sqrt((self.a+i.a)/PI)
                   food.pop(food.index(i))
        
    def move(self,speed):
        self.maxSpeed = 30/self.r
        self.pos.x+=cos(PI*self.angle/180)*self.maxSpeed*speed
        self.pos.y+=sin(PI*self.angle/180)*self.maxSpeed*speed
        
        if self == best:
            stroke(0)
            strokeWeight(3)
            line(self.pos.x,self.pos.y,self.pos.x+cos(PI*self.angle/180)*self.r,self.pos.y+sin(PI*self.angle/180)*self.r)
            strokeWeight(1)
        
    def fast(self,inc):
        if inc == "u":
            self.speed += self.maxSpeed * .1
            #print(self.speed)
        if inc == "d":
            self.speed -= self.maxSpeed * .1
            #print(self.speed)
            
        if self.speed >= self.maxSpeed:
            self.speed = self.maxSpeed
        if self.speed <= 0:
            self.speed = 0
        
    def rot(self,dir):
        if dir == "r":
            self.angle+=self.rotSpeed
        elif dir == "l":
            self.angle-=self.rotSpeed
        self.angle %= 360
                
    def sig(self,x):
        return 1.0/(1+e**-x)
    
    def areaText(self):
        textSize(10)
        fill(0)
        text(str(int(self.a)),self.pos.x,self.pos.y)
                   
    def NN(self):
        global cells, best
        #self.closestCell = cell or self.closestCell
        for i in cells:            
            if self.closestCell == None:
                self.closestCell = i
            else:
                if i != self and dist(self.pos.x,self.pos.y,i.pos.x,i.pos.y)-(self.r+i.r)<dist(self.pos.x,self.pos.y,self.closestCell.pos.x,self.closestCell.pos.y)-(self.r+self.closestCell.r):
                    self.closestCell = i
            
                
            if dist(self.pos.x,self.pos.y,i.pos.x,i.pos.y)<(self.r+i.r/2.0) and i != self:
                if self.a > i.a:
                   self.a += i.a
                   cells.pop(cells.index(i))
                   
        for i in food:
            if self.closestFood == None:
                self.closestFood = i
            else:
                if i != self and dist(self.pos.x,self.pos.y,i.pos.x,i.pos.y)-(self.r+i.r)<dist(self.pos.x,self.pos.y,self.closestFood.pos.x,self.closestFood.pos.y)-(self.r+self.closestFood.r):
                    self.closestFood = i
            
            
        #x,y,a,closestCellDist,closestCellR,closestFood
        inputs = [self.pos.x/width,self.pos.y/height,best.a/self.a,dist(self.pos.x,self.pos.y,self.closestCell.pos.x,self.closestCell.pos.y)/self.r,self.closestCell.r/self.r,dist(self.pos.x,self.pos.y,self.closestFood.pos.x,self.closestFood.pos.y)/self.r]
        self.outputs = [0,0]
        for i in range(len(self.outputs)):
            for j in range(len(inputs)):
                self.outputs[i] += inputs[j]*self.weights[j][i]
        self.outputs = [self.sig(self.outputs[0]),self.sig(self.outputs[1])]
        
        out = self.outputs
        '''
        if self == best:
            print(out)
        '''
        
        self.move(out[0])
        if out[1] >= .5:
            self.rotSpeed = self.maxRotSpeed * (out[1]-.5)*2
            self.rot('r')
            
        else:
            self.rotSpeed = self.maxRotSpeed * (out[1]-.499)*2
            self.rot('l')
        '''
        if self == best:
            print(out)
        '''
        
    def update(self):
        global cells, best
        
        if self.r >= height:
            cells = []
            best = self
        
        if self.r < .5:
            cells.pop(cells.index(self))
        
        self.eat()
        self.NN()
        
        '''
        if self.pos.x <= self.r:
            self.pos.x = self.r
        if self.pos.x >= width-self.r:
            self.pos.x = width-self.r
        if self.pos.y <= self.r:
            self.pos.y = self.r
        if self.pos.y >= height-self.r:
            self.pos.y = height-self.r
        '''
        
        if best == self:
            fill(255,0,0)
            line(self.pos.x,self.pos.y,self.closestCell.pos.x,self.closestCell.pos.y)
            line(self.pos.x,self.pos.y,self.closestFood.pos.x,self.closestFood.pos.y)
            stroke(0)
        else:
            fill(0,200,200)
            
        self.a -= self.a/3000.0
        self.r = sqrt(self.a/PI)
        stroke(0)
        ellipse(self.pos.x,self.pos.y,self.r*2,self.r*2)
        if self == best:
            self.areaText()
        self.closestCell = None
        self.closestFood = None

        
best = Cell(.1)
cells = [Cell(2.5) for i in range(100)]
food = [Food(PVector(randint(0,width),randint(0,height))) for i in range(200)]

zoom = 0
def draw():
    global cells, best, zoom
    background(255)
    if keyPressed and key == " ":
        if zoom == 0:
            zoom = 1
        else:
            zoom = 0
            
    if zoom == 1:
        translate(-best.pos.x+width/2,-best.pos.y+height/2,150.0/(best.r/10.0))
    else:
        translate(0,0)
    fill(255)
    rect(0,0,width,height)
    
    
    
    if len(cells) < 100:
        #if best == None:
        r = 5
        pos = PVector(randint(0,width),randint(0,height))
        gen = 0
        while True:
            for i in cells:
                if dist(pos.x,pos.y,i.pos.x,i.pos.y)>(r+i.r/2.0):
                    gen = 1
                else:
                    gen = 0
                    pos = PVector(randint(0,width),randint(0,height))
                    break
            if gen == 1:
                cells.append(Cell(2.5,pos))
                '''
                if best == None:
                    cells.append(Cell(2.5,pos))
                else:
                    w = best.weights
                    for i in range(len(w)):
                        for j in range(len(w[i])):
                            w[i][j] *= choice([.99,1.01])
                            if w[i][j] > 1:
                                w[i][j] = 1
                            elif w[i][j] < 0:
                                w[i][j] = 0
                    cells.append(Cell(2.5,pos,w))
                '''
                break
        #else:
            '''
            w = best.weights
            for i in range(len(w)):
                for j in range(len(w[i])):
                    w[i][j] *= choice([.99,1.01])
                    if w[i][j] > 1:
                        w[i][j] = 1
                    elif w[i][j] < 0:
                        w[i][j] = 0
            r = 5
            pos = PVector(randint(0,width),randint(0,height))
            gen = 0
            while True:
                for i in cells:
                    if dist(pos.x,pos.y,i.pos.x,i.pos.y)>(r+i.r/2.0):
                        gen = 1
                    else:
                        gen = 0
                        pos = PVector(randint(0,width),randint(0,height))
                        break
                if gen == 1:
                    cells.append(Cell(5,pos,w))
                    break
            '''
    if len(food)<200:
        food.append(Food(PVector(randint(0,width),randint(0,height))))
    
    for i in cells:
        i.update()
        if i.a > best.a:
            best = i
    for i in food:
        i.update()
    
