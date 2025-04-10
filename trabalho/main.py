# Import from known modules
import pygame, sys
import time

# Import from the folder that contains all my other files
from packages import constants
from packages.game import Game


from packages.ai_player import RandomAI
from packages.minimax_1 import Minimax1
from packages.minimax_2 import Minimax2
from packages.minimax_3 import MinimaxAlphaBeta

# pygame setup
pygame.init()
screen = pygame.display.set_mode((constants.ORIGINAL_WIDTH, constants.ORIGINAL_HEIGHT), pygame.RESIZABLE)  # Start in resizable windowed mode
pygame.display.set_caption('DAMEO') # Make the window caption
MAX_FPS = 60 # Max fps of the game

#function that calculates the rows and collumns of where the mouse is pressing
def get_row_col_from_mouse(position):
    x, y = position
    row = 8 - int((y - ((44*constants.screen_h)/720)) // ((8*constants.screen_h)/72))
    col = int((x-((33*constants.screen_w)/128)) // ((8*constants.screen_w)/128)) + 1
    return row, col


def main():
    # Set the clock of the game, so that we can create the cap of fps
    clock = pygame.time.Clock()
    game = None
    game_state = "lobby"  # Track current screen state

    # Amount of ai players
    ai_player1 = None
    ai_player2 = None

    
    ai_thinking = False  # Flag to control AI turn
    ai_move_delay = 0.2  # Delay in seconds between AI moves
    last_ai_move_time = 0  # Time of last AI move
    display_time = 0.8  # How long to show each step of multi-captures

    constants.resize_elements()  # Initial resize

    while True:
        resized = False  # Track if a resize happened
        current_time = time.time() # To keep track of time

        # This will get all the messages and remove them from the queue
        for event in pygame.event.get(): # Check if the user as quitted the game window
            if event.type == pygame.QUIT:
                pygame.quit() # Quit pygame
                sys.exit() # Close process

            elif event.type == pygame.VIDEORESIZE: # If the event is the resize of the window
                resized = True  # Only resize once per frame

            elif event.type == pygame.MOUSEBUTTONDOWN: # If the event is to press on something
                if game_state == "lobby" and constants.play_button_rect.collidepoint(event.pos):
                    # Checks if the mouse click (event.pos) happened inside the play_button_rect area
                    # event.pos contains the (x, y) coordinates of the mouse click
                    game_state = "game_screen"  # Switch to game screen
                
                elif game_state == "lobby" and constants.scaled_info_button_rect.collidepoint(event.pos):
                    game_state = "rules"


                elif game_state == "game_screen" and constants.button_pvp_rect.collidepoint(event.pos):
                    game_state = "player_vs_player"

                elif (game_state == "game_screen" and constants.button_pvai_rect.collidepoint(event.pos)) or (game_state == "player_vs_ai" and constants.scaled_dif_button_0_rect.collidepoint(event.pos)):
                    game_state = "player_vs_ai"
                    game = Game(screen)
                    ai_player1 = RandomAI(game, 'r')
                    print(0)
                
                elif game_state == "game_screen" and constants.button_aivai_rect.collidepoint(event.pos):
                    game_state = "ai_vs_ai"
                    game = Game(screen)  # Initialize game when entering AI vs AI mode

                elif game_state == "player_vs_ai" and constants.scaled_dif_button_1_rect.collidepoint(event.pos):
                    game = Game(screen)
                    ai_player1 = Minimax1(game, 'r')
                    print(1)

                elif game_state == "player_vs_ai" and constants.scaled_dif_button_2_rect.collidepoint(event.pos):
                    game = Game(screen)
                    ai_player1 = Minimax2(game, 'r')
                    print(2)

                elif game_state == "player_vs_ai" and constants.scaled_dif_button_3_rect.collidepoint(event.pos):
                    game = Game(screen)
                    ai_player1 = MinimaxAlphaBeta(game, 'r')
                    print(3)
                
                # Reset button for both scenerious
                elif (game_state == "player_vs_player" or game_state == "player_vs_ai" or game_state == "ai_vs_ai") and constants.reset_button_rect.collidepoint(event.pos):
                    constants.reset_the_game(game)
                    # Reset AI thinking state when game resets
                    ai_thinking = False
                    ai_player1 = None
                    ai_player2 = None

                elif (game_state == "player_vs_player" or game_state == "player_vs_ai" or game_state == "game_screen" or game_state == "ai_vs_ai" or game_state == "rules") and constants.scaled_return_to_lobby_rect.collidepoint(event.pos):
                    game = None
                    ai_player1 = None
                    ai_player2 = None
                    game_state = "lobby"
                    ai_thinking = False

                elif game_state == "ai_vs_ai":
                    # Red AI (Player 1) selection
                    if constants.scaled_dif_button_0_rect.collidepoint(event.pos):
                        ai_player1 = RandomAI(game, 'r')
                        print("Red AI: Random")
                    elif constants.scaled_dif_button_1_rect.collidepoint(event.pos):
                        ai_player1 = Minimax1(game, 'r')
                        print("Red AI: Minimax1")
                    elif constants.scaled_dif_button_2_rect.collidepoint(event.pos):
                        ai_player1 = Minimax2(game, 'r')
                        print("Red AI: Minimax2")
                    elif constants.scaled_dif_button_3_rect.collidepoint(event.pos):
                        ai_player1 = MinimaxAlphaBeta(game, 'r')
                        print("Red AI: MinimaxAlphaBeta")
                        
                    # Blue AI (Player 2) selection
                    elif constants.scaled_b_dif_button_0_rect.collidepoint(event.pos):
                        ai_player2 = RandomAI(game, 'b')  # Corrected to 'b' for blue
                        print("Blue AI: Random")
                    elif constants.scaled_b_dif_button_1_rect.collidepoint(event.pos):
                        ai_player2 = Minimax1(game, 'b')  # Corrected to 'b' for blue
                        print("Blue AI: Minimax1")
                    elif constants.scaled_b_dif_button_2_rect.collidepoint(event.pos):
                        ai_player2 = Minimax2(game, 'b')  # Corrected to 'b' for blue
                        print("Blue AI: Minimax2")
                    elif constants.scaled_b_dif_button_3_rect.collidepoint(event.pos):
                        ai_player2 = MinimaxAlphaBeta(game, 'b')  # Corrected to 'b' for blue
                        print("Blue AI: MinimaxAlphaBeta")

                elif game_state == "player_vs_player":
                    # get the position of the mouse
                    position = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(position)

                    if 1 <= row <= 8 and 1 <= col <= 8:
                        game.select(row, col)

                # When player is thinking
                elif game_state == "player_vs_ai" and game.turn == "b" and not ai_thinking:
                    # Only handle player input when it's the player's turn
                    position = pygame.mouse.get_pos()
                    row, col = get_row_col_from_mouse(position)
                    
                    if 1 <= row <= 8 and 1 <= col <= 8:
                        game.select(row, col)
                

        if resized:
            constants.resize_elements() # If the window was resized, then the element also need to be resized

        if game_state == "lobby":
            screen.blit(constants.scaled_lobby, (0, 0)) # Display the lobby image
            screen.blit(constants.scaled_play, constants.play_button_rect.topleft) # Display the play button
            screen.blit(constants.scaled_info_button, constants.scaled_info_button_rect.topleft) # Display the play button
            
        
        elif game_state == "rules":
            screen.blit(constants.scaled_info_screen, (0, 0)) # Display the lobby image
            screen.blit(constants.scaled_return_to_lobby, constants.scaled_return_to_lobby_rect.topleft)

        elif game_state == "game_screen":
            screen.fill("White")  # Display the game screen
            screen.blit(constants.scaled_board, constants.board_rect.topleft) # Display the board
            # Display the different buttons for the modes
            screen.blit(constants.scaled_button_pvp, constants.button_pvp_rect.topleft)
            screen.blit(constants.scaled_button_pvai, constants.button_pvai_rect.topleft)
            screen.blit(constants.scaled_button_aivai, constants.button_aivai_rect.topleft)
            screen.blit(constants.scaled_return_to_lobby, constants.scaled_return_to_lobby_rect.topleft)

        elif game_state == "player_vs_player":
            # Create/Initialize the game (board and pieces)
            if not game:
                game = Game(screen)

            screen.fill("White")  # Display the game screen
            screen.blit(constants.scaled_board, constants.board_rect.topleft) # Display the board
            screen.blit(constants.scaled_reset_button, constants.reset_button_rect.topleft)
            screen.blit(constants.scaled_return_to_lobby, constants.scaled_return_to_lobby_rect)
            if not game.winner(): 
                game.update()
            
            constants.winner(screen, game)

        elif game_state == "player_vs_ai":
            # Screen fixed things
            screen.fill("White")
            screen.blit(constants.scaled_board, constants.board_rect.topleft)
            screen.blit(constants.scaled_reset_button, constants.reset_button_rect.topleft)

            screen.blit(constants.scaled_dif_button_0, constants.scaled_dif_button_0_rect.topleft)
            screen.blit(constants.scaled_dif_button_1, constants.scaled_dif_button_1_rect.topleft)
            screen.blit(constants.scaled_dif_button_2, constants.scaled_dif_button_2_rect.topleft)
            screen.blit(constants.scaled_dif_button_3, constants.scaled_dif_button_3_rect.topleft)

            screen.blit(constants.scaled_return_to_lobby, constants.scaled_return_to_lobby_rect)
            
            if not game.winner():
                # AI's turn (red pieces)
                if game.turn == "r" and not ai_thinking:
                    # Start AI thinking process
                    ai_thinking = True
                    last_ai_move_time = current_time
                
                # Execute AI move after a delay
                if (ai_thinking # If the ai is thinking 
                     and current_time - last_ai_move_time >= ai_move_delay):
                    ai_move = ai_player1.make_move()
                    if ai_move:
                        piece_row, piece_col, move_row, move_col = ai_move
                        
                        # First select the piece
                        game.select(piece_row, piece_col)
                        game.update()  # Show the selected piece and valid moves
                        pygame.display.update()
                        
                        # Wait a moment to show the selection
                        time.sleep(display_time)
                        
                        # Then make the move
                        game.select(move_row, move_col)
                        
                        # If there are no more captures to make, end AI's turn
                        if not game.must_continue_capturing:
                            ai_thinking = False
                        else:
                            # If there are more captures, reset the timer for the next move
                            last_ai_move_time = current_time
                    else:
                        # No valid moves, end AI's turn (shouldn't happen if game logic is correct)
                        ai_thinking = False
            
            if not game.winner(): game.update()
            
            constants.winner(screen, game)

        elif game_state == "ai_vs_ai":
            # Initialize game if needed
            if not game:
                game = Game(screen)
                
            # Screen fixed things
            screen.fill("White")
            screen.blit(constants.scaled_board, constants.board_rect.topleft)
            screen.blit(constants.scaled_reset_button, constants.reset_button_rect.topleft)
            screen.blit(constants.scaled_return_to_lobby, constants.scaled_return_to_lobby_rect)

            # Display the Red AI selection buttons with labels
            screen.blit(constants.scaled_dif_button_0, constants.scaled_dif_button_0_rect.topleft)
            screen.blit(constants.scaled_dif_button_1, constants.scaled_dif_button_1_rect.topleft)
            screen.blit(constants.scaled_dif_button_2, constants.scaled_dif_button_2_rect.topleft)
            screen.blit(constants.scaled_dif_button_3, constants.scaled_dif_button_3_rect.topleft)

            # Display the Blue AI selection buttons
            screen.blit(constants.scaled_dif_button_0, constants.scaled_b_dif_button_0_rect.topleft)
            screen.blit(constants.scaled_dif_button_1, constants.scaled_b_dif_button_1_rect.topleft)
            screen.blit(constants.scaled_dif_button_2, constants.scaled_b_dif_button_2_rect.topleft)
            screen.blit(constants.scaled_dif_button_3, constants.scaled_b_dif_button_3_rect.topleft)
            
            # Check if both AIs are selected before starting gameplay
            if ai_player1 and ai_player2 and not game.winner():
                # Display which AIs are playing
                # (You would need to add text rendering for this)
                
                # Red AI's turn
                if game.turn == "r" and not ai_thinking:
                    ai_thinking = True
                    last_ai_move_time = current_time
                
                # Blue AI's turn
                elif game.turn == "b" and not ai_thinking:
                    ai_thinking = True
                    last_ai_move_time = current_time
                
                # Execute Red AI move
                if (ai_thinking and 
                    game.turn == 'r' and 
                    current_time - last_ai_move_time >= ai_move_delay):
                    
                    ai_move = ai_player1.make_move()
                    if ai_move:
                        piece_row, piece_col, move_row, move_col = ai_move
                        
                        # First select the piece
                        game.select(piece_row, piece_col)
                        game.update()  # Show the selected piece and valid moves
                        pygame.display.update()
                        
                        # Wait a moment to show the selection
                        time.sleep(display_time)
                        
                        # Then make the move
                        game.select(move_row, move_col)
                        
                        # If there are no more captures to make, end AI's turn
                        if not game.must_continue_capturing:
                            ai_thinking = False
                        else:
                            # If there are more captures, reset the timer for the next move
                            last_ai_move_time = current_time
                    else:
                        # No valid moves, end AI's turn
                        ai_thinking = False
                
                # Execute Blue AI move
                elif (ai_thinking and 
                      game.turn == 'b' and 
                      current_time - last_ai_move_time >= ai_move_delay):
                    
                    ai_move = ai_player2.make_move()
                    if ai_move:
                        piece_row, piece_col, move_row, move_col = ai_move
                        
                        # First select the piece
                        game.select(piece_row, piece_col)
                        game.update()  # Show the selected piece and valid moves
                        pygame.display.update()
                        
                        # Wait a moment to show the selection
                        time.sleep(display_time)
                        
                        # Then make the move
                        game.select(move_row, move_col)
                        
                        # If there are no more captures to make, end AI's turn
                        if not game.must_continue_capturing:
                            ai_thinking = False
                        else:
                            # If there are more captures, reset the timer for the next move
                            last_ai_move_time = current_time
                    else:
                        # No valid moves, end AI's turn
                        ai_thinking = False
                        
            # Update game and check for winner
            if not game.winner(): 
                game.update()
                
            constants.winner(screen, game)

        pygame.display.update() # Update the game
        clock.tick(MAX_FPS) # Max frame rate

main()