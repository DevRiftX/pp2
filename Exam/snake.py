import pygame, random, sys, json

pygame.init()

WIDTH, HEIGHT, CELL_SIZE = 800, 500, 40
CELL_WIDTH = WIDTH // CELL_SIZE
CELL_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!!!")
clock = pygame.time.Clock()

BASE_SPEED = 10
FOOD_PER_LEVEL = 3  # каждые 3 очка увеличиваем уровень
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY  = (100, 100, 100)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)

# Генерируем случайную позицию, не совпадающую со змеёй
def random_food_position(snake):
    while True:
        pos = (random.randint(0, CELL_WIDTH - 1), random.randint(0, CELL_HEIGHT - 1))
        if pos not in snake:
            return pos

def create_food(snake):
    return {
        "pos": random_food_position(snake),
        "weight": random.randint(1, 3),              # сколько очков даёт еда
        "spawn_time": pygame.time.get_ticks(),       # время создания
        "lifetime": random.randint(3000, 6000)       # через сколько мс исчезнет
    }

def draw_grid():
    for x in range(0, WIDTH, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL_SIZE):
        pygame.draw.line(screen, GRAY, (0, y), (WIDTH, y))

def pause_game():
    paused = True
    font = pygame.font.SysFont(None, 25)
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                paused = False

        screen.fill(BLACK)
        text = font.render("Пауза. Нажмите любую клавишу.", True, WHITE)
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.blit(text, text_rect)
        pygame.display.flip()
    
def save_game(snake, dx, dy, score, level, speed, foods):
    data = {
        "snake" : snake,
        "dx" : dx, 
        "dy" : dy,
        "score" : score,
        "level" : level,
        "speed" : speed,
        "pos1" : foods[0]["pos"],
        "pos2" : foods[1]["pos"]
        }

    with open("save.json", "w") as f:
        json.dump(data, f)
    print("Игра сохранена!")

def load_game():
    try:
        with open("save.json", "r") as f:
            data = json.load(f)
            print("Игра загружена!")
            return data
    except json.JSONDecodeError as e:
        print(f"Ошибка при обработке JSON: {e}")
    
def main():
    snake = [
        (CELL_WIDTH // 2, CELL_HEIGHT // 2),
        (CELL_WIDTH // 2 - 1, CELL_HEIGHT // 2),
        (CELL_WIDTH // 2 - 2, CELL_HEIGHT // 2)
    ]
    dx, dy = 1, 0
    score = 0
    level = 1
    speed = BASE_SPEED
    
    foods = [create_food(snake) for _ in range(2)]
    running = True

    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0:
                    dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0:
                    dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0:
                    dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0:
                    dx, dy = 1, 0
                elif event.key == pygame.K_p:
                    pause_game()
                elif event.key == pygame.K_s:
                    save_game(snake, dx, dy, score, level, speed, foods)
                elif event.key == pygame.K_l:
                    data = load_game()
                    if data:
                        snake = data["snake"]
                        dx = data["dx"]
                        dy = data["dy"]
                        score = data["score"]
                        level = data["level"]
                        speed = data["speed"]
                        foods[0]["pos"] = data["pos1"]
                        foods[1]["pos"] = data["pos2"]

        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        if (new_head[0] < 0 or new_head[0] >= CELL_WIDTH or
            new_head[1] < 0 or new_head[1] >= CELL_HEIGHT or
            new_head in snake):
            pygame.quit()
            sys.exit()

        snake.insert(0, new_head)

        eaten_food = None
        for food in foods:
            if new_head == food["pos"]:
                score += food["weight"] 
                eaten_food = food
                break

        if eaten_food:
            foods.remove(eaten_food)
            foods.append(create_food(snake))
            if score % FOOD_PER_LEVEL == 0:
                level += 1
                speed = BASE_SPEED + (level - 1) # * 2
        else:
            snake.pop()

        current_time = pygame.time.get_ticks()
        foods = [
            f for f in foods
            if current_time - f["spawn_time"] < f["lifetime"]
        ]
        while len(foods) < 2:
            foods.append(create_food(snake))

        screen.fill(BLACK)
        draw_grid()

        for segment in snake:
            pygame.draw.rect(
                screen, GREEN,
                (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
        for food in foods:
            pygame.draw.rect(
                screen, RED,
                (food["pos"][0] * CELL_SIZE, food["pos"][1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {score}  Level: {level}", True, WHITE)
        screen.blit(text, (5, 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()