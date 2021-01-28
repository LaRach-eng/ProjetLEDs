# -*- coding: utf-8 -*-
"""
Created on Tue Jan 26 18:32:21 2021

@author: chere
"""


import math

class Wave():
    def __init__(self,strip, bounds, Wheel ,intensity = 1, goingUp = True, wavelength = 5, period = 10):
        self.strip = strip
        self.bounds = bounds
        self.Wheel = Wheel
        self.intensity = intensity
        self.goingUp = goingUp
        self.wavelength = wavelength
        self.period = period
        self.time = 0
    def new_step(self):
        if self.time < self.period:
            self.time +=1
        else:
            self.time = 0
        for i in range(self.bounds[0],self.bounds[1]):
            if self.goingUp:
                self.strip.setPixelColor(i,self.update_intensity(self.Wheel(int(255/2*(math.sin(2*math.pi*(self.time/self.period+i/self.wavelength))+1))),self.intensity))
            else:
                self.strip.setPixelColor(i,self.update_intensity(self.Wheel(int(255/2*(math.sin(2*math.pi*(self.time/self.period-i/self.wavelength))+1))),self.intensity))
    def update_intensity(self,color, intensity):
        b = int((color & 255)*intensity)
        g = int(((color >> 8) & 255)*intensity)
        r = int(((color >> 16) & 255)*intensity)
        return (r<<16) + (g<<8) + b
        