import pygame

from pygame.locals import *
from pygame.rect import *
import sys
from variables import *
from  move_body import *

def set_body(display):
    for pos in snack_body:
        pygame.draw.rect(display, BLACK, (pos[0] - 1, pos[1] - 1, SIZE_RECT + 2, SIZE_RECT + 2))
        pygame.draw.rect(display, RED, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))

def	effect_move(action):
	if action == pygame.K_UP and LAST_ACTION != pygame.K_DOWN:
		print("before 0 ", snack_body)
		up_act()
	if action == pygame.K_DOWN and LAST_ACTION != pygame.K_UP:
		down_act()
	if action == pygame.K_RIGHT and LAST_ACTION != pygame.K_LEFT:
		print("right")
		right_act()
	if action == pygame.K_LEFT and LAST_ACTION != pygame.K_RIGHT:
		print("left")
		left_act()
	set_body(display)

display = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption('Game')
display.fill(WHITE)
x = 0
y = 0
set_body(display)
while True:
	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN and event.key in MOVE_KEY:
			display.fill(WHITE)
			effect_move(event.key)

		pygame.display.update()

