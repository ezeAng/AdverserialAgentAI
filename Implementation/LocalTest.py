import cProfile
from random import Random, randint
import sys
##To submit


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
    icon = "♔"

    def __init__(self, x, y):
        super().__init__(x,y,self.name)

    
    '''
    Takes in a board state or config, checks the possible threats the King can make
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)
    '''
    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        x = self.x
        y = self.y

        threatens = 0
        

        #Gets possible locations, given the board limits and obstacles 
        #(Does not remove locations with pieces or threatened locations)
        #NorthWest
        if x-1 >= 0 and y-1 >= 0: #e.g this checks board limits
            if grid[x-1][y-1] >= 0: #this checks if its not an obstacle
                
                if (x-1, y-1) in other_piece_locations:
                    threatens += 1

        #North
        if x-1 >= 0:
            if grid[x-1][y] >= 0:

                if (x-1, y) in other_piece_locations:
                    threatens += 1

        #NorthEast
        if x-1 >= 0 and y+1 < cols:
            if grid[x-1][y+1] >= 0:

                if (x-1, y+1) in other_piece_locations:
                    threatens += 1

        #West
        if y-1 >= 0:
            if grid[x][y-1] >= 0:

                if (x, y-1) in other_piece_locations:
                    threatens += 1

        #East
        if y+1 < cols:
            if grid[x][y+1] >= 0:

                if (x, y+1) in other_piece_locations:
                    threatens += 1
                
        #SouthWest
        if x+1 < rows and y-1 >= 0:
            if grid[x+1][y-1] >= 0:

                if (x+1, y-1) in other_piece_locations:
                    threatens += 1

        #South
        if x+1 < rows:
            if grid[x+1][y] >= 0:

                if (x+1,y) in other_piece_locations:
                    threatens += 1

        #SouthEast
        if x+1 < rows and y+1 < cols:
            if grid[x+1][y+1] >= 0:

                if (x+1,y+1) in other_piece_locations:
                    threatens += 1
        
        
        return (acts, threatens)
        
class Knight(Piece):
    name = "Knight"
    icon = "♘"

    def __init__(self, x, y):
        super().__init__(x,y ,self.name)

    '''
    Returns a list of action locations, which the knight can move to from its current location,
    that are unoccupied by any other pieces and not an obstacle
    This also works to find out the threat locations of a piece
    '''
    def actions(self, grid, rows, cols, other_piece_locations):
        
        x = self.x
        y = self.y

        threatens = 0

        #|-
        #|
        if y+1 < cols and x-2 >= 0:
            if grid[x-2][y+1] >= 0:
                if (x-2, y+1) in other_piece_locations:
                    threatens += 1
            

        #---
        #|
        if y+2 < cols and x-1 >= 0:
            if grid[x-1][y+2] >= 0:
                if (x-1, y+2) in other_piece_locations:
                    threatens += 1

        #|
        #---
        if y+2 < cols and x+1 < rows:
            if grid[x+1][y+2] >= 0:
                if (x+1, y+2) in other_piece_locations:
                    threatens += 1


        #|
        #|-
        if y+1 < cols and x+2 < rows:
            if grid[x+2][y+1] >= 0:
                if (x+2, y+1) in other_piece_locations:
                    threatens += 1

        # |
        #-|
        if y-1 >= 0 and x+2 < rows:
            if grid[x+2][y-1] >= 0:
                if (x+2, y-1) in other_piece_locations:
                    threatens += 1

        #   |
        #---
        if y-2 >= 0 and x+1 < rows:
            if grid[x+1][y-2] >= 0:
                if (x+1, y-2) in other_piece_locations:
                    threatens += 1


        #-|
        # |
        if y-1 >= 0 and x-2 >= 0:
            if grid[x-2][y-1] >= 0:
                if (x-2, y-1) in other_piece_locations:
                    threatens += 1
            

        #---
        #|
        if y-2 >= 0 and x-1 >= 0:
            if grid[x-1][y-2] >= 0:
                if (x-1, y-2) in other_piece_locations:
                    threatens += 1

        return ([], threatens)
        # return acts

