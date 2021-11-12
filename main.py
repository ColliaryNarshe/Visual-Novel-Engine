from game.game_engine import Game

# Project:
project_dir = "demo"
starting_chapter = "chapter1"
starting_scene = 'title'

game = Game(project_dir, starting_chapter, starting_scene)

while True:
    game.run()
