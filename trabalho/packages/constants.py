import pygame

# Original Size (width, height)
ORIGINAL_WIDTH = 1280
ORIGINAL_HEIGHT = 720

# Load images
lobby_screen = pygame.image.load('images/Dameo!!!!.png')
play_button = pygame.image.load('images/Play_button(1).png')
board = pygame.image.load('images/Board.png')
button_pvp = pygame.image.load('images/pl_pl.png')
button_pvai = pygame.image.load('images/pl_ai.png')
button_aivai = pygame.image.load('images/ai_ai.png')
red_wins = pygame.image.load('images/Redwins.png')
blue_wins = pygame.image.load('images/Bluewins.png')

dif_button_0 = pygame.image.load('images/Nivel_0.png')
dif_button_1 = pygame.image.load('images/Nivel_1.png')
dif_button_2 = pygame.image.load('images/Nivel_2.png')
dif_button_3 = pygame.image.load('images/Nivel_3.png')

reset_button = pygame.image.load('images/reset_button.png')
return_to_lobby = pygame.image.load('images/return_to_lobby.png')
info_button = pygame.image.load('images/Instructions.png')
info_screen = pygame.image.load('images/Instructions_screen.png')


def resize_elements():
    # Global variables
    global screen_w, screen_h, scaled_lobby, scaled_play, play_button_rect, scaled_board, board_rect, scaled_button_pvp, button_pvp_rect, scaled_button_pvai, button_pvai_rect, scaled_button_aivai, button_aivai_rect, scaled_red_wins,red_wins_rect, scaled_blue_wins, blue_wins_rect, scaled_reset_button, reset_button_rect, scaled_dif_button_0,scaled_dif_button_1, scaled_dif_button_0_rect, scaled_dif_button_1_rect, scaled_dif_button_2,scaled_dif_button_3, scaled_dif_button_2_rect, scaled_dif_button_3_rect, scaled_return_to_lobby, scaled_return_to_lobby_rect, scaled_b_dif_button_0_rect, scaled_b_dif_button_1_rect, scaled_b_dif_button_2_rect, scaled_b_dif_button_3_rect, scaled_info_button, scaled_info_button_rect, scaled_info_screen
    
    # Get the screen width and height
    screen_w, screen_h = pygame.display.get_surface().get_size()
    
    # Scale lobby screen to fit window

    scaled_lobby = pygame.transform.scale(lobby_screen, (screen_w, screen_h)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    
    # Scale play button proportionally (adjust sizes as needed)

    scaled_play = pygame.transform.scale(play_button, (screen_w // 7, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    play_button_rect = scaled_play.get_rect(center=(screen_w // 2, screen_h - (screen_h // 4))) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    
    scaled_button_pvp = pygame.transform.scale(button_pvp, (screen_w // 8, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    button_pvp_rect = scaled_button_pvp.get_rect(center=(screen_w // 3, screen_h // 2)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    
    scaled_button_pvai = pygame.transform.scale(button_pvai, (screen_w // 8, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    button_pvai_rect = scaled_button_pvai.get_rect(center=(screen_w // 2, screen_h // 2)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    
    scaled_button_aivai = pygame.transform.scale(button_aivai, (screen_w // 8, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    button_aivai_rect = scaled_button_aivai.get_rect(center=(screen_w - (screen_w // 3), screen_h // 2)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    
    scaled_reset_button = pygame.transform.scale(reset_button, (screen_w // 15, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    reset_button_rect = scaled_reset_button.get_rect(center=(screen_w - (screen_w // 5.1), screen_h // 12)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    
    # Scale board proportionally (adjust sizes as needed)

    scaled_board = pygame.transform.scale(board, (screen_w // (32/17), screen_h // (18/17))) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    board_rect = scaled_board.get_rect(center=(screen_w // 2, screen_h // 2)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
   
    scaled_red_wins = pygame.transform.scale(red_wins, (screen_w // (32/17), screen_h // (18/17))) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    red_wins_rect = scaled_red_wins.get_rect(center=(screen_w // 2, screen_h // 2)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    
    scaled_blue_wins = pygame.transform.scale(blue_wins, (screen_w // (32/17), screen_h // (18/17))) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    blue_wins_rect = scaled_blue_wins.get_rect(center=(screen_w // 2, screen_h // 2)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    
    # With the keyword argument center we make the rectangle be in the center of the screen, originaly at (300, 20)

    # BOARD_W, BOARD_H = (screen_w // (32/17), screen_h // (18/17))# The initial size of the board is (680, 680)
    # scaled_r_piece = pygame.transform.scale(red_piece, (screen_w // 11, screen_h // (180 / 29)))
    # piece_r_rect = scaled_r_piece.get_rect(center=(((screen_w * 28) / 128) + ((screen_w * 8) / 128)*2, 5 + (screen_h / 9)*8))

    # scaled_b_piece = pygame.transform.scale(blue_piece, (screen_w // 11, screen_h // (180 / 29)))
    # piece_b_rect = scaled_b_piece.get_rect(center=(((screen_w * 28) / 128) + ((screen_w * 8) / 128)*2, 5 + (screen_h / 9)*2))

    scaled_dif_button_0 = pygame.transform.scale(dif_button_0, (screen_w // 15, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    scaled_dif_button_0_rect = scaled_dif_button_0.get_rect(center=(screen_w // 5.1, screen_h // 12)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    scaled_b_dif_button_0_rect = scaled_dif_button_0.get_rect(center=(screen_w // 5.1, screen_h -(screen_h // 12))) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image


    scaled_dif_button_1 = pygame.transform.scale(dif_button_1, (screen_w // 15, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    scaled_dif_button_1_rect = scaled_dif_button_1.get_rect(center=(screen_w // 5.1, screen_h // 5)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    scaled_b_dif_button_1_rect = scaled_dif_button_1.get_rect(center=(screen_w // 5.1, screen_h - (screen_h // 5))) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image


    scaled_dif_button_2 = pygame.transform.scale(dif_button_2, (screen_w // 15, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    scaled_dif_button_2_rect = scaled_dif_button_2.get_rect(center=(screen_w // 5.1, screen_h // 3.15)) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image
    scaled_b_dif_button_2_rect = scaled_dif_button_2.get_rect(center=(screen_w // 5.1, screen_h -(screen_h // 3.15))) # Returns a new rectangle covering the entire surface. This rectangle will always start at (0, 0) with a width and height the same size as the image


    scaled_dif_button_3 = pygame.transform.scale(dif_button_3, (screen_w // 15, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    scaled_dif_button_3_rect = scaled_dif_button_3.get_rect(center=(screen_w // 5.1, screen_h // 2.3)) # Returns a new rectangle covering the entire surf`ace. This rectangle will always start at (0, 0) with a width and height the same size as the image
    scaled_b_dif_button_3_rect = scaled_dif_button_3.get_rect(center=(screen_w // 5.1, screen_h - (screen_h // 2.3))) # Returns a new rectangle covering the entire surf`ace. This rectangle will always start at (0, 0) with a width and height the same size as the image


    scaled_return_to_lobby = pygame.transform.scale(return_to_lobby, (screen_w // 15, screen_h // 10)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results
    scaled_return_to_lobby_rect = scaled_return_to_lobby.get_rect(center=(screen_w - (screen_w // 5.1), screen_h - (screen_h // 12))) # Returns a new rectangle covering the entire surf`ace. This rectangle will always start at (0, 0) with a width and height the same size as the image

    scaled_info_button = pygame.transform.scale(info_button, (screen_w // 15, screen_h // 10))
    scaled_info_button_rect = scaled_info_button.get_rect(center=(screen_w - (screen_w // 2), screen_h - (screen_h // 12))) # Returns a new rectangle covering the entire surf`ace. This rectangle will always start at (0, 0) with a width and height the same size as the image

    scaled_info_screen = pygame.transform.scale(info_screen, (screen_w, screen_h)) # Resizes the Surface to a new size, given as (width, height). This is a fast scale operation that does not sample the results



def reset_the_game(game):
    game.reset()

def winner(window, game):
    if game.winner() == "b":
        window.blit(scaled_blue_wins, blue_wins_rect.topleft)
    elif game.winner() == "r":
        window.blit(scaled_red_wins, red_wins_rect.topleft)
    else: return None
