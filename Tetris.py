import pygame
from pathlib import Path

# Import all modules
from constants import WINDOW_SIZE
from menu import Menu
from game import Game
from drawing import draw_board, draw_piece, draw_leaderboard, draw_name_input_screen
from database import get_leaderboard, save_score_to_database


def main():
    # Initialize pygame
    pygame.mixer.pre_init()
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    pygame.display.set_caption("Tetris")
    clock = pygame.time.Clock()

    # Asset path
    BASE_DIR = Path(__file__).parent
    ASSETS_DIR = BASE_DIR / "assets"

    # Play song
    pygame.mixer.music.load(str(ASSETS_DIR / "intro-theme.mp3"))
    pygame.mixer.music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    # Load sound effects early
    sounds = {
        'placed': pygame.mixer.Sound(str(ASSETS_DIR / "bloop-short.mp3")),
        'line_clear': pygame.mixer.Sound(str(ASSETS_DIR /"debris-break.mp3")),
    }
    
    # Game settings
    start_x, start_y = 100, 60
    preview_x, preview_y = 350, 100
    block_size = 20
    fps = 25
    
    # Initialize menu and game state
    menu = Menu()
    game = None
    game_state = "menu"  # "menu" or "playing"
    counter = 0
    pressing_down = False
    done = False
    
    # Fetch leaderboard at start
    leaderboard_data = get_leaderboard()
    
    while not done:
        counter += 1
        if counter > 100000:
            counter = 0
        
        # Automatic piece dropping (only when playing)
        if counter % (fps // 2) == 0 or pressing_down:
            if game_state == "playing" and game and game.state == "playing":
                game.tick()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                
            if event.type == pygame.KEYDOWN:
                if game_state == "menu":
                    # Handle menu input
                    menu_action = menu.handle_input(event)
                    if menu_action == "start_game":
                        # Start the game with the selected theme
                        game = Game(sounds=sounds, theme_name=menu.theme_name)
                        game_state = "playing"
                        counter = 0
                        pressing_down = False
                    elif menu_action == "quit":
                        done = True
                
                elif game_state == "playing" and game:
                    if event.key == pygame.K_ESCAPE and game.state == "playing":
                        # Return to menu from game
                        game_state = "menu"
                        menu = Menu(theme_name=game.theme_name if game else "Dark")
                        game = None
                    elif event.key == pygame.K_UP:
                        game.rotate_piece()
                    elif event.key == pygame.K_LEFT:
                        game.move_piece(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        game.move_piece(1, 0)
                    elif event.key == pygame.K_SPACE:
                        game.drop_piece()
                    elif event.key == pygame.K_DOWN:
                        pressing_down = True
                    elif game.state == "entering_name":
                        if event.key == pygame.K_RETURN:
                            # Save score if name is entered
                            if game.player_name.strip():
                                if save_score_to_database(game.player_name.strip(), game.score):
                                    leaderboard_data = get_leaderboard()  # Refresh leaderboard
                                    game.score_saved = True
                                game.state = "gameover"
                            else:
                                # Don't allow empty names
                                pass
                        elif event.key == pygame.K_ESCAPE:
                            # Skip saving and go to game over screen
                            game.state = "gameover"
                        elif event.key == pygame.K_BACKSPACE:
                            # Remove last character
                            game.player_name = game.player_name[:-1]
                        else:
                            # Add character to name (limit to reasonable length)
                            if len(game.player_name) < 20:
                                if event.unicode.isprintable():
                                    game.player_name += event.unicode
                    elif event.key == pygame.K_1:
                        game.set_theme("Classic")
                    elif event.key == pygame.K_2:
                        game.set_theme("Starry")
                    elif event.key == pygame.K_3:
                        game.set_theme("Dark")
                    elif event.key == pygame.K_q and game.state == "gameover":
                        game_state = "menu"
                        menu = Menu(theme_name=game.theme_name)  # Keep the theme from game
                        game = None
                    elif event.key == pygame.K_r and game.state == "gameover":
                        game = Game(sounds=sounds, theme_name=game.theme_name)
                        counter = 0
                        pressing_down = False
                        
            if event.type == pygame.KEYUP and event.key == pygame.K_DOWN:
                pressing_down = False
        
        # Draw everything based on current state
        if game_state == "menu":
            menu.draw(screen)
        elif game_state == "playing" and game:
            # Draw game
            draw_board(screen, game.board, start_x, start_y, preview_x, preview_y, block_size, game.theme)
            draw_piece(screen, game.current_piece, start_x, start_y, block_size)
            
            # Place preview piece in box
            draw_piece(screen, game.next_piece, preview_x, preview_y, block_size)

            # Draw score
            font = pygame.font.SysFont('Calibri', 25, True, False)
            score_text = font.render(f"Score: {game.score}", True, game.theme["text"])
            screen.blit(score_text, [10, 10])
            
            # Draw leaderboard
            draw_leaderboard(screen, leaderboard_data, 350, 200, game.theme)
            
            # Draw name input screen
            if game.state == "entering_name":
                draw_name_input_screen(screen, game)
            
            # Draw game over screen
            elif game.state == "gameover":
                font_large = pygame.font.SysFont('Calibri', 65, True, False)
                font_medium = pygame.font.SysFont('Calibri', 40, True, False)
                font_small = pygame.font.SysFont('Calibri', 24, False, False)
                game_over_text = font_large.render("Game Over", True, (255, 0, 0))
                quit_text = font_medium.render("Press Q to Menu", True, (255, 215, 0))
                replay_text = font_large.render("Press R to Replay", True, (0, 0, 255))
                screen.blit(game_over_text, [20, 200])
                screen.blit(quit_text, [25, 265])
                screen.blit(replay_text, [25, 330])
        
        pygame.display.flip()
        clock.tick(fps)
    
    pygame.quit()


if __name__ == "__main__":
    main()