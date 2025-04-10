# First try of the minimax code, guided by the video

# import pygame
# from copy import deepcopy

# class Minimax2:
#     def __init__(self, game, color):
#         self.game = game
#         self.color = color
#         self.max_depth = 1

#     def _evaluate(self):
#         return self.game.board.blue_left - self.game.board.red_left + (self.game.board.blue_kings * 0.5 - self.game.board.red_kings * 0.5)
    
#     def make_move(self):
#         # Handle multi-capture sequence
#         if (self.game.must_continue_capturing
#             and self.game.capturing_piece
#             and self.game.capturing_piece.color == self.color):
#             valid_moves = list(self.game.valid_moves.keys())
#             if valid_moves:
#                 # In a capture sequence, just use the first available move
#                 # (we could also evaluate these moves, but since captures are forced, this is simpler)
#                 move = valid_moves[0]
#                 return self.game.capturing_piece.row, self.game.capturing_piece.col, move[0], move[1]
#             return None
        
#         # forced_pieces = self.game.get_all_forced_moves()
#         # pieces_to_evaluate = []
#         # if forced_pieces:
#         #     for piece_pos in forced_pieces:
#         #         piece = self.game.board.get_piece(piece_pos[0], piece_pos[1])
#         #         valid_moves = self.game.board.get_valid_moves(piece)
#         #         pieces_to_evaluate.append((piece, valid_moves))
#         print("hello")
#         print(self._minimax(self.game.get_board(), self.max_depth, self.color))
    
#     def _minimax(self, board_position, depth, color):
#         if depth == 0 or board_position.winner() != None:
#             print(board_position)
#             return self._evaluate(), board_position

#         if color == self.game.turn:
#             maxEval = float('-inf')
#             best_move = None
#             for move in self.get_all_moves(board_position, color, self.game):
#                 evaluation = self._minimax(move, depth-1, self._color_opposite(color))[0]
#                 maxEval = max(maxEval, evaluation)
#                 if maxEval == evaluation:
#                     best_move = move
#             return maxEval, best_move
        
#         else:
#             minEval = float('inf')
#             best_move = None
#             for move in self.get_all_moves(board_position, color, self.game):
#                 evaluation = self._minimax(move, depth-1, self._color_opposite(color))[0]
#                 minEval = min(minEval, evaluation)
#                 if minEval == evaluation:
#                     best_move = move
            
#             return minEval, best_move



#     def get_all_moves(self, board_position, color, game):
#         moves = []

#         for piece in board_position.get_all_pieces_of_a_color(color):
#             valid_moves = game.board.get_valid_moves(piece)

#             for move, skip in valid_moves.items():

#                 temp_board = deepcopy(board_position)
#                 temp_piece = temp_board.get_piece(piece.row, piece.col)

#                 new_board = self.simulate_move(temp_piece, move, temp_board, skip)
#                 moves.append(new_board)
        
#         return moves
    
#     def simulate_move(self, piece, move, board, skip):
#         board.move(piece, move[0], move[1])
#         if skip:
#             board.remove(skip)

#         return board

#     def _color_opposite(self, color):
#         if color == 'b':
#             return 'r'
#         else:
#             return 'b'
    

from copy import deepcopy

