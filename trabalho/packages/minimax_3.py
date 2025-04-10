from copy import deepcopy

class MinimaxAlphaBeta:
    def __init__(self, game, color):
        self.game = game
        self.color = color
        self.max_depth = 4

    def _evaluate(self, board):
        """Evaluate the board position for the minimax algorithm"""
        # Basic evaluation: difference in number of pieces + kings advantage
        if self.color == 'b':
            return board.blue_left - board.red_left + (board.blue_kings * 0.5 - board.red_kings * 0.5)
        else:
            return board.red_left - board.blue_left + (board.red_kings * 0.5 - board.blue_kings * 0.5)
    
    def make_move(self):
        """Make a move using the minimax algorithm with alpha-beta pruning"""
        # Handle multi-capture sequence
        if (self.game.must_continue_capturing
            and self.game.capturing_piece
            and self.game.capturing_piece.color == self.color):
            
            valid_moves = list(self.game.valid_moves.keys())
            if valid_moves:
                # In a capture sequence, just use the first available move
                move = valid_moves[0]
                return self.game.capturing_piece.row, self.game.capturing_piece.col, move[0], move[1]
            return None
        
        # Use the minimax algorithm with alpha-beta pruning to find the best move
        best_score = float('-inf')
        best_move = None
        alpha = float('-inf')
        beta = float('inf')
        
        # Get all pieces that can move
        forced_pieces = self.game.get_all_forced_moves()
        pieces_to_evaluate = []
        
        if forced_pieces:
            # If there are forced captures, evaluate only those
            for piece_pos in forced_pieces:
                piece = self.game.board.get_piece(piece_pos[0], piece_pos[1])
                valid_moves = self.game.board.get_valid_moves(piece)
                pieces_to_evaluate.append((piece, valid_moves))
        else:
            # Otherwise, evaluate all pieces
            for piece in self.game.board.get_all_pieces_of_a_color(self.color):
                valid_moves = self.game.board.get_valid_moves(piece)
                if valid_moves:
                    pieces_to_evaluate.append((piece, valid_moves))
        
        # Evaluate each possible move
        for piece, valid_moves in pieces_to_evaluate:
            for move, skip in valid_moves.items():
                # Simulate the move
                temp_board = deepcopy(self.game.board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                
                # Apply the move to the temporary board
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                
                # Evaluate the position using minimax with alpha-beta pruning
                eval_score = self._minimax(new_board, self.max_depth - 1, False, alpha, beta)
                
                # Keep track of the best move
                if eval_score > best_score:
                    best_score = eval_score
                    best_move = (piece.row, piece.col, move[0], move[1])
                
                # Update alpha
                alpha = max(alpha, eval_score)
        
        return best_move
    
    def _minimax(self, board, depth, is_maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning implementation"""
        # Base cases: maximum depth reached or terminal state
        if depth == 0 or board.winner() is not None:
            return self._evaluate(board)
        
        if is_maximizing:
            # Maximizing player (AI)
            max_eval = float('-inf')
            
            # Get all possible moves for the AI's pieces
            for piece in board.get_all_pieces_of_a_color(self.color):
                valid_moves = board.get_valid_moves(piece)
                
                for move, skip in valid_moves.items():
                    # Create a copy and simulate the move
                    temp_board = deepcopy(board)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                    
                    # Recursive evaluation with alpha-beta pruning
                    eval_score = self._minimax(new_board, depth - 1, False, alpha, beta)
                    max_eval = max(max_eval, eval_score)
                    
                    # Alpha-beta pruning
                    alpha = max(alpha, max_eval)
                    if beta <= alpha:
                        # Beta cut-off
                        break
                
                # Check for beta cut-off at piece level
                if beta <= alpha:
                    break
                    
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
                    
                    # Recursive evaluation with alpha-beta pruning
                    eval_score = self._minimax(new_board, depth - 1, True, alpha, beta)
                    min_eval = min(min_eval, eval_score)
                    
                    # Alpha-beta pruning
                    beta = min(beta, min_eval)
                    if beta <= alpha:
                        # Alpha cut-off
                        break
                
                # Check for alpha cut-off at piece level
                if beta <= alpha:
                    break
                    
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
                
                # Simulate the move
                new_board = self.simulate_move(temp_piece, move, temp_board, skip)
                moves.append(new_board)
        
        return moves
    
    def simulate_move(self, piece, move, board, skip):
        """Simulate a move on a temporary board"""
        # Move the piece
        board.move(piece, move[0], move[1])
        
        # If there's a capture, remove the captured piece(s)
        if skip:
            board.remove_piece(skip)
        
        return board

    def _color_opposite(self, color):
        """Get the opposite color"""
        return 'r' if color == 'b' else 'b'