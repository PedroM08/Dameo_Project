import pygame, time

from packages import constants
from packages.board import Board
from packages.piece import Piece

class Game:
    def __init__(self, window):
        self._init()
        self.window = window

        self.initial_time = time.time()
        self.end_time = None

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = "b"
        self.valid_moves = {}

        # Track the turns of the game
        self.game_turns = 0

        self.must_continue_capturing = False
        self.capturing_piece = None
        self.last_direction = None  # Track the last direction the king moved

    def update(self):
        self.board.draw_board(self.window) # draw the board and the pieces
        self.draw_valid_moves(self.valid_moves) # draw the valid moves of the pieces
        pygame.display.update()

    def winner(self):
        result = self.board.winner()
        if result and self.end_time is None:
            print(self.game_turns)
            self.end_time = time.time()  # Record when game ends
            elapsed_time = self.end_time - self.initial_time
            print(f"Total time: {elapsed_time:.2f} seconds")
        return result

    def reset(self):
        """Resets the game to the initial state"""
        self._init()
        self.initial_time = time.time()  # Reset timer on game reset
        self.end_time = None

    def select(self, row, col):
        """cheks if selected piece is valid and the respective possible moves"""
        # When you have multiple captures to complete with a piece

        if self.must_continue_capturing: # This is on the begginig to prevent the valid moves being erased when doing forced multiple captures
            # Player must continue capturing with the same piece
            if self.capturing_piece and (row, col) in self.valid_moves:
                self.selected = self.capturing_piece # we previously cleaned the selected, but because we still need to make captures with the same piece we assigned it again to the same one  
                return self._move(row, col) # We know it can make a capture that is why we are in this part of the code, we just want to make it
            return False

        # When you click on a legal move and want to move the selected piece to it

        if self.selected: # if the attribute sel.selected is not empty (True) it means it already as opperated through the piece before
            result = self._move(row, col) # Result either is false, wich means that the cords (row, col) correspond to a piece; if true it moves the piece to the given cords

            if not result: # Based on the condition above, if the cords correspond to something different then the legal_moves of the piece we want to call again this method from scratch
                self.selected = None # This resets the selected piece and prepares it to receive another piece
                self.valid_moves = {} # Resets the valid_moves
                self.update() # Updates the visual changes of the game
                return self.select(row, col) # Call again, but this time is from scratch

        # When you click on a piece to select it

        piece = self.board.get_piece(row, col) # gets the piece from the rows and cols we clicked on
        if piece != 0 and piece.color == self.turn: # If the piece exists and is the color of the players turn
            # Check if forced captures exist
            force_capture_moves = self.get_all_forced_moves()

            # If force captures exist, they are the only legal moves to make
            if force_capture_moves and (row, col) not in force_capture_moves: # if force captures not empty and (row, col) is not in there, means you need to select a piece that can capture
                print("Select another piece")
                return False  # Must pick a piece that can capture

            self.selected = piece # Make so that the (class attribute) selected is equal to the piece
            self.valid_moves = self.board.get_valid_moves(piece) # calculate the valid moves of the piece
            return True # exits the method so the next click as the info to go to other part of the function

        return False # clicked on a empty space or in a wrong color piece, so we exit the method

    def _move(self, row, col): # Check if the move is possible and if it is, makes the implications (captures, regular moves, promotions) of that move
        piece = self.board.get_piece(row, col) #gets the object of the piece
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            # Before moving, track direction if it's a king
            if self.selected.king:
                old_row, old_col = self.selected.row - 1, self.selected.col - 1
                new_row, new_col = row - 1, col - 1
                dx = 1 if new_row > old_row else (-1 if new_row < old_row else 0)
                dy = 1 if new_col > old_col else (-1 if new_col < old_col else 0)
                self.last_direction = self.board._get_direction(dx, dy)
            
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row, col)] # get the object of the piece in case there was a capture
            
            if skipped: # If a piece was captured
                self.board.remove_piece(skipped)
                
                # After capture, check for more captures with the direction restriction
                if self.selected.king:
                    # Get valid moves with direction restriction
                    moves = {}
                    self.board._find_king_captures(
                        row - 1, col - 1, self.selected, 
                        [(-1, 0), (1, 0), (0, -1), (0, 1)],  # orthogonal directions
                        [], self.last_direction, moves
                    )
                    self.valid_moves = moves
                else:
                    # Regular piece logic
                    self.valid_moves = self.board.get_valid_moves(self.selected)
                    
                force_capture_moves = self.get_all_forced_moves()
                if self.valid_moves and (row, col) in force_capture_moves:
                    self.must_continue_capturing = True
                    self.capturing_piece = self.selected
                    return True
                else:
                    # Check if we're on a king row after completing all captures
                    is_king_row = (row == 8 and self.selected.color == "b") or (row == 1 and self.selected.color == "r")
                    if is_king_row and not self.selected.king:
                        self.selected.make_king()
                        if self.selected.color == "b":
                            self.board.blue_kings += 1
                        else:
                            self.board.red_kings += 1
                    
                    self.must_continue_capturing = False
                    self.capturing_piece = None
                    self.last_direction = None  # Reset direction when turn ends
                    self.change_turn()
                    return True
            else:
                # Normal move (no captures), check for king promotion
                is_king_row = (row == 8 and self.selected.color == "b") or (row == 1 and self.selected.color == "r")
                if is_king_row and not self.selected.king:
                    self.selected.make_king()
                    if self.selected.color == "b":
                        self.board.blue_kings += 1
                    else:
                        self.board.red_kings += 1
                        
                self.last_direction = None  # Reset direction when turn ends
                self.change_turn()
            
            return True
        else:
            return False

    
    def get_all_forced_moves(self): # Runs through all pieces and checks if there are any captures and returns a set with the (rows, cols) of the pieces to move
        """Checks all the squares and all the pieces so it can calculate if there are capture moves that make the play in question forced"""
        forced_pieces = set() # is a set to make shure we don't repeat a piece
        for row in range(1, 9):
            for col in range(1, 9):
                piece = self.board.get_piece(row, col)
                if piece != 0 and piece.color == self.turn: # if it is a piece and is the color of the turn playing
                    moves = self.board.get_valid_moves(piece) # gets the legal moves of the piece
                    for move, captured in moves.items(): 
                        if captured:
                            forced_pieces.add((row, col))
        return forced_pieces

    
    def draw_valid_moves(self, moves):
        #print(self.valid_moves)
        for move in moves:
            row, col = move
            pygame.draw.circle(self.window, "Green", (((constants.screen_w * 28) / 128) + ((constants.screen_w * 8) / 128)* col, 5 + (constants.screen_h / 9)*(9 - row)), 10)

    
    def change_turn(self):
        self.valid_moves = {} # Reset the valid_moves for the next piece
        if self.turn == "b":
            self.turn = "r"
            self.game_turns += 1
            #print("r turn")
            
        else:
            self.turn = "b"
            #print("b turn")

    def get_board(self):
        return self.board