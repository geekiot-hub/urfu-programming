import random
import sys
from time import sleep

from pathlib import Path

import pygame

# --- Constants ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
PLAYER_WIDTH = 156  # 130 * 1.2
PLAYER_HEIGHT = 156  # 130 * 1.2
BULLET_WIDTH = PLAYER_WIDTH / 2
BULLET_HEIGHT = PLAYER_HEIGHT / 2
ASTEROID_MIN_SIZE = 40  # Increased from 30
ASTEROID_MAX_SIZE = 90  # Increased from 80
FPS = 60

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 150, 255)

# --- File Paths ---
BASE_DIR = Path(__file__).parent
IMG_PATH = BASE_DIR / "sprites"
SCORE_FILE = BASE_DIR / "data" / "highscore.txt"

# --- Pygame Initialization ---
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Starlander")
clock = pygame.time.Clock()

# --- Game info ---
best_score = 0

# --- Asset Loading ---
try:
    player_img = pygame.image.load(IMG_PATH / "player.png").convert_alpha()
    asteroid_img = pygame.image.load(IMG_PATH / "asteroid.png").convert_alpha()
    background_particles = pygame.image.load(
        IMG_PATH / "background_particle.png"
    ).convert_alpha()

    # Load and rotate the bullet image once for efficiency.
    bullet_img = pygame.image.load(IMG_PATH / "bullet.png").convert_alpha()

except pygame.error as e:
    print(f"Fatal Error: Could not load image. {e}")
    sys.exit()


class Player(pygame.sprite.Sprite):
    """
    Represents a player's spaceship.

    Handles movement, shooting mechanics, and collision detection. The ship's
    color can be customized upon initialization.

    Attributes:
        image (pygame.Surface): The player's sprite image.
        rect (pygame.Rect): The rectangle that encloses the sprite.
        speedx (int): The current horizontal speed of the player.
        shoot_delay (int): The minimum time in ms between shots.
        last_shot (int): The timestamp of the last shot.
        key_left (int): The pygame key constant for moving left.
        key_right (int): The pygame key constant for moving right.
        key_shoot (int): The pygame key constant for shooting.
        double_shot (bool): Whether the player has double shot power-up.
    """

    def __init__(self, key_left, key_right, key_shoot, color, player_id=1):
        """
        Initializes the Player object.

        Args:
            key_left (int): The pygame.K_* constant for moving left.
            key_right (int): The pygame.K_* constant for moving right.
            key_shoot (int): The pygame.K_* constant for shooting.
            color (tuple): An (R, G, B) tuple to tint the player's sprite.
            player_id (int): Player identifier (1 or 2) for positioning.
        """
        super().__init__()
        base_image = pygame.transform.scale(
            player_img, (int(PLAYER_WIDTH), int(PLAYER_HEIGHT))
        ).copy()

        # Create a color mask to tint the base image.
        color_surface = pygame.Surface(base_image.get_size(), pygame.SRCALPHA)
        color_surface.fill(color)
        base_image.blit(
            color_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT
        )

        self.image = base_image
        # Position players side by side with spacing
        if player_id == 1:
            center_x = SCREEN_WIDTH // 2 - 100  # Left player
        else:
            center_x = SCREEN_WIDTH // 2 + 100  # Right player

        self.rect = self.image.get_rect(
            centerx=center_x, bottom=SCREEN_HEIGHT - 10
        )
        self.speedx = 0
        self.shoot_delay = 250  # 250ms between shots by default
        self.last_shot = pygame.time.get_ticks()
        self.key_left = key_left
        self.key_right = key_right
        self.key_shoot = key_shoot
        self.double_shot = False
        self.invincible_bullets = False
        self.powerup_end_time = 0
        all_sprites.add(self)

    def update(self):
        """Updates the player's position based on key presses."""
        self.speedx = 0
        key_state = pygame.key.get_pressed()
        if key_state[self.key_left]:
            self.speedx = -8
        if key_state[self.key_right]:
            self.speedx = 8

        self.rect.x += self.speedx

        # Keep player on the screen.
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        """Creates Bullet instance(s) if the shoot delay has passed."""
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.double_shot:
                # Fire two bullets with horizontal offset
                bullet1 = Bullet(
                    self.rect.centerx - 15,
                    self.rect.top,
                    self.invincible_bullets,
                )
                bullet2 = Bullet(
                    self.rect.centerx + 15,
                    self.rect.top,
                    self.invincible_bullets,
                )
                all_sprites.add(bullet1, bullet2)
                bullets.add(bullet1, bullet2)
            else:
                bullet = Bullet(
                    self.rect.centerx, self.rect.top, self.invincible_bullets
                )
                all_sprites.add(bullet)
                bullets.add(bullet)

    def do_shot(self, key_event):
        """
        Checks if the pressed key matches the player's shoot key.

        Args:
            key_event (int): The pygame.key constant from a KEYDOWN event.

        Returns:
            bool: True if the key matches the shoot key, False otherwise.
        """
        return key_event == self.key_shoot

    def check_collision(self, asteroids_sprites):
        """
        Checks for collisions between the player and asteroids.

        Args:
            asteroids_sprites (pygame.sprite.Group): The group of asteroids.

        Returns:
            bool: True if a collision occurs, False otherwise.
        """
        return bool(pygame.sprite.spritecollide(self, asteroids_sprites, False))