class Rook(Piece):
    name = "Rook"
    icon = "♖"
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

        threatens = 0
        #North
        x_avail = x
        for i in range(1, x_avail+1):
            # if grid[x-i][y] >= 0 and (x-i, y) not in other_piece_locations:
            #     #if the spot is movable -> no obstacle and no piece blocking
            #     acts.append((x-i,y))
            
            if grid[x-i][y] >= 0 and (x-i,y) in other_piece_locations:
                #if spot if only movable, but is in other piece locations
                # acts.append((x-i,y))
                threatens += 1
                break
            else: 
                #we have to break here due to obstacle or piece block
                break

        #East
        y_avail = cols - y - 1
        for i in range(1, y_avail+1):
            
            # if grid[x][y+i] >= 0 and (x, y+i) not in other_piece_locations:
            #     #if the spot is movable -> no obstacle and no piece blocking
            #     acts.append((x,y+i))
            if grid[x][y+i] >= 0 and (x, y+i) in other_piece_locations:
                #if spot if only movable, but is in other piece locations
                # acts.append((x,y+i))
                threatens += 1
                break
            else:   
                #we have to break here due to obstacle or piece block
                break

        #South
        x_avail = rows - x - 1
        for i in range(1, x_avail+1):
            # if grid[x+i][y] >= 0 and (x+i, y) not in other_piece_locations:
            #     #if the spot is movable -> no obstacle and no piece blocking
            #     acts.append((x+i,y))
            if grid[x+i][y] >= 0 and (x+i,y) in other_piece_locations:
                #if spot if only movable, but is in other piece locations
                # acts.append((x+i,y))
                threatens += 1
                break
            else:
                #we have to break here due to obstacle or piece block
                break


        #West
        y_avail = y
        for i in range(1, y_avail+1):
            # if grid[x][y-i] >= 0 and (x, y-i) not in other_piece_locations:
            #     #if the spot is movable -> no obstacle and no piece blocking
            #     acts.append((x,y-i))
            if grid[x][y-i] >= 0 and (x, y-i) in other_piece_locations:
                #if spot if only movable, but is in other piece locations
                # acts.append((x,y-i))
                threatens += 1
                break
            else:   
                #we have to break here due to obstacle or piece block
                break

        
        return (acts, threatens)

class Bishop(Piece):
    name = "Bishop"
    icon = "♗"

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

        threatens = 0
        
        #NorthWest
        x_avail = x
        y_avail = y
        while x_avail - 1 >= 0 and y_avail - 1 >= 0:
            # if grid[x_avail-1][y_avail-1] >= 0 and ((x_avail-1, y_avail-1) not in other_piece_locations):
            #     #if the spot is movable -> no obstacle and no piece blocking
                
            #     acts.append((x_avail-1, y_avail-1))
            #     x_avail -= 1
            #     y_avail -= 1
            if grid[x_avail-1][y_avail-1] >= 0 and ((x_avail-1, y_avail-1) in other_piece_locations):
                threatens += 1
                # acts.append((x_avail-1, y_avail-1))
                break
            else:
                
                break

        
        #NorthEast
        x_avail = x
        y_avail = y
        while x_avail - 1 >= 0 and y_avail + 1 < cols:
            # if grid[x_avail-1][y_avail+1] >= 0 and ((x_avail-1, y_avail+1) not in other_piece_locations):
            #     #if the spot is movable -> no obstacle and no piece blocking
                
            #     acts.append((x_avail-1, y_avail+1))
            #     x_avail -= 1
            #     y_avail += 1

            if grid[x_avail-1][y_avail+1] >= 0 and ((x_avail-1, y_avail+1) in other_piece_locations):
                threatens += 1
                # acts.append((x_avail-1, y_avail+1))
                break

            else:
                 
                break


        #SouthEast
        x_avail = x
        y_avail = y
        while x_avail + 1 < rows and y_avail + 1 < cols:
            # if grid[x_avail+1][y_avail+1] >= 0 and ((x_avail+1, y_avail+1) not in other_piece_locations):
            #     #if the spot is movable -> no obstacle and no piece blocking
            #     acts.append((x_avail+1,y_avail+1))
            #     x_avail += 1
            #     y_avail += 1

            if grid[x_avail+1][y_avail+1] >= 0 and ((x_avail+1, y_avail+1) in other_piece_locations):
                # acts.append((x_avail+1,y_avail+1))
                threatens += 1
                break

            else:
                break

        
        #SouthWest
        x_avail = x
        y_avail = y
        while x_avail + 1 < rows and y_avail - 1 >= 0:
            # if grid[x_avail+1][y_avail-1] >= 0 and ((x_avail+1, y_avail-1) not in other_piece_locations):
            #     #if the spot is movable -> no obstacle and no piece blocking
            #     acts.append((x_avail+1, y_avail-1))
            #     x_avail += 1
            #     y_avail -= 1
            
            if grid[x_avail+1][y_avail-1] >= 0 and ((x_avail+1, y_avail-1) in other_piece_locations):
                # acts.append((x_avail+1, y_avail-1))
                threatens += 1
                break

            else: 
                break

        
        return (acts, threatens)

