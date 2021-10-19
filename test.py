from time import sleep
from brain import Brain
from dqn import Dqn
from env import reset_env, step
import variables
from variables import *
import numpy as np

# criet env
game_display = reset_env()
# criet model
jump = int(SIZE_RECT)
table_size = int(SCREEN_SIZE[0] / jump)
Ai_brain = Brain((table_size, table_size, 1), learningRate) # 3 !!!!!
Ai_model = Ai_brain.loadModel('model_snack_24k.h5')
# criet dqn
Ai_memory = Dqn(variables.memSize, variables.gamma)
# Starting the main loop
game = 1
variables.epsilon = 0
while 1:
	game_display, current_state = reset_env()
	gameOver = False
	while not gameOver:
		if np.random.rand() < variables.epsilon:
			action = np.random.randint(0, 4)
		else:
			q_value = Ai_model.predict(current_state)
			action = np.argmax(q_value)
		# Updating the environment
		state, reward, gameOver = step(game_display, action)
		current_state = state
		sleep(0.05)
	game += 1

	print('Game: ', game, '\t\t SCORE IS : ', variables.SCORE)

	
    





