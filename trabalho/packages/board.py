from packages.piece import Piece

class Board:
    def __init__(self):
        self.board = [[0 for x in range(8)] for x in range(8)] # Set the array of the game board 8 x 8 
        
        self.red_left = self.blue_left = 18 # Total pieces left
        self.red_kings = self.blue_kings = 0 # Number of kings

        self.set_board()
        

    def set_board(self): # Set the Pieces in the array/board, with the object piece from the piece.py file
        """Sets the board with the object on the pieces places"""
        # Place 1 and 8 rank pieces
        for i in range(8):
            self.board[0][i] = Piece(1, i+1, 'b')
            self.board[8-1][i] = Piece(8, i+1, 'r')
        
        # Place 2 and 7 rank pieces
        for i in range(1, 8 - 1):
            self.board[1][i] = Piece(2, i+1, 'b')
            self.board[8-2][i] = Piece(7, i+1, 'r')

        # Place 3 and 6 rank pieces
        for i in range(2, 8 - 2):
            self.board[2][i] = Piece(3, i+1, 'b')
            self.board[8-3][i] = Piece(6, i+1, 'r')


    def draw_board(self, window): # Draw the board through the Piece object
        """Draws the pieces on the board"""
        for row in self.board:
                for piece in row:
                    if piece != 0: piece.draw(window)

    def get_piece(self, row, col): # Given cords (row, col) returns the object of the piece inside the 2d list of self.board
        """Gets a piece"""
        return self.board[row - 1][col - 1]
 
    def get_all_pieces_of_a_color(self, color): # Gets all objects of the pieces from self.board of a specific color and returns a list with all of them
        """Gets all the """
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col): # Moves a piece in the self.board list and calls the piece method to alter the cords in the piece object itself
        """Takes the piece and changes its coords to the new row and col"""
        # Change the place of the piece in the array
        self.board[piece.row - 1][piece.col - 1], self.board[row-1][col-1] = self.board[row-1][col-1], self.board[piece.row - 1][piece.col - 1]

        # Display the change of place of the piece
        piece.move_piece(row, col)

        # Temporarily store if this is a king row for this piece
        # Only promote if no further captures are possible from this position
        is_king_row = (row == 8 and piece.color == "b") or (row == 1 and piece.color == "r")
        
        # Check if there are any more captures possible from this position
        captures = self._check_captures(row-1, col-1, piece, [(-1, 0), (1, 0), (0, -1), (0, 1)])
        
        # Only make the piece a king if it's on the king row AND there are no more captures
        if is_king_row and not captures:
            if not piece.king:  # Only promote if not already a king
                piece.make_king()
                if piece.color == "b":
                    self.blue_kings += 1
                else:
                    self.red_kings += 1

    def remove_piece(self, pieces):
        """Removes a determined piece from the board"""
        for piece in pieces:
            self.board[piece.row - 1][piece.col - 1] = 0
            if piece != 0:
                if piece.color == "b":
                    self.blue_left -= 1
                else:
                    self.red_left -= 1

    def get_number_of_pieces(self, color):
        """Gets the number of the pieces left of a determined color"""
        if color == 'b':
            return self.blue_left
        else:
            return self.red_left

    def winner(self):
        """Check if a color as won"""
        if self.red_left <= 0:
            return "b"
        elif self.blue_left <= 0:
            return "r"
        
        return None 

    def get_valid_moves(self, piece): # Returns a dictionary where the keys are the places the piece can go to and the value is the object of the captured piece (*Note: value is empty if there is no capture)
        """Get al the valid moves for the piece"""
        all_moves = {}
        #capturing_moves = {}

        row, col = piece.row - 1, piece.col - 1  # Convert to 0-indexed to search through the board list
        
        # Normal possible moves for each piece
        if piece.color == 'b':
            directions = [(1, 0), (1, -1), (1, 1)]
        else:
            directions = [(-1, 0), (-1, -1), (-1, 1)]

        if piece.king:
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        # Define directions for captures - only orthogonal directions are allowed
        # (-1, 0): up, (1, 0): down, (0, -1): left, (0, 1): right
        capture_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        # If any captures are available, only return those, because captures are forced
        captures = self._check_captures(row, col, piece, capture_directions)
        if captures:
            return captures

        # Check all types of moves
        regular_moves = self._check_regular_moves(row, col, directions, piece)
        orthogonal_moves = self._check_orthogonal_moves(row, col, directions, piece)

        # If no captures, combine regular and orthogonal
        all_moves.update(regular_moves) # Update the all_moves dictionary with the regular
        all_moves.update(orthogonal_moves) # Update the all_moves dictionary with the orthogonal
        return all_moves # Returns the dictionary with the legal moves as keys (row, col) and empty values

    def _check_regular_moves(self, row, col, directions, piece):
        """Check for regular diagonal and forward moves."""
        moves = {}
        if piece.king:
            for dx, dy in directions:
                current_row, current_col = row, col
                # Start from i=1 to avoid counting the current position
                for i in range(1, 8):
                    new_row, new_col = current_row + dx, current_col + dy
                    # Check if the new position is within the board
                    if 0 <= new_row < 8 and 0 <= new_col < 8:
                        # Check if the square is empty
                        if self.board[new_row][new_col] == 0:
                            # Store the move in 1-indexed form for consistency with the rest of the code
                            moves[(new_row + 1, new_col + 1)] = []
                            # Update current position to continue in the same direction
                            current_row, current_col = new_row, new_col
                        else:
                            # Stop if we hit a piece
                            break
                    else:
                        # Stop if we're off the board
                        break
        else:
            for dx, dy in directions:
                new_row, new_col = row + dx, col + dy

                # Check if the new position is within the board
                if 0 <= new_row < 8 and 0 <= new_col < 8:
                    # Check if the square is empty
                    if self.board[new_row][new_col] == 0:
                        # Store the move in 1-indexed form for consistency with the rest of the code
                        moves[(new_row + 1, new_col + 1)] = []
            
        
        return moves

    def _check_orthogonal_moves(self, row, col, directions, piece):
        """Check for orthogonal line moves (specific to Dameo)."""
        moves = {}

        # Skip orthogonal line moves for kings
        if piece.king:
            return moves

        for dx, dy in directions:
            current_row, current_col = row, col

            # Check if there's a friendly piece adjacent in this direction
            if (0 <= current_row + dx < 8 and 0 <= current_col + dy < 8 and
                self.board[current_row + dx][current_col + dy] != 0 and
                self.board[current_row + dx][current_col + dy].color == piece.color):

                # Count consecutive friendly pieces in this direction
                line_length = 0
                while (0 <= current_row + dx < 8 and 0 <= current_col + dy < 8 and
                       self.board[current_row + dx][current_col + dy] != 0 and
                       self.board[current_row + dx][current_col + dy].color == piece.color):
                    line_length += 1
                    current_row += dx
                    current_col += dy

                # Check if there's an empty square after the line
                if (0 <= current_row + dx < 8 and 0 <= current_col + dy < 8 and
                    self.board[current_row + dx][current_col + dy] == 0):

                    # The move is to the empty square after the line
                    moves[(current_row + dx + 1, current_col + dy + 1)] = []
                    # print(moves)

        return moves

    
    def _check_captures(self, row, col, piece, capture_directions):
        """Check for capture moves in orthogonal directions only (forward, backward, sideways)."""
        moves = {}
        
        if piece.king:
            # For kings, use the directional tracking approach
            # Initial direction is None since the king hasn't moved yet
            self._find_king_captures(row, col, piece, capture_directions, [], None, moves)
        else:
            # Regular piece capture logic (unchanged)
            for dx, dy in capture_directions:
                new_row, new_col = row + dx, col + dy
                
                # Check if there's an opponent's piece adjacent
                if (0 <= new_row < 8 and 0 <= new_col < 8 and
                    self.board[new_row][new_col] != 0 and # if our piece cords + one of the capture cords = a piece
                    self.board[new_row][new_col].color != piece.color): # and if that piece is a different color from ours
                    
                    # Check if there's an empty square after the opponent's piece
                    jump_row, jump_col = new_row + dx, new_col + dy
                    if (0 <= jump_row < 8 and 0 <= jump_col < 8 and
                        self.board[jump_row][jump_col] == 0): # check if the space ahead of the enemy piece is free
                        # Store the captured piece and the move
                        # Convert back to 1-indexed for the moves dictionary keys
                        moves[(jump_row + 1, jump_col + 1)] = [self.board[new_row][new_col]]
                        # The key of the dictionary is the position of where the piece can jump after the capture
                        # The value is the object of the captured piece

        return moves # return the dictionary
    
    def _find_king_captures(self, row, col, piece, capture_directions, captured_so_far, last_direction, all_moves):
        """find all possible capture sequences for a king piece with directional restrictions."""
        # Check captures in all directions from the current position
        for dx, dy in capture_directions:
            current_direction = self._get_direction(dx, dy) # specifies if the king is going up, down, left or right
            
            # Skip opposite direction from the last move
            if (last_direction is not None # If the last direction exist (is different of None in this case)
                 and self._is_opposite_direction(last_direction, current_direction)): # and 
                continue
                
            current_row, current_col = row, col
            
            # Find the next piece in this direction
            found_piece = False
            new_row, new_col = current_row, current_col
            
            while True:
                new_row += dx
                new_col += dy
                
                # Stop if we've reached the edge of the board
                if not (0 <= new_row < 8 and 0 <= new_col < 8):
                    break
                    
                # If we find a piece, stop searching in this direction
                if self.board[new_row][new_col] != 0:
                    found_piece = True
                    break
            
            # If we found an opponent's piece that hasn't been captured yet
            if (found_piece and 
                self.board[new_row][new_col].color != piece.color and
                self.board[new_row][new_col] not in captured_so_far):
                
                # Check for landing squares after the captured piece
                jump_row, jump_col = new_row, new_col
                landing_squares = []
                
                while True:
                    jump_row += dx
                    jump_col += dy
                    
                    # Stop if we've reached the edge or found another piece
                    if not (0 <= jump_row < 8 and 0 <= jump_col < 8) or self.board[jump_row][jump_col] != 0:
                        break
                        
                    # Add this landing position to our list
                    landing_squares.append((jump_row, jump_col))
                
                # For each possible landing square, check for further captures
                for landing_row, landing_col in landing_squares:
                    # Create a new list with the current captured piece added
                    new_captured = captured_so_far + [self.board[new_row][new_col]]
                    
                    # Store this move with captured pieces
                    all_moves[(landing_row + 1, landing_col + 1)] = new_captured.copy()
                    
                    # Recursively check for additional captures from this landing position / this line of code let's you see all the path to the end of the kingd capture
                    # Pass the current direction for the next recursive call
                    # self._find_king_captures(landing_row, landing_col, piece, capture_directions, new_captured, current_direction, all_moves)

    def _get_direction(self, dx, dy):
        """Convert dx, dy to a named direction."""
        if dx == -1 and dy == 0:
            return "up"
        elif dx == 1 and dy == 0:
            return "down"
        elif dx == 0 and dy == -1:
            return "left"
        elif dx == 0 and dy == 1:
            return "right"
        else:
            return "diagonal"  # For diagonal moves if needed

    def _is_opposite_direction(self, dir1, dir2):
        """Check if two directions are opposite."""
        opposites = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left"
        }
        return opposites.get(dir1) == dir2