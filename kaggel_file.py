import os
import numpy as np
import matplotlib.pyplot as plt
import pygame
from  tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten
from tensorflow.keras.optimizers import Adam
from pygame.locals import *
from pygame.rect import *
import random

####################_____________VARIABLES

os.environ["SDL_VIDEODRIVER"] = "dummy"
#	ENV_VARIABLES
snack_body = [[0, 100], [20, 100], [40, 100], [60, 100]]

RED = (255, 0, 0)
BLACK = (0, 0, 0)	
GREEN = (0,255,0)
BLUE = (0,0,255)
WHITE = (255, 255, 255)
GRIS = (156, 156, 156, 0)

SIZE_RECT = 20
MOVE_SIZE = 20

SCREEN_SIZE = (200, 200)

LAST_ACTION = pygame.K_RIGHT
LAST_PRESSED = pygame.K_RIGHT


MOVE_KEY = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]

TARGET = [0, 0]
SHOULD_POP = [True]

SCORE = 0

#	BRAIN_ENV

memSize = 60000
batchSize = 32
learningRate = 0.0001
gamma = 0.9
epsilon = 1
epsilonDecayRate = 0.0002
minEpsilon = 0.0005
filepathToSave = './model_snack.h5'

####################_______________________________________

####################_____________BRAIN

class Brain():
	def __init__(self, format=(80,80,3), lr=0.0005):
		self.learning_rate = lr
		self.input_shape = format
		self.number_of_output = 4
	
		self.model = Sequential()
		self.model.add(Conv2D(32, (3,3), activation = 'relu', input_shape = self.input_shape))
		self.model.add(MaxPooling2D((2,2)))
		self.model.add(Conv2D(64, (2,2), activation = 'relu'))
		self.model.add(Flatten())
		self.model.add(Dense(units = 256, activation = 'relu'))
		self.model.add(Dense(units = self.number_of_output))
		print(self.model.summary())

		# Compiling the model
		self.model.compile(loss = 'mean_squared_error', optimizer = Adam(lr = self.learning_rate))
	def loadModel(self, filepath):
		self.model = load_model(filepath)
		return self.model
####################_______________________________________



####################_____________DQN
class Dqn():
	def __init__(self, max_memory, descount):
		self.max_memory = max_memory
		self.descount = descount
		self.memory = list()
		self.memory_size = 0

	def remember(self, transition, game_over):
		self.memory.append([transition, game_over])
		self.memory_size += 1
		if self.memory_size > self.max_memory:
			del self.memory[0]
			self.memory_size -= 1

	def get_batch(self, model, batch_size = 10):
		table_size = int(SCREEN_SIZE[0] / int(MOVE_SIZE))

		num_outputs = model.output_shape[-1]
		min_len = min(self.memory_size, batch_size)
		inputs = np.zeros((min_len, self.memory[0][0][0].shape[1],self.memory[0][0][0].shape[2],self.memory[0][0][0].shape[3]))
		targets = np.zeros((min_len, num_outputs))
		tab_current = np.zeros((min_len, table_size, table_size, 1)) #3
		tab_next_current = np.zeros((min_len, table_size, table_size, 1)) #3
		tab_action = []
		tab_reward = []
		tab_over = []
		for i, idx in enumerate(np.random.randint(0, self.memory_size, size = min_len)):
			current_state, action, reward, next_state = self.memory[idx][0]
			tab_current[i] = current_state
			tab_next_current[i] = next_state    
			tab_action.append(action)
			tab_reward.append(reward)
			tab_over.append(self.memory[idx][1])
		tab_current_predict = model.predict(tab_current)
		tab_next_current_predict = model.predict(tab_next_current)
		
		for i, idx in enumerate(np.random.randint(0, self.memory_size, size = min_len)):
			inputs[i] = tab_current[i]
			targets[i] = tab_current_predict[i]
			Q_sa = np.max(tab_next_current_predict[i])
			if tab_over[i]:
				targets[i, tab_action[i]] = tab_reward[i]
			else:
				targets[i, tab_action[i]] = tab_reward[i] + self.descount * Q_sa
		return inputs, targets
####################_______________________________________



####################_____________MOVE_BODY


def up_act():

    global LAST_ACTION, SHOULD_POP, snack_body
    head = snack_body[-1]
    snack_body.append([head[0], head[1] - SIZE_RECT])
    if SHOULD_POP[0] == True:
        snack_body.pop(0)
    SHOULD_POP[0] = True 
    LAST_ACTION = pygame.K_UP


def down_act():
    global LAST_ACTION, SHOULD_POP, snack_body

    head = snack_body[-1]
    snack_body.append([head[0], head[1] + SIZE_RECT])
    if SHOULD_POP[0] == True:
        snack_body.pop(0)
    SHOULD_POP[0] = True 
    LAST_ACTION = pygame.K_DOWN

def left_act():
    global LAST_ACTION, SHOULD_POP, snack_body
    head = snack_body[-1]
    snack_body.append([head[0] - SIZE_RECT, head[1]])
    if SHOULD_POP[0] == True:
        snack_body.pop(0)
    SHOULD_POP[0] = True 
    LAST_ACTION = pygame.K_LEFT

def right_act():
    global LAST_ACTION, SHOULD_POP, snack_body
    head = snack_body[-1]
    snack_body.append([head[0] + SIZE_RECT, head[1]])
    if SHOULD_POP[0] == True:
        snack_body.pop(0)
    SHOULD_POP[0] = True 
    LAST_ACTION = pygame.K_RIGHT
    

def updae_body():
    global LAST_ACTION
    if LAST_ACTION == pygame.K_UP:
        up_act()
    if LAST_ACTION == pygame.K_DOWN:
       down_act()
    if LAST_ACTION == pygame.K_RIGHT:
        right_act()
    if LAST_ACTION == pygame.K_LEFT:
        left_act()
