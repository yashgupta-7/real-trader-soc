import matplotlib.pyplot as plt


def NicePixel(pix):
    if pix[0] < 0.363 and pix[0] > 0.359 and pix[1] < 0.378 and pix[1] > 0.374 and pix[2] < 0.44 and pix[2] > 0.40:
        return True
    else:
        return False

def Degree(pix):
    return ((pix[0]-0.361)**2)+((pix[1]-0.376)**2)+((pix[2]-0.42)**2)

def ConvertHeightToAmount(height):
    global offset
    global offsetpix
    global secondoffset
    global secondoffsetpix
    
    return (((offsetpix-float(height))*(secondoffset-offset))/(offsetpix-secondoffsetpix))+offset

num = input('Number of images?')
L = []
for i in range(0,int(num)):
    X = plt.imread(str(i+1)+'.png')
    print('Currently Processing for '+ str(i+1)+'.png')
    start = int(input('What will be the right start input?'))
    starth = int(input('What will be the height of initial start input ?'))
    
    offset = float(input('What is the minimum value of price shown?'))
    offsetpix = float(input('What is its pixel height?'))
    secondoffset = float(input('What is the minimum value of second price shown?'))
    secondoffsetpix = float(input('What is second pixel height?'))
    i = start
    j = starth
    ThisList = []
    while i >=7:
        ThisList.append(ConvertHeightToAmount(j))
        if Degree(X[j][i-1]) < Degree(X[j-1][i-1]) and Degree(X[j][i-1]) < Degree(X[j+1][i-1]):
            i-=1
        elif Degree(X[j-1][i-1]) < Degree(X[j][i-1]) and Degree(X[j-1][i-1]) < Degree(X[j+1][i-1]):
            i-=1
            j-=1
        else:
            i-=1
            j+=1
    L+=reversed(ThisList)

import numpy as np

nam = input('Name of file?')
with open(nam+'.png','wb') as f:
    np.save(f,np.array(L))
