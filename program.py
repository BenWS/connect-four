import pygame
import math
from collections import namedtuple

from pygame.locals import *

class Token(pygame.sprite.Sprite):
  def __init__(self):
    self.surf = pygame.Surface((75,75))
    self.surf.fill((255,0,0))
    self.surf.set_colorkey((255,255,255),RLEACCEL)
    self.rect = self.surf.get_rect()
  
  def find_open_board_cell(self, Board):
    '''
    Find and move the token to the available board cell
    '''

    '''
    ....PPP
    get the set of board columns
    identify and select which of the board columns positions is the closest
    determine whether any of the board column cells are populated
    determine whether the token is in correct part of the screen for it to be dropped
    '''
    pass

class Board():
  '''
  The Board object is composed of BoardCell objects.

  This class is a visual container of grid cells and offers facilities for determining
  how the Token class should interact with such. For example, in the context of a user
  dragging and dropping a token, the game runtime should be able to determine which slot
  the token falls into.
  '''
  def __init__(self, board_size, board_position, cell_width):
    self.board_size = board_size # enforcing provided type?
    self.board_position = board_position
    self.cell_width = cell_width
    self.board_cell_group = pygame.sprite.Group()

    num_columns = board_size[0]
    num_rows = board_size[1]

  
    # assign column positions
    column_position_list = []
    for num in range(num_columns):
      column_position = (num,self.board_position[0] + self.cell_width * num)
      column_position_list.append(column_position)

    # assign row positions
    row_position_list = []
    for num in range(num_rows):
      row_position = (num,self.board_position[0] + self.cell_width * num)
      row_position_list.append(row_position)

    # get cartesian product of column and row positions
    CellPosition = namedtuple('CellPosition','position coordinate')
    cell_position_list = [
      CellPosition((column_position[1],row_position[1]),(column_position[0],row_position[0]))
      for column_position in column_position_list 
      for row_position in row_position_list
      ]
    
    for cell_position in cell_position_list:
      board_cell = Board.BoardCell(
        size=cell_width
        ,position=cell_position.position
        ,coordinate=cell_position.coordinate
        )
      self.board_cell_group.add(board_cell)

    board_column = Board.BoardColumn(self.board_cell_group,0)		

  class BoardCell(pygame.sprite.Sprite):
    def __init__(self, size, position, coordinate):
      super(Board.BoardCell,self).__init__()
      self.surf = pygame.Surface((size,size))
      self.rect = self.surf.get_rect()
      self.rect = pygame.draw.rect(self.surf, color=(255,0,0), rect=self.rect, width=2)
      
      self.size = size
      self.coordinate = coordinate
      self.position = position
      self.rect.left = position[0]
      self.rect.top = position[1]
  
  class BoardColumn():
    '''
    TODO: 2023_07_29_3 - Find Open Board Cell
    '''
    def __init__(self,board_cell_group, column_index):
      self.member_board_cell_list = [
        board_cell for board_cell 
        in board_cell_group 
        if board_cell.coordinate[0] == column_index
        ]
      
      column_center_position = \
        self.member_board_cell_list[0].position[0] \
        + self.member_board_cell_list[0].size*1.0/2

      print(column_center_position)

# create token object 
token = Token()
token.rect.top = 50
token.rect.right = 50

# create grid_square objects
board = Board(board_size=(7,6),board_position=(100,100), cell_width=75)
    
def run_game():
  # Initialize Pygame
  pygame.init()

  # Set up the display
  width, height = 800, 600
  screen = pygame.display.set_mode((width, height))

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
      for board_cell in board.board_cell_group:
        screen.blit(board_cell.surf,board_cell.rect)
      screen.blit(token.surf,token.rect)
      
      # Draw the game elements

      # Update the display
      pygame.display.flip()

  # Quit the game
  pygame.quit()

if __name__ == '__main__':
  # run_game()
  # token = Token()
  # token.rect.top = 50
  # token.rect.right = 50
  
  # board = Board(board_size=(7,6),board_position=(200,200), cell_width=20)
  # token.find_open_board_cell(board)
  # board.get_board_column_positions()
  pass