class Queen(Piece):
    name = "Queen"
    icon = "♕"

    def __init__(self, x, y):
        super().__init__(x,y,self.name)
        self.bishop_part = Bishop(x,y)
        self.rook_part = Rook(x,y)

    def actions(self, grid, rows, cols, other_piece_locations):
        actions_bishop = self.bishop_part.actions(grid, rows, cols, other_piece_locations)
        actions_rook = self.rook_part.actions(grid, rows, cols, other_piece_locations)
        acts = []
        # acts.extend(actions_bishop[0])
        # acts.extend(actions_rook[0])
        threatens = actions_bishop[1] + actions_rook[1]
        
        return (acts, threatens)

class Ferz(Piece):
    name = "Ferz"
    icon = "F"
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

        threatens = 0

        #NorthWest
        if x-1 >= 0 and y-1 >= 0:
            if grid[x-1][y-1] >= 0 and (x-1,y-1) in other_piece_locations:
                threatens += 1

        #NorthEast
        if x-1 >= 0 and y+1 < cols:
            if grid[x-1][y+1] >= 0 and (x-1, y+1) in other_piece_locations:
                threatens += 1

        
        #SouthWest
        if x+1 < rows and y-1 >= 0:
            if grid[x+1][y-1] >= 0 and (x+1, y-1) in other_piece_locations:
                threatens += 1


        #SouthEast
        if x+1 < rows and y+1 < cols:
            if grid[x+1][y+1] >= 0 and (x+1,y+1) in other_piece_locations:
                threatens += 1

        # #track count of which pieces ferz threaten
        # for each in other_piece_locations:
        #     if each in acts:
        #         threatens += 1
        
        return (acts, threatens)

class Princess(Piece):
    name = "Princess"
    icon = "P"

    def __init__(self, x, y):
        super().__init__(x,y,self.name)
        self.bishop_part = Bishop(x,y)
        self.knight_part = Knight(x,y)

    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []
        # acts.extend(self.bishop_part.actions(grid, rows, cols, other_piece_locations))
        # acts.extend(self.knight_part.actions(grid, rows, cols, other_piece_locations))

        actions_bishop = self.bishop_part.actions(grid, rows, cols, other_piece_locations)
        actions_knight = self.knight_part.actions(grid, rows, cols, other_piece_locations)
        # acts = []
        # acts.extend(actions_bishop[0])
        # acts.extend(actions_knight[0])
        threatens = actions_bishop[1] + actions_knight[1]
        
        return (acts, threatens)
        # return acts

class Empress(Piece):
    name = "Empress"
    icon = "E"

    def __init__(self, x, y):
        super().__init__(x,y,self.name)
        self.rook_part = Rook(x,y)
        self.knight_part = Knight(x,y)

    def actions(self, grid, rows, cols, other_piece_locations):
        acts = []

        actions_rook = self.rook_part.actions(grid, rows, cols, other_piece_locations)
        actions_knight = self.knight_part.actions(grid, rows, cols, other_piece_locations)
        # acts = []
        # acts.extend(actions_rook[0])
        # acts.extend(actions_knight[0])
        threatens = actions_rook[1] + actions_knight[1]
        
        return (acts, threatens)
        # return acts


