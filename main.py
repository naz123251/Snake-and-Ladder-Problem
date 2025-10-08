import pygame
import random
import sys
import math
import time

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 1000, 800
GRID_SIZE = 10
CELL_SIZE = 70
BOARD_MARGIN = 50
FPS = 60

# Colors (RGB tuples only)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 60, 60)
GREEN = (60, 180, 75)
BLUE = (65, 105, 225)
YELLOW = (255, 215, 0)
PURPLE = (147, 112, 219)
ORANGE = (255, 140, 0)
LIGHT_BLUE = (173, 216, 230)
LIGHT_GREEN = (144, 238, 144)
LIGHT_RED = (255, 182, 193)
BROWN = (139, 69, 19)
DARK_GREEN = (0, 100, 0)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BOARD_BG = (240, 240, 240)
GRID_COLOR1 = (255, 250, 240)
GRID_COLOR2 = (245, 245, 245)

# Define snakes and ladders
snakes = {
    16: 6, 47: 26, 49: 11, 56: 53, 62: 19, 
    64: 60, 87: 24, 93: 73, 95: 75, 98: 78
}

ladders = {
    1: 38, 4: 14, 9: 31, 21: 42, 28: 84, 
    36: 44, 51: 67, 71: 91, 80: 100
}

class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 5)
        self.speed_x = random.uniform(-3, 3)
        self.speed_y = random.uniform(-3, 3)
        self.life = random.uniform(0.5, 1.5)
        
    def update(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.life -= 0.03
        self.size -= 0.1
        return self.life > 0 and self.size > 0
        
    def draw(self, screen):
        alpha = min(255, max(0, int(255 * self.life)))
        # Create surface with alpha channel
        surf = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        # Use the original color but adjust brightness based on life
        r, g, b = self.color
        adjusted_color = (r, g, b, alpha)
        pygame.draw.circle(surf, adjusted_color, (int(self.size), int(self.size)), int(self.size))
        screen.blit(surf, (int(self.x - self.size), int(self.y - self.size)))

class Player:
    def __init__(self, number, color, name):
        self.number = number
        self.color = color
        self.name = name
        self.position = 0
        self.won = False
        self.target_position = 0
        self.moving = False
        self.move_progress = 0
        self.move_path = []
        self.current_move_index = 0
        self.particles = []
        
    def move_to(self, target_pos):
        self.target_position = target_pos
        self.moving = True
        self.move_progress = 0
        self.current_move_index = 0
        self.move_path = self.calculate_move_path(self.position, target_pos)
        
    def calculate_move_path(self, start, end):
        """Calculate path for smooth movement"""
        path = []
        current = start
        
        while current != end:
            if current < end:
                current += 1
            else:
                current -= 1
            path.append(current)
            
        return path
    
    def update_movement(self):
        if self.moving:
            self.move_progress += 0.05
            if self.move_progress >= 1:
                self.move_progress = 0
                self.position = self.move_path[self.current_move_index]
                self.current_move_index += 1
                
                # Create particles at new position
                x, y = game.get_cell_position(self.position)
                for _ in range(5):
                    self.particles.append(Particle(x, y, self.color))
                
                if self.current_move_index >= len(self.move_path):
                    self.moving = False
                    self.position = self.target_position
                    
                    # Check for win
                    if self.position == 100:
                        self.won = True
                        # Create celebration particles
                        x, y = game.get_cell_position(100)
                        for _ in range(30):
                            self.particles.append(Particle(x, y, GOLD))
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
    def draw(self, screen, x, y):
        # Draw particles
        for particle in self.particles:
            particle.draw(screen)
            
        # Draw player token with gradient effect
        radius = CELL_SIZE // 3
        pygame.draw.circle(screen, self.color, (x, y), radius)
        pygame.draw.circle(screen, WHITE, (x, y), radius, 2)
        
        # Add shine effect
        shine_radius = max(2, radius // 3)
        shine_pos = (x - radius//3, y - radius//3)
        pygame.draw.circle(screen, WHITE, shine_pos, shine_radius)
        
        # Draw player number
        font = pygame.font.SysFont('arial', 16, bold=True)
        text = font.render(str(self.number), True, WHITE)
        text_rect = text.get_rect(center=(x, y))
        screen.blit(text, text_rect)
        
        # Draw player name if space allows
        if CELL_SIZE > 50:
            name_font = pygame.font.SysFont('arial', 10)
            name_text = name_font.render(self.name, True, WHITE)
            name_rect = name_text.get_rect(center=(x, y + radius + 10))
            screen.blit(name_text, name_rect)

class AnimatedDice:
    def __init__(self):
        self.value = 1
        self.rolling = False
        self.roll_start_time = 0
        self.animation_angle = 0
        self.create_dice_surfaces()
        
    def create_dice_surfaces(self):
        self.surfaces = {}
        for value in range(1, 7):
            surf = pygame.Surface((80, 80), pygame.SRCALPHA)
            
            # Draw dice with 3D effect
            # Main face
            pygame.draw.rect(surf, WHITE, (0, 0, 80, 80), border_radius=12)
            pygame.draw.rect(surf, BLACK, (0, 0, 80, 80), 3, border_radius=12)
            
            # Shadow for 3D effect
            pygame.draw.rect(surf, (200, 200, 200), (2, 2, 76, 76), border_radius=10)
            
            # Draw dots
            dot_color = BLACK
            dot_radius = 6
            
            positions = {
                1: [(40, 40)],
                2: [(20, 20), (60, 60)],
                3: [(20, 20), (40, 40), (60, 60)],
                4: [(20, 20), (60, 20), (20, 60), (60, 60)],
                5: [(20, 20), (60, 20), (40, 40), (20, 60), (60, 60)],
                6: [(20, 20), (60, 20), (20, 40), (60, 40), (20, 60), (60, 60)]
            }
            
            for pos in positions[value]:
                pygame.draw.circle(surf, dot_color, pos, dot_radius)
                
            self.surfaces[value] = surf
    
    def roll(self):
        self.rolling = True
        self.roll_start_time = time.time()
        self.animation_angle = 0
        
    def update(self):
        if self.rolling:
            self.animation_angle += 30
            if time.time() - self.roll_start_time > 1.0:
                self.rolling = False
                self.value = random.randint(1, 6)
                return True
            else:
                self.value = random.randint(1, 6)
        return False
    
    def draw(self, screen, x, y):
        if self.rolling:
            # Animated rotation during roll
            rotated_surface = pygame.transform.rotate(self.surfaces[self.value], self.animation_angle)
            new_rect = rotated_surface.get_rect(center=(x + 40, y + 40))
            screen.blit(rotated_surface, new_rect)
        else:
            screen.blit(self.surfaces[self.value], (x, y))

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake and Ladders - Enhanced Edition")
        self.clock = pygame.time.Clock()
        
        # Create players with names
        self.players = [
            Player(1, RED, "Player 1"),
            Player(2, BLUE, "Player 2")
        ]
        
        self.dice = AnimatedDice()
        self.current_player = 0
        self.game_over = False
        self.winner = None
        self.message = "Player 1's turn - Click to roll dice"
        self.font = pygame.font.SysFont('arial', 24)
        self.small_font = pygame.font.SysFont('arial', 18)
        self.title_font = pygame.font.SysFont('arial', 36, bold=True)
        
        # Load background image (optional)
        self.background = self.create_background()
        
    def create_background(self):
        """Create a gradient background"""
        surf = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            # Gradient from light blue to lighter blue
            color = (200 - y//8, 230 - y//8, 255 - y//8)
            pygame.draw.line(surf, color, (0, y), (WIDTH, y))
        return surf
    
    def get_cell_position(self, cell_number):
        """Convert cell number to screen coordinates"""
        if cell_number == 0:
            return BOARD_MARGIN - CELL_SIZE//2, HEIGHT - BOARD_MARGIN - CELL_SIZE//2
            
        row = (cell_number - 1) // GRID_SIZE
        col = (cell_number - 1) % GRID_SIZE
        
        # Alternate direction for each row
        if row % 2 == 1:
            col = GRID_SIZE - 1 - col
            
        x = BOARD_MARGIN + col * CELL_SIZE + CELL_SIZE // 2
        y = HEIGHT - BOARD_MARGIN - row * CELL_SIZE - CELL_SIZE // 2
        return x, y
    
    def draw_board(self):
        # Draw background
        self.screen.blit(self.background, (0, 0))
        
        # Draw board background
        board_rect = pygame.Rect(
            BOARD_MARGIN - 20, 
            BOARD_MARGIN - 20,
            GRID_SIZE * CELL_SIZE + 40,
            GRID_SIZE * CELL_SIZE + 40
        )
        pygame.draw.rect(self.screen, BOARD_BG, board_rect, border_radius=15)
        pygame.draw.rect(self.screen, BLACK, board_rect, 3, border_radius=15)
        
        # Draw title
        title_text = self.title_font.render("SNAKE AND LADDERS", True, BLUE)
        self.screen.blit(title_text, (WIDTH//2 - title_text.get_width()//2, 10))
        
        # Draw cells
        for i in range(1, 101):
            x, y = self.get_cell_position(i)
            
            # Alternate cell colors
            row = (i - 1) // GRID_SIZE
            col = (i - 1) % GRID_SIZE
            color = GRID_COLOR1 if (row + col) % 2 == 0 else GRID_COLOR2
            
            # Draw cell with rounded corners
            cell_rect = pygame.Rect(
                x - CELL_SIZE // 2, 
                y - CELL_SIZE // 2,
                CELL_SIZE, 
                CELL_SIZE
            )
            pygame.draw.rect(self.screen, color, cell_rect, border_radius=8)
            pygame.draw.rect(self.screen, BLACK, cell_rect, 1, border_radius=8)
            
            # Draw cell number
            text = self.small_font.render(str(i), True, BLACK)
            self.screen.blit(text, (x - text.get_width() // 2, y - text.get_height() // 2))
        
        # Draw snakes with better graphics
        for start, end in snakes.items():
            start_pos = self.get_cell_position(start)
            end_pos = self.get_cell_position(end)
            
            # Draw snake body with curves
            self.draw_snake(start_pos, end_pos)
            
            # Draw snake head at start
            self.draw_snake_head(start_pos, end_pos)
            
            # Draw snake tail at end
            pygame.draw.circle(self.screen, DARK_GREEN, end_pos, 8)
        
        # Draw ladders with better graphics
        for start, end in ladders.items():
            start_pos = self.get_cell_position(start)
            end_pos = self.get_cell_position(end)
            self.draw_ladder(start_pos, end_pos)
        
        # Draw players
        player_positions = {}
        for player in self.players:
            if player.position > 0:
                x, y = self.get_cell_position(player.position)
                
                # Offset players so they don't overlap completely
                if player.position in player_positions:
                    count = player_positions[player.position]
                    angle = (count * 90) * (3.14159 / 180)
                    offset_x = math.cos(angle) * 15
                    offset_y = math.sin(angle) * 15
                else:
                    player_positions[player.position] = 0
                    offset_x, offset_y = 0, 0
                
                player.draw(self.screen, int(x + offset_x), int(y + offset_y))
                player_positions[player.position] += 1
        
        # Draw dice area
        dice_area = pygame.Rect(WIDTH - 150, 100, 120, 120)
        pygame.draw.rect(self.screen, WHITE, dice_area, border_radius=15)
        pygame.draw.rect(self.screen, BLACK, dice_area, 2, border_radius=15)
        
        # Draw dice
        self.dice.draw(self.screen, WIDTH - 140, 110)
        
        # Draw game info panel
        info_panel = pygame.Rect(WIDTH - 300, HEIGHT - 200, 280, 180)
        pygame.draw.rect(self.screen, WHITE, info_panel, border_radius=10)
        pygame.draw.rect(self.screen, BLACK, info_panel, 2, border_radius=10)
        
        # Draw message
        text = self.font.render(self.message, True, BLUE)
        self.screen.blit(text, (20, 20))
        
        # Draw player status
        for i, player in enumerate(self.players):
            status = f"{player.name}: Position {player.position}"
            if player.won:
                status += " - 🏆 WINNER!"
            text = self.small_font.render(status, True, player.color)
            self.screen.blit(text, (WIDTH - 290, HEIGHT - 180 + i * 30))
    
    def draw_snake(self, start_pos, end_pos):
        """Draw a curved snake between two points"""
        # Calculate control points for bezier curve
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        
        # Create curved path
        control_x = (start_pos[0] + end_pos[0]) / 2 + dy * 0.3
        control_y = (start_pos[1] + end_pos[1]) / 2 - dx * 0.3
        
        # Draw snake body with multiple segments
        points = []
        for t in range(0, 101, 5):
            t = t / 100
            # Quadratic bezier curve
            x = (1-t)**2 * start_pos[0] + 2*(1-t)*t * control_x + t**2 * end_pos[0]
            y = (1-t)**2 * start_pos[1] + 2*(1-t)*t * control_y + t**2 * end_pos[1]
            points.append((x, y))
        
        # Draw the snake body
        if len(points) > 1:
            pygame.draw.lines(self.screen, RED, False, points, 4)
            
            # Add pattern to snake
            for i in range(0, len(points)-1, 3):
                if i + 1 < len(points):
                    seg_start = points[i]
                    seg_end = points[i + 1]
                    mid_x = (seg_start[0] + seg_end[0]) / 2
                    mid_y = (seg_start[1] + seg_end[1]) / 2
                    pygame.draw.circle(self.screen, (200, 50, 50), (int(mid_x), int(mid_y)), 3)
    
    def draw_snake_head(self, start_pos, end_pos):
        """Draw snake head with direction"""
        # Calculate direction
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        angle = math.atan2(dy, dx)
        
        # Draw snake head (triangle)
        head_size = 12
        points = [
            (start_pos[0] + math.cos(angle) * head_size, 
             start_pos[1] + math.sin(angle) * head_size),
            (start_pos[0] + math.cos(angle + 2.5) * head_size * 0.7, 
             start_pos[1] + math.sin(angle + 2.5) * head_size * 0.7),
            (start_pos[0] + math.cos(angle - 2.5) * head_size * 0.7, 
             start_pos[1] + math.sin(angle - 2.5) * head_size * 0.7)
        ]
        
        pygame.draw.polygon(self.screen, RED, points)
        # Draw eyes
        eye_pos = (
            start_pos[0] + math.cos(angle) * head_size * 0.5,
            start_pos[1] + math.sin(angle) * head_size * 0.5
        )
        pygame.draw.circle(self.screen, WHITE, (int(eye_pos[0]), int(eye_pos[1])), 3)
        pygame.draw.circle(self.screen, BLACK, (int(eye_pos[0]), int(eye_pos[1])), 1)
    
    def draw_ladder(self, start_pos, end_pos):
        """Draw a detailed ladder between two points"""
        dx = end_pos[0] - start_pos[0]
        dy = end_pos[1] - start_pos[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
            
        # Normalize direction
        dx, dy = dx/length, dy/length
        
        # Perpendicular vector
        perp_dx, perp_dy = -dy, dx
        
        # Draw ladder sides
        side_offset = 8
        side1_start = (start_pos[0] + perp_dx * side_offset, start_pos[1] + perp_dy * side_offset)
        side1_end = (end_pos[0] + perp_dx * side_offset, end_pos[1] + perp_dy * side_offset)
        side2_start = (start_pos[0] - perp_dx * side_offset, start_pos[1] - perp_dy * side_offset)
        side2_end = (end_pos[0] - perp_dx * side_offset, end_pos[1] - perp_dy * side_offset)
        
        pygame.draw.line(self.screen, BROWN, side1_start, side1_end, 4)
        pygame.draw.line(self.screen, BROWN, side2_start, side2_end, 4)
        
        # Draw ladder rungs
        num_rungs = max(3, int(length / 20))
        for i in range(1, num_rungs):
            t = i / num_rungs
            rung_start = (
                side1_start[0] + (side1_end[0] - side1_start[0]) * t,
                side1_start[1] + (side1_end[1] - side1_start[1]) * t
            )
            rung_end = (
                side2_start[0] + (side2_end[0] - side2_start[0]) * t,
                side2_start[1] + (side2_end[1] - side2_start[1]) * t
            )
            pygame.draw.line(self.screen, BROWN, rung_start, rung_end, 3)
    
    def handle_click(self):
        if self.game_over:
            # Reset game
            self.__init__()
            return
            
        if not self.dice.rolling and not any(player.moving for player in self.players):
            self.dice.roll()
            self.message = f"{self.players[self.current_player].name} is rolling..."
    
    def update(self):
        # Update player movements
        for player in self.players:
            player.update_movement()
        
        # Update dice
        if self.dice.rolling:
            if self.dice.update():
                # Dice finished rolling
                if not any(player.moving for player in self.players):
                    steps = self.dice.value
                    current_player = self.players[self.current_player]
                    
                    # Calculate new position
                    new_pos = current_player.position + steps
                    if new_pos > 100:
                        new_pos = 100 - (new_pos - 100)
                    
                    # Apply snakes and ladders
                    if new_pos in snakes:
                        new_pos = snakes[new_pos]
                    elif new_pos in ladders:
                        new_pos = ladders[new_pos]
                    
                    # Start movement animation
                    current_player.move_to(new_pos)
                    
                    if new_pos == 100:
                        self.game_over = True
                        self.winner = self.current_player
                        self.message = f"🎉 {current_player.name} WINS! Click to play again"
                    else:
                        self.current_player = (self.current_player + 1) % len(self.players)
                        self.message = f"{self.players[self.current_player].name}'s turn - Click to roll dice"
    
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