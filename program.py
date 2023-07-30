import pygame
import math
from collections import namedtuple

from pygame.locals import *
import copy

'''
Game Object Definitions
'''
class Token(pygame.sprite.Sprite):
  def __init__(self, position):
    super(Token,self).__init__()
    self.surf = pygame.Surface((position[0],position[1]))
    self.surf.fill((255,0,0))
    self.surf.set_colorkey((255,255,255),RLEACCEL)
    self.rect = self.surf.get_rect()
    self._is_moveable = True

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
    self.board_cell_array = [[None]*board_size[1]] * board_size[0]

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
    
    # add board cell to (1) cell sprite group and (2) cell array
    for cell_position in cell_position_list:
      board_cell = Board.BoardCell(
        size=cell_width
        ,position=cell_position.position
        ,coordinate=cell_position.coordinate
        )
      self.board_cell_group.add(board_cell)
      self.board_cell_array[cell_position.coordinate[0]][cell_position.coordinate[1]] = board_cell

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
      self.rect.top = position[1]
      self.rect.left = position[0]
      
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
      self.column_index = column_index

      self.board_cell_list = [
        board_cell for board_cell 
        in board_cell_group 
        if board_cell.coordinate[0] == column_index
        ]
      
      self.center = self.board_cell_list[0].rect.centerx

  def get_board_cell(self,x,y):
    ''''
    Get board cell a specific coordinate.

    NOTE: This is a somewhat inefficient approach as this
    iterates through the full set of board cells to find
    a matching coordinate. Plan is to update this function
    to a more efficient retreival method.
    '''
    #  return self.board_cell_array[0][0]
    for cell in self.board_cell_group:
      if x >= self.board_size[0] or y >= self.board_size[1]:
         return
      elif x < 0 or y < 0:
        return
      elif cell.coordinate == (x, y):
        return cell
    
  def get_game_status(self, board_cell, contiguity_limit):
    '''
    For given board cell, identify if there n-in-a-row connections in
    any given direction.
    '''
    coordinate_delta_list = [(1,0),(0,1),(1,1),(-1,1)]

    for coordinate_delta in coordinate_delta_list: # for all directions
      delta_x = coordinate_delta[0]
      delta_y = coordinate_delta[1]
      contiguous_cell_counter = 1 # continugous cell count is at least one since we at least count the token we've just placed
      contiguous_cell_list = [board_cell]
      
      # the continguous cell count should include both the positive (forward) and negative (reverse) traversal of each direction
      positive_direction = (delta_x,delta_y)
      negative_direction = (-delta_x,-delta_y)
      for direction in [positive_direction,negative_direction]:
        direction_x = direction[0]
        direction_y = direction[1]

        current_x = board_cell.coordinate[0] + direction_x
        current_y = board_cell.coordinate[1] + direction_y

        current_cell = self.get_board_cell(current_x,current_y)
        
        while current_cell is not None:
          current_x += direction_x
          current_y += direction_y
          if current_cell.token is not None: 
            contiguous_cell_counter += 1
            contiguous_cell_list.append(current_cell)
          current_cell = self.get_board_cell(current_x,current_y)

      if len(contiguous_cell_list) > 1: 
        print(contiguous_cell_list)
      
      if len(contiguous_cell_list) == contiguity_limit:
          return 'CONTIGUITY_LIMIT_REACED'
      else:
          continue
          

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

'''
Animation Management
'''
def move_sprite_to_sprite(sprite_source,sprite_target):
   sprite_source.rect.left = sprite_target.rect.left
   sprite_source.rect.top = sprite_target.rect.top

def run_game():
  # Initialize Pygame
  pygame.init()

  # Set up the display
  width, height = 800, 600
  screen = pygame.display.set_mode((width, height))
  
  # create token object 
  active_token = Token((75,75))
  token_group = pygame.sprite.Group()
  token_group.add(active_token)

  # initialize other runtime objects
  target_board_cell = None

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
            mouse_token_collide = active_token.rect.collidepoint(event.pos)
            if mouse_token_collide and mouse_button_down:
                mouse_holding_token = True
          if event.type == MOUSEMOTION:
              mouse_token_collide = active_token.rect.collidepoint(event.pos)
              if not mouse_token_collide:
                  mouse_holding_token = False
          elif event.type == MOUSEBUTTONUP:
            mouse_holding_token = False
            mouse_button_down = False
            if active_token.rect.collidepoint(event.pos):
              target_board_cell = board.find_board_cell(active_token)				
              target_board_cell.token = active_token
              move_sprite_to_sprite(target_board_cell.token,target_board_cell)
              active_token = Token((75,75))
              token_group.add(active_token)
            
            # evaluate game status
            if target_board_cell is not None:
              game_status = board.get_game_status(target_board_cell,4)
              if game_status == 'CONTIGUITY_LIMIT_REACED':
                running = False

            # print([cell for cell in board.board_cell_group if cell.token])
          if mouse_holding_token:
              if event.type == MOUSEMOTION:
                  token.rect.move_ip(event.rel)

          
          
          # other event processing
          if event.type == pygame.QUIT:
              running = False
          
      # Clear the screen
      screen.fill((0, 0, 0))

      # Update the game state
      for board_cell in board.board_cell_group:
        screen.blit(board_cell.surf,board_cell.rect)
      for token in token_group:
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
  # print([cell for cell in board.board_cell_group if cell.token])
  # board.find_board_cell(token)
  # token.find_open_board_cell(board)
  # board.get_board_column_positions()
  pass