########################## Helper Functions ############

'''
Creates an instance of a piece and returns it. 
Returns None if no such piece fits the description
'''
def create_piece(piece_desc, location):

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


#############################################################################
######## Board
#############################################################################

# Board will hold the initial board configuration and the instance will be passed into functions
# Search will create an initial board config, then pieces are added, removed and have their threat positions edited
# Board can help to retrieve the number of threats,
# State will hold the board as its actual data
class Board:
    
    def __init__(self, rows, cols, grid, pieces):
        self.rows = rows
        self.cols = cols
        self.grid = grid
        self.pieces = pieces #dictionary {loc: piece} loc is in r,c!!
        self.piece_locations = [] # in (r,c) format

        #Holds the actual piece instances
        self.init_pieces = []
    
        
        
        #Add and create initial pieces (object) to board
        for loc, piece_name in self.pieces.items():
            self.add_piece_to_board(create_piece(piece_name, loc))
            self.piece_locations.append(loc)
        
        self.threat_pairs_count = self.get_threat_pairs_count()
        # print("State threat counts:", self.threat_pairs_count)
        
        #Holds the list of pairs of pieces threatening each other
        #Populate threat pairs with current threats based on current pieces
        # self.threat_pairs = self.get_threat_pairs()

    '''
    Adds piece object instance to board
    '''
    def add_piece_to_board(self, piece):
        self.init_pieces.append(piece)
        # print("---- Added: " + piece.name + " at " + str((piece.x, piece.y)))
    
    def get_threat_pairs_count(self):
        
        threat_count = 0
        for piece in self.init_pieces:
            
            #Get the threatened locations of each piece, given current board
            
            threat_locs = piece.actions(self.grid, self.rows, self.cols, self.piece_locations)
            
            threat_count += threat_locs[1]
            
        return threat_count
    
    
    # def get_threat_pairs(self):

    #     threat_pairs_new = {}
        
    #     for piece in self.init_pieces:
            
    #         #Get the threatened locations of each piece, given current board
            
    #         threat_locs = piece.actions(self.grid, self.rows, self.cols, self.piece_locations)
            
    #         #Checks the threatened locations for pieces
    #         for loc in threat_locs:
    #             if loc in self.piece_locations:
    #                 if (piece.name,piece.x,piece.y) in threat_pairs_new.keys():
    #                     threat_pairs_new[(piece.name,piece.x,piece.y)].append((self.pieces[loc],loc[0],loc[1]))
                    
    #                 else:
    #                     threat_pairs_new[(piece.name,piece.x,piece.y)] = []
    #                     threat_pairs_new[(piece.name,piece.x,piece.y)].append((self.pieces[loc],loc[0],loc[1]))
    #     return threat_pairs_new

    # def print_statistics(self):
    #     print("Pieces: ", self.pieces)
    #     print("Piece Locations: ", self.piece_locations)
    #     print("Length of objects i.e init pieces:", len(self.init_pieces))
    #     # print("Threat pairs dict: ", self.threat_pairs)

    #     print("Board layout \n")
    #     self.print_board()
    #     return

    # def print_board(self):
    #     top_bot_line = " "
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
    #                 if (i,j) in self.piece_locations:
    #                     for piece in self.init_pieces:
    #                         if piece.x == i and piece.y == j:
    #                             string += piece.icon
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

    def __init__(self, board, k):
        self.k = k
        self.board = board
        self.num_pieces = len(board.init_pieces)
        self.value_ = - self.value() ## MAKE SURE THIS IS NEGATIVE

    # State should hold info on: #Maybe each state creates a board instance? or references board static
    # 1) which pieces are still on the board and their locations
    # 2) number of pieces removed or num remaining
    # 3) Number of threats by 1 piece to another

    '''
    Returns possible new states of the current state
    '''
    def actions(self):
        new_states = []
        
        #If at this state, we have already reached limit, then we cannot remove anymore
        if self.num_pieces <= int(self.k):
            return new_states
        
        for each_piece in self.board.init_pieces:
            new_pieces = self.board.pieces.copy()
            new_pieces.pop((each_piece.x, each_piece.y))
            new_board = Board(self.board.rows, self.board.cols, self.board.grid, new_pieces)
            new_state = State(new_board, self.k)

            new_states.append((new_state.value_, new_state))

        return new_states

    def get_highest_valued_successor(self):
        #selects action (a State) which leads to best value
        list_actions = self.actions()
        if list_actions:
            return max(list_actions)[1]
        else:
            return None

        
    def value(self):
        return self.board.threat_pairs_count


    '''
    Takes a state instance as input
    Returns boolean depending on whether it is a goal state
    '''
    
    def is_goal(self, k):
        #IF 2) >= k and 3) == 0 then return true, else false
        if self.num_pieces >= k and self.value_ == 0:
            return True
        else:
            return False
        
    # def print_statistics(self):
    #     print("------ State Statistics  ------ \n")
    #     print("Num pieces: ", self.num_pieces)
    #     print("K remaining limit: ", self.k)
    #     print("Value: ", self.value_)
    #     print("Is goal? ", self.is_goal(self.k))
    #     self.board.print_statistics()
    #     print("------ END OF State Statistics  ------")
        
    def __eq__(self, other):
        return self.value_ == other.value_
    def __lt__(self, other):
        return self.value_ < other.value_


