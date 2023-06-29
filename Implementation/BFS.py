
from cmath import pi
import math
import sys

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.name = name

class King(Piece):
    name = "King"

    def __init__(self, x, y):
        super().__init__(x,y,self.name)

    
    '''
    Takes in a State object, checks the possible moves the King can take
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)

    '''
    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        x = self.x
        y = self.y

        
        #Gets possible locations, given the board limits and obstacles 
        #(Does not remove locations with pieces or threatened locations)
        #NorthWest
        if x-1 >= 0 and y-1 >= 0: #e.g this checks board limits
            if grid[x-1][y-1] > 0: #this checks if its not an obstacle 
                acts.append((x-1,y-1))

        #North
        if x-1 >= 0:
            if grid[x-1][y] > 0:
                acts.append((x-1, y))

        #NorthEast
        if x-1 >= 0 and y+1 < cols:
            if grid[x-1][y+1] > 0:
                acts.append((x-1, y+1))

        #West
        if y-1 >= 0:
            if grid[x][y-1] > 0:
                acts.append((x, y-1))

        #East
        if y+1 < cols:
            if grid[x][y+1] > 0:
                acts.append((x, y+1))
                
        #SouthWest
        if x+1 < rows and y-1 >= 0:
            if grid[x+1][y-1] > 0:
                acts.append((x+1, y-1))

        #South
        if x+1 < rows:
            if grid[x+1][y] > 0:
                acts.append((x+1, y))

        #SouthEast
        if x+1 < rows and y+1 < cols:
            if grid[x+1][y+1] > 0:
                acts.append((x+1,y+1))

        #Only here we remove locations which are occupied by other pieces
        #Remove actions which step on other-piece locations
        for each in acts:
            if each in other_piece_locations:
                acts.remove(each)
        
        return acts
        
class Knight(Piece):
    name = "Knight"

    def __init__(self, x, y):
        super().__init__(x,y ,self.name)

    '''
    Returns a list of action locations, which the knight can move to from its current location,
    that are unoccupied by any other pieces and not an obstacle
    This also works to find out the threat locations of a piece
    '''
    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        x = self.x
        y = self.y

        #|-
        #|
        if y+1 < cols and x-2 >= 0:
            if grid[x-2][y+1] > 0:
                acts.append((x-2, y+1))
            

        #---
        #|
        if y+2 < cols and x-1 >= 0:
            if grid[x-1][y+2] > 0:
                acts.append((x-1, y+2))

        #|
        #---
        
        if y+2 < cols and x+1 < rows:
            if grid[x+1][y+2] > 0:
                acts.append((x+1, y+2))


        #|
        #|-
        if y+1 < cols and x+2 < rows:
            if grid[x+2][y+1] > 0:
                acts.append((x+2, y+1))

        # |
        #-|
        if y-1 >= 0 and x+2 < rows:
            if grid[x+2][y-1] > 0:
                acts.append((x+2, y-1))

        #   |
        #---
        if y-2 >= 0 and x+1 < rows:
            if grid[x+1][y-2] > 0:
                acts.append((x+1, y-2))


        #-|
        # |
        if y-1 >= 0 and x-2 >= 0:
            if grid[x-2][y-1] > 0:
                acts.append((x-2, y-1))
            

        #---
        #|
        if y-2 >= 0 and x-1 >= 0:
            if grid[x-1][y-2] > 0:
                acts.append((x-1, y-2))

        #Remove actions which step on other-piece locations
        for each in acts:
            if each in other_piece_locations:
                acts.remove(each)

        return acts