class Minimax2:
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.max_depth = 2

    def _evaluate(self, board):
        """Evaluate the position (heuristic function)"""
        # Basic evaluation: difference in number of pieces + kings advantage
        evaluation = 0
        if self.color == 'b':
            evaluation += board.blue_left - board.red_left + (board.blue_kings * 0.5 - board.red_kings * 0.5)
        else:
            evaluation += board.red_left - board.blue_left + (board.red_kings * 0.5 - board.blue_kings * 0.5)

        
        pieces_rows = []
        for row in board.board:
            for piece in row:
                if piece != 0 and not piece.king:
                    if piece.color == 'b':
                        pieces_rows.append(piece.row * 1.5)
                    else:
                        pieces_rows.append((9 - piece.row) * 1.5)
        distance_to_king = sum(pieces_rows)

        return evaluation + distance_to_king * 0.08


    
    def make_move(self):
        """Make a move using the minimax algorithm"""
        # Handle multi-capture sequence
        if (self.game.must_continue_capturing # If the flag continue to capture is active
            and self.game.capturing_piece   # If we have a capturing piece selected
            and self.game.capturing_piece.color == self.color): # If the capturing piece color is equal to the the players playing color
            
            valid_moves = list(self.game.valid_moves.keys()) # Get a dictionary with the value moves and turn into a list with the only the possible moves of the selected piece
            if valid_moves:
                # To max the efficency,  in a capture sequence just use the first available move
                move = valid_moves[0] 
                return self.game.capturing_piece.row, self.game.capturing_piece.col, move[0], move[1] # The first two values are the piece to move row and col and the other two where that piece needs to move row and col
            return None
        
        # Use the minimax algorithm to find the best move
        best_score = float('-inf') # negative inf
        best_move = None
        
        # Get all pieces that can move
        forced_pieces = self.game.get_all_forced_moves() # check if there are forced moves the piece needs to make
        pieces_to_evaluate = []
        
        if forced_pieces:
            # If there are forced captures, evaluate only those
            for piece_pos in forced_pieces:
                piece = self.game.board.get_piece(piece_pos[0], piece_pos[1]) # get the object of the piece we want
                valid_moves = self.game.board.get_valid_moves(piece) # get the value moves for the piece
                pieces_to_evaluate.append((piece, valid_moves)) # add to the list the valid moves for the choosen piece
        else:
            # Otherwise, evaluate all pieces
            for piece in self.game.board.get_all_pieces_of_a_color(self.color):
                valid_moves = self.game.board.get_valid_moves(piece) # get the value moves for the piece
                if valid_moves:
                    pieces_to_evaluate.append((piece, valid_moves)) # add to the list the valid moves for the choosen piece
        
        # Evaluate each possible move
        for piece, valid_moves in pieces_to_evaluate:
            for move, skip in valid_moves.items():
                # Simulate the move, so we create copies of the board and the piece so that we don't change the real one
                temp_board = deepcopy(self.game.board) # create a temporary board to make the simulations on
                temp_piece = temp_board.get_piece(piece.row, piece.col) # create a temporary piece for the simulation
                
                # Apply the move to the temporary board
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                
                # Evaluate the position using minimax
                eval_score = self._minimax(new_board, self.max_depth - 1, False)
                
                # Trackthe best move
                if eval_score > best_score:
                    best_score = eval_score
                    best_move = (piece.row, piece.col, move[0], move[1])
        
        return best_move
    
    def _minimax(self, board, depth, is_maximizing):
        """Minimax algorithm implementation"""
        # Base cases: maximum depth reached or terminal state
        if depth == 0 or board.winner() is not None: # if the depth as rech is limit or the path found a way to win, end the simulation and retrieve the value
            return self._evaluate(board)
        
        if is_maximizing:
            # Maximizing player (AI)
            max_eval = float('-inf')
            
            # Get all possible moves for the ais pieces
            for piece in board.get_all_pieces_of_a_color(self.color):
                valid_moves = board.get_valid_moves(piece)
                
                for move, skip in valid_moves.items():
                    # Create a copy and simulate the move
                    temp_board = deepcopy(board)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                    
                    # Recursive evaluation
                    eval_score = self._minimax(new_board, depth - 1, False)
                    max_eval = max(max_eval, eval_score)
                    
            return max_eval
        else:
            # Minimizing player (opponent)
            min_eval = float('inf')
            opponent_color = 'r' if self.color == 'b' else 'b'
            
            # Get all possible moves for the opponent's pieces
            for piece in board.get_all_pieces_of_a_color(opponent_color):
                valid_moves = board.get_valid_moves(piece)
                
                for move, skip in valid_moves.items():
                    # Create a copy and simulate the move
                    temp_board = deepcopy(board)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                    
                    # Recursive evaluation
                    eval_score = self._minimax(new_board, depth - 1, True)
                    min_eval = min(min_eval, eval_score)
                    
            return min_eval

    def get_all_moves(self, board, color):
        """Get all possible moves for pieces of a given color"""
        moves = []
        
        for piece in board.get_all_pieces_of_a_color(color):
            valid_moves = board.get_valid_moves(piece)
            
            for move, skip in valid_moves.items():
                # Create a temporary board for simulation
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                
                # Simulate themove
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append(new_board)
        
        return moves
    
    def simulate_move(self, piece, move, board, skip):
        """Simulate a move on a temporary board"""

        board.move(piece, move[0], move[1]) # move the piece
        
        if skip: # if a piece is skipped then remove it 
            board.remove_piece(skip) 
        
        return board

    def _color_opposite(self, color):
        """Get the opposite color"""
        return 'r' if color == 'b' else 'b'