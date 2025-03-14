import pygame
import sys
import time
from pygame.transform import rotate

pygame.init()

# Window settings
WIDTH, HEIGHT = 880, 880
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")
clock = pygame.time.Clock()

# import images
background = pygame.image.load(r".\images\back.png")  # background
right_hand = pygame.image.load(r".\images\min.png")  # min
left_hand = pygame.image.load(r".\images\sec.png")  # sec

# center
center_x, center_y = WIDTH // 2, HEIGHT // 2
font = pygame.font.Font(None, 50)

while True:
    screen.fill((255, 255, 255))
    screen.blit(background, (0, 0))

    # import current time
    current_time = time.localtime()
    hours = current_time.tm_hour
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    # angles
    min_angle = -minutes * 6
    sec_angle = -seconds * 6

    # rotate sticks
    rotated_right_hand = rotate(right_hand, min_angle)
    rotated_left_hand = rotate(left_hand, sec_angle)

    # center sticks
    right_rect = rotated_right_hand.get_rect(center=(center_x, center_y))
    left_rect = rotated_left_hand.get_rect(center=(center_x, center_y))

    screen.blit(rotated_right_hand, right_rect.topleft)
    screen.blit(rotated_left_hand, left_rect.topleft)

    # show cur time
    time_text = font.render(f"{hours:02}:{minutes:02}:{seconds:02}", True, (0, 0, 0))
    screen.blit(time_text, (WIDTH - 160, 20))  # top-right 

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.flip()
    clock.tick(30)