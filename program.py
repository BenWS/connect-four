import pygame
import math
from collections import namedtuple

from pygame.locals import *

class Token(pygame.sprite.Sprite):
  def __init__(self, position):
    self.surf = pygame.Surface((position[0],position[1]))
    self.surf.fill((255,0,0))
    self.surf.set_colorkey((255,255,255),RLEACCEL)
    self.rect = self.surf.get_rect()

  @property
  def centerx(self):
     return self.rect.centerx
  
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

    # construct board columns
    self.board_column_list = [ ] 
    for num in range(num_columns):
      board_column = Board.BoardColumn(self.board_cell_group,num)
      self.board_column_list.append(board_column)

    # print(self.board_column_list)

  class BoardCell(pygame.sprite.Sprite):
    def __init__(self, size, position, coordinate):
      super(Board.BoardCell,self).__init__()
      self.surf = pygame.Surface((size,size))
      self.rect = self.surf.get_rect()
      self.rect = pygame.draw.rect(self.surf, color=(255,0,0), rect=self.rect, width=2)
      self.rect.center = position
      self.center = position
      
      self._token = None
      self._size = size
      self._coordinate = coordinate
      self._position = position

    @property
    def token(self):
      return self._token
    
    @token.setter
    def token(self, token):
        self._token = token
    
    @property
    def coordinate(self):
      return self._coordinate

    @property
    def position(self):
      return self._position
    
    @property
    def size(self):
      return self._size
  
  
  class BoardColumn():
    '''
    TODO: 2023_07_29_3 - Find Open Board Cell

    - [ ] Board iterates through board columns to find the closest column for token (simply print column index)
    - [ ] Token iterates through board cells to find the first available board cell 
    - [ ] Board sets board cell with token
    - [ ] Game runtime moves token to the destination cell
    '''
    def __init__(self,board_cell_group, column_index):
      self.board_cell_list = [ ] 
      self.center = None

      self.board_cell_list = [
        board_cell for board_cell 
        in board_cell_group 
        if board_cell.coordinate[0] == column_index
        ]
      
      self.center = \
        self.board_cell_list[0].position[0] \
        + self.board_cell_list[0].size*1.0/2
      
    

  def find_board_cell(self,token):
    '''
    Find the board cell for which the provided token should populate.

    The 'correct' board cell is determined via a combination of factors:
      - Closest board cell column to the token
      - First unpopulated board cell in the board
    '''

    # token_center_horizontal = token.get_position()[0]

    # get the closest board column for token
    token_distances = []
    for board_column in self.board_column_list:
       token_distance = abs(board_column.center - token.centerx)
       token_distances.append((token_distance,board_column))
    
    closest_column = sorted(token_distances, key=lambda x: x[0])[0][1]

    # get the first unpopulated board cell 
    board_cell_list = [
       board_cell 
       for board_cell in closest_column.board_cell_list 
       if board_cell.token is None
       ]
    target_board_cell = sorted(board_cell_list,key=lambda x: x.coordinate, reverse=True)[0]
    return target_board_cell


def run_game():
  # Initialize Pygame
  pygame.init()

  # Set up the display
  width, height = 800, 600
  screen = pygame.display.set_mode((width, height))
  
  # create token object 
  token = Token((50,50))

  # create grid_square objects
  board = Board(board_size=(7,6),board_position=(100,100), cell_width=75)
      
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
            target_board_cell = board.find_board_cell(token)				
            token.rect.left = target_board_cell.position[0]
            token.rect.top = target_board_cell.position[1]

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
  run_game()
  # token_position = (50,50)
  # token = Token(token_position)
  
  # board = Board(board_size=(7,6),board_position=(200,200), cell_width=20)
  # board.find_board_cell(token)
  # token.find_open_board_cell(board)
  # board.get_board_column_positions()
  pass