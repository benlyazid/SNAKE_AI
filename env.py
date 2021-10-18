import pygame
from pygame.locals import *
from pygame.rect import *
from  move_body import *
from variables import *
import variables
import numpy as np
import random

def get_game_status(display):
	jump = int(SIZE_RECT)
	table_size = int(SCREEN_SIZE[0] / jump)
	status = np.zeros((1, table_size, table_size, 1))
	index = 0
	center = 1
	for x in range(center, SCREEN_SIZE[0] + center, jump):
		row = np.zeros((10,1))
		i  = 0
		for y in range(center, SCREEN_SIZE[1] + center, jump):
			color = pygame.Surface.get_at(display, (y, x))
			color = color[:-1]
			if color == variables.RED:
				color = 1
			elif color == variables.GREEN:
				color = 0.5
			elif color == variables.BLUE:
				color = 0.75
			elif color == variables.WHITE:
				color = 0
			row[i] = (color)
			i += 1
		status[0][index] = row
		index += 1
	return  status

def Game_still_running():
	head = variables.snack_body[-1]
	if head[0] < 0 or head[0] >= SCREEN_SIZE[0]:
		return 0
	if head[1] < 0 or head[1] >= SCREEN_SIZE[1]:
		return 0
	if variables.snack_body.count(head) != 1:
		return 0
	return 1

def	generate_point():
	while 1:
		variables.TARGET[0] = random.randint(0, (SCREEN_SIZE[0] - 20) / 20) * 20
		variables.TARGET[1] = random.randint(0, (SCREEN_SIZE[1] - 20) / 20) * 20
		if TARGET not in variables.snack_body:
			return

def	draw_point(display):
	pygame.draw.rect(display, GREEN, (variables.TARGET[0], variables.TARGET[1], SIZE_RECT, SIZE_RECT))

def update_score():
	if TARGET in variables.snack_body:
		generate_point()
		variables.SHOULD_POP[0] = False
		variables.SCORE += 1

def set_body(display):
	head = variables.snack_body[-1]
	for pos in variables.snack_body:
		pygame.draw.rect(display, BLACK, (pos[0] - 1, pos[1] - 1, SIZE_RECT + 2, SIZE_RECT + 2))
		if pos != head:
			pygame.draw.rect(display, RED, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))
		else:
			pygame.draw.rect(display, BLUE, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))

def	effect_move(action, display):
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

def	step(display, action):
	reward = -0.03
	game_over = False
	display.fill(WHITE)
	variables.LAST_PRESSED = variables.MOVE_KEY[action] # action
	effect_move(variables.LAST_PRESSED, display)
	if Game_still_running() == 0:
		game_over = True
		reward = -1
	elif TARGET in variables.snack_body:
		generate_point()
		variables.SHOULD_POP[0] = False
		variables.SCORE += 1
		reward = 10
	draw_point(display)
	pygame.display.update()
	status = get_game_status(display)
	return status, reward, game_over

def reset_env():
	display = pygame.display.set_mode(SCREEN_SIZE)
	generate_point()
	variables.SCORE = 0
	variables.snack_body = [[0, 100], [20, 100], [40, 100], [60, 100]]
	variables.SHOULD_POP[0] =  [True]
	variables.LAST_ACTION = pygame.K_RIGHT
	variables.LAST_PRESSED = pygame.K_RIGHT
	pygame.display.set_caption('Game')
	display.fill(WHITE)
	draw_point(display)
	set_body(display)
	current_state = get_game_status(display)
	pygame.display.update()
	return display, current_state