class Asteroid(pygame.sprite.Sprite):
    """
    Represents a falling asteroid enemy.

    Asteroids spawn off-screen at the top and move downwards at a random
    speed. They reappear at the top after leaving the screen.
    """

    def __init__(self):
        """Initializes the Asteroid object with random properties."""
        super().__init__()
        size = random.randint(30, 80)
        self.image = pygame.transform.scale(asteroid_img, (size, size))
        self.rect = self.image.get_rect(
            x=random.randrange(SCREEN_WIDTH - size),
            y=random.randrange(-150, -100),
        )
        self.base_speed = random.randrange(1, 5)
        self.speedy = self.base_speed
        self.reached_bottom = False  # Track if asteroid reached bottom

    def update(self):
        """Moves the asteroid down and respawns it if it goes off-screen."""
        global asteroids_missed
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            if not self.reached_bottom:
                self.reached_bottom = True
                asteroids_missed += 1
            self.rect.x = random.randrange(SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.base_speed = random.randrange(1, 4)
            self.speedy = self.base_speed
            self.reached_bottom = False  # Reset for next cycle


class Bullet(pygame.sprite.Sprite):
    """
    Represents a bullet fired by a player.

    Bullets travel upwards from the player's position and are destroyed
    when they go off-screen.
    """

    def __init__(self, x, y, invincible=False):
        """
        Initializes the Bullet object.

        Args:
            x (int): The initial x-coordinate (center of the bullet).
            y (int): The initial y-coordinate (top of the bullet).
            invincible (bool): Whether the bullet can pass through asteroids.
        """
        super().__init__()
        self.image = pygame.transform.scale(
            bullet_img, (int(BULLET_WIDTH), int(BULLET_HEIGHT))
        )
        self.rect = self.image.get_rect(centerx=x, bottom=y)
        self.speedy = -10
        self.invincible = invincible

    def update(self):
        """Moves the bullet up and destroys it if it goes off-screen."""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()


class PowerUp(pygame.sprite.Sprite):
    """
    Represents a power-up object that falls from the top of the screen.

    When hit by a bullet, it grants a power-up effect to players.
    """

    def __init__(self):
        """Initializes the PowerUp object."""
        super().__init__()
        # Use a placeholder sprite for now
        try:
            powerup_img = pygame.image.load(
                IMG_PATH / "wow.png"
            ).convert_alpha()
            size = 60
            self.image = pygame.transform.scale(powerup_img, (size, size))
        except pygame.error:
            # Fallback: create a colored square if image not found
            self.image = pygame.Surface((60, 60))
            self.image.fill((255, 215, 0))  # Gold color
        self.rect = self.image.get_rect(
            x=random.randrange(SCREEN_WIDTH - 60),
            y=random.randrange(-150, -100),
        )
        self.speedy = 2

    def update(self):
        """Moves the power-up down the screen."""
        self.rect.y += self.speedy
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.kill()


class Pizza(pygame.sprite.Sprite):
    """
    Represents a decorative background pizza slice.

    These sprites are semi-transparent, move slowly up the screen, and rotate.
    They serve as a dynamic background effect.
    """

    def __init__(self):
        """Initializes the Pizza object with random properties."""
        super().__init__()
        size = random.randint(20, 150)
        self.original_image = pygame.transform.scale(
            background_particles, (size, size)
        )

        # Set transparency (alpha)
        alpha_value = 50
        self.original_image.set_alpha(alpha_value)

        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(
            x=random.randrange(0, SCREEN_WIDTH - size),
            y=random.randrange(-100, SCREEN_HEIGHT),
        )
        self.speedy = random.uniform(-0.5, -1.5)
        self.angle = 0
        self.rotation_speed = random.uniform(-0.5, 0.5)

    def update(self):
        """Moves and rotates the pizza slice, and respawns if off-screen."""
        self.rect.y += self.speedy
        self.angle = (self.angle + self.rotation_speed) % 360
        self._rotate()

        if self.rect.bottom < 0:
            self._reset()

    def _rotate(self):
        """Rotates the sprite image around its center."""
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)

    def _reset(self):
        """Resets the pizza's properties and position to the bottom."""
        size = random.randint(50, 150)
        self.original_image = pygame.transform.scale(
            background_particles, (size, size)
        )
        self.original_image.set_alpha(50)
        self.rect = self.original_image.get_rect(
            x=random.randrange(0, SCREEN_WIDTH - size),
            y=SCREEN_HEIGHT + random.randrange(50, 150),
        )
        self.speedy = random.uniform(-0.5, -1.5)
        self.rotation_speed = random.uniform(-0.5, 0.5)


