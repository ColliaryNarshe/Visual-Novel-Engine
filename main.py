import pygame
from game.game_engine import Game

pygame.init()

WIN = pygame.display.set_mode((1100,700))
pygame.display.set_caption("Visual Novel Engine")

# Project:
project_dir = "test_project"
starting_chapter = "chapter1"
starting_scene = 'title'

while True:
    game = Game(WIN, project_dir, starting_chapter, starting_scene)

    while game.game_running:

        game.run()
