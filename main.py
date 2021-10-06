
from env import *
import env

if '__main__' == __name__:
	display = pygame.display.set_mode(SCREEN_SIZE)
	initial_game(display)
	AI = Brain()
	run_the_game_env(display, AI)
	status = get_game_status(display)
	AI.model.predict(status)