from os import stat
from numpy.core.fromnumeric import var
from numpy.core.records import array
from numpy.lib.function_base import disp
import pygame
from pygame import display
from pygame.locals import *
from pygame.rect import *
import sys
from brain import Brain
from  move_body import *
from variables import *
import variables
import time
import numpy as np
import random

def get_game_status(display):
	status = np.zeros((1,80,80,3))
	index = 0
	for x in range(0, SCREEN_SIZE[0], 10):
		row = []
		for y in range(0, SCREEN_SIZE[1], 10):
			color = pygame.Surface.get_at(display, (x, y))
			row.append(color[:-1])
		status[0][index] = (row)
		index += 1
	return  status#np.asarray(status)



def Game_still_running():
	head = variables.snack_body[-1]
	if head[0] < 0 or head[0] >= SCREEN_SIZE[0]:
		return 0
	if head[1] < 0 or head[1] >= SCREEN_SIZE[1]:
		return 0
	if snack_body.count(snack_body[0]) != 1:
		return 0
	return 1

def	generate_point():
	variables.TARGET[0] = random.randint(0, (SCREEN_SIZE[0] - 20) / 20) * 20
	variables.TARGET[1] = random.randint(0, (SCREEN_SIZE[1] - 20) / 20) * 20

def	draw_point(display):
	pygame.draw.rect(display, GREEN, (variables.TARGET[0], variables.TARGET[1], SIZE_RECT, SIZE_RECT))

def update_score():
	if TARGET in snack_body:
		generate_point()
		variables.SHOULD_POP[0] = False
		variables.SCORE += 10

def set_body(display):
	head = snack_body[-1]
	for pos in snack_body:
		pygame.draw.rect(display, BLACK, (pos[0] - 1, pos[1] - 1, SIZE_RECT + 2, SIZE_RECT + 2))
		if pos != head:
			pygame.draw.rect(display, RED, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))
		else:
			pygame.draw.rect(display, RED_HEAD, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))


def	effect_move(action, display, draw=1):
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
	if draw:
		set_body(display)



def initial_game(display):
	pygame.display.set_caption('Game')
	display.fill(WHITE)
	set_body(display)

def	run_the_game(display, Ai):
	generate_point()
	while 1:
		if Game_still_running() == 0:
			exit()
		update_score()
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN and event.key in MOVE_KEY:
				variables.LAST_PRESSED = event.key
		display.fill(WHITE)
		effect_move(variables.LAST_PRESSED, display)
		draw_point(display)

		status = get_game_status(display)
		result = Ai.model.predict(status)
		print("result is ", result)
		#pygame.display.update()
		#break
		time.sleep(0.05)


def	step(display, Ai, action):
	if Game_still_running() == 0:
		exit() # ??
	update_score()
	for event in pygame.event.get(): #
		if event.type == QUIT: #
			pygame.quit() #
			sys.exit() #

		if event.type == pygame.KEYDOWN and event.key in MOVE_KEY: # change by action
			variables.LAST_PRESSED = event.key # action
	display.fill(WHITE)
	effect_move(variables.LAST_PRESSED, display)
	draw_point(display)

	status = get_game_status(display)

	#result = Ai.model.predict(status)
	#print("status[0]", status[0][0][0])
	time.sleep(0.5)

def reset_env():
	generate_point()
	variables.SCORE = 0
	variables.snack_body = [[300, 300], [320, 300], [340, 300], [360, 300]]
	variables.SHOULD_POP =  False