class Rook(Piece):
    name = "Rook"

    #Lists the possible moves, specifically changes in the x,y directions (reference pt top left of board)
    # the numbers correspond to the limit of how much the direction val can be changed
    #e.g queen will then be able to move the entire board

    #Rook movement
    #       ^
    #       |
    #  <--- R --->
    #       |
    #       v


    def __init__(self, x, y):
        super().__init__(x,y ,self.name)

    
        '''
    Takes in a State object, checks the possible moves the King can take
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)

    '''
    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        x = self.x
        y = self.y

        #North
        x_avail = x
        for i in range(1, x_avail+1):
            if grid[x-i][y] > 0 and (x-i, y) not in other_piece_locations:
                #if the spot is movable -> no obstacle and no piece blocking
                acts.append((x-i,y))
            else:
                #we have to break here due to obstacle or piece block
                break

        #East
        y_avail = cols - y - 1
        for i in range(1, y_avail+1):
            # print(i)
            if grid[x][y+i] > 0 and (x, y+i) not in other_piece_locations:
                #if the spot is movable -> no obstacle and no piece blocking
                acts.append((x,y+i))
            else:
                #we have to break here due to obstacle or piece block
                break

        #South
        x_avail = rows - x - 1
        for i in range(1, x_avail+1):
            if grid[x+i][y] > 0 and (x+i, y) not in other_piece_locations:
                #if the spot is movable -> no obstacle and no piece blocking
                acts.append((x+i,y))
            else:
                #we have to break here due to obstacle or piece block
                break


        #West
        y_avail = y
        for i in range(1, y_avail+1):
            if grid[x][y-i] > 0 and (x, y-i) not in other_piece_locations:
                #if the spot is movable -> no obstacle and no piece blocking
                acts.append((x,y-i))
            else:
                #we have to break here due to obstacle or piece block
                break

        #(redundant)
        #Remove actions which step on other-piece locations
        # for each in acts:
        #     if each in other_piece_locations:
        #         acts.remove(each)
        
        return acts

class Bishop(Piece):
    name = "Bishop"

    #Lists the possible moves, specifically changes in the x,y directions (reference pt top left of board)
    # the numbers correspond to the limit of how much the direction val can be changed
    #e.g queen will then be able to move the entire board

    #Bishop movement
    #   ^       ^
    #    \     /
    #       R
    #    /     \
    #   v       v


    def __init__(self, x, y):
        super().__init__(x,y,self.name)

    
    '''
    Takes in a State object, checks the possible moves the King can take
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)

    '''
    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        x = self.x
        y = self.y


        #NorthWest
        x_avail = x
        y_avail = y
        while x_avail - 1 >= 0 and y_avail - 1 >= 0:
            if grid[x_avail-1][y_avail-1] > 0 and ((x_avail-1, y_avail-1) not in other_piece_locations):
                #if the spot is movable -> no obstacle and no piece blocking
                acts.append((x_avail-1, y_avail-1))
                x_avail -= 1
                y_avail -= 1
            else:
                break

        
        #NorthEast
        x_avail = x
        y_avail = y
        while x_avail - 1 >= 0 and y_avail + 1 < cols:
            if grid[x_avail-1][y_avail+1] > 0 and ((x_avail-1, y_avail+1) not in other_piece_locations):
                #if the spot is movable -> no obstacle and no piece blocking
                
                acts.append((x_avail-1, y_avail+1))



                x_avail -= 1
                y_avail += 1
            else:
                break


        #SouthEast
        x_avail = x
        y_avail = y
        while x_avail + 1 < rows and y_avail + 1 < cols:
            if grid[x_avail+1][y_avail+1] > 0 and ((x_avail+1, y_avail+1) not in other_piece_locations):
                #if the spot is movable -> no obstacle and no piece blocking
                acts.append((x_avail+1,y_avail+1))
                x_avail += 1
                y_avail += 1
            else:
                break

        
        #SouthWest
        x_avail = x
        y_avail = y
        while x_avail + 1 < rows and y_avail - 1 >= 0:
            if grid[x_avail+1][y_avail-1] > 0 and ((x_avail+1, y_avail-1) not in other_piece_locations):
                #if the spot is movable -> no obstacle and no piece blocking
                acts.append((x_avail+1, y_avail-1))
                x_avail += 1
                y_avail -= 1
            else:
                break


        #(redundant)
        #Remove actions which step on other-piece locations
        # for each in acts:
        #     if each in other_piece_locations:
        #         acts.remove(each)
        
        return acts

class Queen(Piece):
    name = "Queen"
    def __init__(self, x, y):
        super().__init__(x,y,self.name)
        self.bishop_part = Bishop(x,y)
        self.rook_part = Rook(x,y)

    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        acts.extend(self.bishop_part.actions(grid, rows, cols, other_piece_locations))
        acts.extend(self.rook_part.actions(grid, rows, cols, other_piece_locations))
        return acts

