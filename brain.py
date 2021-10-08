import tensorflow.keras
from tensorflow.keras import activations
#from tensorflow.keras.engine.training import Model
#from keras.mixed_precision import loss_scale_optimizer
from  tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Conv2D, MaxPooling2D, Flatten
#from tensorflow.keras import optimizers
from tensorflow.keras.optimizers import Adam
from numpy.core.defchararray import mod


class Brain():
	def __init__(self, format=(80,80,3), lr=0.0005):
		self.learning_rate = lr
		self.input_shape = format
		self.number_of_output = 4
		self.model = Sequential()
		self.model.add(Conv2D(32, (3,3), activation='relu', input_shape=self.input_shape))
		self.model.add(MaxPooling2D((2)))
		self.model.add(Conv2D(64, (2), activation='relu'))
		self.model.add(Flatten())
		self.model.add(Dense(units=256, activation='relu'))
		self.model.add(Dense(units =self.number_of_output))
		self.model.compile(loss='mean_squared_error', optimizer=Adam(lr=self.learning_rate))
		#print(self.model.summary())

	def loadModel(self, filepath):
		self.model = load_model(filepath)
		return self.model