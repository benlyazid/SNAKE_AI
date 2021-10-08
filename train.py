# train the nueral network 
import os
from os import stat
#os.environ['KERAS_BACKEND'] = "plaidml.keras.backend"
from time import sleep, time
from brain import Brain
from dqn import Dqn
from env import reset_env, step
import variables
from variables import *
import numpy as np
import matplotlib.pyplot as plt
import time
os.environ["SDL_VIDEODRIVER"] = "dummy"

# criet env

game_display = reset_env()

# criet model
Ai_brain = Brain((80,80,3), 0.0001)
Ai_model = Ai_brain.model

# criet dqn
Ai_memory = Dqn(variables.memSize, variables.gamma)

# Starting the main loop
epoch = 0
scores = list()
maxNCollected = 0
totNCollected = 0

while 1:
	game_display, current_state = reset_env()
	epoch += 1
	gameOver = False
	while not gameOver:
		start = time.monotonic()
		if np.random.rand() < variables.epsilon:
			action = np.random.randint(0, 4)
		else:
			q_value = Ai_model.predict(current_state)[0]
			action = np.argmax(q_value)
		# Updating the environment
		state, reward, gameOver = step(game_display, action)
		#print(variables.snack_body, gameOver, reward)
		#remember
		
		Ai_memory.remember([current_state, action, reward, state], gameOver)
		inputs, targets = Ai_memory.get_batch(Ai_model, batchSize)
		current_state = state
		#Ai_model.train_on_batch(inputs, targets)
		
		end = time.monotonic()

		print("time : ", end - start)

	if variables.SCORE > maxNCollected and variables.SCORE > 2:
		maxNCollected = variables.SCORE
		Ai_model.save(variables.filepathToSave)
	totNCollected += variables.SCORE
	# Showing the results each 100 games
	if epoch % 100 == 0 and epoch != 0:
		scores.append(totNCollected / 100)
		totNCollected = 0
		plt.plot(scores)
		plt.xlabel('Epoch / 100')
		plt.ylabel('Average Score')
		plt.savefig('stats.png')
		plt.close()
    
    # Lowering the epsilon
	if variables.epsilon > variables.minEpsilon:
		variables.epsilon -= variables.epsilonDecayRate
    
    # Showing the results each game
	print('Epoch: ' + str(epoch) + ' Current Best: ' + str(maxNCollected) + ' Epsilon: {:.5f}'.format(epsilon))
