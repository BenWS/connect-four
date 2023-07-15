'''
REF: Game Recreation - 'Connect Four'
'''

'''
TODO: T_2023_07_15 - Game Skeleton

- [x] Create working game skeleton (i.e. game that displays a static image)
'''

'''
TODO: 2023_07_15_2 - Click Events

Click events.

- [x] Enable game runtime to:
	- [x] Detect click events
	- [x] Detect click release
	- [x] Detect click down (without release)
	- [x] Detect that click down event is occurring on static sprite
	- [x] Return no result if click and hold is occurring any where else besides sprite
- [ ] Discover how the event registry or related might be used to drag a sprite

References:
	- https://www.geeksforgeeks.org/how-to-move-an-image-with-the-mouse-in-pygame/
	- https://stackoverflow.com/a/59009852
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

# Game loop
running = True
while running:
		# Handle events
		for event in pygame.event.get():
				if event.type == pygame.QUIT:
						running = False
				elif event.type == MOUSEBUTTONDOWN:	
					if token.rect.collidepoint(event.pos):
							print('Mouse Button Down')
				elif event.type == MOUSEBUTTONUP:	
					if token.rect.collidepoint(event.pos):
							print('Mouse Button Up')

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