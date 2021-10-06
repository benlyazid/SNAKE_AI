import pygame
#	ENV_VARIABLES

snack_body = [[300, 300], [320, 300], [340, 300], [360, 300]]

RED = (255, 0, 0)
BLACK = (0, 0, 0)	
GREEN = (0,128,0)
RED_HEAD = (128,0,0)
WHITE = (255, 255, 255)
GRIS = (156, 156, 156, 0)

SIZE_RECT = 20
MOVE_SIZE = 20

SCREEN_SIZE = (800, 800)

LAST_ACTION = pygame.K_RIGHT
LAST_PRESSED = pygame.K_RIGHT

MOVE_KEY = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]


TARGET = [0, 0]
SHOULD_POP = [False]

SCORE = 0

#	BRAIN_ENV

memSize = 60000
batchSize = 32
learningRate = 0.0001
gamma = 0.9
nLastStates = 1 # 4 ??
epsilon = 1.
epsilonDecayRate = 0.0002
minEpsilon = 0.05
filepathToSave = './model_snack.h5'