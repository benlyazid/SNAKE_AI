import pygame
from pygame.locals import *
from pygame.rect import *
import sys
from  move_body import *
from variables import *
import variables
import time
import random

def Game_still_running():
	head = variables.snack_body[-1]
	if head[0] < 0 or head[0] > SCREEN_SIZE[0]:
		return 0
	if head[1] < 0 or head[1] > SCREEN_SIZE[1]:
		return 0
	if snack_body.count(snack_body[0]) != 1:
		return 0
	return 1

def	generate_point(display):
	variables.TARGET[0] = random.randint(0, (SCREEN_SIZE[0] - 20) / 20) * 20
	variables.TARGET[1] = random.randint(0, (SCREEN_SIZE[1] - 20) / 20) * 20

def	draw_point():
	pygame.draw.rect(display, GREEN, (variables.TARGET[0], variables.TARGET[1], SIZE_RECT, SIZE_RECT))

def update_score(display):
	if TARGET in snack_body:
		generate_point(display)
		variables.SHOULD_POP[0] = False
		variables.SCORE += 10

def set_body(display):
    for pos in snack_body:
        pygame.draw.rect(display, BLACK, (pos[0] - 1, pos[1] - 1, SIZE_RECT + 2, SIZE_RECT + 2))
        pygame.draw.rect(display, RED, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))

def	effect_move(action):
	if action == pygame.K_UP and variables.LAST_ACTION != pygame.K_DOWN:
		up_act()
	elif action == pygame.K_DOWN and variables.LAST_ACTION != pygame.K_UP:
		down_act()
	elif action == pygame.K_RIGHT and variables.LAST_ACTION != pygame.K_LEFT:
		right_act()
	elif action == pygame.K_LEFT and variables.LAST_ACTION != pygame.K_RIGHT:
		left_act()
	else:
		updae_body()
	set_body(display)

def initial_game(display):
	pygame.display.set_caption('Game')
	display.fill(WHITE)
	set_body(display)

def	run_the_game():
	generate_point(display)
	while 1:
		if Game_still_running() == 0:
			exit()
		update_score(display)
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key in MOVE_KEY:
				variables.LAST_PRESSED = event.key
		display.fill(WHITE)
		effect_move(variables.LAST_PRESSED)
		draw_point()
		pygame.display.update()
		print(variables.SCORE)
		time.sleep(0.05)


if '__main__' == __name__:
	display = pygame.display.set_mode(SCREEN_SIZE)
	initial_game(display)
	run_the_game()	