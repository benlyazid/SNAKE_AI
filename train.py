# train the nueral network 
from brain import Brain
from dqn import Dqn
from env import reset_env, step
import variables
from variables import *
import numpy as np
import matplotlib.pyplot as plt

game_display = reset_env()
# criet mode
jump = int(SIZE_RECT)
table_size = int(SCREEN_SIZE[0] / jump)
Ai_brain = Brain((table_size, table_size, 1), learningRate)
Ai_model = Ai_brain.model
#Ai_model = Ai_brain.loadModel("./model_snack.h5")
# criet dqn
Ai_memory = Dqn(variables.memSize, variables.gamma)
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
		if np.random.rand() < variables.epsilon:
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
	print(variables.SCORE)
	if variables.SCORE > maxNCollected:
		maxNCollected = variables.SCORE
	if  variables.SCORE > 2 :
	 	Ai_model.save(variables.filepathToSave)
	totNCollected += variables.SCORE
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
	if variables.epsilon > variables.minEpsilon:
		variables.epsilon -= variables.epsilonDecayRate
    
    # Showing the results each game
	print('Epoch: ' + str(epoch) + ' Current Best: ' + str(maxNCollected) + ' Epsilon: {:.5f}'.format(variables.epsilon))