####################_______________________________________


####################_____________ENV


def get_game_status(display):
	global RED, GREEN, BLUE, WHITE
	jump = int(MOVE_SIZE)
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
			if color == RED:
				color = 1
			elif color == GREEN:
				color = 0.5
			elif color == BLUE:
				color = 0.75
			elif color == WHITE:
				color = 0
			row[i] = color
			i += 1
		status[0][index] = row
		index += 1
	return status



def Game_still_running():
	global snack_body
	head = snack_body[-1]
	if head[0] < 0 or head[0] >= SCREEN_SIZE[0]:
		return 0
	if head[1] < 0 or head[1] >= SCREEN_SIZE[1]:
		return 0
	if snack_body.count(head) != 1:
		return 0
	return 1

def	generate_point():
	global TARGET, snack_body
	while 1:
		TARGET[0] = random.randint(0, (SCREEN_SIZE[0] - 20) / 20) * 20
		TARGET[1] = random.randint(0, (SCREEN_SIZE[1] - 20) / 20) * 20
		if TARGET not in snack_body:
			return

def	draw_point(display):
	global TARGET, SIZE_RECT
	pygame.draw.rect(display, GREEN, (TARGET[0], TARGET[1], SIZE_RECT, SIZE_RECT))

def set_body(display):
	global snack_body, SIZE_RECT
	head = snack_body[-1]
	for pos in snack_body:
		pygame.draw.rect(display, BLACK, (pos[0] - 1, pos[1] - 1, SIZE_RECT + 2, SIZE_RECT + 2))
		if pos != head:
			pygame.draw.rect(display, RED, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))
		else:
			pygame.draw.rect(display, BLUE, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))

def	effect_move(action, display):
	global LAST_ACTION
	if action == pygame.K_UP and LAST_ACTION != pygame.K_DOWN:
		up_act()
	elif action == pygame.K_DOWN and LAST_ACTION != pygame.K_UP:
		down_act()
	elif action == pygame.K_RIGHT and LAST_ACTION != pygame.K_LEFT:
		right_act()
	elif action == pygame.K_LEFT and LAST_ACTION != pygame.K_RIGHT:
		left_act()
	else:
		updae_body()
	set_body(display)

def	step(display, action):
	global MOVE_KEY, LAST_PRESSED, snack_body, SHOULD_POP, SCORE
	reward = -0.03
	game_over = False
	display.fill(WHITE)
	LAST_PRESSED = MOVE_KEY[action] # action
	effect_move(LAST_PRESSED, display)
	if Game_still_running() == 0:
		game_over = True
		reward = -1
	elif TARGET in snack_body:
		generate_point()
		SHOULD_POP[0] = False
		SCORE += 1
		reward = 10
	draw_point(display)
	pygame.display.update()
	status = get_game_status(display)
	return status, reward, game_over

def reset_env():
	global SCORE, SHOULD_POP, LAST_ACTION, LAST_PRESSED, snack_body
	display = pygame.display.set_mode(SCREEN_SIZE)
	generate_point()

	SCORE = 0
	snack_body = [[0, 100], [20, 100], [40, 100], [60, 100]]
	SHOULD_POP =  [True]
	LAST_ACTION = pygame.K_RIGHT
	LAST_PRESSED = pygame.K_RIGHT
	pygame.display.set_caption('Game')
	display.fill(WHITE)
	draw_point(display)
	set_body(display)
	current_state = get_game_status(display)
	pygame.display.update()
	return display, current_state
####################_______________________________________



####################_____________TRAIN
# train the nueral network 

game_display = reset_env()
jump = int(MOVE_SIZE)
table_size = int(SCREEN_SIZE[0] / jump)
Ai_brain = Brain((table_size, table_size, 1), learningRate) # 3 !!!!!
# Ai_model = Ai_brain.model
Ai_model = Ai_brain.loadModel("./model_snack.h5")

# criet dqn
Ai_memory = Dqn(memSize, gamma)

# Starting the main loop
epoch = 0
scores = list()
steps_ = list()
maxNCollected = 0
totNCollected = 0
totSteps = 0
while 1:
	game_display, current_state = reset_env()
	epoch += 1
	gameOver = False
	i = 0
	while not gameOver:
		if np.random.rand() < epsilon:
			action = np.random.randint(0, 4)
		else:

			q_value = Ai_model.predict(current_state)
			action = np.argmax(q_value)
		# Updating the environment
		state, reward, gameOver = step(game_display, action)
		Ai_memory.remember([current_state, action, reward, state], gameOver)
		inputs, targets = Ai_memory.get_batch(Ai_model, batchSize)
		current_state = state
		loss = Ai_model.train_on_batch(inputs, targets)
		
		i += 1

	if SCORE > maxNCollected:
		maxNCollected = SCORE
	if  SCORE > 2 :
		Ai_model.save(filepathToSave)
	totNCollected += SCORE
	totSteps += i

	# Showing the results each 100 games
	if epoch % 10 == 0 and epoch != 0:
		scores.append(totNCollected / 10)
		steps_.append(totSteps / 10)
		totNCollected = 0
		totSteps = 0
		plt.plot(scores)
		plt.plot(steps_)
		plt.xlabel('Epoch / 10')
		plt.ylabel('Average')
		plt.savefig('stats.png')
		plt.close()
	
    
    # Lowering the epsilon
	if epsilon > minEpsilon:
		epsilon -= epsilonDecayRate
    
    # Showing the results each game
	print('Epoch: ' + str(epoch) + ' Current Best: ' + str(maxNCollected) + ' Epsilon: {:.5f}'.format(epsilon) + ' Last Loss: ', loss)
####################_______________________________________