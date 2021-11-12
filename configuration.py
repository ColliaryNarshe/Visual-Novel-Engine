# Variables to use during game.
flag_variables = {
    'variable1': False,
    'variable2': False
}

dialog_settings = {
    'width': '80%',
    'height': '20%',
    'max_lines': 'auto',
    'txt_wrap_length': 70, # Can also use 'auto' to fit between x_txt_padding
    'gradual_typing': True,
    'typing_speed': 15,  # Pause between characters, higher is slower
    'font_name': 'Georgia',
    'font_size': 25,
    'bold': False,
    'name_tag_font_size': 40,
    'name_tag_y': -35,  # 0 aligns with top of box
    'name_tag_x_multiplier': .5,  # Multiplied by width of character portrait.
    'y_txt_padding': 30,  # Space between top of box and first line of text.
    'x_txt_padding': 30,
    'font_color': 'White',
    'bg_color': 'DarkBlue',
    'box_transparency': 255, # 0-255
    'border_color': 'Grey',
    'border_width': 3,
    'highlight_color': 'Red',
    # Default positions:
    'bottom_x': '10%',
    'bottom_y': '75%',
    'top_x': '10%',
    'top_y': '10%',
    'choice_menu_x': -40,  # From right edge of dialog box
    'choice_menu_y': .20,  # Multiplier for height of dialog box then added from top
    'image_size': 'auto', # Takes also percent (eg '20%') or int; 'auto' matches height
    'image_border_width': 2
}

narration_settings = {
    'x': '15%',
    'y': '5%',
    'width': '70%',
    'height': '90%',
    'max_lines': 'auto',  # Also takes an int
    'txt_wrap_length': 'auto',
    'gradual_typing': False,
    'typing_speed': 2,
    'font_name': 'Georgia',
    'font_size': 25,
    'bold': False,
    'x_txt_padding': 55,
    'y_txt_padding': 30,
    'txt_indentation': 5,
    'font_color': 'White',
    'bg_color': 'Black',
    'box_transparency': 150, # 0-255
    'border_color': 'Grey',
    'border_width': 4,
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
    'dot_transparency': 200,
    'padding_multiplier': .025,  # Multiplied by window width (can edit individually in map_coordinates)
    'txt_color': 'White',
    'txt_bg': 'Black',
    'txt_bg_transparency': 150,
    'font_size': 50,
    'bold': True,
    'font': 'Georgia'
}

portrait_settings = {
    'animation_speed': 20
}

# Change the default sound effects here, or use None. Additional sounds can also be added to use during script.
sound_effects = [
    ['menu_sound', "assets/audio/sound_effects/menu.wav"],
    ['selected', "assets/audio/sound_effects/save.mp3"],
    ['error_sound', "assets/audio/sound_effects/error.mp3"]
]

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
        ['Slums', (0.153, 0.318), None, True],
        ['Bridge', (0.637, 0.425), None, True],
        ['Castle', (0.336, 0.498), None, True],
        ['Pub', (0.27, 0.525), None, True],
        ['Market', (0.356, 0.621), None, True],
        ['Inn', (0.473, 0.671), None, True],
        ['Entrance', (0.575, 0.820), None, True]
        ]
    ]
]

# Characters (not yet implemented)
game_characters = [
    {'name': 'Arjen', 'preset': 'knight'},
    {'name': 'Eilan', 'preset': 'archer'},
    {'name': 'Julia', 'hp': 500, 'mp': 500, 'attack': 500, 'defense': 500, 'speed': 500, 'target': 500}
]
