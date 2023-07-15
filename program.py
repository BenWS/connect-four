'''
REF: Game Recreation - 'Connect Four'
'''

'''
TODO: T_2023_07_15 - Game Skeleton

- [ ] Create working game skeleton (i.e. game that displays a static image)
'''

'''
TODO:

Click events.

- [ ] Enable game runtime to:
	- [ ] Detect click events
	- [ ] Detect click release
	- [ ] Detect click down (without release)
	- [ ] Detect that click down event is occurring on static sprite
- [ ] Discover how the event registry or related might be used to drag a sprite
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

from pygame.locals import (
	RLEACCEL,
	K_UP,
	K_DOWN,
	K_LEFT,
	K_RIGHT,
	K_ESCAPE,
	KEYDOWN,
	QUIT,
)

# Initialize Pygame
pygame.init()

# Set up the display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))

class Token(pygame.sprite.Sprite):
	def __init__(self):
		self.surf = pygame.Surface((10,10))
		self.surf.fill((255,0,0))
		self.surf.set_colorkey((255,255,255),RLEACCEL)
		self.rect = self.surf.get_rect()

# create token object 
token = Token()

# Game loop
running = True
while running:
		# Handle events
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						running = False

		# Clear the screen
		screen.fill((0, 0, 0))

		# Update the game state
		screen.blit(token.surf,token.rect)
		token.rect.right = token.rect.right + 1

		# Draw the game elements
		# TODO: Add your drawing code here

		# Update the display
		pygame.display.flip()

# Quit the game
pygame.quit()