class Ferz(Piece):
    name = "Ferz"
    def __init__(self, x, y):
        super().__init__(x,y,self.name)


    '''
    Takes in a State object, checks the possible moves the King can take
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)

    '''
    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        x = self.x
        y = self.y

        
        #NorthWest
        if x-1 >= 0 and y-1 >= 0:
            if grid[x-1][y-1] > 0:
                acts.append((x-1,y-1))

        #NorthEast
        if x-1 >= 0 and y+1 < cols:
            if grid[x-1][y+1] > 0:
                acts.append((x-1, y+1))

        
        #SouthWest
        if x+1 < rows and y-1 >= 0:
            if grid[x+1][y-1] > 0:
                acts.append((x+1, y-1))


        #SouthEast
        if x+1 < rows and y+1 < cols:
            if grid[x+1][y+1] > 0:
                acts.append((x+1,y+1))

        #Remove actions which step on other-piece locations
        for each in acts:
            if each in other_piece_locations:
                acts.remove(each)
        
        return acts

class Princess(Piece):
    name = "Princess"
    def __init__(self, x, y):
        super().__init__(x,y,self.name)
        self.bishop_part = Bishop(x,y)
        self.knight_part = Knight(x,y)

    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        acts.extend(self.bishop_part.actions(grid, rows, cols, other_piece_locations))
        acts.extend(self.knight_part.actions(grid, rows, cols, other_piece_locations))
        return acts

class Empress(Piece):
    name = "Empress"
    def __init__(self, x, y):
        super().__init__(x,y,self.name)
        self.rook_part = Rook(x,y)
        self.knight_part = Knight(x,y)

    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        acts.extend(self.rook_part.actions(grid, rows, cols, other_piece_locations))
        acts.extend(self.knight_part.actions(grid, rows, cols, other_piece_locations))
        return acts





#############################################################################
######## Board
#############################################################################
class Board:
    enemy_pieces = []
    enemy_locations = None
    
    def __init__(self, rows, cols, grid, goals, enemies):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.goals = goals

        #Add and create enemy pieces to board
        for each in enemies:
            self.add_piece_to_board(create_piece(each))
            
        
        # Note the enemy location coordinates
        self.enemy_locations = self.get_enemy_piece_occupied_locations()
        
    
    def add_piece_to_board(self, piece):
        self.enemy_pieces.append(piece)
        # print("---- Added: " + piece.name + " at " + str((piece.x, piece.y)))
    
    def get_enemy_piece_occupied_locations(self):
        locations = []

        for piece in self.enemy_pieces:
            piece_location = (piece.x, piece.y)
            locations.append(piece_location) 
        # print(locations)
        return locations

    def is_goal(self, x,y): #state ADT: (x,y)
        if (x,y) in self.goals:
            return True
        else:
            return False

    '''
    Gets all of the threatened locations based on the pieces added
    Will not be accurate if no pieces added to the board.pieces yet
    '''
    def get_threatened_locations(self):
        threatened_locations = []
        for piece in self.enemy_pieces:
            #Get available actions of each piece, given that they know
            #where all the other pieces are.
            threatened_locations.extend(
                piece.actions(self.grid, self.rows, self.cols, self.enemy_locations))
            
        # print(threatened_locations)
        return threatened_locations 
    
    # def print_board(self):
    #     string = ""
    #     for i in range(self.rows):
    #         row = self.grid[i]
    #         for j in range(self.cols):
                
    #             col_item = row[j]
    #             if col_item < 0:
    #                 to_add = 'X'
    #                 string += to_add
    #             else:

    #                 string += str(col_item)
    #             string += " "
    #         string += "\n"
            
        
    #     print(string)
    

    # def print_board_goal(self):
    #     top_bot_line = ""
    #     x_axis = "   "
    #     for i in range(self.cols+1):
    #         top_bot_line += "__"
            
    #     for i in range(self.cols):
            
    #         x_axis += chr(i + 97)
    #         x_axis += " "
    #     print(top_bot_line)
    #     string = ""
    #     for i in range(self.rows):
    #         string += str(i)
    #         string += " |"
    #         row = self.grid[i]
    #         for j in range(self.cols):
                
    #             col_item = row[j]
    #             if col_item < 0:
    #                 to_add = 'X'
    #                 string += to_add
    #             else:
    #                 if self.is_goal(i,j):
    #                     string += "G"
    #                 else:
    #                     string += str("_")
    #             string += "|"
    #         if i == self.rows - 1:
    #             break
    #         string += "\n"
            
        
    #     print(string)
    #     print(x_axis)



