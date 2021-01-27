# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 18:24:43 2021

@author: chere
"""

class MixingCanvas():
    def __init__(self,strip,bounds):
        self.strip = strip
        self.bounds = bounds
        self.dic = {}
    def setPixelColor(self, pixel, color):
        if pixel in self.dic.keys():
            self.dic[pixel].append(color)
        else:
            self.dic[pixel]=[color]
    def mergeColors(self,Colors):
        r,g,b = 0,0,0
        for k in Colors:
            r += ((k>>16) & 255)
            g += ((k>>8) & 255)
            b += (k & 255)
        r = int(r/len(Colors))
        g = int(g/len(Colors))
        b = int(b/len(Colors))
        return (r<<16) + (g<<8) + b
    def printPixels(self):
        for pixel,colors in self.dic.items():
            self.strip.setPixelColor(pixel,self.mergeColors(colors))
        self.dic = {}