from tkinter import *
import time
import random as rd

# from rpi_ws281x import *
import argparse
#import numpy as np
import random
import math

import Codes.MontagneRusse as MontagneRusse
import Codes.wave as wave
import Codes.MixingCanvas as MixingCanvas

import ColorWheels.VaporWave as VaporWave
import ColorWheels.defaultWheel as defaultWheel

# LED strip configuration:
LED_COUNT = 300  # Number of LED pixels.
LED_PIN = 18  # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ = 800000  # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10  # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255  # Set to 0 for darkest and 255 for brightest
LED_INVERT = False  # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0  # set to '1' for GPIOs 13, 19, 41, 45 or 53

RADIUS_LED = 2
DIST_LED = 10
OFFSET_DRAWING_X = 500
OFFSET_DRAWING_Y = -80

x = 12  # Number of LEDs in a unit distance
a = list(range(5 * x))
b_0 = list(range(a[-1] + 1, a[-1] + 1 + 4 * x))
b_1 = list(range(b_0[-1] + 1, b_0[-1] + 1 + 4 * x))
c_0 = list(range(b_1[-1] + 1, b_1[-1] + 1 + 3 * x))
c_1 = list(range(c_0[-1] + 1, c_0[-1] + 1 + 3 * x))
d_0 = list(range(c_1[-1] + 1, c_1[-1] + 1 + 2 * x))
d_1 = list(range(d_0[-1] + 1, d_0[-1] + 1 + 2 * x))
e_0 = list(range(d_1[-1] + 1, d_1[-1] + 1 + x))
e_1 = list(range(e_0[-1] + 1, e_0[-1] + 1 + x))

vertical_indices = a + b_1 + c_1 + d_1 + e_1
horizontal_indices = b_0 + c_0 + d_0 + e_0
all_indices = list(range(LED_COUNT))

all_segments = [a, b_0, b_1, c_0, c_1, d_0, d_1, e_0, e_1]

verticalUp = [(0,a[-1]),(c_1[0],c_1[-1]),(e_1[0],e_1[-1])]
horizontalUp = [(b_0[0],b_0[-1]),(d_0[0],d_0[-1])]
verticalDown = [(b_1[0],b_1[-1]),(d_1[0],d_1[-1])]
horizontalDown = [(c_0[0],c_0[-1]),(e_0[0],e_0[-1])]
def Color(r, g, b):
    return (r<< 16) + (g<<8) + b

RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)
WHITE = Color(255, 255, 255)
YELLOW = Color(255, 200, 0)

positions = []
pixels = []

master = Tk()
canvas_width = 1500
canvas_height = 800
master.title("LEDs p'tite coloc")
# master.attributes("-fullscreen", True)
w = Canvas(master, width=canvas_width - 50, height=canvas_height - 50)


def paint(x, y, r, g, b):
    colorval = "#%02x%02x%02x" % (r, g, b)
    x1, y1 = (x - RADIUS_LED), (y - RADIUS_LED)
    x2, y2 = (x + RADIUS_LED), (y + RADIUS_LED)
    pixel = w.create_oval(x1, y1, x2, y2, fill=colorval, outline=colorval)
    pixels.append(pixel)


def repaint(i, r, g, b):
    colorval = "#%02x%02x%02x" % (r, g, b)
    pixel = pixels[i]
    w.itemconfig(pixel, fill=colorval, outline=colorval)
    x = positions[i][0]
    y = positions[i][1]
    if r == 0 and g == 0 and b == 0:
        x1, y1 = (x), (y)
        x2, y2 = (x), (y)
    else:
        x1, y1 = (x - 3), (y - 3)
        x2, y2 = (x + 3), (y + 3)
    w.coords(pixel, x1, y1, x2, y2)


class Strip:
    def __init__(self):
        return

    def begin(self):
        print("Lets start !")

    def numPixels(self):
        return LED_COUNT

    def setPixelColor(self, pixel, color):
        c = color
        if isinstance(color, int):
            c = [(color>>16)&255, (color>>8)&255, color&255]
        repaint(pixel, c[0], c[1], c[2])

    def show(self):
        w.update()

    def set_color_list(self, pixel_list, color):
        for pixel in pixel_list:
            self.setPixelColor(pixel, color)


