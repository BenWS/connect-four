import pygame

from pygame.locals import *

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

class Token(pygame.sprite.Sprite):
	def __init__(self):
		self.surf = pygame.Surface((30,30))
		self.surf.fill((255,0,0))
		self.surf.set_colorkey((255,255,255),RLEACCEL)
		self.rect = self.surf.get_rect()

class GridSquare(pygame.sprite.Sprite):
	def __init__(self):
		self.surf = pygame.Surface((30,30))
		self.rect = self.surf.get_rect()
		self.rect = pygame.draw.rect(self.surf, color=(255,0,0), rect=self.rect, width=2)

# create token object 
token = Token()
token.rect.top = 50
token.rect.right = 50

# create grid_square objects
grid_square = GridSquare()
grid_square.rect.top = 100
grid_square.rect.right = 100

grid_square_2 = GridSquare()
grid_square_2.rect.top = 130
grid_square_2.rect.right = 130

grid_square_3 = GridSquare()
grid_square_3.rect.top = 100
grid_square_3.rect.right = 130

grid_square_4 = GridSquare()
grid_square_4.rect.top = 130
grid_square_4.rect.right = 100

class Grid():

	'''
	TODO: 2023_07_21_3 - Draw Grid on Screen

	 - [ ] Construct simple Board consisting of BoardCells and BoardColumns
	 - [ ] Prove that a rectangular image can be used in place of the drawn rectangle
	'''

	'''
	Grid object is composed of GridCell objects.

	This class is a visual container of grid cells and offers facilities for determining
	how the Token class should interact with such. For example, in the context of a user
	dragging and dropping a token, the game runtime should be able to determine which slot
	the token falls into.

	Our constructor receives the 'center' argument and then constructs position of each cell accordingly.
	'''
	def __init__(self):
		pass

# mouse state
mouse_holding_token = False
mouse_button_down = False
mouse_token_collide = False

# Game loop
running = True
while running:
		# Handle events
		for event in pygame.event.get():
				# set persistent states

				# is token held by user
				if event.type == MOUSEBUTTONDOWN:
					mouse_button_down = True
					mouse_token_collide = token.rect.collidepoint(event.pos)
					if mouse_token_collide and mouse_button_down:
							mouse_holding_token = True
				if event.type == MOUSEMOTION:
						mouse_token_collide = token.rect.collidepoint(event.pos)
						if not mouse_token_collide:
								mouse_holding_token = False
				elif event.type == MOUSEBUTTONUP:
					mouse_holding_token = False
					mouse_button_down = False				

				if mouse_holding_token:
						if event.type == MOUSEMOTION:
								token.rect.move_ip(event.rel)
								# token.rect.right = token.rect.right + 1
				
				# other event processing
				if event.type == pygame.QUIT:
						running = False
				
		# Clear the screen
		screen.fill((0, 0, 0))

		# Update the game state
		screen.blit(token.surf,token.rect)
		screen.blit(grid_square.surf,grid_square.rect)
		screen.blit(grid_square_2.surf,grid_square_2.rect)
		screen.blit(grid_square_3.surf,grid_square_3.rect)
		screen.blit(grid_square_4.surf,grid_square_4.rect)

		# Draw the game elements
		# TODO: Add your drawing code here

		# Update the display
		pygame.display.flip()

# Quit the game
pygame.quit()