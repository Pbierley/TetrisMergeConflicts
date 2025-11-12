import pygame
from constants import THEMES, WINDOW_SIZE


class Menu:
    """Manages the start menu system"""
    
    def __init__(self, theme_name="Dark"):
        self.state = "main"  # "main", "settings"
        self.selected_option = 0  # Currently selected menu option
        self.theme_name = theme_name
        self.theme = THEMES[theme_name]
        self.theme_options = list(THEMES.keys())
        self.selected_theme_index = self.theme_options.index(theme_name)
        
        # Menu options
        self.main_menu_options = ["Start Game", "Settings", "Quit"]
        self.settings_menu_options = ["Theme", "Back"]
    
    def handle_input(self, event):
        """Handle menu input"""
        if event.type == pygame.KEYDOWN:
            if self.state == "main":
                return self._handle_main_menu_input(event)
            elif self.state == "settings":
                return self._handle_settings_menu_input(event)
        return None
    
    def _handle_main_menu_input(self, event):
        """Handle main menu input"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.main_menu_options)
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.main_menu_options)
        elif event.key == pygame.K_RETURN:
            if self.selected_option == 0:  # Start Game
                return "start_game"
            elif self.selected_option == 1:  # Settings
                self.state = "settings"
                self.selected_option = 0
            elif self.selected_option == 2:  # Quit
                return "quit"
        return None
    
    def _handle_settings_menu_input(self, event):
        """Handle settings menu input"""
        if event.key == pygame.K_UP:
            self.selected_option = (self.selected_option - 1) % len(self.settings_menu_options)
        elif event.key == pygame.K_DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.settings_menu_options)
        elif event.key == pygame.K_RETURN:
            if self.selected_option == 0:  # Theme
                self._cycle_theme()
            elif self.selected_option == 1:  # Back
                self.state = "main"
                self.selected_option = 0
        elif event.key == pygame.K_ESCAPE:
            self.state = "main"
            self.selected_option = 0
        elif event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            if self.selected_option == 0:  # Theme option selected
                self._cycle_theme()
        return None
    
    def _cycle_theme(self):
        """Cycle through available themes"""
        self.selected_theme_index = (self.selected_theme_index + 1) % len(self.theme_options)
        self.theme_name = self.theme_options[self.selected_theme_index]
        self.theme = THEMES[self.theme_name]
    
    def draw(self, screen):
        """Draw the menu"""
        screen.fill(self.theme["background"])
        
        if self.state == "main":
            self._draw_main_menu(screen)
        elif self.state == "settings":
            self._draw_settings_menu(screen)
    
    def _draw_main_menu(self, screen):
        """Draw the main menu"""
        # Title
        title_font = pygame.font.SysFont('Calibri', 72, True, False)
        title_text = title_font.render("TETRIS", True, self.theme["text"])
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_font = pygame.font.SysFont('Calibri', 24, False, True)
        subtitle_text = subtitle_font.render("Classic Block Puzzle Game", True, self.theme["text"])
        subtitle_rect = subtitle_text.get_rect(center=(WINDOW_SIZE[0] // 2, 120))
        screen.blit(subtitle_text, subtitle_rect)
        
        # Menu options
        menu_font = pygame.font.SysFont('Calibri', 48, True, False)
        start_y = 200
        
        for i, option in enumerate(self.main_menu_options):
            color = (255, 255, 0) if i == self.selected_option else self.theme["text"]
            option_text = menu_font.render(option, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_SIZE[0] // 2, start_y + i * 60))
            screen.blit(option_text, option_rect)
            
            # Draw selection indicator
            if i == self.selected_option:
                pygame.draw.rect(screen, (255, 255, 0), option_rect.inflate(20, 10), 3)
        
        # Instructions
        instruction_font = pygame.font.SysFont('Calibri', 20, False, False)
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER to select",
            "Press ESC during game to return to menu"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = instruction_font.render(instruction, True, self.theme["text"])
            instruction_rect = instruction_text.get_rect(center=(WINDOW_SIZE[0] // 2, 420 + i * 22))
            screen.blit(instruction_text, instruction_rect)
    
    def _draw_settings_menu(self, screen):
        """Draw the settings menu"""
        # Title
        title_font = pygame.font.SysFont('Calibri', 48, True, False)
        title_text = title_font.render("SETTINGS", True, self.theme["text"])
        title_rect = title_text.get_rect(center=(WINDOW_SIZE[0] // 2, 80))
        screen.blit(title_text, title_rect)
        
        # Settings options
        menu_font = pygame.font.SysFont('Calibri', 36, True, False)
        start_y = 180
        
        for i, option in enumerate(self.settings_menu_options):
            if option == "Theme":
                display_text = f"Theme: {self.theme_name}"
            else:
                display_text = option
                
            color = (255, 255, 0) if i == self.selected_option else self.theme["text"]
            option_text = menu_font.render(display_text, True, color)
            option_rect = option_text.get_rect(center=(WINDOW_SIZE[0] // 2, start_y + i * 80))
            screen.blit(option_text, option_rect)
            
            # Draw selection indicator
            if i == self.selected_option:
                pygame.draw.rect(screen, (255, 255, 0), option_rect.inflate(20, 10), 3)
        
        # Theme preview
        if self.selected_option == 0:  # Theme option selected
            preview_font = pygame.font.SysFont('Calibri', 24, False, False)
            preview_text = preview_font.render("Press LEFT/RIGHT or ENTER to change theme", True, self.theme["text"])
            preview_rect = preview_text.get_rect(center=(WINDOW_SIZE[0] // 2, 320))
            screen.blit(preview_text, preview_rect)
        
        # Instructions
        instruction_font = pygame.font.SysFont('Calibri', 24, False, False)
        instructions = [
            "Use UP/DOWN arrows to navigate",
            "Press ENTER to select/change",
            "Press ESC to go back"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = instruction_font.render(instruction, True, self.theme["text"])
            instruction_rect = instruction_text.get_rect(center=(WINDOW_SIZE[0] // 2, 380 + i * 25))
            screen.blit(instruction_text, instruction_rect)

