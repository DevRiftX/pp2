import pygame, random, sys

pygame.init()

WIDTH, HEIGHT, CELL_SIZE = 400, 300, 25
CELL_WIDTH = WIDTH // CELL_SIZE
CELL_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!!!")
clock = pygame.time.Clock()

BASE_SPEED = 10
FOOD_PER_LEVEL = 3

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (100, 100, 100)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

def random_food_position(snake):
    while True:
        pos = (random.randint(0, CELL_WIDTH - 1), random.randint(0, CELL_HEIGHT - 1))
        if pos not in snake:
            return pos

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def main():
    snake = [(CELL_WIDTH // 2, CELL_HEIGHT // 2),
             (CELL_WIDTH // 2 - 1, CELL_HEIGHT // 2),
             (CELL_WIDTH // 2 - 2, CELL_HEIGHT // 2)]
    dx, dy = 1, 0
    food = random_food_position(snake)
    score = 0
    level = 1
    speed = BASE_SPEED

    while True:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = 1, 0

        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        if (new_head[0] < 0 or new_head[0] >= CELL_WIDTH or 
            new_head[1] < 0 or new_head[1] >= CELL_HEIGHT or 
            new_head in snake):
            pygame.quit(); sys.exit()

        snake.insert(0, new_head)

        if new_head == food:
            score += 1
            if score % FOOD_PER_LEVEL == 0:
                level += 1
                speed = BASE_SPEED + (level - 1) * 2
            food = random_food_position(snake)
        else:
            snake.pop()

        screen.fill(BLACK)
        draw_grid()
        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(screen, RED, (food[0] * CELL_SIZE, food[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(text, (5, 5))
        pygame.display.flip()

if __name__ == "__main__":
    main()