'''
REF: Game Recreation - 'Connect Four'
'''

'''
TODO:
- [ ] Logic for moving a sprite from point (x1,y1) to point (x2,y2)
- [ ] Logic for rounding a sprite's x-position to the nearest allowed value
	- This will allow the game engine to decide into which vertical slot a token should fall

The developed motion logic should be independent of the click-and-hold mouse event described in separate TODO. The intent here is for the game to move a token for where
the user released such to a slot position
'''

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

# create token object 
token = Token()
token.rect.top = 50
token.rect.right = 50

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

		# Draw the game elements
		# TODO: Add your drawing code here

		# Update the display
		pygame.display.flip()

# Quit the game
pygame.quit()