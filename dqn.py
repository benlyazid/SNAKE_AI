from env import *

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
		num_outputs = model.output_shape[-1]
		min_len = min(self.memory_size, batch_size)
		# Modifying the inputs batch to work with 3D states
		inputs = np.zeros((min_len, self.memory[0][0][0].shape[1],self.memory[0][0][0].shape[2],self.memory[0][0][0].shape[3]))

		targets = np.zeros(min_len, num_outputs)
		for i, idx in enumerate(np.random.randint(0, self.memory_size, size = min_len)):
			current_state, action, reward, next_state = self.memory[idx][0]
			game_over = self.memory[idx][1]
			inputs[i] = current_state
			targets[i] = model.predict(current_state)[0] # What if we give him a big score to achive that he is impossible ? like INT_MAX 
			Q_sa = np.max(model.predict(next_state)[0])
			if game_over:
				targets[i, action] = reward
			else:
				targets[i, action] = reward + self.discount * Q_sa
		return inputs, targets
