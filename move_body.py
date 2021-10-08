from variables import *
import variables
import pygame
from pygame.locals import *
from pygame.rect import *
import sys

def up_act():
    global LAST_ACTION
    head = variables.snack_body[-1]
    variables.snack_body.append([head[0], head[1] - SIZE_RECT])
    if variables.SHOULD_POP[0] == True:
        variables.snack_body.pop(0)
    variables.SHOULD_POP[0] = True 
    variables.LAST_ACTION = pygame.K_UP


def down_act():
    head = variables.snack_body[-1]
    variables.snack_body.append([head[0], head[1] + SIZE_RECT])
    if variables.SHOULD_POP[0] == True:
        variables.snack_body.pop(0)
    variables.SHOULD_POP[0] = True 
    variables.LAST_ACTION = pygame.K_DOWN

def left_act():
    head = variables.snack_body[-1]
    variables.snack_body.append([head[0] - SIZE_RECT, head[1]])
    if variables.SHOULD_POP[0] == True:
        variables.snack_body.pop(0)
    variables.SHOULD_POP[0] = True 
    variables.LAST_ACTION = pygame.K_LEFT

def right_act():
    head = variables.snack_body[-1]
    variables.snack_body.append([head[0] + SIZE_RECT, head[1]])
    if variables.SHOULD_POP[0] == True:
        variables.snack_body.pop(0)
    variables.SHOULD_POP[0] = True 
    variables.LAST_ACTION = pygame.K_RIGHT
    

def updae_body():
    if variables.LAST_ACTION == pygame.K_UP:
        up_act()
    if variables.LAST_ACTION == pygame.K_DOWN:
       down_act()
    if variables.LAST_ACTION == pygame.K_RIGHT:
        right_act()
    if variables.LAST_ACTION == pygame.K_LEFT:
        left_act()

