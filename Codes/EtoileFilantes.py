# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 14:19:38 2020

@author: LaRach
"""

import random
from rpi_ws281x import Color

class EtoileFilante():
    def __init__(self,position,speed,goingUp, bounds, tailLenght,color=(255,255,255)):
        self.position = position
        self.speed = speed
        self.goingUp = goingUp
        self.tailLenght = tailLenght if tailLenght > 1 else 2
        self.bounds = bounds
        self.color = color
    def update(self):
        if self.goingUp:
            self.position += self.speed
            if self.position - self.tailLenght > max(self.bounds):
                return True
        else:
            self.position -= self.speed
            if self.position + self.tailLenght < min(self.bounds):
                return True
        return False
    def getColor(self, intensity):
        newColor = [0,0,0]            
        for k,v in enumerate(self.color):
            newColor[k] = int(v*intensity/100)
        return Color(newColor[0], newColor[1], newColor[2])
    def getPositions(self):
        if self.goingUp:
            return [self.position - k for k in range(self.tailLenght + self.speed) if ((self.position-k) < max(self.bounds) and (self.position-k) > min(self.bounds))]
        else:
            return [self.position + k for k in range(self.tailLenght + self.speed) if (self.position+k) > min(self.bounds) and (self.position+k) < max(self.bounds)]
    def getColors(self):
        return [self.getColor(max(0,int(100-100*(k/(self.tailLenght-1))))) for k in range(self.tailLenght+self.speed)
                if ((self.goingUp and ((self.position-k) < max(self.bounds) and (self.position-k) > min(self.bounds)))
                    or ((not self.goingUp) and ((self.position+k) > min(self.bounds) and (self.position+k) <max(self.bounds))))]
    
class NuitEtoile():
    etoiles = []
    count = 0
    def __init__(self, strip, bounds, color = (255,255,255), speed = 1, tailLenght = 5, nbEtoile = 1, newEtoileDelay = 10, randomColor = False, randomTailLength = False, randomBounds = False):
        self.strip = strip
        self.bounds = bounds
        self.color = color
        self.speed = speed
        self.tailLenght = tailLenght
        self.nbEtoile = nbEtoile
        self.newEtoileDelay = newEtoileDelay
        self.randomColor = randomColor
        self.randomTailLength = randomTailLength
        self.randomBounds = randomBounds
        self.etoiles = []
        self.count = 0
    def new_step(self):
        #cretion de nouveau flocons si nécaissaire
        if (self.count == self.newEtoileDelay):
            self.count = 0
            for i in range(self.nbEtoile):
                self.makeNewEtoile()
        else:
            self.count += 1
        #update des flocons
        
        for f in self.etoiles:
            if f.update():
                self.etoiles.remove(f)

            else:
                pos = f.getPositions()
                col = f.getColors()
                for k,v in enumerate(pos):
                    self.strip.setPixelColor(v,col[k])

    def makeNewEtoile(self):
        goingUp = random.random() < 0.5
        if goingUp:
            position = min(self.bounds)
        else:
            position = max(self.bounds)
        if self.randomColor:
            newEtoileColor = tuple([random.randint(3,255) for k in range(3)])
        else:
            newEtoileColor = self.color
        if self.randomTailLength:    
            newEtoileTailLength = random.randint(0,self.tailLenght)
        else:
            newEtoileTailLength = self.TailLength
        if self.randomBounds:
            newEtoileBounds = [random.randint(min(self.bounds),max(self.bounds)) for i in range(2)]
        else:
            newEtoileBounds = self.bounds
        
        self.etoiles.append(EtoileFilante(position, self.speed, goingUp, newEtoileBounds, newEtoileTailLength, newEtoileColor))
    
    