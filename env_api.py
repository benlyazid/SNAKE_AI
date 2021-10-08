import variables
from env import *

def reset_board():
	for y in range(variables.SCREEN_SIZE[0]):
		for x in range(variables.SCREEN_SIZE[1]):
			variables.BOARD[0][y][x][0] = variables.WHITE
			variables.BOARD[0][y][x][1] = variables.WHITE
			variables.BOARD[0][y][x][2] = variables.WHITE


def draw_rect_env(color, x, y, size):
	for i in range(size):
		for j in range(size):
			variables.BOARD[0][y + i][x + i][0] = color[0]
			variables[0][y + i][x + i][1] = color[1]
			variables[0][y + i][x + i][2] = color[2]

def set_body_env():
	head = variables.snack_body[-1]
	for pos in variables.snack_body:
		# pygame.draw.rect(display, BLACK, (pos[0] - 1, pos[1] - 1, SIZE_RECT + 2, SIZE_RECT + 2))
		draw_rect_env(BLACK, pos[0] - 1, pos[1] - 1, SIZE_RECT + 2)
		if pos != head:
			#pygame.draw.rect(display, RED, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))
			draw_rect_env(RED, pos[0], pos[1] , SIZE_RECT)

		else:
			#pygame.draw.rect(display, RED_HEAD, (pos[0], pos[1], SIZE_RECT, SIZE_RECT))
			draw_rect_env(RED_HEAD, pos[0], pos[1] , SIZE_RECT)

		#print("draw ", pos)
def reset_env_api():
	generate_point()
	variables.SCORE = 0
	variables.snack_body = [[300, 300], [320, 300], [340, 300], [360, 300]]
	variables.SHOULD_POP =  [True]
	variables.LAST_ACTION = pygame.K_RIGHT
	variables.LAST_PRESSED = pygame.K_RIGHT
	# display.fill(WHITE) # ====> transform to matrix  ???
	reset_board()

	set_body_env()  # remove display
	current_state = get_game_status(display)
	return display, current_state

def get_game_status_env(display):
	status = np.zeros((1,80,80,3))
	index = 0
	for x in range(0, SCREEN_SIZE[0], 10):
		row = []
		for y in range(0, SCREEN_SIZE[1], 10):
			color = variables.BOARD[0][x][y]
			row.append(color[:-1])
		status[0][index] = (row)
		index += 1
	return  status#np.asarray(status)