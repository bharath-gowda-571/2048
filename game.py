import pygame
import random
from copy import deepcopy
import time
import os


os.chdir("resources")
pygame.init()

# Global Variables
screen=pygame.display.set_mode((400,400))
pygame.display.set_caption("2048")
background_colour=(242, 190, 107)
colour={2:pygame.image.load("2.png"),
        4:pygame.image.load("4.png"),
        8:pygame.image.load("8.png"),
        16:pygame.image.load("16.png"),
        32:pygame.image.load("32.png"),
        64:pygame.image.load("64.png"),
        128:pygame.image.load("128.png"),
        256:pygame.image.load("256.png"),
        512:pygame.image.load("512.png"),
        1024:pygame.image.load("1024.png"),
        2048:pygame.image.load("2048.png")}
beginning_image=pygame.image.load("beginning_image.png")
logo=pygame.image.load("logo.png")
pygame.display.set_icon(logo)
won=False
lost=False

# GRID list
Font_big=pygame.font.Font("freesansbold.ttf",50)
font_small=pygame.font.Font("freesansbold.ttf",15)
reset_text=font_small.render('Press "R" to restart the game',1,(0,0,0))

lis=[[0,0,0,0],
     [0,0,0,0],
     [0,0,0,0],
     [0,0,0,0]]


def show_screen():
    global background_colour
    global screen
    screen.fill(background_colour)

def draw_grid():
    global screen
    for i in range(100,400,100):
        pygame.draw.line(screen,(158, 156, 153),(i,0),(i,400),5)
    for j in range(100,400,100):
        pygame.draw.line(screen,(158, 156, 153),(0,j),(400,j),5)

# Spawing 2's
def spawn_2():
    try:
        empty_slots=[(i,j)for i in range(4) for j in range(4) if not lis[i][j]]
        spawn_place=random.choice(empty_slots)
        lis[spawn_place[0]][spawn_place[1]]=2
    except:
        pass
def check_lost():
    for i in range(4):
        if 0 in lis[i]:
            return False
    for x in range(3):
        for y in range(3):
            if lis[x][y]==lis[x][y+1] or lis[x][y]==lis[x+1][y]:
                return False
    for j in range(3):
        if lis[3][j]==lis[3][j+1]:
            return False
        if lis[j][3]==lis[j+1][3]:
            return False
    return True

def check_win():
    for i in range(4):
        if 2048 in lis[i]:
            return True

def push_left():
    global lis,won,lost
    lis_copy=deepcopy(lis)
    for i in range(4):
        zero_count=0
        for j in range(4):
            if lis[i][j]==0:
                zero_count+=1
        for _ in range(zero_count):
            lis[i].remove(0)
            lis[i].append(0)
    for x in range(4):
        for y in range(3):
            if lis[x][y]==lis[x][y+1]:
                lis[x][y]*=2
                lis[x].pop(y+1)
                lis[x].append(0)
    if lis_copy!=lis:
        spawn_2()
        won=check_win()
        lost=check_lost()

def push_right():
    global lis,won,lost
    lis_copy = deepcopy(lis)
    for i in range(4):
        zero_count=0
        for j in range(4):
            if lis[i][j]==0:
                zero_count+=1
        for _ in range(zero_count):
            lis[i].remove(0)
        for _ in range(zero_count):
            lis[i].insert(0,0)
    for x in range(4):
        for y in range(3,0,-1):
            if lis[x][y]==lis[x][y-1]:
                lis[x][y]*=2
                lis[x].pop(y-1)
                lis[x].insert(0,0)
    if lis_copy != lis:
        spawn_2()
        won=check_win()
        lost=check_lost()

def push_down():
    global lis,won,lost
    lis_vert = list(map(list, zip(*lis)))
    lis_copy = deepcopy(lis)
    for i in range(4):
        zero_count=0
        for j in range(4):
            if lis_vert[i][j]==0:
                zero_count+=1
        for _ in range(zero_count):
            lis_vert[i].remove(0)
        for _ in range(zero_count):
            lis_vert[i].insert(0,0)
    for x in range(4):
        for y in range(3,0,-1):
            if lis_vert[x][y]==lis_vert[x][y-1]:
                lis_vert[x][y]*=2
                lis_vert[x].pop(y-1)
                lis_vert[x].insert(0,0)
    lis=list(map(list,zip(*lis_vert)))
    if lis_copy != lis:
        spawn_2()
        won=check_win()
        lost=check_lost()

def push_up():
    global lis,won,lost
    lis_vert = list(map(list, zip(*lis)))
    lis_copy = deepcopy(lis)
    for i in range(4):
        zero_count = 0
        for j in range(4):
            if lis_vert[i][j] == 0:
                zero_count += 1
        for _ in range(zero_count):
            lis_vert[i].remove(0)
            lis_vert[i].append(0)
    for x in range(4):
        for y in range(3):
            if lis_vert[x][y] == lis_vert[x][y + 1]:
                lis_vert[x][y] *= 2
                lis_vert[x].pop(y + 1)
                lis_vert[x].append(0)
    lis = list(map(list, zip(*lis_vert)))
    if lis_copy != lis:
        spawn_2()
        won=check_win()
        lost=check_lost()


def map_values_on_to_board():
    global screen
    for i in range(4):
        for j in range(4):
            if lis[i][j]==0:
                continue
            screen.blit(colour[lis[i][j]],(j*100+2,i*100+2))


if __name__=="__main__":
    run=True
    screen.blit(beginning_image,(150,70))
    loading_text=font_small.render("Loading...",1,(255,255,255))
    beginning_text=font_small.render("Use Arrow Keys to play the game.",1,(255,255,255))
    screen.blit(loading_text,(170,200))
    screen.blit(beginning_text,(85,350))
    pygame.display.update()
    time.sleep(1)
    spawn_2()
    spawn_2()
    while run:
        show_screen()
        if not(won or lost):
            draw_grid()
            map_values_on_to_board()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                run = False
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_DOWN:
                    push_down()
                if event.key==pygame.K_LEFT:
                    push_left()
                if event.key==pygame.K_UP:
                    push_up()
                if event.key==pygame.K_RIGHT:
                    push_right()
                if event.key==pygame.K_r:
                    lost=False
                    won=False
                    lis=[[0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0],
                         [0,0,0,0]]
                    spawn_2()
                    spawn_2()

        if won:
            won_text=Font_big.render("YOU WON!!",1,(0,0,0))
            screen.blit(won_text,(65,100))
            screen.blit(reset_text,(100,200))
        if lost:
            lost_text=Font_big.render("YOU LOST!!",1,(0,0,0))
            screen.blit(lost_text,(60,100))
            screen.blit(reset_text,(100,200))
        pygame.display.update()
    pygame.display.quit()