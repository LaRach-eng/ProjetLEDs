# -*- coding: utf-8 -*-
"""
Created on Thu Dec  3 14:35:12 2020

@author: chere
"""
import random


class Flocon():
    maxIntensity = 100;
    position = 0
    intensity = 0
    speed=0
    montante = True
    def __init__(self,position,speed,color):
        self.position = position
        self.speed = speed
        self.color = color
    def update(self):
        if self.montante:
            if self.intensity + self.speed >= self.maxIntensity:
                self.intensity = self.maxIntensity
                self.montante = False
            else:
                self.intensity += self.speed 
        else:
            if (self.intensity>=self.speed):
                self.intensity -= self.speed
            else:
                self.intensity = 0
                return True
        return False
    def getColor(self):
        newColor = [0,0,0]            
        for k,v in enumerate(self.color):
            newColor[k] = int(v*self.intensity/100)
        return tuple(newColor)
    def getPosition(self):
        return self.position
    def getIntensity(self):
        return self.intensity
class Neige():
    flocons = []
    count = 0
    def __init__(self,strip,color=(255,255,255),speed = 5,nbFlocon=1,newFloconDelay=10,randomColor = False):
        self.strip = strip
        self.color = color
        self.speed = speed
        self.nbFlocon = nbFlocon
        self.newFloconDelay = newFloconDelay
    def new_step(self):
        #cretion de nouveau flocons si nécaissaire
        if (self.count == self.newFloconDelay):
            self.count = 0
            for i in range(self.nbFlocon):
                self.makeNewFlocon()
        else:
            self.count += 1
        #update des flocons
        
        for f in self.flocons:
            if f.update():
                self.flocons.remove(f)

            else:
                self.strip.setPixelColor(f.getPosition(),f.getColor())
    def getColor(self,intensity):
        newColor = [0,0,0]            
        for k,v in enumerate(self.color):
            newColor[k] = int(v*intensity/100)
        return newColor
    def makeNewFlocon(self):
        position = random.randrange(0,self.strip.numPixels())
        if self.randomColor:
            newFloconColor = tuple([random.randint(0,255) for k in range(3)])
        else:
            newFloconColor = self.color
        self.flocons.append(Flocon(position,self.speed,newFloconColor))

        
class EtoileFilante():
    def __init__(self,position,speed,goingUp, bounds, tailLenght,color=(255,255,255)):
        self.position = position
        self.speed = speed
        self.goingUp = goingUp
        self.tailLenght = tailLenght
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
        return tuple(newColor)
    def getPositions(self):
        if self.goingUp:
            return [self.position - k for k in range(self.tailLenght)]
        else:
            return [self.position + k for k in range(self.tailLenght)]
    def getColors(self):
        return [self.getColor(int(100-100*(k/(self.tailLenght-1)))) for k in range(self.tailLenght)]
    
class NuitEtoile():
    etoiles = []
    count = 0
    def __init__(self, strip, bounds, color = (255,255,255), speed = 1, tailLenght = 5, nbEtoile = 1, newEtoileDelay = 10, randomColor = False, randomTailLength = False):
        self.strip = strip
        self.bounds = bounds
        self.color = color
        self.speed = speed
        self.tailLenght = tailLenght
        self.nbEtoile = nbEtoile
        self.newEtoileDelay = newEtoileDelay
        self.randomColor = randomColor
        self.randomTailLength = randomTailLength
    def new_step(self):
        #cretion de nouveau flocons si nécaissaire
        if (self.count == self.newEtoileDelay):
            self.count = 0
            for i in range(self.nbEtoile):
                self.makeNewFlocon()
        else:
            self.count += 1
        #update des flocons
        
        for f in self.flocons:
            if f.update():
                self.flocons.remove(f)

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
            newEtoileColor = tuple([random.randint(0,255) for k in range(3)])
        else:
            newEtoileColor = self.color
        if self.randomTailLength:    
            newEtoileTailLength = random.randint(0,self.tailLenght)
        else:
            newEtoileTailLength = self.TailLength
        self.etoiles.append(EtoileFilante(position, self.speed, goingUp, self.bounds, newEtoileTailLength, newEtoileColor))
    
    
    