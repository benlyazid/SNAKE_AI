import pygame
import numpy as np

#	ENV_VARIABLES

snack_body = [[0, 100], [20, 100], [40, 100], [60, 100]]

RED = (255, 0, 0)
BLACK = (0, 0, 0)	
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255, 255, 255)
GRIS = (156, 156, 156, 0)

SIZE_RECT = 20

SCREEN_SIZE = (200, 200)

LAST_ACTION = pygame.K_RIGHT
LAST_PRESSED = pygame.K_RIGHT

MOVE_KEY = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]


TARGET = [0, 0]
SHOULD_POP = [True]

SCORE = 0

#BRAIN_ENV
memSize = 60000
batchSize = 32
learningRate = 0.005
gamma = 0
epsilon = 1
epsilonDecayRate = 0.0002
minEpsilon = 0.0005
filepathToSave = './model_snack.h5'


