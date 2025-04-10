# ai_player.py - Create this file in the packages directory
import random

class RandomAI:
    def __init__(self, game, color):
        self.game = game
        self.color = color
    
    def make_move(self):
        """Make a random valid move for the AI (red pieces)"""
        # Check if we're in the middle of a multi-capture sequence
        if (self.game.must_continue_capturing
             and self.game.capturing_piece
            and self.game.capturing_piece.color == self.color):
            # If we're in a multi-capture, get the valid moves for the capturing piece
            valid_moves = list(self.game.valid_moves.keys())
            if valid_moves:
                # Choose a random move from the available capture moves
                move = random.choice(valid_moves)
                return self.game.capturing_piece.row, self.game.capturing_piece.col, move[0], move[1]
            return None
        
        # Check if there are any forced captures
        forced_pieces = self.game.get_all_forced_moves()
        if forced_pieces:
            # If there are forced captures, choose a random piece that can capture
            forced_list = list(forced_pieces) # a list with the cords (row, col) of the pieces forced to move
            piece_pos = random.choice(forced_list) # returns a random set of cords (touple with row, col) from the forced_list
            piece = self.game.board.get_piece(piece_pos[0], piece_pos[1]) # gets the object of the selected piece
            
            # Get valid moves for this piece
            valid_moves = self.game.board.get_valid_moves(piece)
            capture_moves = {move: captures for move, captures in valid_moves.items() if captures} # Is a dict with the legal moves as keys and the respective captures as values
            
            if capture_moves: # If there are captures for the selected piece
                # Choose a random capture move
                move = random.choice(list(capture_moves.keys())) # Chooses a random move from a list with the forced moves
                return piece.row, piece.col, move[0], move[1] 
        
        # If no forced captures, get all pieces of the AI's color
        pieces = [] # A list with a touple (object of the piece, dictionary with the valid moves for the piece)
        all_pieces = self.game.board.get_all_pieces_of_a_color(self.color)
        
        for piece in all_pieces:
            valid_moves = self.game.board.get_valid_moves(piece)
            if valid_moves:
                pieces.append((piece, valid_moves))

        if pieces:
            # Choose a random piece that has valid moves
            piece, valid_moves = random.choice(pieces) #chooses a random touple
            # Choose a random move for this piece
            move = random.choice(list(valid_moves.keys())) # From the dict of valid moves, chooses one at random and returns a touple with (row, col)
            
            return (piece.row, piece.col, move[0], move[1])
        
        return None  # No valid moves found
    
        