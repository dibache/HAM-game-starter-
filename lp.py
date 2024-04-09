import pygame
import random

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400
FPS = 30
WHITE = (255, 255, 255)
RED = (255, 0, 0)
CLOUD_COLOR = (255, 255, 255)
CLOUD_RADIUS = 30
CLOUD_SPACING = 150
OBSTACLE_WIDTH = 15
OBSTACLE_HEIGHT = 30
OBSTACLE_SPEED = 5

class Dinosaur(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('dino.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 50
        self.jump = False
        self.jump_count = 10
        self.jump_speed = 1

    def update(self):
        if self.jump:
            if self.jump_count >= -10:
                neg = 1
                if self.jump_count < 0:
                    neg = -1
                self.rect.y -= (self.jump_count ** 2) * 0.5 * neg
                self.jump_count -= 1
            else:
                self.jump = False
                self.jump_count = 10
        else:
            if self.rect.y < SCREEN_HEIGHT - self.rect.height - 50:
                self.rect.y += self.jump_speed
            else:
                self.rect.y = SCREEN_HEIGHT - self.rect.height - 50

class Obstacle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH + 20
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 50

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.x < 0:
            self.rect.x = SCREEN_WIDTH + 20

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Dino Run")
    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    dinosaur = Dinosaur()
    all_sprites.add(dinosaur)

    for i in range((SCREEN_WIDTH - 50) // CLOUD_SPACING):
        cloud = pygame.sprite.Sprite()
        cloud.image = pygame.Surface((CLOUD_RADIUS * 2, CLOUD_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(cloud.image, CLOUD_COLOR, (CLOUD_RADIUS, CLOUD_RADIUS), CLOUD_RADIUS)
        cloud.rect = cloud.image.get_rect(center=(50 + i * CLOUD_SPACING, 100))
        all_sprites.add(cloud)
        clouds.add(cloud)

    running = True
    score = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not dinosaur.jump:
                    dinosaur.jump = True

        all_sprites.update()

        if pygame.sprite.spritecollide(dinosaur, obstacles, False):
            running = False

        screen.fill((135, 206, 235))
        all_sprites.draw(screen)

        obstacles.update()
        obstacles.draw(screen)

        if random.randint(0, 100) < 2:
            obstacle = Obstacle()
            all_sprites.add(obstacle)
            obstacles.add(obstacle)

        score += 1

        font = pygame.font.Font(None, 36)
        score_text = font.render("Score: " + str(score // 30), True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
