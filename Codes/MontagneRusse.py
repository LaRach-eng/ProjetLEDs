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
        if self.speed+self.acc >= self.minSpeed:
            self.speed+=self.acc
        if self.goingUp:
            self.position += self.speed
        else:
            self.position -= self.speed
        
        return self.updateTail()
    
    def change_acc(self):
        self.acc = self.master.getAcc(int(self.position))
    
    def getColor(self, intensity):
        newColor = [0,0,0]            
        for k,v in enumerate(self.color):
            newColor[k] = int(v*intensity/100)
        return Color(newColor[0], newColor[1], newColor[2])
    def getPositions(self):
        return [v[0] for v in self.tail]
    def getColors(self):
        return [self.getColor(v[1]) for v in self.tail]
    def updateTail(self):
        newTail = []
        position = int(self.position)
        if position != self.tail[-1][0]:
            #Updating previous pixels
            for v in self.tail:
                if v[1] > 0:
                    newTail.append((v[0],max(0,v[1]-self.tailFactor)))
            if len(newTail) > 0:
                if self.goingUp == ( self.speed>0 ):    
                    newTail += [(k,newTail[-1][1]+((100-newTail[-1][1])/(position-newTail[-1][0]))*(k-newTail[-1][0])) for k in range(newTail[-1][0]+1,min(position,max(self.bounds))+1)]
                else:
                    newTail += [(k,newTail[-1][1]+((100-newTail[-1][1])/abs(position-newTail[-1][0]))*abs(k-newTail[-1][0])) for k in range(newTail[-1][0]-1,max(position-1,min(self.bounds)-1),-1)]
            self.tail = newTail
        return len(self.tail) == 0
                
    
    
    
class Rails():
    def __init__(self, strip, bounds, boundsFalling, boundsRising, color = (255,255,255), initialSpeed = 0,minSpeed = 1, g = 0.1, goingUp = False, tailFactor = 30, newTrainDelay = 50, randomColor = True, randomNewTrainDelay = 30,maxTrainNb = 3):
        self.strip = strip
        self.bounds = bounds
        self.boundsFalling = boundsFalling
        self.boundsRising = boundsRising
        self.color = color
        self.speed = initialSpeed
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
        #update des trains
        for f in self.trains:
            if f.update():
                self.trains.remove(f)
                
            else:
                pos = f.getPositions()
                col = f.getColors()
                for k,v in enumerate(pos):
                    self.strip.setPixelColor(v,col[k])
    def getAcc(self, position):
        for i in self.boundsFalling:
            if i[0] <= position <= i[1]:
                return self.g
        for i in self.boundsRising:
            if i[0] <= position <= i[1]:
                return -self.g
        return 0
    def makeNewTrain(self):
        if self.goingUp:
            position = min(self.bounds)
        else:
            position = max(self.bounds)
        if self.randomColor:
            newTrainColor = tuple([random.randint(3,255) for k in range(3)])
        else:
            newTrainColor = self.color  
    
        self.trains.append(Train(self, position, self.speed, self.minSpeed, self.getAcc(position) , self.goingUp, self.bounds , self.tailFactor, newTrainColor))
    