import pygame
import sys
import os
import time

pygame.init()
pygame.mixer.init()

# Window settings
WIDTH, HEIGHT = 500, 300
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Музыкальный Плеер")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.Font(None, 36)

# Playlist settings
MUSIC_FOLDER = "music"
playlist = [os.path.join(MUSIC_FOLDER, f) for f in os.listdir(MUSIC_FOLDER) if f.endswith(".mp3")]
current_track = 0
track_length = 0
start_time = 0
paused = False  # Flag for pause

# functions to load and play
def play():
    global start_time, track_length, paused
    if paused:
        pygame.mixer.music.unpause()
        paused = False
    else:
        pygame.mixer.music.load(playlist[current_track])
        pygame.mixer.music.play()
        track_length = pygame.mixer.Sound(playlist[current_track]).get_length()
        start_time = time.time()

def pause():
    global paused
    pygame.mixer.music.pause()
    paused = True

def next_track():
    global current_track, paused
    paused = False
    current_track = (current_track + 1) % len(playlist)
    play()

def prev_track():
    global current_track, paused
    paused = False
    current_track = (current_track - 1) % len(playlist)
    play()

if playlist:
    play()

last_update_time = time.time() # For smooth updating

while True:
    screen.fill(WHITE)

    # Show music name
    if playlist:
        track_name = os.path.basename(playlist[current_track])
        elapsed_time = max(0, time.time() - start_time) if not paused else elapsed_time
        remaining_time = max(0, track_length - elapsed_time)
    else:
        track_name = "Нет доступных треков"
        elapsed_time, remaining_time = 0, 0

    # Limit the time update to every 500 milliseconds (0.5 seconds)
    if time.time() - last_update_time >= 0.5:
        last_update_time = time.time()

        # Shwo info about music
        screen.fill(WHITE)
        text_track = font.render(f"Трек: {track_name}", True, BLACK)
        text_time = font.render(f"Прошло: {int(elapsed_time)}s / Осталось: {int(remaining_time)}s", True, BLACK)

        screen.blit(text_track, (20, 100))
        screen.blit(text_time, (20, 150))

        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Play / Resume
                play()
            elif event.key == pygame.K_s:  # Pause
                pause()
            elif event.key == pygame.K_n:  # Next
                next_track()
            elif event.key == pygame.K_b:  # Previous
                prev_track()

    pygame.time.delay(10)
