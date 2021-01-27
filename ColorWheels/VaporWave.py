from rpi_ws281x import *



palette=[[255,113,206], [1,205,254], [5,255,161], [185,103,255], [255,251,150]]
differences=[]
for i in range(len(palette)):
    colorDifferences=[]
    for j in range(len(palette[i])):
        colorDifferences+=[palette[(1+i)%len(palette)][j]-palette[i][j]]
    differences+=[colorDifferences]
    
def wheel(pos):
    colors_size=255//len(palette)
    if pos < 51:
        return Color(palette[0][0]+int(pos*differences[0][0]/colors_size),palette[0][1]+int(pos*differences[0][1]/colors_size),palette[0][2]+int(pos*differences[0][2]/colors_size))
    elif pos < 102:
        pos -= 51
        return Color(palette[1][0]+int(pos*differences[1][0]/colors_size),palette[1][1]+int(pos*differences[1][1]/colors_size),palette[1][2]+int(pos*differences[1][2]/colors_size))
    elif pos < 153:
        pos -= 102
        return Color(palette[2][0]+int(pos*differences[2][0]/colors_size),palette[2][1]+int(pos*differences[2][1]/colors_size),palette[2][2]+int(pos*differences[2][2]/colors_size))
    elif pos < 204:
        pos -= 153
        return Color(palette[3][0]+int(pos*differences[3][0]/colors_size),palette[3][1]+int(pos*differences[3][1]/colors_size),palette[3][2]+int(pos*differences[3][2]/colors_size))
    else:
        pos -= 204
        return Color(palette[4][0]+int(pos*differences[4][0]/colors_size),palette[4][1]+int(pos*differences[4][1]/colors_size),palette[4][2]+int(pos*differences[4][2]/colors_size))
    
    
    
    
    
    
    