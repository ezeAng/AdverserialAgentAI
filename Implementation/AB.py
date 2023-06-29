import cProfile
import copy




# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece
#############################################################################
class Piece:
    def __init__(self, x, y, name, is_white):
        self.x = x
        self.y = y
        self.name = name
        self.is_white = is_white

        
class Pawn(Piece):
    name = "Pawn"
    worth = 1 #piece worthiness 
    black_icon = "♙"
    white_icon = "♟"
    icon = white_icon

    def __init__(self, x, y, is_white):
        super().__init__(x, y, self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth

    
    '''
    Takes in a board state or config, checks the possible moves the pawn can make
    other_piece_locations refers to the piece locations that are of the enemy
    
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)
    '''
    def actions(self, board, enemy_locations, allied_locations):
        
        x = self.x
        y = self.y
        is_white = self.is_white
        rows = board.rows
        cols = board.cols
        

        movement = []
        kills = []


        if is_white:
            #SouthWest - only available when there is piece to eat
            if x+1 < rows and y-1 >= 0 and (x+1, y-1) in allied_locations:
                kills.append((x+1, y-1))

            #South
            if x+1 < rows and (x+1,y) not in enemy_locations and (x+1,y) not in allied_locations:
                movement.append((x+1, y))

            #SouthEast - only available when there is piece to eat
            if x+1 < rows and y+1 < cols and (x+1,y+1) in enemy_locations:
                kills.append((x+1,y+1))

                
        else:
            #black moves up- only
            #Gets possible locations, given the board limits and obstacles 
            #(Does not remove locations with pieces or threatened locations)

            #NorthWest - only available when there is piece to eat
            if (x-1, y-1) in enemy_locations and x-1 >= 0 and y-1 >= 0: #e.g this checks board limits and piece to eat
                kills.append((x-1, y-1))
        
            #North
            if x-1 >= 0 and (x-1, y) not in enemy_locations and (x-1, y) not in allied_locations:
                movement.append((x-1, y))

            #NorthEast - only available when there is piece to eat
            if (x-1, y+1) in enemy_locations and x-1 >= 0 and y+1 < cols: #e.g this checks board limits and piece to eat
                kills.append((x-1, y+1))
        

        return {'movement': movement, 'kills' : kills}

class King(Piece):
    name = "King"
    icon = "♔"
    black_icon = "♔"
    white_icon = "♚"
    worth = 1000

    def __init__(self, x, y, is_white):
        super().__init__(x,y, self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth

    
    '''
    Takes in a board state or config, checks the possible threats the King can make
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)
    '''
    def actions(self, board, enemy_locations, allied_locations):
        x = self.x
        y = self.y
        # is_white = self.is_white
        rows = board.rows
        cols = board.cols
        # other_piece_locations = board.get_opposing_locations(is_white).keys()
        # own_piece_locations = board.get_opposing_locations(not is_white).keys()

        movement = []
        kills = []

        
        #Gets possible locations, given the board limits
        #(Does not remove locations with pieces or threatened locations)
        #NorthWest
        if x-1 >= 0 and y-1 >= 0: #e.g this checks board limits
            if (x-1, y-1) in enemy_locations:
                kills.append((x-1, y-1))
            elif (x-1, y-1) not in allied_locations:
                movement.append((x-1, y-1))

        #North
        if x-1 >= 0:
            if (x-1, y) in enemy_locations:
                kills.append((x-1, y))
            elif (x-1, y) not in allied_locations:
                movement.append((x-1, y))

        #NorthEast
        if x-1 >= 0 and y+1 < cols:
            if (x-1, y+1) in enemy_locations:
                kills.append((x-1, y+1))
            elif (x-1, y+1) not in allied_locations:
                movement.append((x-1, y+1))

        #West
        if y-1 >= 0:
            if (x, y-1) in enemy_locations:
                kills.append((x, y-1))
            elif (x, y-1) not in allied_locations:
                movement.append((x, y-1))

        #East
        if y+1 < cols:
            if (x, y+1) in enemy_locations:
                kills.append((x, y+1))
            elif (x, y+1) not in allied_locations:
                movement.append((x, y+1))
                
        #SouthWest
        if x+1 < rows and y-1 >= 0:
            if (x+1, y-1) in enemy_locations:
                kills.append((x+1, y-1))
            elif (x+1, y-1) not in allied_locations:
                movement.append((x+1, y-1))

        #South
        if x+1 < rows:
            if (x+1,y) in enemy_locations:
                kills.append((x+1, y))
            elif (x+1, y) not in allied_locations:
                movement.append((x+1, y))

        #SouthEast
        if x+1 < rows and y+1 < cols:
            if (x+1,y+1) in enemy_locations:
                kills.append((x+1, y+1))
            elif (x+1, y+1) not in allied_locations:
                movement.append((x+1, y+1))
        
        
        return {'movement': movement, 'kills': kills}
       
class Knight(Piece):
    name = "Knight"
    icon = "♘"
    black_icon = "♘"
    white_icon = "♞"
    worth = 3

    def __init__(self, x, y, is_white):
        super().__init__(x, y, self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth

    '''
    Returns a list of action locations, which the knight can move to from its current location,
    that are unoccupied by any other pieces and not an obstacle
    This also works to find out the threat locations of a piece
    '''
    def actions(self, board, enemy_locations, allied_locations):
        
        rows = board.rows
        cols = board.cols
        x = self.x
        y = self.y
        # other_piece_locations = board.get_opposing_locations(self.is_white).keys()
        # own_piece_locations = board.get_opposing_locations(not self.is_white).keys()

        movement = []
        kills = []

        #|-
        #|
        if y+1 < cols and x-2 >= 0:
            if (x-2, y+1) in enemy_locations:
                kills.append((x-2, y+1))
            elif (x-2, y+1) not in allied_locations:
                movement.append((x-2, y+1))
            
            

        #---
        #|
        if y+2 < cols and x-1 >= 0:
            if (x-1, y+2) in enemy_locations:
                kills.append((x-1, y+2))
            elif (x-1, y+2) not in allied_locations:
                movement.append((x-1, y+2))

        #|
        #---
        if y+2 < cols and x+1 < rows:
            if (x+1, y+2) in enemy_locations:
                kills.append((x+1, y+2))
            elif (x+1, y+2) not in allied_locations:
                movement.append((x+1, y+2))


        #|
        #|-
        if y+1 < cols and x+2 < rows:
            if (x+2, y+1) in enemy_locations:
                kills.append((x+2, y+1))
            elif (x+2, y+1) not in allied_locations:
                movement.append((x+2, y+1))

        # |
        #-|
        if y-1 >= 0 and x+2 < rows:
            if (x+2, y-1) in enemy_locations:
                kills.append((x+2, y-1))
            elif (x+2, y-1) not in allied_locations:
                movement.append((x+2, y-1))

        #   |
        #---
        if y-2 >= 0 and x+1 < rows:
            if (x+1, y-2) in enemy_locations:
                kills.append((x+1, y-2))
            elif (x+1, y-2) not in allied_locations:
                movement.append((x+1, y-2))


        #-|
        # |
        if y-1 >= 0 and x-2 >= 0:
            if (x-2, y-1) in enemy_locations:
                kills.append((x-2, y-1))
            elif (x-2, y-1) not in allied_locations:
                movement.append((x-2, y-1))
            

        #---
        #|
        if y-2 >= 0 and x-1 >= 0:
            if (x-1, y-2) in enemy_locations:
                kills.append((x-1, y-2))
            elif (x-1, y-2) not in allied_locations:
                movement.append((x-1, y-2))

        return {'movement': movement, 'kills': kills}

class Rook(Piece):
    name = "Rook"
    icon = "♖"
    white_icon = "♖"
    black_icon = "♜"
    worth = 5
    #Lists the possible moves, specifically changes in the x,y directions (reference pt top left of board)
    # the numbers correspond to the limit of how much the direction val can be changed
    #e.g queen will then be able to move the entire board

    #Rook movement
    #       ^
    #       |
    #  <--- R --->
    #       |
    #       v


    def __init__(self, x, y, is_white):
        super().__init__(x, y, self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth

    
        '''
    Takes in a State object, checks the possible moves the King can take
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)

    '''
    def actions(self, board, enemy_locations, allied_locations):
        rows = board.rows
        cols = board.cols
        x = self.x
        y = self.y
        # opposing_piece_locations = board.get_opposing_locations(self.is_white).keys()
        # allied_piece_locations = board.get_opposing_locations(not self.is_white).keys()
        movement = []
        kills = []


        #North
        x_avail = x
        for i in range(1, x_avail+1):
            #if the spot is movable -> no obstacle and no piece blocking
            if (x-i, y) in enemy_locations:
                kills.append((x-i, y))
                break
            elif (x-i, y) in allied_locations:
                break
            else:
                movement.append((x-i,y))

        #East
        y_avail = cols - y - 1
        for i in range(1, y_avail+1):
            if (x, y+i) in enemy_locations:
                kills.append((x, y+i))
                break
            elif (x, y+i) in allied_locations:
                break
            else:
                movement.append((x, y+i))

            

        #South
        x_avail = rows - x - 1
        for i in range(1, x_avail+1):
            if (x+i,y) in enemy_locations:
                kills.append((x+i,y))
                break
            elif (x+i, y) in allied_locations:
                break
            else:
                movement.append((x+i,y))


        #West
        y_avail = y
        for i in range(1, y_avail+1):
            if (x, y-i) in enemy_locations:
                kills.append((x, y-i))
                break
            elif (x, y-i) in allied_locations:
                break
            else:   
                movement.append((x, y-i))

        
        return {'movement': movement, 'kills': kills}

class Bishop(Piece):
    name = "Bishop"
    icon = "♗"
    black_icon = "♗"
    white_icon = "♝"
    worth = 3

    #Lists the possible moves, specifically changes in the x,y directions (reference pt top left of board)
    # the numbers correspond to the limit of how much the direction val can be changed
    #e.g queen will then be able to move the entire board

    #Bishop movement
    #   ^       ^
    #    \     /
    #       R
    #    /     \
    #   v       v


    def __init__(self, x, y, is_white):
        super().__init__(x, y, self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth

    
    '''
    Takes in a State object, checks the possible moves the Bishop can take
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)

    '''
    def actions(self, board, enemy_locations, allied_locations):
        
        x = self.x
        y = self.y
        rows = board.rows
        cols = board.cols
        kills = []
        movement = []
        # opposing_piece_locations = board.get_opposing_locations(self.is_white).keys()
        # allied_piece_locations = board.get_opposing_locations(not self.is_white).keys()
        
        #NorthWest
        x_avail = x
        y_avail = y
        while x_avail - 1 >= 0 and y_avail - 1 >= 0:
            if ((x_avail-1, y_avail-1) in enemy_locations):
                kills.append((x_avail-1, y_avail-1))
                break
            elif ((x_avail-1, y_avail-1) in allied_locations):
                break
            else:
                movement.append((x_avail-1, y_avail-1))
                x_avail -= 1
                y_avail -= 1

        
        #NorthEast
        x_avail = x
        y_avail = y
        while x_avail - 1 >= 0 and y_avail + 1 < cols:
            if ((x_avail-1, y_avail+1) in enemy_locations):
                kills.append((x_avail-1, y_avail+1))
                break
            elif ((x_avail-1, y_avail+1) in allied_locations):
                break
            else:
                movement.append((x_avail-1, y_avail+1))
                x_avail -= 1
                y_avail += 1
                


        #SouthEast
        x_avail = x
        y_avail = y
        while x_avail + 1 < rows and y_avail + 1 < cols:
            if ((x_avail+1, y_avail+1) in enemy_locations):
                kills.append((x_avail+1,y_avail+1))
                break
            elif ((x_avail+1, y_avail+1) in allied_locations):
                break
            else:
                movement.append((x_avail+1, y_avail+1))
                x_avail += 1
                y_avail += 1

        
        #SouthWest
        x_avail = x
        y_avail = y
        while x_avail + 1 < rows and y_avail - 1 >= 0:
            if ((x_avail+1, y_avail-1) in enemy_locations):
                kills.append((x_avail+1, y_avail-1))
                break
            elif ((x_avail+1, y_avail-1) in allied_locations):
                break
            else: 
                movement.append((x_avail+1, y_avail-1))
                x_avail += 1
                y_avail -= 1  

        
        return {'movement': movement, 'kills': kills}

class Queen(Piece):
    name = "Queen"
    icon = "♕"
    white_icon = "♛"
    black_icon = "♕"
    worth = 9


    def __init__(self, x, y, is_white):
        super().__init__(x,y,self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth
        
        self.bishop_part = Bishop(x,y, is_white)
        self.rook_part = Rook(x,y, is_white)
        
        

    def actions(self, board, enemy_locations, allied_locations):
        actions_bishop = self.bishop_part.actions(board, enemy_locations, allied_locations)
        actions_rook = self.rook_part.actions(board, enemy_locations, allied_locations)
        
        movement = []
        movement.extend(actions_bishop['movement'])
        movement.extend(actions_rook['movement'])

        kills = []
        kills.extend(actions_bishop['kills'])
        kills.extend(actions_rook['kills'])

        
        return {'movement': movement, 'kills': kills}

class Ferz(Piece):
    name = "Ferz"
    white_icon = "F"
    black_icon = "ｷ"
    icon = ""
    worth = 2

    def __init__(self, x, y, is_white):
        super().__init__(x,y,self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth


    '''
    Takes in a State object, checks the possible moves the King can take
    and checks if the coordinate at that grid is walkable ( >0 )
    Then returns list possible action outcomes (x,y) from this state
    @Returns list of tuple of numbers (x,y)

    '''
    def actions(self, board, enemy_locations, allied_locations):
        x = self.x
        y = self.y
        rows = board.rows
        cols = board.cols

        movement = []
        kills = []
        # other_piece_locations = board.get_opposing_locations(self.is_white).keys()
        # own_piece_locations = board.get_opposing_locations(not self.is_white).keys()

        #NorthWest
        if x-1 >= 0 and y-1 >= 0:
            if (x-1,y-1) in enemy_locations:
                kills.append((x-1,y-1))
            elif (x-1,y-1) not in allied_locations:
                movement.append((x-1,y-1))

        #NorthEast
        if x-1 >= 0 and y+1 < cols:
            if (x-1, y+1) in enemy_locations:
                kills.append((x-1, y+1))
            elif (x-1, y+1) not in allied_locations:
                movement.append((x-1, y+1))

        
        #SouthWest
        if x+1 < rows and y-1 >= 0:
            if (x+1, y-1) in enemy_locations:
                kills.append((x+1, y-1))
            elif (x+1, y-1) not in allied_locations:
                movement.append((x+1, y-1))


        #SouthEast
        if x+1 < rows and y+1 < cols:
            if (x+1,y+1) in enemy_locations:
                kills.append((x+1,y+1))
            elif (x+1, y+1) not in allied_locations:
                movement.append((x+1,y+1))


        
        return {'movement': movement, 'kills': kills}

class Princess(Piece):
    name = "Princess"
    white_icon = "P"
    black_icon = "$"
    icon = ""
    worth = 6

    def __init__(self, x, y, is_white):
        super().__init__(x,y,self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth
        self.bishop_part = Bishop(x,y, is_white)
        self.knight_part = Knight(x,y, is_white)

    def actions(self, board, enemy_locations, allied_locations):
        
        actions_bishop = self.bishop_part.actions(board, enemy_locations, allied_locations)
        actions_knight = self.knight_part.actions(board, enemy_locations, allied_locations)
        movement = []
        movement.extend(actions_bishop['movement'])
        movement.extend(actions_knight['movement'])

        kills = []
        kills.extend(actions_bishop['kills'])
        kills.extend(actions_knight['kills'])

        return {'movement': movement, 'kills': kills}

class Empress(Piece):
    name = "Empress"
    white_icon = "E"
    black_icon = "ἐ"
    icon = ""
    
    worth = 8

    def __init__(self, x, y, is_white):
        super().__init__(x,y,self.name, is_white)
        if is_white:
            self.icon = self.white_icon
        else:
            self.icon = self.black_icon
            self.worth = -1 * self.worth
        self.rook_part = Rook(x,y, is_white)
        self.knight_part = Knight(x,y, is_white)

    def actions(self, board, enemy_locations, allied_locations):

        actions_rook = self.rook_part.actions(board, enemy_locations, allied_locations)
        actions_knight = self.knight_part.actions(board, enemy_locations, allied_locations)

        movement = []
        movement.extend(actions_rook['movement'])
        movement.extend(actions_knight['movement'])

        kills = []
        kills.extend(actions_rook['kills'])
        kills.extend(actions_knight['kills'])

        return {'movement': movement, 'kills': kills}
  

########################## Helper Functions ############

'''
Creates an instance of a piece with r,c locations and colour and returns it. 
Returns None if no such piece fits the description
'''
def create_piece(location, colour, piece_desc):
    if colour == 'White':
        is_white = True
    else:
        is_white = False

    if piece_desc == "King":
        return King(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Rook":
        return Rook(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Bishop":
        return Bishop(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Queen":
        return Queen(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Knight":
        return Knight(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Ferz":
        return Ferz(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Princess":
        return Princess(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Empress":
        return Empress(x = location[0], y = location[1], is_white = is_white)
    elif piece_desc == "Pawn":
        return Pawn(x= location[0], y = location[1], is_white = is_white)   
    else:
        return None

'''
Returns String of x val, i.e the column label of a x-axis index
'''
def col_to_txt(x):
    return str(chr(ord("a") + x))

def rc_to_si(rc_tup):
    return (col_to_txt(rc_tup[1]), rc_tup[0])

def from_chess_coord(ch_coord):
    return (int(ch_coord[1]), ord(ch_coord[0]) - 97)

def board_to_rc_board(input_gameboard):
    
    new_gameboard = {

    }
    for si_loc, piece_data in input_gameboard.items():
        rc_loc = from_chess_coord(si_loc)
        new_gameboard[rc_loc] = piece_data
            
    return new_gameboard

class Board:
    
    def __init__(self, gameboard):
        self.rows = 7 #FIXED
        self.cols = 7 #FIXED

        # gameboard example: {(r, c) : ('Queen', 'White'), (r, c) : ('Rook', 'White')}
        self.gameboard = gameboard
        
        self.piece_locations = {
            'White' : {},
            'Black' : {}
        } # in (r,c) format 'White' : { rc_loc : piece_type }

        #Holds the actual piece instances in format rc_loc : piece_instance
        self.init_pieces = {

        }
    
        
        #Add and create initial pieces (object) to board - loc is in (col-string, int)
        for rc_loc, piece_data in gameboard.items():
            
            piece = create_piece(rc_loc, piece_data[1], piece_data[0])

            # Add actual pieces to board
            self.add_piece_to_board(rc_loc, piece)

            #Separates white and black sets - creates nested dict
            self.piece_locations[piece_data[1]][rc_loc] = piece_data[0]
            
        
    '''
    Adds piece object instance to board
    '''
    def add_piece_to_board(self, loc, piece):
        self.init_pieces[loc] = piece
    
    '''
    Returns a dict of {loc: piece type, loc2: piece-type2, ... } of opposing pieces
    '''
    def get_opposing_locations(self, is_white):
        if is_white:
            return self.piece_locations['Black']
        else:
            return self.piece_locations['White']

    def remove_piece_from_board(self, piece, loc, type):
        pass

    def get_sum_values(self):
        sum = 0
        for piece in self.init_pieces.values():
            sum += piece.worth
        return sum

    

    def print_statistics(self):
        print("Gameboard: ", self.gameboard)
        print("Value: ", self.get_sum_values())
        print("Piece Locations: ", self.piece_locations)
        print("Number of pieces on board i.e init pieces:", len(self.init_pieces.items()))

        print("Board layout \n")
        self.print_board()
        return

    def print_board(self):
        top_bot_line = " "
        x_axis = "   "
        for i in range(self.cols+1):
            top_bot_line += "__"
            
        for i in range(self.cols):
            x_axis += chr(i + 97)
            x_axis += " "
        print(top_bot_line)
        string = ""
        for i in range(self.rows):
            string += str(i)
            string += " |"
            for j in range(self.cols):
                
                if (i,j) in self.init_pieces.keys():
                    for piece in self.init_pieces.values():
                        if piece.x == i and piece.y == j:
                            string += piece.icon
                else:
                    string += str("_")
                string += "|"
            if i == self.rows - 1:
                break
            string += "\n"
        print(string)
        print(x_axis)
      

class Game:

    starting_board = {
        ('a', 5): ('Ferz', 'Black'), 
        ('b', 5): ('Pawn', 'Black'), 
        ('c', 5): ('Pawn', 'Black'),
        ('d', 5): ('Pawn', 'Black'),
        ('e', 5): ('Pawn', 'Black'),
        ('f', 5): ('Pawn', 'Black'),
        ('g', 5): ('Ferz', 'Black'),
        ('a', 6): ('Knight', 'Black'),
        ('b', 6): ('Bishop', 'Black'),
        ('c', 6) : ('Queen', 'Black'),
        ('d', 6) : ('King', 'Black'),
        ('e', 6) : ('Princess', 'Black'),
        ('f', 6) : ('Empress', 'Black'),
        ('g', 6) : ('Rook', 'Black'),

        ('a', 1): ('Ferz', 'White'), 
        ('b', 1): ('Pawn', 'White'), 
        ('c', 1): ('Pawn', 'White'),
        ('d', 1): ('Pawn', 'White'),
        ('e', 1): ('Pawn', 'White'),
        ('f', 1): ('Pawn', 'White'),
        ('g', 1): ('Ferz', 'White'),
        ('a', 0): ('Knight', 'White'),
        ('b', 0): ('Bishop', 'White'),
        ('c', 0) : ('Queen', 'White'),
        ('d', 0) : ('King', 'White'),
        ('e', 0) : ('Princess', 'White'),
        ('f', 0) : ('Empress', 'White'),
        ('g', 0) : ('Rook', 'White'),
    }

    #Make a method, which takes in a board-state, move, and turn -> output corresponding board
    def board_after_move(move, old_board):
        # from_coord = from_chess_coord(move[0])
        # to_coord = from_chess_coord(move[1])
        # print(from_coord, to_coord)
        new_board = copy.deepcopy(old_board)
        piece = new_board.pop(move[0])
        new_board[move[1]] = piece
        return new_board
    
    
    def check_terminal_state(board):
        pass

    


    def play():
        board = Game.starting_board
        # while not check_terminal_state(board):
        #     continue

class State:
    def __init__(self, board, is_white_turn): 
        self.is_white_turn = is_white_turn
        self.board = board

        #We value the states using
        # ** the sum of all the pieces, the more positive it is the better it is for white agent
        self.value = board.get_sum_values()
        

    def get_child_action_states(self):
        
        #if is white turn, next is black
        child_turn = not self.is_white_turn 

        #Initialise empty array to return possible new child states
        child_states = [] 

        current_board_config = self.board.gameboard
        #Current board pieces for reference
        opposing_locations = self.board.get_opposing_locations(self.is_white_turn)
        allied_locations = self.board.get_opposing_locations(not self.is_white_turn)

        #for each piece on the board
        for piece in self.board.init_pieces.values():
            
            #Get possible actions of each allied piece i.e same colour as user
            if piece.is_white == self.is_white_turn:
                #if piece is of this turn, get its possible actions
                cur_loc = (piece.x, piece.y)

                #current version repeats work - to change this
                actions = piece.actions(self.board, opposing_locations, allied_locations) #returns a dict {'movement': movement, 'kills': kills}

                # Add childstates where current piece is simply moved
                for each_move in actions['movement']:
                    #Clear old piece
                    
                    new_board_config = copy.deepcopy(current_board_config)
                    
                    old_piece = new_board_config.pop(cur_loc)
                    
                    #Move piece to new location
                    new_board_config[each_move] = old_piece

                    #Create new state from there and add to list of states
                    new_board = Board(new_board_config)
                    new_state = State(new_board, child_turn)

                    state_obj = {
                        "prev_loc": cur_loc,
                        "move_to": each_move,
                        "state" : new_state
                    }
                    child_states.append(state_obj)
       
                # Add childstates where a piece was eaten
                for each_move in actions['kills']:
                    #Clear old piece
                    new_board_config = copy.deepcopy(current_board_config)
                    old_piece = new_board_config.pop(cur_loc)

                    #Remove killed piece from new location
                    new_board_config.pop(each_move) 
                    
                    #Move piece to new location
                    new_board_config[each_move] = old_piece

                    #Create new state from there and add to list of states
                    new_board = Board(new_board_config)
                    new_state = State(new_board, child_turn)

                    state_obj = {
                        "prev_loc": cur_loc,
                        "move_to": each_move,
                        "state" : new_state
                    }
                    child_states.append(state_obj)
        return child_states

    def is_terminal(self):
        #If King has been slaughtered
        if 'King' not in self.board.piece_locations['White'].values() or 'King' not in self.board.piece_locations['Black'].values():
            return True
        else:
            return False


def minimax(state, depth, alpha, beta, is_white_player):
    if depth == 0 or state.is_terminal():
        return state.value, state #(eval function used here)
    
    if is_white_player:
        maxEval = float('-inf')
        best_move = None
        #Get all possible moves from current state
        for each_child_state_obj in state.get_child_action_states(): #get_child_action_states must update the board with new move location and remove any pieces eaten
            eval = minimax(each_child_state_obj['state'], depth - 1, alpha, beta, False)[0]
            if eval > maxEval:
                maxEval = eval
                best_move = each_child_state_obj

            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return maxEval, best_move
    
    else: #black turn
        minEval = float('inf')
        best_move = None
        for each_child_state_obj in state.get_child_action_states():
            eval = minimax(each_child_state_obj['state'], depth - 1, alpha, beta, True)[0]
            if eval < minEval:
                minEval = eval
                best_move = each_child_state_obj

            beta = min(beta, eval)
            if beta <= alpha:
                break
        return minEval, best_move

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(gameboard):

    #depth limit
    depth = 2
    alpha = float('-inf')
    beta = float('inf')
    is_white_player_initially = True

    #create new initial state with new gameboard
    initial_board = Board(gameboard)
    initial_state = State(initial_board, is_white_player_initially)
    

    #choose initial move
    move_obj = minimax(initial_state, depth, alpha, beta, is_white_player_initially)
    # print(move_obj)

    return (rc_to_si(move_obj[1]['prev_loc']), rc_to_si(move_obj[1]['move_to']))
    
    # move_board = move_obj[1]['state'].board
    # move_board.print_board()
    # print(move)




    



### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard):
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    # config = sys.argv[1] #OPTIONAL (Since you can hardcode the board): Takes in config.txt

    #Converts to r,c 
    adjusted_gameboard = board_to_rc_board(gameboard)
    
    move = ab(adjusted_gameboard)

    return move #Format to be returned (('a', 0), ('b', 3))


# my_move = studentAgent(Game.starting_board)
# cProfile.run('studentAgent(Game.starting_board)')

# Board(board_to_rc_board(Game.board_after_move(my_move, Game.starting_board))).print_statistics()

