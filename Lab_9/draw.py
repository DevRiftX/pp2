import pygame, sys
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = pygame.Surface(screen.get_size())
canvas.fill((0, 0, 0))

radius = 15
color = (0, 0, 255)
mode = 'line'
start_pos = None

def get_color(c):
    return (255, 0, 0) if c=='red' else (0, 255, 0) if c=='green' else (0, 0, 255)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
            if event.unicode == '+' or event.key == pygame.K_KP_PLUS:
                radius = min(200, radius + 1)
            elif event.unicode == '-' or event.key == pygame.K_KP_MINUS:
                radius = max(1, radius - 1)
            if event.key == pygame.K_r:
                color = get_color('red')
            elif event.key == pygame.K_g:
                color = get_color('green')
            elif event.key == pygame.K_b:
                color = get_color('blue')
            elif event.key == pygame.K_1:
                mode = 'line'
            elif event.key == pygame.K_2:
                mode = 'rect'
            elif event.key == pygame.K_3:
                mode = 'circle'
            elif event.key == pygame.K_4:
                mode = 'eraser'
            elif event.key == pygame.K_5:
                mode = 'square'
            elif event.key == pygame.K_6:
                mode = 'right_triangle'
            elif event.key == pygame.K_7:
                mode = 'equilateral_triangle'
            elif event.key == pygame.K_8:
                mode = 'rhombus'

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode in ('rect','circle','square','right_triangle','equilateral_triangle','rhombus'):
                start_pos = event.pos
            else:
                pygame.draw.circle(canvas, color if mode != 'eraser' else (0, 0, 0), event.pos, radius)

        if event.type == pygame.MOUSEMOTION:
            if mode in ('line','eraser') and event.buttons[0]:
                pygame.draw.circle(canvas, color if mode != 'eraser' else (0, 0, 0), event.pos, radius)

        if event.type == pygame.MOUSEBUTTONUP:
            if start_pos:
                end_pos = event.pos
                x1, y1 = start_pos
                x2, y2 = end_pos

                if mode == 'rect':
                    rect = pygame.Rect(min(x1, x2), min(y1, y2), abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(canvas, color, rect, radius)

                elif mode == 'circle':
                    r = int(((x2 - x1)**2 + (y2 - y1)**2) ** 0.5)
                    pygame.draw.circle(canvas, color, start_pos, r, radius)

                elif mode == 'square':
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    if x2 < x1:
                        x1 -= side
                    if y2 < y1:
                        y1 -= side
                    rect = pygame.Rect(x1, y1, side, side)
                    pygame.draw.rect(canvas, color, rect, radius)

                elif mode == 'right_triangle':
                    # Правильная ориентация треугольника
                    points = [start_pos, (x1, y2), (x2, y2)]
                    pygame.draw.polygon(canvas, color, points, radius)

                elif mode == 'equilateral_triangle':
                    # Сторона и высота
                    side = abs(x2 - x1)
                    height = side * (3**0.5) / 2
                    points = [
                        (x1, y1),                         # Вершина треугольника
                        (x1 - side / 2, y1 + height),     # Левая нижняя
                        (x1 + side / 2, y1 + height)      # Правая нижняя
                    ]
                    pygame.draw.polygon(canvas, color, points, radius)

                elif mode == 'rhombus':
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2
                    points = [
                        (cx, y1),  # верх
                        (x2, cy),  # правый
                        (cx, y2),  # низ
                        (x1, cy)   # левый
                    ]
                    pygame.draw.polygon(canvas, color, points, radius)

                start_pos = None


    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    clock.tick(60)
