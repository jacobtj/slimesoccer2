import pygame
import random

# Define game constants
WIDTH = 800
HEIGHT = 600
FPS = 60

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialize Pygame
pygame.init()

# Set up the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Slime Soccer")

# Set up the game clock
clock = pygame.time.Clock()

# Define player constants
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 10
PLAYER_GRAVITY = 0.5
PLAYER_SIZE = 50

# Define ball constants
BALL_SPEED = 5
BALL_SIZE = 25
BALL_GRAVITY = 0.2

# Define player classes
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, color, player_number):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = 0
        self.vel_y = 0
        self.player_number = player_number
        self.score = 0

    def update(self):
        self.vel_y += PLAYER_GRAVITY
        keys = pygame.key.get_pressed()
        if self.player_number == 1:
            if keys[pygame.K_a]:
                self.vel_x = -PLAYER_SPEED
            elif keys[pygame.K_d]:
                self.vel_x = PLAYER_SPEED
            else:
                self.vel_x = 0
            if keys[pygame.K_w] and self.rect.bottom >= HEIGHT:
                self.vel_y = -PLAYER_JUMP_SPEED
        else:
            if keys[pygame.K_LEFT]:
                self.vel_x = -PLAYER_SPEED
            elif keys[pygame.K_RIGHT]:
                self.vel_x = PLAYER_SPEED
            else:
                self.vel_x = 0
            if keys[pygame.K_UP] and self.rect.bottom >= HEIGHT:
                self.vel_y = -PLAYER_JUMP_SPEED
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.vel_x = BALL_SPEED
        self.vel_y = 0

    def update(self, collided_players, player1, player2):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        self.vel_y += BALL_GRAVITY
        if self.rect.left < 0:
            self.rect.left = 0
            self.vel_x *= -1
        elif self.rect.right > WIDTH:
            self.rect.right = WIDTH
            self.vel_x *= -1
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y *= -1
        elif self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
            self.vel_y = -self.vel_y * 0.8
        self.vel_x *= 0.99
        self.vel_y *= 0.99
        if collided_players:
            self.vel_y = -BALL_SPEED
            player = collided_players[0]
            offset = self.rect.centerx - player.rect.centerx
            self.vel_x = offset * 0.2

    
    def reset(self, screen_width, screen_height):
        self.x = screen_width // 2
        self.y = screen_height // 2
        self.rect.x = screen_width // 2
        self.rect.y = screen_height // 2
        self.vel_x = 0

# define the menu options
menu_options = ['Resume Game', 'Restart Game']

# define the menu function
def render_menu():
    # create a menu surface
    menu_surface = pygame.Surface((WIDTH, HEIGHT))
    menu_surface.fill(WHITE)

    # add the menu options to the surface
    for i, option in enumerate(menu_options):
        text_surface = font.render(option, True, BLACK)
        text_rect = text_surface.get_rect()
        text_rect.center = (WIDTH / 2, HEIGHT / 2 + i * 50)
        menu_surface.blit(text_surface, text_rect)

    # draw the menu surface to the screen
    screen.blit(menu_surface, (0, 0))

    # update the display
    pygame.display.flip()

def restart_game():
    pass


# Create players and ball
player1 = Player(100, HEIGHT - PLAYER_SIZE, (255, 0, 0), 1)
player2 = Player(WIDTH - 100 - PLAYER_SIZE, HEIGHT - PLAYER_SIZE, (0, 0, 255), 2)
ball = Ball(WIDTH/2 - BALL_SIZE/2, HEIGHT/2 - BALL_SIZE/2)

# Create sprite groups
all_sprites = pygame.sprite.Group()
all_sprites.add(player1)
all_sprites.add(player2)
all_sprites.add(ball)

players = pygame.sprite.Group()
players.add(player1)
players.add(player2)

ball_sprite = pygame.sprite.GroupSingle()
ball_sprite.add(ball)

# define the goal dimensions and positions
goal_width = 50
goal_height = 130
goal_left = pygame.Rect(0, (HEIGHT - goal_height), goal_width, goal_height)
goal_right = pygame.Rect(WIDTH - goal_width, (HEIGHT - goal_height), goal_width, goal_height)
cross_b_left = pygame.Rect(0, (HEIGHT - goal_height) - 10, goal_width, 10)
cross_b_right = pygame.Rect(WIDTH - goal_width, (HEIGHT - goal_height) - 10, goal_width, 10)

# draw the goals on the screen
pygame.draw.rect(screen, (255, 255, 255), goal_left)
pygame.draw.rect(screen, (255, 255, 255), goal_right)
pygame.draw.rect(screen, (0, 0, 255), cross_b_left)
pygame.draw.rect(screen, (0, 0, 255), cross_b_right)


# define the initial scores
score_left = 0
score_right = 0

# Game loop
running = True
while running:
    #print("Game loop running")
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Detect collisions
    collided_players = pygame.sprite.spritecollide(ball, players, False)
    if collided_players:
        if ball.vel_y > 0:
            ball.vel_y = -BALL_SPEED
    
    if ball.rect.colliderect(cross_b_left) or ball.rect.colliderect(cross_b_right):
        ball.vel_y = -ball.vel_y * 0.8
        ball.vel_x = -ball.vel_x * 0.8
        ball.x = 0
        ball.y = 0
        ball.rect.move(ball.vel_x, ball.vel_y)

    # update the scores when a goal is scored
    if ball.rect.colliderect(goal_left) and ball.rect.bottom >= goal_left.top:
        score_right += 1
        ball.reset(WIDTH, HEIGHT)
    elif ball.rect.colliderect(goal_right) and ball.rect.bottom >= goal_right.top:
        score_left += 1
        ball.reset(WIDTH, HEIGHT)

    # Update game objects
    players.update()
    ball_sprite.update(collided_players, player1, player2)

    # Draw the screen
    screen.fill(BLACK)
    pygame.draw.rect(screen, (255, 255, 255), goal_left)
    pygame.draw.rect(screen, (255, 255, 255), goal_right)
    pygame.draw.rect(screen, (0, 255, 255), cross_b_left)
    pygame.draw.rect(screen, (0, 255, 255), cross_b_right)
    all_sprites.draw(screen)

    # display the scores on the screen
    font = pygame.font.SysFont("calibrims", 72)
    score_text = font.render(str(score_left) + " - " + str(score_right), True, WHITE)
    screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 70))
    

    # Flip the display
    pygame.display.flip()

    # Set the game's frame rate
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    show_menu = True
                    while show_menu:
                        # Render the menu
                        render_menu()
                        # Handle events for the menu
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                            elif event.type == pygame.KEYDOWN:
                                if event.key == pygame.K_ESCAPE:
                                    show_menu = False
                                elif event.key == pygame.K_r:
                                    restart_game()
                                    show_menu = False
                                elif event.key == pygame.K_q:
                                    pygame.quit()

# Quit the game
pygame.quit()