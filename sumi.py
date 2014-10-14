#-*- coding: utf-8 -*-

import numpy as np
import random
import matplotlib.pyplot as plt
import  matplotlib.animation as animation
import pymc as mc

###########################################################################
x_center=25
y_center=25

width=x_center*2
height=y_center*2

end_time=70

probability=0.1

sight_factor=0.25

first_sumi_range=3
eps=1e-5

############################################################################

def moved_sumi(quantity):
    res=np.zeros((height,width,2))
    dx=[1,0,-1,0,0]
    dy=[0,1,0,-1,0]
    for y in np.arange(height):
        for x in np.arange(width):
            res[y][x][0]-=quantity[y][x][0]
            for k in range(5):
                xk=x+dx[k]
                yk=y+dy[k]
                if xk<0 or xk>=width or yk<0 or yk>=height:
                    continue
                if quantity[y][x][0]<eps:
                    continue
                if random.random()<probability:
                    res[yk][xk][1]+=quantity[y][x][0]/5.0
                else:
                    res[yk][xk][0]+=quantity[y][x][0]/5.0
    return res


def show(quantity):
    for y in np.arange(height):
        for x in np.arange(width):
            print "%.4f" % (quantity[y][x][0]+quantity[y][x][1]), ' ',
        print ''
    print ''
    return


if __name__=='__main__':
    quantity=np.zeros((height,width,2))
    for i in range(first_sumi_range):
        for j in range(first_sumi_range):
            quantity[y_center+i][x_center+j][0]=100.0
    ims=[]
    fig=plt.figure()
    X,Y = np.meshgrid(np.arange(width),np.arange(height))
    for t in np.arange(end_time):
        quantity+=moved_sumi(quantity)
        #show(quantity)
        res=np.zeros((height,width))
        for y in np.arange(height):
            for x in np.arange(width):
                res[y][x]=-(quantity[y][x][0]+quantity[y][x][1])**sight_factor
        im=plt.pcolor(X,Y,res)
        plt.gray()
        ims.append([plt.pcolor(X,Y,res)])
    ani=animation.ArtistAnimation(fig,ims,interval=300,blit=True,repeat_delay=1000)
    plt.show()
    #ani.save('sumi_diffusion.gif',writer='imagemagick',fps=4);

