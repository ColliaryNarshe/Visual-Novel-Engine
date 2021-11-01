# Variables to use during game.
flag_variables = {
    'variable1': False,
    'variable2': False
}

dialog_settings = {
    'gradual_typing': True,
    'typing_speed': 15,  # Pause between characters, higher is slower
    'font_name': 'Georgia',
    'font_size': 25,
    'name_tag_font_size': 40,
    'name_tag_y': -45,  # 0 aligns with top of box
    'name_tag_x_multiplier': .5,  # Multiplied by width of character portrait.
    'y_txt_padding': 30,  # Space between top of box and first line of text.
    'x_txt_padding': 50,
    'font_color': 'White',
    'bg_color': 'DarkBlue',
    'border_color': 'Grey',
    'border_width': 5,
    'highlight_color': 'Red',
    # Default positions:
    'bottom_x': '10%',
    'bottom_y': '75%',
    'top_x': '10%',
    'top_y': '8%',
}

narration_settings = {
    'gradual_typing': False,
    'typing_speed': 2,
    'font_name': 'Georgia',
    'font_size': 25,
    'x_txt_padding': 55,
    'y_txt_padding': 30,
    'font_color': 'White',
    'bg_color': 'Black',
    'border_color': 'Grey',
    'border_width': 5,
    'highlight_color': 'Red'
}

map_settings = {
    'x_y': (15, 15),
    'width_height': ('80%', '80%'),
    'border_color': 'grey',
    'border_width': 4,
    'dot_radius': 15,
    'dot_color': 'LightBlue',
    'dot_highlight_color': 'Red',
    'padding_multiplier': .025,  # Multiplied by window width (can edit individually in map_coordinates)
    'txt_color': 'White',
    'txt_bg': 'Black',
    'font_size': 50,
    'bold': True,
    'font': 'Georgia'
}

# Change the default sound effects here. Can also add more to call during script.
sound_effects = [
    ['menu_sound', "assets/audio/sound_effects/menu.wav"],
    ['error_sound', "assets/audio/sound_effects/error.mp3"],
    ['selected', "assets/audio/sound_effects/save.mp3"]
]

# Add more pygame colors if necessary. (Used with changing color at start of text)
# Find a list of all pygame colors by looping through: pygame.color.THECOLORS.keys()
# Not looping entire list in game since it goes through it every frame
pygame_colors = ['red', 'green', 'blue', 'pink', 'orange', 'yellow', 'white',
                 'black', 'grey', 'cyan', 'aquamarine', 'magenta']


# Sheets of 8 images, 144x144 pixels each. List of nums represents which images to use
dialog_image_sheets = [
    ["Arjen", 'assets/faces/Arjen.png', [0,1,2,3,4,5]],
    ["Eilan", 'assets/faces/Eilan.png', [0]],
]

map_coordinates = [
    ['city1.png',
        [
        # [Name, coordinates, padding, show/hide]
        # Padding is clickable area (pixels from center) not dot size. None=default (defined above as padding_multiplier)
        ['Entrance', (0.585, 0.829), None, True],
        ['Inn', (0.473, 0.671), None, True],
        ['Market', (0.356, 0.621), None, True],
        ['Pub', (0.27, 0.525), None, True],
        ['Castle', (0.336, 0.498), None, True],
        ['Slums', (0.153, 0.318), None, True],
        ['Bridge', (0.637, 0.425), None, True],
        ]
    ]
]

# Characters (not yet implemented)
game_characters = [
    {'name': 'Arjen', 'preset': 'knight'},
    {'name': 'Eilan', 'preset': 'archer'},
    {'name': 'Julia', 'hp': 500, 'mp': 500, 'attack': 500, 'defense': 500, 'speed': 500, 'target': 500}
]