def initialize():
    w.configure(background="black")
    last = [OFFSET_DRAWING_X, canvas_height + OFFSET_DRAWING_Y]
    for i in range(len(a)):
        newx, newy = last[0], last[1] - DIST_LED
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][1] -= DIST_LED
    for i in range(len(b_0)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] + DIST_LED, last[1] - DIST_LED
        else:
            newx, newy = last[0] + DIST_LED, last[1]
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][0] += DIST_LED
    for i in range(len(b_1)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] + DIST_LED, last[1] + DIST_LED
        else:
            newx, newy = last[0], last[1] + DIST_LED
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][1] += DIST_LED
    for i in range(len(c_0)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] - DIST_LED, last[1] + DIST_LED
        else:
            newx, newy = last[0] - DIST_LED, last[1]
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][0] -= DIST_LED
    for i in range(len(c_1)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] - DIST_LED, last[1] - DIST_LED
        else:
            newx, newy = last[0], last[1] - DIST_LED
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][1] -= DIST_LED
    for i in range(len(d_0)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] + DIST_LED, last[1] - DIST_LED
        else:
            newx, newy = last[0] + DIST_LED, last[1]
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][0] += DIST_LED
    for i in range(len(d_1)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] + DIST_LED, last[1] + DIST_LED
        else:
            newx, newy = last[0], last[1] + DIST_LED
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][1] += DIST_LED
    for i in range(len(e_0)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] - DIST_LED, last[1] + DIST_LED
        else:
            newx, newy = last[0] - DIST_LED, last[1]
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)
    # positions[-1][0] -= DIST_LED
    for i in range(len(e_1)):
        if i == 0:  # for the right angle representation
            newx, newy = last[0] - DIST_LED, last[1] - DIST_LED
        else:
            newx, newy = last[0], last[1] - DIST_LED
        paint(newx, newy, 255, 255, 255)
        last = [newx, newy]
        positions.append(last)

###

rgbPalette = [(255,0,0), (255,255,0), (0,255,0), (0,255,255), (0,0,255), (255,0,255)]
redtopurplePalette = [(255,0,0), (255,0,150), (80,150,255)]
vaporWavePalette = [(255,113,206), (1,205,254), (5,255,161), (185,103,255), (255,251,150)]
neonPalette = [(254,0,0), (253,254,2), (11,255,1), (1,30,254), (254,0,246)]
flamesPalette = [[0,255,0], [255,100,0], [255,0,0], [255,255,0]]
jamaRedPalette = [[255,0,0], [255,100,0], [255,0,0], [255,100,0]]
autumnPalette = [[244,134,0], [255,165,0], [255,153,102], [235,99,98], [238,59,57]]
africaPalette = [(20,253,83), (28,255,238), (253,26,243), (255,184,15), (253,8,8)]
seaPalette = [(70,130,255), (17,35,80), (34,70,150), (80,100,255), (30,40,80), (0, 0, 200)]
mirrorEdgePalette = [(253,17,17), (255,92,4), (251,232,22), (75,246,36), (13,52,193)]

def colorWipe(strip, color=Color(255,0,0), wait_ms=10):
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms/1000)
        
def wheelPalette(state, palette):
    return Color(palette[state][0], palette[state][1], palette[state][2])
        
def colorEdge(strip, seq, color = Color(0, 255, 0)):
    for pos in seq:
        strip.setPixelColor(pos, color)
    
def cleanEdge(strip, seq):
    for pos in seq:
        strip.setPixelColor(pos, 0)
       
def soiree(strip, palette = neonPalette, numSeq = 3, freq = 2, tmax=100):
    segs = all_segments
    wait_s=1/freq
    N = [random.randint(0, len(segs)-1) for i in range(numSeq)]
    t=0
    while t<tmax:
        states = [random.randint(0, len(palette)-1) for i in range(numSeq)]
        
        for i in range(len(N)):
            colorEdge(strip, seq = segs[N[i]], color = wheelPalette(states[i], palette))
        strip.show()
        time.sleep(wait_s)
        for i in range(len(N)):
            cleanEdge(strip, seq = segs[N[i]])
        strip.show()
        
        N2 = [random.randint(0, len(segs)-1) for i in range(numSeq)]
        for i in range(len(N2)):
            A = N2[:i] + N2[i+1:]
            while (N2[i] in N) or (N2[i] in A):
                N2[i] = random.randint(0, len(segs)-1)
        t+=1
        N = N2
            
            
###

# Create NeoPixel object with appropriate configuration.
# strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip = Strip()

can = MixingCanvas.MixingCanvas(strip,(a[0],e_1[-1]))

boost = []
for b in verticalUp:
    boost.append(wave.Wave(can,b,defaultWheel.wheel, intensity = 0.2,goingUp = True, period = 10, wavelength = 10))
for b in verticalDown:
    boost.append(wave.Wave(can,b,defaultWheel.wheel, intensity = 0.2,goingUp = False, period = 10, wavelength = 10))

circuit = MontagneRusse.Rails(can,(a[0],e_1[-1]),verticalUp,verticalDown,goingUp = False, randomColor = True, initialSpeed = 1,minSpeed = 0, g = 0.2)


def run():
    print("Au niveau du nice..")
    #### ENTRER LE NOM DE LA FONCTION CI-DESSOUS
    while True:
        for v in boost:
            v.new_step()
        circuit.new_step()
        can.printPixels()
        strip.show()
        time.sleep(0.05)
    print("Program ended")


w.pack(expand=YES, fill=BOTH)

b = Button(master, bg="white", fg="black", text="Run", command=run)
b.pack(expand=YES, fill=BOTH)

initialize()


mainloop()
