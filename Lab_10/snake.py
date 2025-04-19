import pygame, random, sys, json, psycopg2

conn = psycopg2.connect(
    host="localhost",
    database="mydatabase",
    user="postgres",
    password="Danko17100603"
)
cur = conn.cursor()

def save_to_db(username, snake, dx, dy, score, level):
    cur.execute("""
    INSERT INTO user_scores (username, score, level, dx, dy, snake)
    VALUES (%s, %s, %s, %s, %s, %s)
    ON CONFLICT (username)
    DO UPDATE SET score = %s, level = %s, dx = %s, dy = %s, snake = %s
    """, (username, score, level, dx, dy, json.dumps(snake),
          score, level, dx, dy, json.dumps(snake)))
    conn.commit()
    print("Сохранено в БД!")

def load_from_db(username):
    cur.execute("SELECT score, level, dx, dy, snake FROM user_scores WHERE username=%s", (username,))
    result = cur.fetchone()
    if result:
        print("Загружено из БД!")
        return {
            "score": result[0],
            "level": result[1],
            "dx": result[2],
            "dy": result[3],
            "snake": result[4]
        }

def get_or_create_user():
    username = input("Введите имя пользователя: ")
    cur.execute("INSERT INTO users (username) VALUES (%s) ON CONFLICT DO NOTHING", (username,))
    conn.commit()
    return username

pygame.init()
WIDTH, HEIGHT, CELL_SIZE = 800, 480, 40
CELL_WIDTH = WIDTH // CELL_SIZE
CELL_HEIGHT = HEIGHT // CELL_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake!!!")
clock = pygame.time.Clock()

BASE_SPEED = 10
FOOD_PER_LEVEL = 3
WHITE, BLACK, GRAY, RED, GREEN = (255,255,255), (0,0,0), (100,100,100), (255,0,0), (0,255,0)

def random_food_position(snake):
    while True:
        pos = (random.randint(0, CELL_WIDTH-1), random.randint(0, CELL_HEIGHT-1))
        if pos not in snake:
            return pos

def create_food(snake):
    return {
        "pos": random_food_position(snake),
        "weight": random.randint(1, 3),
        "spawn_time": pygame.time.get_ticks(),
        "lifetime": random.randint(3000, 6000)
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
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            if event.type == pygame.KEYDOWN: paused = False
        screen.fill(BLACK)
        text = font.render("Пауза. Нажмите любую клавишу.", True, WHITE)
        screen.blit(text, text.get_rect(center=(WIDTH//2, HEIGHT//2)))
        pygame.display.flip()

def level_walls(level):
    if level < 2: return []
    wall = []
    for i in range(5, 15):
        wall.append((i, 5))
    if level >= 3:
        for i in range(10, 18):
            wall.append((i, 8))
    return wall

def main():
    username = get_or_create_user()
    saved = load_from_db(username)
    if saved:
        snake = saved["snake"]
        dx, dy = saved["dx"], saved["dy"]
        score, level = saved["score"], saved["level"]
    else:
        snake = [
            (CELL_WIDTH//2, CELL_HEIGHT//2),
            (CELL_WIDTH//2 - 1, CELL_HEIGHT//2),
            (CELL_WIDTH//2 - 2, CELL_HEIGHT//2)
        ]
        dx, dy, score, level = 1, 0, 0, 1

    speed = BASE_SPEED + (level - 1)
    foods = [create_food(snake) for _ in range(2)]
    running = True

    pause_game()
    while running:
        clock.tick(speed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and dy == 0: dx, dy = 0, -1
                elif event.key == pygame.K_DOWN and dy == 0: dx, dy = 0, 1
                elif event.key == pygame.K_LEFT and dx == 0: dx, dy = -1, 0
                elif event.key == pygame.K_RIGHT and dx == 0: dx, dy = 1, 0
                elif event.key == pygame.K_p: pause_game()
                elif event.key == pygame.K_s:
                    save_to_db(username, snake, dx, dy, score, level)

        new_head = (snake[0][0] + dx, snake[0][1] + dy)
        if (new_head[0] < 0 or new_head[0] >= CELL_WIDTH or
            new_head[1] < 0 or new_head[1] >= CELL_HEIGHT or
            new_head in snake or new_head in level_walls(level)):
            print("Game Over")
            pygame.quit(); sys.exit()

        snake.insert(0, new_head)
        eaten = None
        for food in foods:
            if new_head == food["pos"]:
                score += food["weight"]
                eaten = food
                break
        if eaten:
            foods.remove(eaten)
            foods.append(create_food(snake))
            if score % FOOD_PER_LEVEL == 0:
                level += 1
                speed = BASE_SPEED + (level - 1)
        else:
            snake.pop()

        current_time = pygame.time.get_ticks()
        foods = [f for f in foods if current_time - f["spawn_time"] < f["lifetime"]]
        while len(foods) < 2: foods.append(create_food(snake))

        screen.fill(BLACK)
        draw_grid()

        for segment in snake:
            pygame.draw.rect(screen, GREEN, (segment[0]*CELL_SIZE, segment[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for food in foods:
            pygame.draw.rect(screen, RED, (food["pos"][0]*CELL_SIZE, food["pos"][1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        for wall in level_walls(level):
            pygame.draw.rect(screen, GRAY, (wall[0]*CELL_SIZE, wall[1]*CELL_SIZE, CELL_SIZE, CELL_SIZE))

        font = pygame.font.SysFont(None, 30)
        text = font.render(f"{username} | Score: {score} | Level: {level}", True, WHITE)
        screen.blit(text, (5, 5))

        pygame.display.flip()

if __name__ == "__main__":
    main()