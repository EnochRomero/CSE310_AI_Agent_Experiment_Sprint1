"""A small platform game with an endless, procedurally generated level."""

import math
import random

import pygame


SCREEN_WIDTH = 800
SCREEN_HEIGHT = 450
FPS = 60
PLAYER_SPEED = 260
JUMP_SPEED = 560
GRAVITY = 1500
CHUNK_WIDTH = 600


class Player:
    """Store the player's rectangle and update its simple platform physics."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 40)
        self.velocity_y = 0.0
        self.on_ground = False

    def update(self, delta_time, direction, jump_pressed, platforms):
        """Move, jump, and resolve collisions with the level platforms."""
        direction = max(-1, min(1, direction))

        if jump_pressed and self.on_ground:
            self.velocity_y = -JUMP_SPEED
            self.on_ground = False

        horizontal_step = round(direction * PLAYER_SPEED * delta_time)
        self.rect.x += horizontal_step
        for platform in platforms:
            if self.rect.colliderect(platform):
                if horizontal_step > 0:
                    self.rect.right = platform.left
                elif horizontal_step < 0:
                    self.rect.left = platform.right

        previous_top = self.rect.top
        previous_bottom = self.rect.bottom
        self.velocity_y += GRAVITY * delta_time
        self.rect.y += round(self.velocity_y * delta_time)
        self.on_ground = False

        for platform in platforms:
            overlaps_horizontally = (
                self.rect.right > platform.left and self.rect.left < platform.right
            )
            if not overlaps_horizontally:
                continue

            if (
                self.velocity_y >= 0
                and previous_bottom <= platform.top
                and self.rect.bottom >= platform.top
            ):
                self.rect.bottom = platform.top
                self.velocity_y = 0
                self.on_ground = True
            elif (
                self.velocity_y < 0
                and previous_top >= platform.bottom
                and self.rect.top <= platform.bottom
            ):
                self.rect.top = platform.bottom
                self.velocity_y = 0


class Enemy:
    """Patrol a short ground route and disappear when stomped by the player."""

    def __init__(self, x, y, patrol_left, patrol_right):
        self.rect = pygame.Rect(x, y, 34, 26)
        self.patrol_left = patrol_left
        self.patrol_right = patrol_right
        self.speed = 90
        self.direction = 1
        self.alive = True

    def update(self, delta_time):
        """Walk between the enemy's patrol boundaries."""
        self.rect.x += round(self.direction * self.speed * delta_time)
        if self.rect.left < self.patrol_left:
            self.rect.left = self.patrol_left
            self.direction = 1
        elif self.rect.right > self.patrol_right:
            self.rect.right = self.patrol_right
            self.direction = -1

    def resolve_player_collision(self, player, previous_bottom, direction):
        """Stomp the enemy from above or block the player from its sides."""
        if not self.alive or not player.rect.colliderect(self.rect):
            return None

        if player.velocity_y > 0 and previous_bottom <= self.rect.top:
            self.alive = False
            player.rect.bottom = self.rect.top
            player.velocity_y = -JUMP_SPEED * 0.55
            player.on_ground = False
            return "stomped"

        if direction > 0 or (direction == 0 and player.rect.centerx < self.rect.centerx):
            player.rect.right = self.rect.left
        else:
            player.rect.left = self.rect.right
        return "hit"


class PlatformWorld:
    """Generate and cache the platform chunks around the camera."""

    def __init__(self):
        self.chunks = {}

    @property
    def platforms(self):
        """Return platforms from the chunks currently held in memory."""
        return [
            platform
            for platforms, _ in self.chunks.values()
            for platform in platforms
        ]

    @property
    def enemies(self):
        """Return living enemies from the chunks currently held in memory."""
        return [
            enemy
            for _, enemies in self.chunks.values()
            for enemy in enemies
            if enemy.alive
        ]

    def update(self, camera_x):
        """Generate nearby chunks and discard chunks far outside the view."""
        first_chunk = math.floor((camera_x - CHUNK_WIDTH) / CHUNK_WIDTH)
        last_chunk = math.floor(
            (camera_x + SCREEN_WIDTH + CHUNK_WIDTH) / CHUNK_WIDTH
        )
        needed_chunks = set(range(first_chunk, last_chunk + 1))

        for chunk_index in needed_chunks:
            if chunk_index not in self.chunks:
                self.chunks[chunk_index] = self._generate_chunk(chunk_index)

        self.chunks = {
            index: chunk
            for index, chunk in self.chunks.items()
            if index in needed_chunks
        }

    @staticmethod
    def _generate_chunk(chunk_index):
        """Build ground, raised platforms, and one patrol enemy."""
        chunk_start = chunk_index * CHUNK_WIDTH
        generator = random.Random(chunk_index)
        platforms = [pygame.Rect(chunk_start, 410, CHUNK_WIDTH, 40)]

        for slot in range(3):
            x = chunk_start + 70 + slot * 180 + generator.randint(0, 20)
            width = generator.randint(100, 135)
            y = generator.randint(300, 350)
            platforms.append(pygame.Rect(x, y, width, 14))

        enemies = [
            Enemy(
                chunk_start + 280,
                384,
                chunk_start + 24,
                chunk_start + CHUNK_WIDTH - 24,
            )
        ]
        return platforms, enemies


def make_level():
    """Return a player and generated world positioned around the start."""
    player = Player(0, 370)
    world = PlatformWorld()
    camera_x = player.rect.centerx - SCREEN_WIDTH // 2
    world.update(camera_x)
    return player, world


