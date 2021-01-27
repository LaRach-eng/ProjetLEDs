# -*- coding: utf-8 -*-
"""
Created on Sun Jan 24 14:04:13 2021

@author: chere
"""

import random
from rpi_ws281x import Color

class Train():
    def __init__(self,master,position,speed,minSpeed,acc,goingUp, bounds, tailFactor,color=(255,255,255)):
        self.master = master
        self.position = position
        self.speed = speed
        self.minSpeed = minSpeed
        self.acc = acc
        self.goingUp = goingUp        
        self.bounds = bounds
        self.tailFactor = tailFactor
        self.color = color
        self.tail = [(self.position,100)]
    def update(self):
        self.change_acc()
        
        self.position += self.speed

        if abs(self.speed+self.acc) >= abs(self.minSpeed) or self.minSpeed == 0:
            self.speed+=self.acc
        return self.updateTail()
    
    def change_acc(self):
        self.acc = self.master.getAcc(int(self.position))
    
    def get_acc(self):
        return self.acc
    def get_speed(self):
        return self.speed
    
    def set_speed(self,new_speed):
        self.speed = new_speed
    def set_pos(self,new_position):
        self.position = new_position
    
    def getColor(self, intensity):
        newColor = [0,0,0]            
        for k,v in enumerate(self.color):
            newColor[k] = int(v*intensity/100)
        return Color(newColor[0], newColor[1], newColor[2])
    def getPositions(self):
        return [v[0] for v in self.tail]
    def getPosition(self):
        return self.position
    def getColors(self):
        return [self.getColor(v[1]) for v in self.tail]
    def updateTail(self):
        newTail = []
        position = int(self.position)
        for v in self.tail:
            #Updating previous pixels
            if v[1] > 0:
                newTail.append((v[0],max(0,v[1]-self.tailFactor)))
        if len(newTail) > 0:
            if position != newTail[-1][0]:
                    if ( self.speed>0 ):    
                        newTail += [(k,newTail[-1][1]+((100-newTail[-1][1])/(position-newTail[-1][0]))*(k-newTail[-1][0])) for k in range(newTail[-1][0]+1,min(position,max(self.bounds))+1)]
                    else:
                        newTail += [(k,newTail[-1][1]+((100-newTail[-1][1])/abs(position-newTail[-1][0]))*abs(k-newTail[-1][0])) for k in range(newTail[-1][0]-1,max(position-1,min(self.bounds)-1),-1)]
            else:
                newTail[-1] = (position,100)
        self.tail = newTail
        return len(self.tail) == 0
                
    
    
    
class Rails():
    
    def __init__(self, strip, bounds, boundsFalling, boundsRising, color = (255,255,255), initialSpeed = 0, randomSpeed = 3.5,minSpeed = 1, g = 0.1, goingUp = False, tailFactor = 30, newTrainDelay = 30, randomColor = True, randomNewTrainDelay = 1,maxTrainNb = 6):
        self.strip = strip
        self.bounds = bounds
        self.boundsFalling = boundsFalling
        self.boundsRising = boundsRising
        self.color = color
        self.speed = initialSpeed
        self.randomSpeed = randomSpeed
        self.minSpeed = minSpeed
        self.g = g
        self.goingUp = goingUp
        self.tailFactor = tailFactor
        self.newTrainDelay = newTrainDelay
        self.randomColor = randomColor
        self.randomNewTrainDelay = randomNewTrainDelay
        self.maxTrainNb = maxTrainNb
        self.trains = []
        self.count = 0
        self.makeNewTrain()
    def new_step(self):
        #cretion de nouveau trains si nécaissaire
        if (self.count == self.newTrainDelay):
            if len(self.trains)<self.maxTrainNb:
                self.count = random.randrange(-self.randomNewTrainDelay,self.randomNewTrainDelay)
                self.makeNewTrain()
        else:
            self.count += 1

        collision = [False for t in self.trains]        
        for k,i in enumerate(self.trains):
            i_pos = i.getPosition()
            i_speed = i.get_speed()
            
            for l,j in enumerate(self.trains[k+1:]):
                j_pos = j.getPosition()
                j_speed = j.get_speed()
                if (i_pos-j_pos)*(i_pos+i_speed-j_pos-j_speed)<=0:
                    collision[k] = True
                    collision[k+l+1]= True
                    new_pos = int((i_pos+i_speed+j_pos+j_speed)/2)
                    if i_pos < j_pos:
                        i.set_pos(new_pos)
                        j.set_pos(new_pos+1)
                    else :
                        i.set_pos(new_pos+1)
                        j.set_pos(new_pos)
                    
                    i.updateTail()
                    i.set_speed(j_speed)
                    
                    j.updateTail()
                    j.set_speed(i_speed)
                #update des trains
        for p,train in enumerate(self.trains):
            if not collision[p]:
                if train.update():
                    self.trains.remove(train)
            col = train.getColors()
            for k,v in enumerate(train.getPositions()):
                self.strip.setPixelColor(v,col[k])
            
            
    def getAcc(self, position):
        for i in self.boundsFalling:
            if i[0] <= position <= i[1]:
                if self.goingUp:
                    return self.g
                else:
                    return - self.g
        for i in self.boundsRising:
            if i[0] <= position <= i[1]:
                if self.goingUp:
                    return - self.g
                else:
                    return self.g
        return 0
    def makeNewTrain(self):
        if self.goingUp:
            position = min(self.bounds)
            speed = self.speed+random.random()*self.randomSpeed
        else:
            position = max(self.bounds)
            speed = -self.speed-random.random()*self.randomSpeed
        if self.randomColor:
            newTrainColor = self.wheel(random.randint(0,15)*51)
        else:
            newTrainColor = self.color  
    
        self.trains.append(Train(self, position, speed, self.minSpeed, self.getAcc(position) , self.goingUp, self.bounds , self.tailFactor, newTrainColor))

    def wheel(self,value):
        value = value % (3*255)
        if value <= 255:
            r = 255 - value
            g = value
            b = 0
        elif value <= 2*255:
            r = 0
            g = 2*255-value
            b = value-255
        else:
            r = value-2*255
            g = 0
            b = 3*255-value
        return (r,g,b)