#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, pieces, k):
    
    
    num_pieces = len(pieces)
    required_remaining_limit = int(k)
    
    
    #Initial board configuration
    init_board = Board(rows, cols, grid, pieces)

    # init_board.print_board()
    # init_board.print_statistics()

    initial_state = State(init_board, required_remaining_limit)
    

    #get all actions
    all_actions = initial_state.actions()
    random_actions_history = set()

    def random_initial_state(all_actions):  
        #randomly pick a state from the actions (i.e which piece to remove)
        
        while True:
            random_index = randint(0,len(all_actions)-1)
            if random_index not in random_actions_history:
                random_actions_history.add(random_index)
                return all_actions[random_index][1]

    current = None
    
    outer_limit = 1000 #outer_limit > 0 and 
    while outer_limit > 0 and (current is None or not current.is_goal(required_remaining_limit)):
        outer_limit -= 1
        inner_limit = 100
        current = random_initial_state(all_actions)
        while inner_limit > 0:
            inner_limit -= 1
            if (not current is None) and current.is_goal(required_remaining_limit):
                break
        
            neighbour = current.get_highest_valued_successor()
            
            if ((neighbour is None)) or (neighbour.value_ < current.value_):
                break #if no better neighbour or neighbour is none then we stop
            #else we continue with this better-equal neighbour
            current = neighbour #neighbour

    # current.print_statistics()
    # print("Ended with:",  current.is_goal(int(k)))

    ## Formatting
    formatted_result = {

    }
    for rc_loc, piece_name in current.board.pieces.items():
        formatted_tup = (col_to_txt(rc_loc[1]), rc_loc[0])
        formatted_result[formatted_tup] = piece_name
    
    return formatted_result


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]
    k = 0
    pieces = {}

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    k = handle.readline().split(":")[1] # Read in value of k

    piece_nums = get_par(handle.readline()).split()
    num_pieces = 0
    for num in piece_nums:
        num_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        pieces[coords] = piece    

    return rows, cols, grid, pieces, k

def add_piece( comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

#Returns row and col index in integers respectively
def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, pieces, k = parse(testcase)
    goalstate = search(rows, cols, grid, pieces, k)
    return goalstate #Format to be returned

# rows, cols, grid, pieces, k = parse('Local1.txt')
# res = search(rows, cols, grid, pieces, k)
# cProfile.run("search(rows, cols, grid, pieces, k)")
# print(res)