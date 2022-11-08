#! usr/bin/python3

from ctypes.wintypes import SIZE
from tkinter import CENTER
import pygame
import pygame_gui
import time
import numpy as np
import math

FILE_NAME = "/home/jaime/Desktop/UC3M/Planificacion/master-ipr/map11/map11.csv" #hardcoded mejor por inputs
START_X = 16
START_Y = 4
END_X = 10
END_Y = 4
SIZE_X = 28
SIZE_Y = 31
goalParentId = -1

class Node:
    def __init__(self, x, y, myId, parentId):
        self.x = x
        self.y = y
        self.myId = myId
        self.parentId = parentId
    def dump(self):
        print("---------- x "+str(self.x)+\
                         " | y "+str(self.y)+\
                         " | id "+str(self.myId)+\
                         " | parentId "+str(self.parentId))

def draw_square(x , y, value):
    # R if value=1, G if value=2, W if value=0, Y if value=3, B if value=4
    if value == '0':
        color = (255, 255, 255)
        colorint = (255, 255, 255, 100)
    elif value == '1':
        color = (255, 0, 0)
        colorint = (255, 0, 0, 100)
    elif value == '2':
        color = (0, 255, 0)
        colorint = (0, 255, 0, 100)
    elif value == '3':
        color = (255, 255, 0)
        colorint = (255, 255, 0, 100)
    elif value == '5': # camino
        color = (128, 64, 0)
        colorint = (128, 64, 0, 100)
    else:
        color = (0, 0, 255)
        colorint = (0, 0, 255, 100)
    rec_ext = pygame.draw.rect( window_surface,
                                color, 
                                pygame.Rect(x*window_surface.get_width()/(SIZE_X),
                                            y*window_surface.get_height()/(SIZE_Y),
                                            window_surface.get_width()/(SIZE_X),
                                            window_surface.get_height()/(SIZE_Y)),
                                2,
                                border_radius=12)
    rec_int = pygame.draw.rect( window_surface,
                                colorint, 
                                pygame.Rect(  x*window_surface.get_width()/(SIZE_X),
                                                        y*window_surface.get_height()/(SIZE_Y),
                                                        window_surface.get_width()/(SIZE_X)-10,
                                                        window_surface.get_height()/(SIZE_Y)-10),
                                border_radius=12)
    rec_int.center = rec_ext.center
    pygame.display.update(rec_ext)

def draw_board (charmap):
    for i in range(len(charMap)):
        map_x, map_y = index2map(i)
        draw_square(map_x, map_y, charmap[i])

def index2map(index):
    return(index%(SIZE_X), math.trunc(index/(SIZE_X)))

def map2index(x, y):
    return(SIZE_X * y + x)

def update_value(index, value):
    charMap[index] = value;

def setup(start, goal):
    i_start = map2index(start[0], start[1])
    update_value (i_start, 3)
    i_goal = map2index(goal[0], goal[1])
    update_value (i_goal, 4)

def nhood4(index):
    out = []
    if(index > SIZE_X * SIZE_Y -1):
        print("Evaluating nhood out of the map")
        return out
    if(index % SIZE_X > 0):
        out.append(index - 1)
    if(index % SIZE_X < SIZE_X - 1):
        out.append(index + 1)
    if(index>= SIZE_X):
        out.append(index -SIZE_X)
    if(index < SIZE_X * (SIZE_Y - 1)):
        out.append(index + SIZE_X)
    return out

def nhood8(index):
    out = nhood4(index)
    if(index > SIZE_X * SIZE_Y - 1):
        return out
    if(index % SIZE_X > 0 and index >= SIZE_X):
        out.append(index - 1 -SIZE_X)
    if(index % SIZE_X > 0 and index < SIZE_X * (SIZE_Y - 1)):
        out.append(index - 1 + SIZE_X)
    if(index % SIZE_X < SIZE_X -1 and index >= SIZE_X):
        out.append(index + 1 -SIZE_X)
    if(index % SIZE_X < SIZE_X - 1 and index < SIZE_X * (SIZE_Y - 1)):
        out.append(index + 1 + SIZE_X)
    return out

start = [START_X-1, START_Y-1]
goal = [END_X-1, END_Y-1]

##############################################
nodes = []
bfs = []
charMap = []

## creamos primer nodo

init = Node(start[0], start[1], 0, map2index(start[0],start[1]))
# init.dump()  # comprobar que primer nodo bien

## añadimos el primer nodo a `nodos`

nodes.append(init)
bfs.append(init)

with open(FILE_NAME) as f:
    line = f.readline()
    while line:
        charLine = line.strip().split(',')
        charMap.append(charLine)
        line = f.readline()

########################################################
charMap = np.concatenate(charMap)

setup(start, goal)

pygame.init()

pygame.display.set_caption('Quick Start')
window_surface = pygame.display.set_mode((800, 800))

background = pygame.Surface((800, 800))
background.fill(pygame.Color('#000000'))
                                

clock = pygame.time.Clock()
is_running = True
done = False
visited_flag = np.zeros(SIZE_X * SIZE_Y)

draw_board(charMap)

input('Press Enter to start')
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            is_running = False

    idx = bfs[0]
    index = map2index(idx.x, idx.y)
    bfs.pop(0)

    for n in nhood8(index):
        if (not visited_flag[n]):
            if(charMap[n] == '0'):
                visited_flag[n] = True
                x_tmp, y_tmp = index2map(n)
                node_tmp = Node(x_tmp, y_tmp, n, index)
                bfs.append(node_tmp)
                nodes.append(node_tmp)
                update_value(n, 2)
                draw_square(x_tmp, y_tmp, charMap[n])
                time.sleep(0.05)
            elif (charMap[n] == '4'):
                done = True
                node_tmp = Node(x_tmp, y_tmp, goalParentId, index)
                nodes.append(node_tmp)
                print("Golaso mi nino oleoleole")

input("Press Enter to find the path")
print("%%%%%%%%%%%%%%%%%%%")
ok = False
while not ok:
    for node in nodes:
        if( node.myId == goalParentId):
            update_value(map2index(node.x, node.y), 5)
            draw_square(node.x, node.y, charMap[map2index(node.x, node.y)])
            time.sleep(0.05)
            node.dump()
            goalParentId = node.parentId
            if( goalParentId == -2):
                print("%%%%%%%%%%%%%%%%%2")
                ok = True
input("Press Enter to close")
    


