from rpi_ws281x import *



palette=[[255,0,0], [255,0,150], [80,150,255]]
differences=[]
for i in range(len(palette)):
    colorDifferences=[]
    for j in range(len(palette[i])):
        colorDifferences+=[palette[(1+i)%len(palette)][j]-palette[i][j]]
    differences+=[colorDifferences]
    
def wheel(pos):
    colors_size=255//len(palette)
    if pos < 85:
        return Color(palette[0][0]+int(pos*differences[0][0]/colors_size),palette[0][1]+int(pos*differences[0][1]/colors_size),palette[0][2]+int(pos*differences[0][2]/colors_size))
    elif pos < 170:
        pos -= 85
        return Color(palette[1][0]+int(pos*differences[1][0]/colors_size),palette[1][1]+int(pos*differences[1][1]/colors_size),palette[1][2]+int(pos*differences[1][2]/colors_size))
    else:
        pos -= 170
        return Color(palette[2][0]+int(pos*differences[2][0]/colors_size),palette[2][1]+int(pos*differences[2][1]/colors_size),palette[2][2]+int(pos*differences[2][2]/colors_size))

      