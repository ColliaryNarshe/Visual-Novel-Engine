import pygame
from glob import glob
from os.path import basename

from configuration import map_coordinates, sound_effects, dialog_image_sheets

from display.maps import Map
from display.portraits import Portrait_Image


def get_data(game):
    """Gets assets and adds them to game"""
    get_maps(game)
    get_sound_effects(game)
    get_dialog_images(game)
    get_portraits(game)
    get_backgrounds(game)
    get_music(game)


# ----------------------------------------------------------------------
def get_maps(game):
    """Get map images from: assets/maps/*"""
    map_coor = {}
    for map_name, coordinates in map_coordinates:
        map_coor[map_name] = coordinates


    for loc in glob('assets/maps/*'):
        name = basename(loc).lower()

        if name in map_coor:
            game.maps[name] = Map(game, loc, map_coor[name])
        else:
            game.maps[name] = Map(game, loc)


def get_sound_effects(game):
    """Get sounds effects from assets directory, listed in configuration file"""
    for name, loc in sound_effects:
        game.sounds[name] = pygame.mixer.Sound(loc)
        # Lower volume of all sounds. If you want different levels for each file, can do a check by name
        game.sounds[name].set_volume(.3)


def get_dialog_images(game):
    """
    Get the dialog pictures from assets dir, listed in configuration file.
    dialog image list uses this format: [["Name", 'location', [1,2]], ["Name", 'location', [1]]]
    Adds to dictionary: [Name: [img,img,img]]
    """

    # Loop through the character sheets
    for name, loc, img_nums in dialog_image_sheets:
        # Load the character sheet:
        if loc:
            image_sheet = pygame.image.load(loc).convert_alpha()
        else:
            image_sheet = []

        # Cut the sheet into character images
        char_images = []
        for idx1, row in enumerate(range(2)):
            y = row * 144
            for idx2, img in enumerate(range(4)):
                x = img * 144
                rect = pygame.Rect(x, y, 144, 144)
                # Get image number
                idx = (idx1 * 4) + idx2
                if idx in img_nums:  # Add only specified images
                    char_images.append(image_sheet.subsurface(rect))

        # Add to dictionary: [Name: [img,img,img]]
        game.dialog_images[name] = char_images


def get_portraits(game):
    """Get portraits/images from assets directory"""

    for loc in glob('assets/portraits/*'):
        name = basename(loc)
        game.portraits[name] = Portrait_Image(game, name, loc)


def get_backgrounds(game):
    """Get backdrops from assets directory"""
    for loc in glob('assets/backgrounds/*'):
        name = basename(loc).lower()
        game.backgrounds[name] = pygame.image.load(loc).convert_alpha()
        # 30 added to width for screen shake
        game.backgrounds[name] = pygame.transform.scale(game.backgrounds[name], (game.win_width + 30, game.win_height))


def get_music(game):
    """Get music from assets folder"""

    for loc in glob('assets/audio/music/*'):
        name = basename(loc).lower()
        game.music[name] = loc