#############################################################################
######## State
#############################################################################
class State:
    #State should be representing King's position
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def get_state_format(self):
        #change back to x,y
        return (col_to_txt(self.y), (self.x))
    
    def get_state_number_format(self):
        return ((self.x), (self.y))



class Node:
    def __init__(self, state, prev):
        self.state = state
        self.previous_node = prev
    
    '''
    Returns the position of the state
    '''
    def get_state_position_formatted(self):
        return self.state.get_state_format()
    
    def get_state_number_formatted(self):
        return self.state.get_state_number_format()

    def __str__(self) -> str:
        return str(self.get_state_position_formatted())
    

        






#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, enemy_pieces, own_pieces, goals):

    # print("Initialised Board")
    new_board = Board(rows, cols, grid, goals, enemy_pieces)

    board_threat_locations = new_board.get_threatened_locations()
    board_enemy_locations = new_board.enemy_locations

    #Build a scan of the board, include places that cannot be traversed in this list of no-go zone
    no_go_zone = [] #to fill with threatened locations, locations of enemies, obstacle locations
    no_go_zone.extend(board_threat_locations)
    no_go_zone.extend(board_enemy_locations)
    # print(no_go_zone)

    
    #Creating and adding own pieces
    piece = own_pieces[0] #['King', (20, 0)]

    #Create a new King object
    first_king = create_piece(piece)

    # print(first_king.x, first_king.y)
    #       row, col
    # pos actually is col->char , row
    
    #Define frontier
    frontier = []

    #Defined reached hashtable -> (x,y) : 1 or None
    reached = {}
    source_node = Node(State(first_king.x,first_king.y), None)
    frontier.append(source_node)
    
    soln_path = []
    while len(frontier) > 0:
        
        current = frontier.pop(0)
        # print("Popped: " + str(current))

        #Check if the popped node has a goal state
        if new_board.is_goal(current.state.x, current.state.y):
            soln_path = get_path(current)
            break
        
        #for each action in possible actions from current node
        #action is a tuple of numbers (x,y)
        for action in actions(current.state, grid, rows, cols):

            if action not in no_go_zone and (str(action) not in reached.keys()):
                successor = Node(State(action[0], action[1]), current)
                frontier.append(successor)
                reached[str(successor.get_state_number_formatted())] = 1
                # print("pushed: " + str(successor))
            # else:
            #     print("In reached: " + str(action))
            
    # print(new_board.print_board())
    # print(new_board.print_board_goal())
    # print(soln_path)
    return (soln_path)


########################## Helper Functions ############

'''
Creates an instance of a piece and returns it. 
Returns None if no such piece fits the description
'''
def create_piece(piece):
    piece_desc, location = piece[0], piece[1]
    ### THERE IS BUG WITH XY VALUES PLS RECHECK GRID AND ETC
    if piece_desc == "King":
        return King(x = location[0], y = location[1])
    elif piece_desc == "Rook":
        return Rook(x = location[0], y = location[1])
    elif piece_desc == "Bishop":
        return Bishop(x = location[0], y = location[1])
    elif piece_desc == "Queen":
        return Queen(x = location[0], y = location[1])
    elif piece_desc == "Knight":
        return Knight(x = location[0], y = location[1])
    elif piece_desc == "Ferz":
        return Ferz(x = location[0], y = location[1])
    elif piece_desc == "Princess":
        return Princess(x = location[0], y = location[1])
    elif piece_desc == "Empress":
        return Empress(x = location[0], y = location[1])   
    
    else:
        return None




'''
Returns String of x val, i.e the column label of a x-axis index
'''
def col_to_txt(x):
    return str(chr(ord("a") + x))


