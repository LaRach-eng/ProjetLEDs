from tkinter import *
from win32api import GetSystemMetrics
import time
#from rpi_ws281x import *
import argparse
import time
import numpy as np
import random
import math


from neige import Neige
from EtoileFilantes import NuitEtoile

# LED strip configuration:
LED_COUNT      = 300      # Number of LED pixels.
LED_PIN        = 18      # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10      # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0       # set to '1' for GPIOs 13, 19, 41, 45 or 53
Seq1 = [i for i in range(76)]
Seq2 = [i for i in range(76,214)]
Seq3 = [i for i in range(214, 300)]
lseq = [Seq1, Seq2, Seq3]

positions = []
pixels = []

master = Tk()
print(GetSystemMetrics(0))
print(GetSystemMetrics(1))
canvas_width = 910
canvas_height = 510
master.title("LEDs Bill Bocal")
# master.attributes("-fullscreen", True)
w = Canvas(master,
           width=canvas_width-50,
           height=canvas_height-50)

def paint(x, y, r, g, b):
    colorval = "#%02x%02x%02x" % (r, g, b)
    x1, y1 = (x - 2), (y - 2)
    x2, y2 = (x + 2), (y + 2)
    pixel = w.create_oval(x1, y1, x2, y2, fill=colorval, outline=colorval)
    pixels.append(pixel)
    
def repaint(i, r, g, b):
    colorval = "#%02x%02x%02x" % (r, g, b)
    pixel = pixels[i]
    w.itemconfig(pixel, fill=colorval, outline=colorval)
    x = positions[i][0]
    y = positions[i][1]
    if r==0 and g==0 and b==0:
        x1, y1 = (x), (y)
        x2, y2 = (x), (y)
    else:
        x1, y1 = (x - 3), (y - 3)
        x2, y2 = (x + 3), (y + 3)
    w.coords(pixel, x1, y1, x2, y2 )
    
def Color(r,g,b):
    return (r,g,b)
    
class Strip:
  def __init__(self):
      return
  def begin(self):
      print('Lets start !')
  def numPixels(self):
      return LED_COUNT
  def setPixelColor(self, pixel, color):
      c = color
      # print(type(color))
      if isinstance(color,int):
          c = [color, color, color]
      repaint(pixel, c[0], c[1], c[2])
  def show(self):
      w.update()
    
montagnerus
def initialize():
    w.configure(background='black')
    last = [50, canvas_height-100]
    for yi in Seq1:
        newx, newy = last[0], last[1]-4.5
        paint(newx, newy, 10, 10, 10)
        last = [newx, newy]
        positions.append(last)
    for yi in Seq2:
        newx, newy = last[0]+5.5, last[1]
        paint(newx, newy, 10, 10, 10)
        last = [newx, newy]
        positions.append(last)
    for yi in Seq3:
        newx, newy = last[0], last[1]+4.5
        paint(newx, newy, 10, 10, 10)
        last = [newx, newy]
        positions.append(last)



################################### COLLER LE CODE CI-DESSOUS ####################################################

def colorWipe(strip, color=Color(255,0,0), wait_ms=10):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)
        
      
        
def Scenario():
    #appeller les méthodes new_step
    nuitEtoile.new_step()
    neigeStatique.new_step()
    neigeTombante1.new_step()
    neigeTombante2.new_step()
    #show pour afficher le resultat
    strip.show()
    
        

####################################### FIN DU CODE ##############################################

# Create NeoPixel object with appropriate configuration.
#strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip = Strip()

#-----------Initialisation des classes---------------------------
neigeStatique = Neige(strip,[76,213], (255,255,255),3,3,50,randomColor = False, falling = False, spawnProb = 1)
neigeTombante1 = Neige(strip, [0,75], (255,255,255),3,1,115,randomColor = False,falling = True, posFallDir = False, spawnProb = 0.5)
neigeTombante2 = Neige(strip, [214,299], (255,255,255),3,1,115,randomColor = False,falling = True, posFallDir = True, spawnProb = 0.5)  
nuitEtoile = NuitEtoile(strip, [76,214], color = Color(255,255,255), speed = 5,  tailLenght = 15, nbEtoile = 1, newEtoileDelay = 10, randomColor = True, randomTailLength = True, randomBounds = True)


def run():
    print('Au niveau du nice..')
    # for i in range(100):
       
        
    
    while True:
        #### ENTRER LE NOM DE LA FONCTION CI-DESSOUS
        Scenario()
        time.sleep(0.001)
    print('Program ended')

w.pack(expand=YES, fill=BOTH)

b = Button(master, bg="white", fg="black", text="Run", command=run)
b.pack(expand=YES, fill=BOTH)

initialize()


mainloop()











