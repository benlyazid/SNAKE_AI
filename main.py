
#from env import *
#import env

# if '__main__' == __name__:
# 	display = pygame.display.set_mode(SCREEN_SIZE)
# 	initial_game(display)
# 	AI = Brain()
# 	run_the_game(display, AI)
# 	status = get_game_status(display)
# 	AI.model.predict(status)
import tensorflow as tf


gpus = tf.config.list_physical_devices('GPU')
print(gpus)
if gpus:
  # Restrict TensorFlow to only use the first GPU
  try:
    tf.config.set_visible_devices(gpus[0], 'GPU')
    logical_gpus = tf.config.list_logical_devices('GPU')
    print(len(gpus), "Physical GPUs,", len(logical_gpus), "Logical GPU")
  except RuntimeError as e:
    # Visible devices must be set before GPUs have been initialized
    print(e)

print("Num GPUs Available: ", len(tf.config.list_physical_devices('GPU')))