def draw_player(surface, rect):
    """Draw the player from layered shapes instead of a plain block."""
    pygame.draw.ellipse(
        surface, (52, 62, 72), (rect.x + 3, rect.bottom - 5, rect.width - 6, 8)
    )
    pygame.draw.rect(
        surface,
        (188, 69, 65),
        (rect.x + 4, rect.y + 16, rect.width - 8, rect.height - 18),
        border_radius=6,
    )
    pygame.draw.rect(
        surface,
        (244, 137, 96),
        (rect.x + 5, rect.y + 5, rect.width - 10, 19),
        border_radius=8,
    )
    pygame.draw.circle(surface, (255, 235, 192), (rect.centerx, rect.y + 14), 6)
    pygame.draw.circle(surface, (48, 57, 66), (rect.centerx + 2, rect.y + 13), 2)
    pygame.draw.line(
        surface,
        (255, 210, 109),
        (rect.x + 6, rect.y + 27),
        (rect.right - 6, rect.y + 27),
        3,
    )
    pygame.draw.rect(
        surface, (75, 56, 62), (rect.x + 1, rect.bottom - 5, 12, 5), border_radius=2
    )
    pygame.draw.rect(
        surface,
        (75, 56, 62),
        (rect.right - 13, rect.bottom - 5, 12, 5),
        border_radius=2,
    )


def draw_enemy(surface, rect, direction):
    """Draw a spiked enemy with eyes and feet using Pygame shapes."""
    pygame.draw.ellipse(
        surface, (52, 62, 72), (rect.x + 3, rect.bottom - 4, rect.width - 6, 7)
    )
    pygame.draw.polygon(
        surface,
        (227, 118, 105),
        [
            (rect.x + 5, rect.y + 8),
            (rect.x + 2, rect.y),
            (rect.x + 13, rect.y + 6),
            (rect.centerx, rect.y - 3),
            (rect.centerx + 5, rect.y + 7),
            (rect.right - 3, rect.y + 1),
            (rect.right - 6, rect.y + 12),
        ],
    )
    pygame.draw.ellipse(surface, (227, 118, 105), rect)
    pygame.draw.ellipse(surface, (251, 221, 183), (rect.x + 8, rect.y + 9, 8, 9))
    pygame.draw.ellipse(
        surface, (251, 221, 183), (rect.right - 16, rect.y + 9, 8, 9)
    )
    pupil_offset = 2 if direction > 0 else -2
    pygame.draw.circle(
        surface, (53, 54, 65), (rect.x + 12 + pupil_offset, rect.y + 13), 2
    )
    pygame.draw.circle(
        surface, (53, 54, 65), (rect.right - 12 + pupil_offset, rect.y + 13), 2
    )
    pygame.draw.line(
        surface,
        (117, 54, 64),
        (rect.centerx - 4, rect.y + 21),
        (rect.centerx + 4, rect.y + 21),
        2,
    )


def run():
    """Start the game window and run the input, update, and draw loop."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Starbound Steps")
    clock = pygame.time.Clock()
    font = pygame.font.Font(None, 28)
    game_over_font = pygame.font.Font(None, 72)
    player, world = make_level()
    running = True
    game_over = False

    while running:
        delta_time = min(clock.tick(FPS) / 1000, 1 / 30)
        jump_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key in (pygame.K_SPACE, pygame.K_UP, pygame.K_w):
                    jump_pressed = True
                elif event.key == pygame.K_r and game_over:
                    player, world = make_level()
                    game_over = False

        keys = pygame.key.get_pressed()
        direction = int(keys[pygame.K_RIGHT] or keys[pygame.K_d]) - int(
            keys[pygame.K_LEFT] or keys[pygame.K_a]
        )

        if not game_over:
            previous_bottom = player.rect.bottom
            player.update(delta_time, direction, jump_pressed, world.platforms)
            for enemy in world.enemies:
                enemy.update(delta_time)
                collision = enemy.resolve_player_collision(
                    player, previous_bottom, direction
                )
                if collision == "hit":
                    game_over = True
                    break

        camera_x = player.rect.centerx - SCREEN_WIDTH // 2
        world.update(camera_x)

        screen.fill((75, 93, 112))
        pygame.draw.circle(screen, (246, 207, 96), (690, 62), 24)
        for platform in world.platforms:
            screen_platform = platform.move(-camera_x, 0)
            if screen_platform.right >= 0 and screen_platform.left <= SCREEN_WIDTH:
                pygame.draw.rect(
                    screen, (88, 157, 139), screen_platform, border_radius=4
                )

        for enemy in world.enemies:
            enemy_screen_rect = enemy.rect.move(-camera_x, 0)
            if enemy_screen_rect.right >= 0 and enemy_screen_rect.left <= SCREEN_WIDTH:
                draw_enemy(screen, enemy_screen_rect, enemy.direction)

        player_screen_rect = player.rect.move(-camera_x, 0)
        draw_player(screen, player_screen_rect)

        if game_over:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((19, 25, 38, 215))
            screen.blit(overlay, (0, 0))

            title = game_over_font.render("GAME OVER", True, (255, 226, 190))
            cause = font.render("You touched an enemy's side", True, (250, 250, 244))
            restart = font.render("Press R to restart   |   Esc to quit", True, (250, 250, 244))
            screen.blit(title, title.get_rect(center=(SCREEN_WIDTH // 2, 180)))
            screen.blit(cause, cause.get_rect(center=(SCREEN_WIDTH // 2, 235)))
            screen.blit(restart, restart.get_rect(center=(SCREEN_WIDTH // 2, 275)))
        else:
            message = "Move: A/D or arrows   Jump: Space / W / Up   Stomp enemies"
            text = font.render(message, True, (250, 250, 244))
            screen.blit(text, (18, 18))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    run()