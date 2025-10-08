import pygame
import random
import sys
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 800
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
GREEN = (50, 255, 50)
BLUE = (50, 50, 255)
YELLOW = (255, 255, 50)
PURPLE = (180, 50, 230)
ORANGE = (255, 165, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
BROWN = (165, 42, 42)
DARK_GREEN = (0, 100, 0)

# Define snakes and ladders
snakes = {
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 64: 60, 87: 24, 93: 73, 95: 75, 98: 78
}

ladders = {
    1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 36: 44, 51: 67, 71: 91, 80: 100
}

class Player:
    def __init__(self, number, color):
        self.number = number
        self.color = color
        self.position = 0
        self.won = False
        
    def move(self, steps):
        self.position += steps
        if self.position > 100:
            self.position = 100 - (self.position - 100)
        
        # Check for snakes
        if self.position in snakes:
            self.position = snakes[self.position]
            
        # Check for ladders
        if self.position in ladders:
            self.position = ladders[self.position]
            
        if self.position == 100:
            self.won = True
            
    def draw(self, screen, x, y):
        pygame.draw.circle(screen, self.color, (x, y), CELL_SIZE // 3)
        font = pygame.font.SysFont(None, 24)
        text = font.render(str(self.number), True, WHITE)
        screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))

class Dice:
    def __init__(self):
        self.value = 1
        self.rolling = False
        self.roll_start_time = 0
        
    def create_dice_surface(self, value):
        """Create a dice surface with the given value"""
        surf = pygame.Surface((80, 80))
        surf.fill(WHITE)
        pygame.draw.rect(surf, BLACK, (0, 0, 80, 80), 3)
        
        # Draw dots based on dice value
        dot_color = BLACK
        dot_radius = 6
        
        if value == 1:
            pygame.draw.circle(surf, dot_color, (40, 40), dot_radius)
        elif value == 2:
            pygame.draw.circle(surf, dot_color, (25, 25), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 55), dot_radius)
        elif value == 3:
            pygame.draw.circle(surf, dot_color, (25, 25), dot_radius)
            pygame.draw.circle(surf, dot_color, (40, 40), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 55), dot_radius)
        elif value == 4:
            pygame.draw.circle(surf, dot_color, (25, 25), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 25), dot_radius)
            pygame.draw.circle(surf, dot_color, (25, 55), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 55), dot_radius)
        elif value == 5:
            pygame.draw.circle(surf, dot_color, (25, 25), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 25), dot_radius)
            pygame.draw.circle(surf, dot_color, (40, 40), dot_radius)
            pygame.draw.circle(surf, dot_color, (25, 55), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 55), dot_radius)
        elif value == 6:
            pygame.draw.circle(surf, dot_color, (25, 20), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 20), dot_radius)
            pygame.draw.circle(surf, dot_color, (25, 40), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 40), dot_radius)
            pygame.draw.circle(surf, dot_color, (25, 60), dot_radius)
            pygame.draw.circle(surf, dot_color, (55, 60), dot_radius)
        
        return surf
    
    def roll(self):
        self.rolling = True
        self.roll_start_time = time.time()
        
    def update(self):
        if self.rolling:
            if time.time() - self.roll_start_time > 1.0:  # Roll for 1 second
                self.rolling = False
                self.value = random.randint(1, 6)
                return True
            else:
                self.value = random.randint(1, 6)
        return False
    
    def draw(self, screen, x, y):
        dice_surface = self.create_dice_surface(self.value)
        screen.blit(dice_surface, (x, y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake and Ladders")
        self.clock = pygame.time.Clock()
        self.players = [
            Player(1, RED),
            Player(2, BLUE)
        ]
        self.dice = Dice()
        self.current_player = 0
        self.game_over = False
        self.winner = None
        self.message = "Player 1's turn - Click to roll dice"
        self.font = pygame.font.SysFont(None, 32)
        self.small_font = pygame.font.SysFont(None, 24)
        
    def get_cell_position(self, cell_number):
        """Convert cell number to screen coordinates"""
        row = (cell_number - 1) // GRID_SIZE
        col = (cell_number - 1) % GRID_SIZE
        
        # Alternate direction for each row
        if row % 2 == 1:
            col = GRID_SIZE - 1 - col
            
        x = col * CELL_SIZE + CELL_SIZE // 2
        y = HEIGHT - (row * CELL_SIZE) - CELL_SIZE // 2
        return x, y
    
    def draw_board(self):
        # Draw background
        self.screen.fill(LIGHT_BLUE)
        
        # Draw cells
        for i in range(1, 101):
            x, y = self.get_cell_position(i)
            
            # Alternate cell colors
            row = (i - 1) // GRID_SIZE
            col = (i - 1) % GRID_SIZE
            color = LIGHT_GREEN if (row + col) % 2 == 0 else WHITE
            
            pygame.draw.rect(self.screen, color, 
                           (x - CELL_SIZE // 2, y - CELL_SIZE // 2, 
                            CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(self.screen, BLACK, 
                           (x - CELL_SIZE // 2, y - CELL_SIZE // 2, 
                            CELL_SIZE, CELL_SIZE), 1)
            
            # Draw cell number
            text = self.small_font.render(str(i), True, BLACK)
            self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
        
        # Draw snakes
        for start, end in snakes.items():
            start_pos = self.get_cell_position(start)
            end_pos = self.get_cell_position(end)
            pygame.draw.line(self.screen, RED, start_pos, end_pos, 5)
            pygame.draw.circle(self.screen, RED, start_pos, 8)
            pygame.draw.circle(self.screen, DARK_GREEN, end_pos, 8)
        
        # Draw ladders
        for start, end in ladders.items():
            start_pos = self.get_cell_position(start)
            end_pos = self.get_cell_position(end)
            
            # Draw ladder as multiple lines
            dx = end_pos[0] - start_pos[0]
            dy = end_pos[1] - start_pos[1]
            
            for i in range(-2, 3):
                offset_x = i * 5 * dx / max(1, abs(dx))
                offset_y = i * 5 * dy / max(1, abs(dy))
                pygame.draw.line(self.screen, BROWN, 
                               (start_pos[0] + offset_x, start_pos[1] + offset_y),
                               (end_pos[0] + offset_x, end_pos[1] + offset_y), 3)
        
        # Draw players
        player_positions = {}
        for player in self.players:
            if player.position > 0:
                x, y = self.get_cell_position(player.position)
                # Offset players so they don't overlap completely
                if player.position in player_positions:
                    count = player_positions[player.position]
                    offset_x = (count % 2) * 15 - 7
                    offset_y = (count // 2) * 15 - 7
                else:
                    player_positions[player.position] = 0
                    offset_x, offset_y = 0, 0
                
                player.draw(self.screen, x + offset_x, y + offset_y)
                player_positions[player.position] += 1
        
        # Draw dice
        self.dice.draw(self.screen, WIDTH - 100, 50)
        
        # Draw message
        text = self.font.render(self.message, True, BLACK)
        self.screen.blit(text, (20, 20))
        
        # Draw player status
        for i, player in enumerate(self.players):
            status = f"Player {player.number}: Position {player.position}"
            if player.won:
                status += " - WINNER!"
            text = self.small_font.render(status, True, player.color)
            self.screen.blit(text, (20, 60 + i * 25))
    
    def handle_click(self):
        if self.game_over:
            # Reset game
            self.__init__()
            return
            
        if not self.dice.rolling:
            self.dice.roll()
            self.message = f"Player {self.current_player + 1} rolling..."
    
    def update(self):
        if self.dice.rolling:
            if self.dice.update():
                # Dice finished rolling
                steps = self.dice.value
                self.players[self.current_player].move(steps)
                
                if self.players[self.current_player].won:
                    self.game_over = True
                    self.winner = self.current_player
                    self.message = f"Player {self.current_player + 1} WINS! Click to play again"
                else:
                    self.current_player = (self.current_player + 1) % len(self.players)
                    self.message = f"Player {self.current_player + 1}'s turn - Click to roll dice"
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_click()
            
            self.update()
            self.draw_board()
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()