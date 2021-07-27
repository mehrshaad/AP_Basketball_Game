import datetime as D
import json as J
import sqlite3
import string as S
import time as T
from sqlite3 import Error

import pygame as P

from pygame_functions import *

# display
P.init()  # for creating a display
P.mixer.pre_init(44100, 16, 2, 4096)
display_ground = 480
display_width, display_height = 1200, 680  # x,y of display
main_display = P.display.set_mode((display_width, display_height))
screenSize(display_width, display_height)
setAutoUpdate(True)
Frame = P.time.Clock()
P.display.set_icon(P.image.load(r"Images\icon.png"))
P.mouse.set_cursor(
    (16, 16), (1, 1),
    (0, 0, 96, 0, 120, 0, 62, 0, 63, 128, 31, 224, 31, 248, 15, 254, 15, 254,
     7, 128, 7, 128, 3, 128, 3, 128, 1, 128, 1, 128, 0, 0),
    (224, 0, 248, 0, 254, 0, 127, 128, 127, 224, 63, 248, 63, 254, 31, 255, 31,
     255, 15, 254, 15, 192, 7, 192, 7, 192, 3, 192, 3, 192, 1, 128))
# menu
Mode = ''
Font = P.font.SysFont('mvboli', 30)
Text = Font.render("", True, (0, 0, 0))
mouse_x, mouse_y = 0, 0
solo_key = False  # True = choose solo button
multi_key = False  # True = choose multi button
multi_key2 = False  # True = mode selector in multi
menu_key = False  # True = name menu / False = mode menu
back_key = False  # True = choose back button
name1_key = False  # True = username is in the data (player 1)
name2_key = False  # True = username is in the data (player 2)
menu_done = False  # True = quiting menu and entering game
game_exit = False  # True = the game will end
input_boxes = []
solo_time = {'0:30': 30, '1:00': 60, '1:30': 90}

Menu_Background = P.image.load(r"Images\menu_bg.jpg").convert_alpha()
solo_passive = P.image.load(r"Images\solo_passive.png").convert_alpha()
solo_active = P.image.load(r"Images\solo_active.png").convert_alpha()
multi_passive = P.image.load(r"Images\multi_passive.png").convert_alpha()
multi_active = P.image.load(r"Images\multi_active.png").convert_alpha()
next_passive = P.image.load(r"Images\next.png").convert_alpha()
next_active = P.image.load(r"Images\next_hover.png").convert_alpha()
back_pic = P.image.load(r"Images\back.png").convert_alpha()
yes_pic = r"Images\yes.png"
no_pic = r"Images\no.png"
leaderboard_pics = [
    P.image.load(r"Images\leaderboard.png").convert_alpha(),
    P.image.load(r"Images\leaderboard2.png").convert_alpha(),
    P.image.load(r"Images\leaderboard3.png").convert_alpha()
]

solo_passive = P.transform.scale(solo_passive, (300, 200))
solo_active = P.transform.scale(solo_active, (300, 200))
multi_passive = P.transform.scale(multi_passive, (300, 200))
multi_active = P.transform.scale(multi_active, (300, 200))

pic_solo = solo_passive
pic_multi = multi_passive

# sound
click_sound = P.mixer.Sound("Sounds\click.wav")
keyboard_sound = P.mixer.Sound("Sounds\keyboard.wav")
whistle_sound = P.mixer.Sound("Sounds\whistle.wav")
click_sound.set_volume(0.5)
keyboard_sound.set_volume(0.5)
Music = [
    r"Sounds\main_music1.mp3", r"Sounds\main_music2.mp3",
    r"Sounds\main_music3.mp3"
]
goal_sound = [
    P.mixer.Sound("Sounds\goal1.wav"),
    P.mixer.Sound("Sounds\goal2.wav"),
    P.mixer.Sound("Sounds\goal3.wav")
]
ball_sound = [
    P.mixer.Sound(r"Sounds\ball1.wav"),
    P.mixer.Sound(r"Sounds\ball2.wav")
]
for sound in goal_sound:  # setting volume
    sound.set_volume(0.5)
for sound in ball_sound:
    sound.set_volume(0.5)

# text
Text = Font.render(f'Selected Mode: {Mode}', True, (255, 255, 255))
Text_Hello = Font.render(f'Hello There!', True, (255, 255, 255))
Text_Box_1 = Font.render(f'', True, (255, 255, 255))
Text_Box_2 = Font.render(f'', True, (255, 255, 255))
Text_Help = Font.render(f"Complete Menu Things", True, (255, 0, 0))

# player
Sprite_pics = [  # sprite in all positions
    "Images\sprite_0.png", "Images\sprite_1.png", "Images\sprite_2.png",
    "Images\sprite_3.png", "Images\sprite_4.png", "Images\sprite_5.png",
    "Images\sprite_6.png"
]
Sprite_pics_2 = [  # sprite in one position
    "Images\sprite_0r.png", "Images\sprite_1r.png", "Images\sprite_2r.png",
    "Images\sprite_3r.png", "Images\sprite_4r.png", "Images\sprite_5r.png",
    "Images\sprite_6r.png"
]
Sprite_passive = [  # sprite in passive mode for menu
    "Images\sprite_chr_0.png", "Images\sprite_chr_1.png",
    "Images\sprite_chr_2.png", "Images\sprite_chr_3.png",
    "Images\sprite_chr_4.png", "Images\sprite_chr_5.png",
    "Images\sprite_chr_6.png"
]
Sprite_active = [  # sprite in active/hover mode for menu
    "Images\sprite_chr_hover_0.png", "Images\sprite_chr_hover_1.png",
    "Images\sprite_chr_hover_2.png", "Images\sprite_chr_hover_3.png",
    "Images\sprite_chr_hover_4.png", "Images\sprite_chr_hover_5.png",
    "Images\sprite_chr_hover_6.png"
]
Sprite_colors = [
    'Green', 'Blue', 'Red', 'Pink', 'Dark Red', 'Turquoise', 'Orange'
]
Colors = [(4, 187, 63), (60, 0, 255), (255, 0, 0), (251, 0, 255), (82, 21, 21),
          (0, 255, 187), (255, 135, 0)]
Difficulty_pic = [
    "Images\difficulty_0.png",
    "Images\difficulty_1.png",
    "Images\difficulty_2.png",
    "Images\difficulty_hover_0.png",
    "Images\difficulty_hover_1.png",
    "Images\difficulty_hover_2.png",
]
Difficulty_list = [
    'Easy',
    'Hard',
    'Extreme',
]
Style = 0  # index of selected sprite color for 1st player
Style2 = 1  # index of selected sprite color for 2nd player
Difficulty = 0  # 0 = east , 1 = hard , 2 = extreme
time = -1

Data = {}
Dsl = 4  # data score list limit
try:
    connect = sqlite3.connect(
        'database.db')  # opening db file for storing and reading database
except Error as error:
    print(str(error))

layer_pic_num = 15
i = 0
mid_jump = 15

Player_frame = 0
Event = 0
Style = 0

x1_sabad_2 = 1000
x2_sabad_2 = 1070
y_sabad_2 = 210
x1_sabad_1 = 115
x2_sabad_1 = 190
y_sabad_1 = 210
x1_sabad_solo = 1010
x2_sabad_solo = 1080
y_sabad_solo = 223

mouse_click = True
mouse_ready = False
mouse_ball_num = 100
goal_solo_p = 1
goal_solo_p1 = 1
goals = [0, 0]
scores = [0, 0]
goal_limit = 5
mouse_ball_i = 0
ball_animation_frame = 400

p1_name = ''
p2_name = ''
