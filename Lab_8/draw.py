import pygame, sys
pygame.init()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption("Paint")
clock = pygame.time.Clock()

canvas = pygame.Surface(screen.get_size())
canvas.fill((0, 0, 0))

radius = 15
color = (0, 0, 255)
mode = 'line'  # 'line', 'rect', 'circle', 'eraser'
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            if mode in ('rect', 'circle'):
                start_pos = event.pos
            else:
                pygame.draw.circle(canvas, color if mode != 'eraser' else (0, 0, 0), event.pos, radius)
        if event.type == pygame.MOUSEMOTION:
            if mode in ('line', 'eraser') and event.buttons[0]:
                pygame.draw.circle(canvas, color if mode != 'eraser' else (0, 0, 0), event.pos, radius)
        if event.type == pygame.MOUSEBUTTONUP:
            if mode == 'rect' and start_pos:
                end_pos = event.pos
                rect = pygame.Rect(min(start_pos[0], end_pos[0]), min(start_pos[1], end_pos[1]),
                                   abs(end_pos[0] - start_pos[0]), abs(end_pos[1] - start_pos[1]))
                pygame.draw.rect(canvas, color, rect, radius)
                start_pos = None
            elif mode == 'circle' and start_pos:
                end_pos = event.pos
                r = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                pygame.draw.circle(canvas, color, start_pos, r, radius)
                start_pos = None

    screen.blit(canvas, (0, 0))
    pygame.display.flip()
    clock.tick(60)
