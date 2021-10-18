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
		table_size = int(SCREEN_SIZE[0] / int(SIZE_RECT))
		num_outputs = model.output_shape[-1]
		min_len = min(self.memory_size, batch_size)
		inputs = np.zeros((min_len, self.memory[0][0][0].shape[1],self.memory[0][0][0].shape[2],self.memory[0][0][0].shape[3]))
		targets = np.zeros((min_len, num_outputs))
		tab_current = np.zeros((min_len, table_size, table_size, 1))
		tab_next_current = np.zeros((min_len, table_size, table_size, 1))
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
