from rpi_ws281x import *



palette= [[70,130,255], [17,35,80], [34,70,150], [80,100,255], [30,40,80], [0, 0, 200]]
differences=[]
for i in range(len(palette)):
    colorDifferences=[]
    for j in range(len(palette[i])):
        colorDifferences+=[palette[(1+i)%len(palette)][j]-palette[i][j]]
    differences+=[colorDifferences]
    
def wheel(pos):
    colors_size=255//len(palette)
    if pos < 42:
        return Color(palette[0][0]+int(pos*differences[0][0]/colors_size),palette[0][1]+int(pos*differences[0][1]/colors_size),palette[0][2]+int(pos*differences[0][2]/colors_size))
    elif pos < 84:
        pos -= 42
        return Color(palette[1][0]+int(pos*differences[1][0]/colors_size),palette[1][1]+int(pos*differences[1][1]/colors_size),palette[1][2]+int(pos*differences[1][2]/colors_size))
    elif pos < 126:
        pos -= 84
        return Color(palette[2][0]+int(pos*differences[2][0]/colors_size),palette[2][1]+int(pos*differences[2][1]/colors_size),palette[2][2]+int(pos*differences[2][2]/colors_size))
    elif pos < 168:
        pos -= 126
        return Color(palette[3][0]+int(pos*differences[3][0]/colors_size),palette[3][1]+int(pos*differences[3][1]/colors_size),palette[3][2]+int(pos*differences[3][2]/colors_size))
    elif pos < 210:
        pos -= 168
        return Color(palette[4][0]+int(pos*differences[4][0]/colors_size),palette[4][1]+int(pos*differences[4][1]/colors_size),palette[4][2]+int(pos*differences[4][2]/colors_size))
    else:
        pos -= 210
        return Color(palette[5][0]+int(pos*differences[5][0]/colors_size),palette[5][1]+int(pos*differences[5][1]/colors_size),palette[5][2]+int(pos*differences[5][2]/colors_size))
       
    