import pygame
import sys
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
BALL_SPEED = 5
PADDLE_SPEED = 7
FPS = 60

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED
        self.score = 0
    
    def move_up(self):
        if self.rect.top > 0:
            self.rect.y -= self.speed
    
    def move_down(self):
        if self.rect.bottom < HEIGHT:
            self.rect.y += self.speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.dx = BALL_SPEED * random.choice([-1, 1])
        self.dy = BALL_SPEED * random.choice([-1, 1])
    
    def update(self):
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.dy = -self.dy
        
        if self.rect.left <= 0:
            return "right_score"
        if self.rect.right >= WIDTH:
            return "left_score"
        
        return None
    
    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, self.rect)
    
    def collide_with_paddle(self, paddle):
        if self.rect.colliderect(paddle.rect):
            self.dx = -self.dx
            hit_pos = (self.rect.centery - paddle.rect.centery) / (PADDLE_HEIGHT / 2)
            self.dy = hit_pos * BALL_SPEED
            if self.dx > 0:
                self.rect.left = paddle.rect.right
            else:
                self.rect.right = paddle.rect.left

class PongGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Pong Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)
        
        self.left_paddle = Paddle(20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(WIDTH - 20 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.ball = Ball()
        self.running = True
        self.paused = False
    
    def handle_input(self):
        keys = pygame.key.get_pressed()
        
        
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()
        
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()
        if keys[pygame.K_SPACE]:
            self.paused = not self.paused
            pygame.time.wait(200) 
    
    def update(self):
        if not self.paused:
            result = self.ball.update()
            
            if result == "left_score":
                self.left_paddle.score += 1
                self.ball.reset()
            elif result == "right_score":
                self.right_paddle.score += 1
                self.ball.reset()
            self.ball.collide_with_paddle(self.left_paddle)
            self.ball.collide_with_paddle(self.right_paddle)
    
    def draw(self):
        self.screen.fill(BLACK)
        
        for y in range(0, HEIGHT, 20):
            pygame.draw.rect(self.screen, GRAY, (WIDTH // 2 - 2, y, 4, 10))
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        left_score_text = self.font.render(str(self.left_paddle.score), True, WHITE)
        right_score_text = self.font.render(str(self.right_paddle.score), True, WHITE)
        self.screen.blit(left_score_text, (WIDTH // 4, 20))
        self.screen.blit(right_score_text, (3 * WIDTH // 4, 20))
        
        if self.paused:
            pause_text = self.small_font.render("PAUSED - Press SPACE to continue", True, WHITE)
            text_rect = pause_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
        
        pygame.display.flip()
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
            
            self.handle_input()
            
            self.update()
            
            self.draw()
            
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PongGame()
    game.run()