def draw_text(surf, text, size, x, y):
    """
    Draws text onto a surface.

    Args:
        surf (pygame.Surface): The surface to draw the text on.
        text (str): The text content to draw.
        size (int): The font size.
        x (int): The x-coordinate for the center of the text.
        y (int): The y-coordinate for the top of the text.
    """
    font = pygame.font.Font(None, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(midtop=(x, y))
    surf.blit(text_surface, text_rect)


def load_best_score():
    """
    Loads the best score from the score file.

    Returns:
        int: The best score, or 0 if the file doesn't exist or is invalid.
    """
    try:
        with open(SCORE_FILE, "r") as f:
            return int(f.read())
    except (FileNotFoundError, ValueError):
        return 0


def save_best_score(score):
    """
    Saves a new best score to the score file.

    Args:
        score (int): The new high score to save.
    """
    try:
        with open(SCORE_FILE, "w") as f:
            f.write(str(score))
    except IOError as e:
        print(f"Error: Failed to save high score. {e}")


def check_and_update_best_score(current_score, best_score):
    """
    Checks if a new high score was achieved and saves it if so.

    Args:
        current_score (int): The score from the completed game.
        best_score (int): The current high score.

    Returns:
        tuple: A tuple containing the updated best score (int) and a
               message for the game over screen (str).
    """
    if current_score > best_score:
        save_best_score(current_score)
        message = "НОВЫЙ РЕКОРД!"
        return current_score, message

    message = f"Лучший результат: {best_score}"
    return best_score, message


def initialize_game():
    """Initialize or reinitialize the game state."""
    global all_sprites, asteroids, bullets, pizzas, powerups, player1, player2, score, best_score, running, asteroid_speed_multiplier, last_speed_increase_time, last_powerup_spawn_time, asteroids_missed

    # Clear all sprite groups
    all_sprites.empty()
    asteroids.empty()
    bullets.empty()
    pizzas.empty()
    powerups.empty()

    # Recreate players with proper spacing
    # Player 1 keeps original color, Player 2 gets green tint
    player1 = Player(
        pygame.K_a, pygame.K_d, pygame.K_w, (255, 255, 255), 1
    )  # White = no tint
    player2 = Player(
        pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, (150, 255, 150), 2
    )  # Light green tint

    # Add background pizzas
    for _ in range(20):
        pizzas.add(Pizza())

    # Add asteroids
    for _ in range(8):
        a = Asteroid()
        a.speedy = a.base_speed * asteroid_speed_multiplier
        all_sprites.add(a)
        asteroids.add(a)

    # Reset score and game state
    score = 0
    best_score = load_best_score()
    running = True
    asteroid_speed_multiplier = 1.0
    last_speed_increase_time = pygame.time.get_ticks()
    last_powerup_spawn_time = pygame.time.get_ticks()
    asteroids_missed = 0  # Reset missed asteroids counter


def game_loop():
    """Main game loop - returns True to restart, False to exit."""
    global running, score, asteroid_speed_multiplier, last_speed_increase_time, last_powerup_spawn_time, asteroids_missed

    while running:
        clock.tick(FPS)
        current_time = pygame.time.get_ticks()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Exit to main menu/game over
                if player1.do_shot(event.key):
                    player1.shoot()
                if player2.do_shot(event.key):
                    player2.shoot()

        # Update asteroid speed every 10 seconds
        if current_time - last_speed_increase_time > 10000:  # 10 seconds
            asteroid_speed_multiplier += 0.1
            last_speed_increase_time = current_time
            # Update existing asteroids with new speed multiplier
            for asteroid in asteroids:
                asteroid.speedy = (
                    asteroid.base_speed * asteroid_speed_multiplier
                )

        # Spawn power-up every 10 seconds
        if current_time - last_powerup_spawn_time > 10000:  # 10 seconds
            powerup = PowerUp()
            all_sprites.add(powerup)
            powerups.add(powerup)
            last_powerup_spawn_time = current_time

        # Update
        all_sprites.update()
        pizzas.update()

        # Check for power-up expiration
        current_time = pygame.time.get_ticks()
        if current_time > player1.powerup_end_time:
            player1.double_shot = False
            player1.invincible_bullets = False
            player1.shoot_delay = 250  # Reset to default
        if current_time > player2.powerup_end_time:
            player2.double_shot = False
            player2.invincible_bullets = False
            player2.shoot_delay = 250  # Reset to default

        # Check for bullet-asteroid collisions
        hits = pygame.sprite.groupcollide(asteroids, bullets, False, False)
        for asteroid, bullet_list in hits.items():
            # Process only the first bullet to avoid multiple asteroid spawns
            if bullet_list:
                bullet = bullet_list[0]
                asteroid.kill()
                score += 1

                # Create new asteroid to replace the destroyed one
                a = Asteroid()
                a.speedy = a.base_speed * asteroid_speed_multiplier
                all_sprites.add(a)
                asteroids.add(a)

                # Remove the bullet in both cases (invincible or not)
                bullet.kill()

        # Check for bullet-powerup collisions
        powerup_hits = pygame.sprite.groupcollide(powerups, bullets, True, True)
        for _ in powerup_hits:
            # Randomly choose between double shot and invincible bullets (50% chance each)
            import random

            if random.random() < 0.5:
                # Apply double shot effect
                player1.double_shot = True
                player2.double_shot = True
                player1.shoot_delay = 0  # Remove shoot delay
                player2.shoot_delay = 0  # Remove shoot delay
            else:
                # Apply invincible bullets effect
                player1.invincible_bullets = True
                player2.invincible_bullets = True

            # Set power-up end time (20 seconds from now)
            player1.powerup_end_time = pygame.time.get_ticks() + 20000
            player2.powerup_end_time = pygame.time.get_ticks() + 20000

        # Check for player-asteroid collisions
        if player1.check_collision(asteroids) or player2.check_collision(
            asteroids
        ):
            running = False

        # Check if 10 asteroids reached the bottom (game over condition)
        if asteroids_missed >= 10:
            running = False

        # Draw / Render
        screen.fill(BLACK)
        pizzas.draw(screen)
        all_sprites.draw(screen)

        # UI Text
        draw_text(screen, f"Счёт: {score}", 50, 90, 10)
        draw_text(screen, f"Пропущено: {asteroids_missed}/10", 32, 90, 60)
        draw_text(
            screen,
            f"Лучший счёт: {max(score, best_score)}",
            48,
            SCREEN_WIDTH - 70,
            10,
        )

        pygame.display.flip()

    return True


def game_over_screen():
    """Display game over screen and handle player input.

    Returns:
        bool: True to restart the game, False to exit.
    """
    global best_score, score
    best_score, game_over_message = check_and_update_best_score(
        score, best_score
    )

    screen.fill(BLACK)
    draw_text(
        screen,
        f"Игра окончена. Ваш счёт: {score}",
        50,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2 - 50,
    )
    draw_text(
        screen, game_over_message, 50, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2
    )
    draw_text(
        screen,
        "Нажмите любую кнопку чтобы продолжить.",
        25,
        SCREEN_WIDTH / 2,
        SCREEN_HEIGHT / 2 + 50,
    )
    pygame.display.flip()

    # Wait for player input
    sleep(1)
    waiting = True
    while waiting:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False  # Exit the game
                else:
                    return True  # Restart the game

    return True


# --- Game Setup ---
all_sprites = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
bullets = pygame.sprite.Group()
pizzas = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player1 = None
player2 = None
score = 0
best_score = 0
running = True
asteroid_speed_multiplier = 1.0
last_speed_increase_time = 0
last_powerup_spawn_time = 0
asteroids_missed = 0  # Counter for asteroids that reached the bottom

# Main game cycle - initialize first game
initialize_game()

# Game loop that supports restarting
while True:
    # Run the game
    if not game_loop():
        break

    # Show game over screen and get player choice
    if not game_over_screen():
        break

    # Restart the game
    initialize_game()

pygame.quit()
sys.exit()
