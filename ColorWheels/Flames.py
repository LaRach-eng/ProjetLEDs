from rpi_ws281x import *



palette=[[0,255,0], [255,100,0], [255,0,0], [255,255,0]]
differences=[]
for i in range(len(palette)):
    colorDifferences=[]
    for j in range(len(palette[i])):
        colorDifferences+=[palette[(1+i)%len(palette)][j]-palette[i][j]]
    differences+=[colorDifferences]
    
def wheel(pos):
    colors_size=255//len(palette)
    if pos < 62:
        return Color(palette[0][0]+int(pos*differences[0][0]/colors_size),palette[0][1]+int(pos*differences[0][1]/colors_size),palette[0][2]+int(pos*differences[0][2]/colors_size))
    elif pos < 124:
        pos -= 62
        return Color(palette[1][0]+int(pos*differences[1][0]/colors_size),palette[1][1]+int(pos*differences[1][1]/colors_size),palette[1][2]+int(pos*differences[1][2]/colors_size))
    elif pos < 186:
        pos -= 124
        return Color(palette[2][0]+int(pos*differences[2][0]/colors_size),palette[2][1]+int(pos*differences[2][1]/colors_size),palette[2][2]+int(pos*differences[2][2]/colors_size))
    elif pos<250:
        pos -= 186
        return Color(palette[3][0]+int(pos*differences[3][0]/colors_size),palette[3][1]+int(pos*differences[3][1]/colors_size),palette[3][2]+int(pos*differences[3][2]/colors_size))
    else:
        return Color(palette[3][0],palette[3][1],palette[3][0])
    
    
    
    
    