'''
Returns the path walked to get to this node
'''
def get_path(node): #Node ADT: -state: x,y -previous_node
    path = []
    current = node
    
    while current.previous_node != None:
        move_list = []
        
        move_list.insert(0, current.get_state_position_formatted())
        current = current.previous_node
        move_list.insert(0, current.get_state_position_formatted())
        path.insert(0, move_list)
    
    return path






'''
Specific to King. Takes in a State object, checks the possible moves the King can take
and checks if the coordinate at that grid is walkable ( >0 )
Then returns list possible action outcomes (x,y) from this state
@Returns list of tuple of numbers (x,y)

'''
def actions(state, grid, rows, cols):
    acts = []
    x = state.x
    y = state.y

    #Moves of a king piece
    #This needs to check, based on the king location state, grid, and enemies, where the king cannot go to
    

    #NorthWest
    if x-1 >= 0 and y-1 >= 0:
        if grid[x-1][y-1] > 0:
            acts.append((x-1,y-1))

    #North
    if x-1 >= 0:
        if grid[x-1][y] > 0:
            acts.append((x-1, y))

    #NorthEast
    if x-1 >= 0 and y+1 < cols:
        if grid[x-1][y+1] > 0:
            acts.append((x-1, y+1))

    #West
    if y-1 >= 0:
        if grid[x][y-1] > 0:
            acts.append((x, y-1))

    #East
    if y+1 < cols:
        if grid[x][y+1] > 0:
            acts.append((x, y+1))
            
    #SouthWest
    if x+1 < rows and y-1 >= 0:
        if grid[x+1][y-1] > 0:
            acts.append((x+1, y-1))

    #South
    if x+1 < rows:
        if grid[x+1][y] > 0:
            acts.append((x+1, y))

    #SouthEast
    if x+1 < rows and y+1 < cols:
        if grid[x+1][y+1] > 0:
            acts.append((x+1,y+1))


    return acts
    







#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline())) # Integer
    cols = int(get_par(handle.readline())) # Integer
    grid = [[1 for j in range(cols)] for i in range(rows)] # Dictionary, label empty spaces as 1 (Default Step Cost)
    enemy_pieces = [] # List
    own_pieces = [] # List
    goals = [] # List

    handle.readline()  # Ignore number of obstacles
    for ch_coord in get_par(handle.readline()).split():  # Init obstacles
        r, c = from_chess_coord(ch_coord)
        grid[r][c] = -1 # Label Obstacle as -1

    handle.readline()  # Ignore Step Cost header
    line = handle.readline()
    while line.startswith("["):
        line = line[1:-2].split(",")
        r, c = from_chess_coord(line[0])
        grid[r][c] = int(line[1]) if grid[r][c] == 1 else grid[r][c] #Reinitialize step cost for coordinates with different costs
        line = handle.readline()
    
    line = handle.readline() # Read Enemy Position
    while line.startswith("["):
        line = line[1:-2]
        piece = add_piece(line)
        enemy_pieces.append(piece)
        line = handle.readline()

    # Read Own King Position
    line = handle.readline()[1:-2]
    piece = add_piece(line)
    own_pieces.append(piece)

    # Read Goal Positions
    for ch_coord in get_par(handle.readline()).split():
        r, c = from_chess_coord(ch_coord)
        goals.append((r, c))
    
    return rows, cols, grid, enemy_pieces, own_pieces, goals

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [piece, (r,c)]

def from_chess_coord(ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

#############################################################################
######## Main function to be called
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# To return: List of moves
# Return Format Example: [[('a', 0), ('a', 1)], [('a', 1), ('c', 3)], [('c', 3), ('d', 5)]]
def run_BFS():    
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    moves = search(rows, cols, grid, enemy_pieces, own_pieces, goals)
    return moves


# #May need to remove before submitting
run_BFS()
# rows, cols, grid, enemy_pieces, own_pieces, goals = parse("2.txt")


# print(enemy_pieces, own_pieces)
# enemy_locations = get_piece_locations(enemy_pieces)

# newBoard = Board(rows, cols, grid, goals, enemy_pieces)

# newBoard.print_board()

# newBoard.print_board_goal()
    