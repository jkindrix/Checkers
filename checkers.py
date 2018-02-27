import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')


class Game():

    def __init__(self):
        """Game object constructor"""

        # Clear the screen
        cls()
        # Set a turn counter. Odd is RED. Even is BLACK
        self.turn = 1

        # Set number of pieces
        self.red_pieces, self.black_pieces = 12, 12

        # Create 100 square objects in a list called self.squares
        self.squares = [Square() for i in range(100)]
        
        # Create a list of patterns to display on-screen
        self.patterns = [
            "    " + "_" * 79, # 0 < top line
            "|         ", # 1
            "|_________", # 2
            "|XXXXXXXXX", # 3
            "|X|     |X", # 4
            "|X| RED |X", # 5
            "|X|BLACK|X", # 6
            "|X| KING|X", # 7
            "|X|_____|X", # 8
        ]
        p = self.patterns # Create an alias for self.patterns
        
        # Create patterns for each square in a list to be called later
        # when they need to be displayed on-screen
        self.tlp = p[0] # Top line
        self.erp = [p[1], p[1], p[1], p[1], p[2]] # Empty Red Square
        self.ebp = [p[3], p[3], p[3], p[3], p[3]] # Empty Black Square
        self.rp = [p[3], p[4], p[5], p[8], p[3]] # Red Piece
        self.rkp = [p[3], p[5], p[7], p[8], p[3]] # Red King Piece
        self.bp = [p[3], p[4], p[6], p[8], p[3]] # Black Piece
        self.bkp = [p[3], p[6], p[7], p[8], p[3]] # Black King Piece
        self.blp = ("        A         B         C         D "
                    "        E         F         G         H"
        ) # Bottom Line

        # Assign the coordinates and color attributes of each square
        # Assign the pieces to their initial locations:
        self.out_of_range = []
        i = 0
        while i < 100:
           for x in range(10):
                for y in range(10):
                    if (x < 8 and y < 8):
                        self.squares[i].x = x
                        self.squares[i].y = y
                        self.squares[i].xy = int(str(x) + str(y))
                        self.squares[i].UR = self.squares[i].xy + 11
                        self.squares[i].URUR = self.squares[i].xy + 22
                        self.squares[i].UL = self.squares[i].xy + 9
                        self.squares[i].ULUL = self.squares[i].xy + 18
                        self.squares[i].LL = self.squares[i].xy - 11
                        self.squares[i].LLLL = self.squares[i].xy - 22
                        self.squares[i].LR = self.squares[i].xy - 9
                        self.squares[i].LRLR = self.squares[i].xy - 18
                        if (x % 2 == 0 and y % 2 == 0) or (
                            x % 2 == 1 and y % 2 == 1):
                            self.squares[i].color = "black"
                            if (x < 3) and (x < 8 and y < 8):
                                self.squares[i].current_piece = "red"
                                self.squares[i].pattern = self.rp
                            elif (x > 4) and (x < 8 and y < 8):
                                self.squares[i].current_piece = "black"
                                self.squares[i].pattern = self.bp
                            else:
                                self.squares[i].current_piece = "blank"
                                self.squares[i].pattern = self.ebp
                        else:
                            self.squares[i].color = "red"
                            self.squares[i].current_piece = "blank"
                            self.squares[i].pattern = self.erp
                        if (x < 7 and y < 7):
                            self.out_of_range.append(self.squares[i].xy)
                    else: # everything else is out of the 8x8 range:
                        self.squares[i].x = "out"
                        self.squares[i].y = "out"
                        self.squares[i].xy = "out"
                        self.squares[i].color = "out"
                        self.squares[i].current_piece = "out"
                    # print("square ", i, " at ", x, y, " is", self.squares[i].color, "occupied by ", self.squares[i].current_piece)
                    i += 1

        # Create the initial display for the player
        self.display()
        self.select()
        
    def display(self):
        """Create the game display""" 
        
        cls() # Clear the screen
        print(self.tlp) # Print top line
        low, high = 70, 78 # Set the initial range of squares
        rank = 8 # Set the intial rank to print ( 8 == top row)
        
        # Loop Logic:
        #  For 8 rows of squares...
        #   For 5 lines per row...
        #    If this is the 3rd line:
        #     print the current rank
        #    Else:
        #     Print 3 spaces (as a screen offset)
        #    For each pattern in the square at the given coordinates...
        #     Print the pattern for that square in that specific line
        #     Print a Pipe character and LF/CR at the end.
        
        for row in range(8):
            for line in range(5):
                if line == 2:
                    print(" {} ".format(rank), end="")
                else:
                    print("   ", end="")
                for coordinates in range(low,high):
                    print(self.squares[coordinates].pattern[line], end="")
                print("|\n", end="")
            rank -= 1
            low -= 10
            high -= 10

        print(self.blp + "\n", end="\n") #  Print the bottom line

    def swap(self, selected, target):
        """Swap the attributes of the given squares"""

        difference = self.selected_piece.xy - self.selected_target.xy
        for x in [-22, -18, 18, 22]:
            if difference == x:
                self.captured_piece = (
                    self.squares[self.selected_piece.xy - (x //2)]
                )
                self.capture()
        
        (self.selected_piece.current_piece,
        self.selected_piece.pattern,
        self.selected_target.current_piece,
        self.selected_target.pattern
        ) = (
        self.selected_target.current_piece,
        self.selected_target.pattern,
        self.selected_piece.current_piece,
        self.selected_piece.pattern)

    def capture(self):
        """Capture the given square"""
        
        if self.captured_piece.current_piece == "black":
            self.black_pieces -= 1
        elif self.captured_piece.current_piece == "red":
            self.red_pieces -= 1

        self.captured_piece.current_piece = "blank"
        self.captured_piece.pattern = self.ebp
        
    def return_error(self, error):
        if error == "wrong direction":
            print("\nThe selected piece cannot move backward")

        elif error == "no piece":
            print("\nThere is no piece on the selected square")
            
        elif error == "opponent piece":
            print("\nYou do not own the selected piece")
        
        elif error == "no moves":
            print("\nThe selected piece has no legal moves")
        
        elif error == "illegal move":
            print("\nThe selected target is not a legal move")

        print("Please try again...", end="")
        input()
        cls()
        self.display()
        self.select()

    def check_win(self):
        if self.red_pieces == 0:
            self.game_over("red")
        if self.black_pieces == 0:
            self.game_over("black")
            
    def game_over(self, winner):
        cls()
        print("Congratulations! {0} wins!!!".format(winner))
        exit()
        
    def check_target(self):
        if self.selected_target not in self.valid_selections:
            self.return_error("illegal move")

        self.input_converter_t(self.selected_target)

        if ( 
            self.selected_piece.current_piece == "red" and
            self.selected_piece.is_king == False
        ):
            if self.selected_target.xy < self.selected_piece.xy:
                self.return_error("wrong direction")

        elif (
            self.selected_piece.current_piece == "black" and
            self.selected_piece.is_king == False
        ):
            if self.selected_target.xy > self.selected_piece.xy:
                self.return_error("wrong direction")
        
        if self.selected_target.current_piece != "blank":
            
            self.return_error("illegal move")
        
        if (
            self.selected_target.xy != self.selected_piece.xy + 9 and
            self.selected_target.xy != self.selected_piece.xy + 11 and
            self.selected_target.xy != self.selected_piece.xy + 18 and
            self.selected_target.xy != self.selected_piece.xy + 22 and
            self.selected_target.xy != self.selected_piece.xy - 9 and
            self.selected_target.xy != self.selected_piece.xy - 11 and
            self.selected_target.xy != self.selected_piece.xy - 18 and
            self.selected_target.xy != self.selected_piece.xy - 22
        ):
                self.return_error("illegal move")
        
                
    def check_selection(self):
        if self.turn % 2 == 1:
            self.opposite = "black"
        else:
            self.opposite = "red"

        if self.selected_piece not in self.valid_selections:
            self.return_error("no piece")

        self.input_converter(self.selected_piece)

        UR = self.selected_piece.UR
        self.UR = "invalid"
        URUR = self.selected_piece.URUR
        self.URUR = "invalid"
        UL = self.selected_piece.UL
        self.UL = "invalid"
        ULUL = self.selected_piece.ULUL
        self.ULUL = "invalid"
        LL = self.selected_piece.LL
        self.LL = "invalid"
        LLLL = self.selected_piece.LLLL
        self.LLLL = "invalid"
        LR = self.selected_piece.LR
        self.LR = "invalid"
        LRLR = self.selected_piece.LRLR
        self.LRLR = "invalid"
        
        if self.selected_piece.current_piece == "blank":
            self.return_error("no piece")    
            
        if self.selected_piece.current_piece == self.opposite:
                self.return_error("opponent piece")
        
        if self.squares[UR].current_piece == "blank":
            self.UR = "valid"
        if self.squares[UL].current_piece == "blank":
            self.UL = "valid"
        if self.squares[LL].current_piece == "blank":
            self.LL = "valid"
        if self.squares[LR].current_piece == "blank":
            self.LR = "valid"
        
        if (
            self.squares[UR].current_piece == self.opposite and
            self.squares[URUR].current_piece == "blank"
        ):
                self.URUR = "valid"
        if (
            self.squares[UL].current_piece == self.opposite and
            self.squares[ULUL].current_piece == "blank"
        ):
                self.ULUL = "valid"
        if (
            self.squares[LL].current_piece == self.opposite and
            self.squares[LLLL].current_piece == "blank"
        ):
                self.LLLL = "valid"
        if (
            self.squares[LR].current_piece == self.opposite and
            self.squares[LRLR].current_piece == "blank"
        ):
                self.LRLR = "valid"
                
        if (
            self.UR == "invalid" and 
            self.URUR == "invalid" and
            self.UL == "invalid" and
            self.ULUL == "invalid" and
            self.LL == "invalid" and 
            self.LLLL == "invalid" and 
            self.LR == "invalid" and 
            self.LRLR == "invalid"
        ):
            self.return_error("no moves")

    def check_king(self):
        black_king_line = [0,2,4,6]
        red_king_line = [71,73,75,77]
        if self.turn % 2 == 1:
            if self.selected_target.xy in red_king_line:
                self.selected_target.is_king = True
                self.selected_target.pattern = self.rkp
                self.selected_target.current_piece = "red king"
        elif self.turn % 2 == 0: 
            if self.selected_target.xy in black_king_line:
                self.selected_target.is_king = True
                self.selected_target.pattern = self.bkp
                self.selected_target.current_piece = "black king"

    def input_converter(self, input):

        if input == "a1":
            self.selected_piece=self.squares[0]
        if input == "a3":
            self.selected_piece=self.squares[20]
        if input == "a5":
            self.selected_piece=self.squares[40]
        if input == "a7":
            self.selected_piece=self.squares[60]
        if input == "b2":
            self.selected_piece=self.squares[11]
        if input == "b4":
            self.selected_piece=self.squares[31]
        if input == "b6":
            self.selected_piece=self.squares[51]
        if input == "b8":
            self.selected_piece=self.squares[71]
        if input == "c1":
            self.selected_piece=self.squares[2]
        if input == "c3":
            self.selected_piece=self.squares[22]
        if input == "c5":
            self.selected_piece=self.squares[42]
        if input == "c7":
            self.selected_piece=self.squares[62]
        if input == "d2":
            self.selected_piece=self.squares[13]
        if input == "d4":
            self.selected_piece=self.squares[33]
        if input == "d6":
            self.selected_piece=self.squares[53]
        if input == "d8":
            self.selected_piece=self.squares[73]
        if input == "e1":
            self.selected_piece=self.squares[4]
        if input == "e3":
            self.selected_piece=self.squares[24]
        if input == "e5":
            self.selected_piece=self.squares[44]
        if input == "e7":
            self.selected_piece=self.squares[64]
        if input == "f2":
            self.selected_piece=self.squares[15]
        if input == "f4":
            self.selected_piece=self.squares[35]
        if input == "f6":
            self.selected_piece=self.squares[55]
        if input == "f8":
            self.selected_piece=self.squares[75]
        if input == "g1":
            self.selected_piece=self.squares[6]
        if input == "g3":
            self.selected_piece=self.squares[26]
        if input == "g5":
            self.selected_piece=self.squares[46]
        if input == "g7":
            self.selected_piece=self.squares[66]
        if input == "h2":
            self.selected_piece=self.squares[17]
        if input == "h4":
            self.selected_piece=self.squares[37]
        if input == "h6":
            self.selected_piece=self.squares[57]
        if input == "h8":
            self.selected_piece=self.squares[77]

    def input_converter_t(self, input):

        if input == "a1":
            self.selected_target=self.squares[0]
        if input == "a3":
            self.selected_target=self.squares[20]
        if input == "a5":
            self.selected_target=self.squares[40]
        if input == "a7":
            self.selected_target=self.squares[60]
        if input == "b2":
            self.selected_target=self.squares[11]
        if input == "b4":
            self.selected_target=self.squares[31]
        if input == "b6":
            self.selected_target=self.squares[51]
        if input == "b8":
            self.selected_target=self.squares[71]
        if input == "c1":
            self.selected_target=self.squares[2]
        if input == "c3":
            self.selected_target=self.squares[22]
        if input == "c5":
            self.selected_target=self.squares[42]
        if input == "c7":
            self.selected_target=self.squares[62]
        if input == "d2":
            self.selected_target=self.squares[13]
        if input == "d4":
            self.selected_target=self.squares[33]
        if input == "d6":
            self.selected_target=self.squares[53]
        if input == "d8":
            self.selected_target=self.squares[73]
        if input == "e1":
            self.selected_target=self.squares[4]
        if input == "e3":
            self.selected_target=self.squares[24]
        if input == "e5":
            self.selected_target=self.squares[44]
        if input == "e7":
            self.selected_target=self.squares[64]
        if input == "f2":
            self.selected_target=self.squares[15]
        if input == "f4":
            self.selected_target=self.squares[35]
        if input == "f6":
            self.selected_target=self.squares[55]
        if input == "f8":
            self.selected_target=self.squares[75]
        if input == "g1":
            self.selected_target=self.squares[6]
        if input == "g3":
            self.selected_target=self.squares[26]
        if input == "g5":
            self.selected_target=self.squares[46]
        if input == "g7":
            self.selected_target=self.squares[66]
        if input == "h2":
            self.selected_target=self.squares[17]
        if input == "h4":
            self.selected_target=self.squares[37]
        if input == "h6":
            self.selected_target=self.squares[57]
        if input == "h8":
            self.selected_target=self.squares[77]

    def check_jump():
        pass
        
    def check_double(self): # This is not working yet...
        pass
        self.selected_piece = self.selected_target
        
        UR = self.selected_piece.UR
        self.UR = "invalid"
        URUR = self.selected_piece.URUR
        self.URUR = "invalid"
        UL = self.selected_piece.UL
        self.UL = "invalid"
        ULUL = self.selected_piece.ULUL
        self.ULUL = "invalid"
        LL = self.selected_piece.LL
        self.LL = "invalid"
        LLLL = self.selected_piece.LLLL
        self.LLLL = "invalid"
        LR = self.selected_piece.LR
        self.LR = "invalid"
        LRLR = self.selected_piece.LRLR
        self.LRLR = "invalid"
        
        if (
            self.squares[UR].current_piece == self.opposite and
            self.squares[URUR].current_piece == "blank"
        ):
                self.URUR = "valid"
        if (
            self.squares[UL].current_piece == self.opposite and
            self.squares[ULUL].current_piece == "blank"
        ):
                self.ULUL = "valid"
        if (
            self.squares[LL].current_piece == self.opposite and
            self.squares[LLLL].current_piece == "blank"
        ):
                self.LLLL = "valid"
        if (
            self.squares[LR].current_piece == self.opposite and
            self.squares[LRLR].current_piece == "blank"
        ):
                self.LRLR = "valid"
        
        if (
            URUR == "valid" or ULUL == "valid" or
            LLLL == "valid" or LRLR == "valid"
        ):
            print("There is still a move to be made.")
            self.select()
    
    def select(self):
    
        self.valid_selections = [
            "a1", "a3", "a5", "a7", "b2", "b4", "b6", "b8",
            "c1", "c3", "c5", "c7", "d2", "d4", "d6", "d8",
            "e1", "e3", "e5", "e7", "f2", "f4", "f6", "f8",
            "g1", "g3", "g5", "g7", "h2", "h4", "h6", "h8"
        ]
        
        if self.turn % 2 == 1:
            print("Red player's turn to move:\n")
        else:
            print("Black player's turn to move:\n")

        self.selected_piece = input(" Select a piece to move: ").lower()
        self.check_selection()
        
        self.selected_target = input(" Select a target square: ").lower()
        self.check_target()

        self.swap(self.selected_piece, self.selected_target)
        
        
        self.check_double() # This is not working yet...
        self.check_king()
        self.check_win()
        self.turn += 1
        self.display()
        self.select()


class Square():

    def __init__(self):
        """Square object constructor"""
        self.color = None
        self.name = None
        self.x = None
        self.y = None
        self.is_red_piece = False
        self.is_black_piece = False
        self.current_piece = None
        self.pattern = []
        self.UR = None
        self.URUR = None
        self.UL = None
        self.ULUL = None
        self.LL = None
        self.LLLL = None
        self.LR = None
        self.LRLR = None
        self.is_king = False

# Instantiate a Game object
game_instance = Game()
