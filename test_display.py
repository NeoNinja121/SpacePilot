# test_display.py
import os
os.environ["SDL_VIDEODRIVER"] = "fbcon"
os.environ["SDL_FBDEV"] = "/dev/fb0"

import pygame
pygame.init()
pygame.mouse.set_visible(False)

screen = pygame.display.set_mode((320, 240))
screen.fill((0, 0, 0))  # black
pygame.draw.circle(screen, (255, 0, 0), (160, 120), 40)  # red circle in center
pygame.display.flip()

input("Press Enter to exit...")
