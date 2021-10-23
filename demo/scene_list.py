import demo.chapter1.script
import demo.chapter2.script


def get_scenes(game):
    """Add scenes here, key names used to change scenes"""
    game.scenes['chapter1'] = {
        'title': demo.chapter1.script.TitleScreen(game),
        'scene1': demo.chapter1.script.Scene1(game),
    }

    game.scenes['chapter2'] = {
        'scene1': demo.chapter2.script.Scene1(game)
    }
