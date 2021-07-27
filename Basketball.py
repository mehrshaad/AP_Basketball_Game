import datetime as D
import json as J
import math as M
import random as R
import time as T

import pygame as P

from Basketball_class import *
from Basketball_variable import *
from pygame_functions import *

# menu functions


def blur_pic(surface, amount):
    if amount < 1.0:
        raise ValueError("Arg 'amount' must be greater than 1.0, passed in value is %s" % amount)
    scale = 1.0/float(amount)
    surf_size = surface.get_size()
    scale_size = (int(surf_size[0]*scale), int(surf_size[1]*scale))
    surf = P.transform.smoothscale(surface, scale_size)
    surf = P.transform.smoothscale(surf, surf_size)
    return surf


def reset_menu():  # vase reset hame var ha
    global Text_Hello, Text_Box_1, Text_Box_2, Font, input_boxes, menu_key, solo_key, Style, multi_key, multi_key2, Difficulty, menu_done, name1_key, name2_key, Mode, Style2, goals, scores, time, Player_frame, Event, mouse_click, mouse_ready, mouse_ball_num, goal_solo_p, goal_solo_p1, mouse_ball_i, ball_animation_frame
    Text_Hello = Font.render(f'Hello There!', True, (255, 255, 255))
    Text_Box_1 = Font.render(f'', True, (255, 255, 255))
    Text_Box_2 = Font.render(f'', True, (255, 255, 255))
    menu_key = False
    menu_done = False
    solo_key = False
    multi_key = False
    multi_key2 = False
    name1_key = False
    name2_key = False
    Difficulty = 0
    Style = 0
    Style2 = 1
    Mode = ''
    goals[0], goals[1] = 0, 0  # nope
    scores = [0, 0]
    time = -1
    Player_frame = 0
    Event = 0
    mouse_click = True
    mouse_ready = False
    mouse_ball_num = 20
    goal_solo_p = 1
    goal_solo_p1 = 1
    mouse_ball_i = 0
    ball_animation_frame = 400
    input_boxes.clear()


def read_data():
    global Data
    Data = {}
    for user, name, goals, score, games in connect.execute("SELECT * FROM Users"):
        Data[user] = {
            'Name': str(name),
            'Goals': int(goals),
            'Score': int(score),
            'Games': eval(games)
        }
        Data[user]['Games'] = dict(sorted(Data[user]['Games'].items(), key=lambda x: x[0].lower()))
    Data = dict(sorted(Data.items(), key=lambda x: x[0].lower()))  # sorting data incase sensitive


def store_data():  # in vase ine k data ro bzare to database
    global Data
    try:
        connect.execute("DELETE FROM Users")
        connect.commit()
    except:
        print('table is empty')
    for user in Data.keys():
        connect.execute(f"""INSERT INTO Users VALUES (
            "{user}","{Data[user]['Name']}","{Data[user]['Goals']}",
            "{Data[user]['Score']}","{Data[user]['Games']}")
            """)
        connect.commit()


def update_data():  # update data after game complete
    global Mode, Data, player_name_box_1, player_name_box_2, scores, goals, Difficulty_list, Difficulty, Dsl
    if Mode == 'Solo':  # adding score and result to Data
        Data[player_name_box_1.return_text()]['Score'] += scores[0]
        Data[player_name_box_1.return_text()]['Goals'] += goals[0]
        Data[player_name_box_1.return_text()]['Games']['Solo'].append([Difficulty_list[Difficulty], str(goals[0])])
        temp = len(Data[player_name_box_1.return_text()]['Games']['Solo'])
        if temp > Dsl:
            Data[player_name_box_1.return_text()]['Games']['Solo'] = Data[player_name_box_1.return_text()]['Games']['Solo'][temp-Dsl:]

    else:
        # player 1
        Data[player_name_box_1.return_text()]['Score'] += scores[0]
        Data[player_name_box_1.return_text()]['Goals'] += goals[0]
        Data[player_name_box_1.return_text()]['Games']['Multi-Player'].append([player_name_box_2.return_text(), f"{goals[0]} - {goals[1]}"])
        temp = len(Data[player_name_box_1.return_text()]['Games']['Multi-Player'])
        if temp > Dsl:
            Data[player_name_box_1.return_text()]['Games']['Multi-Player'] = Data[player_name_box_1.return_text()]['Games']['Multi-Player'][temp-Dsl:]
        # player 2
        Data[player_name_box_2.return_text()]['Score'] += scores[1]
        Data[player_name_box_2.return_text()]['Goals'] += goals[1]
        Data[player_name_box_2.return_text()]['Games']['Multi-Player'].append([player_name_box_1.return_text(), f"{goals[1]} - {goals[0]}"])
        temp = len(Data[player_name_box_2.return_text()]['Games']['Multi-Player'])
        if temp > Dsl:
            Data[player_name_box_2.return_text()]['Games']['Multi-Player'] = Data[player_name_box_2.return_text()]['Games']['Multi-Player'][temp-Dsl:]
    store_data()


def sign_up_menu(bg="Images\sign_solo.png", FPS=60):
    global Frame, main_display, display_width, display_height, name1_key, name2_key, Data, mouse_x, mouse_y, click_sound
    sign_box1 = InputBox(display_width//2-100, 250, 200, 35, active_color='red', inactive_color='black')
    sign_box2 = InputBox(display_width//2-100, 420, 200, 35, active_color='white', inactive_color='black', text_filter='alphabet-space', text='Name!')
    sign_boxes = [sign_box1, sign_box2]
    key = False  # True = signed up
    while True:
        Frame.tick(FPS)
        Event = P.event.poll()
        main_display.blit(P.image.load(bg).convert_alpha(), (0, 0))
        for box in sign_boxes:
            box.handle_event(Event)
            box.update()
            box.draw()
        if Event.type == P.QUIT:
            if key:
                Data[sign_box1.return_text()] = {'Name': sign_box2.return_text(), 'Goals': 0, 'Score': 0, 'Games': {'Solo': [], 'Multi-Player': []}}
                store_data()
            return
        if Event.type == P.MOUSEMOTION:
            mouse_x, mouse_y = Event.pos
        if display_width//2-75 <= mouse_x <= display_width//2+75 and display_height-100 <= mouse_y <= display_height-50 and key:
            if Event.type == P.MOUSEBUTTONDOWN:
                click_sound.play()
                Data[sign_box1.return_text()] = {'Name': sign_box2.return_text(), 'Goals': 0, 'Score': 0, 'Games': {'Solo': [], 'Multi-Player': []}}
                store_data()
                return
        if Event.type == P.KEYDOWN and Event.key == P.K_ESCAPE:
            if key:
                Data[sign_box1.return_text()] = {'Name': sign_box2.return_text(), 'Goals': 0, 'Score': 0, 'Games': {'Solo': [], 'Multi-Player': []}}
                store_data()
            return
        if Event.type == P.KEYDOWN and Event.key == P.K_RETURN and key:
            sign_box2.active = False
            Data[sign_box1.return_text()] = {'Name': sign_box2.return_text(), 'Goals': 0, 'Score': 0, 'Games': {'Solo': [], 'Multi-Player': []}}
            store_data()
            return
        if sign_box1.return_text() not in Data.keys() and sign_box1.return_text() != 'Guest' and len(sign_box1.return_text()) > 3:
            sign_box1.COLOR_ACTIVE = P.Color('GREEN')
            sign_box1.COLOR_INACTIVE = P.Color('GREEN')
            if sign_box2.return_text() != 'Guest' and len(sign_box1.return_text()) > 3:
                key = True
            else:
                key = False
        else:
            sign_box1.COLOR_ACTIVE = P.Color('red')
            sign_box1.COLOR_INACTIVE = P.Color('red')
            key = False
        if display_width//2+220 <= mouse_x <= display_width//2+270 and 19 <= mouse_y <= 69:  # back button
            back_pic = P.image.load(r"Images\back2.png").convert_alpha()
            main_display.blit(P.font.SysFont('Aerial', 18).render(f'Back', True, (255, 255, 255)), (display_width//2+230, 80))  # freezed text
            if Event.type == P.MOUSEBUTTONDOWN:
                click_sound.play()
                return
        else:
            back_pic = P.image.load(r"Images\back.png").convert_alpha()  # keifiat ax bala mire
        main_display.blit(back_pic, (display_width//2+220, 19))  # back button
        if key:
            main_display.blit(P.image.load(r"Images\done.png").convert_alpha(), (display_width//2-75, display_height-100))
        else:
            main_display.blit(P.image.load(r"Images\not_done.png").convert_alpha(), (display_width//2-75, display_height-100))
        P.display.flip()


def loading(limit=80, FPS=15, first_image=r"Images\menu_bg.jpg", last_image=r"Images\bg.png"):
    global Menu_Background, Frame, main_display, display_height
    for i in range(1, limit):
        if i % 2 == 0:
            Text = P.font.SysFont('Aerial', 24).render('Loading.../', True, (255, 255, 255))
        else:
            Text = P.font.SysFont('Aerial', 24).render('Loading...\\', True, (255, 255, 255))
        Frame.tick(FPS)
        Event = P.event.poll()
        if Event.type == P.QUIT:
            P.quit()
        if i < limit//2:
            main_display.blit(blur_pic(P.image.load(first_image), i), (-50, -110))
        else:
            main_display.blit(blur_pic(P.image.load(last_image), limit-i), (0, 0))
        main_display.blit(Text, (20, display_height-50))
        main_display.fill((255, 255, 255), (20, display_height-20, 10*i+5*i-40, 10))
        P.display.flip()


def recent_games(data_id='Mehrshad1379'):
    global main_display, display_width, Data
    a = 0
    data = []
    for i in reversed(Data[data_id]['Games']['Solo']):
        data.append([P.font.SysFont('mvboli', 22).render(f"{i[0]}", True, (255, 255, 255)), (display_width//2-225-len(i[0])*5, 237+(83*a))])
        data.append([P.font.SysFont('mvboli', 22).render(f"{i[1]}", True, (255, 255, 255)), (display_width//2-75-len(i[1])*5, 237+(83*a))])
        a += 1
    a = 0
    for i in reversed(Data[data_id]['Games']['Multi-Player']):
        data.append([P.font.SysFont('mvboli', 17).render(f"{i[0]}", True, (255, 255, 255)), (display_width//2+62-len(i[0])*4, 240+(83*a))])
        data.append([P.font.SysFont('mvboli', 22).render(f"{i[1]}", True, (255, 255, 255)), (display_width//2+215-len(i[1])*5, 237+(83*a))])
        a += 1
    return data


def back():
    global menu_key, solo_key, multi_key, multi_key2, input_boxes, player_name_box_1, player_name_box_2, Text_Box_1, Text_Box_2, Style, Style2, menu_done, name1_key, name2_key
    if menu_key and solo_key:
        reset_menu()
        menu_key = False
        solo_key = False
    elif menu_key and multi_key:
        if multi_key2:
            multi_key2 = False
            player_name_box_1 = InputBox(220, 150, 200, 35)
            player_name_box_2 = InputBox(220, 350, 200, 35)
            input_boxes.append(player_name_box_1)
            input_boxes.append(player_name_box_2)
            Text_Box_1 = Font.render(f'Player 1:', True, (255, 255, 255))
            Text_Box_2 = Font.render(f'Player 2:', True, (255, 255, 255))
            Style = 0
            Style2 = 1
            menu_done = False
            name1_key = False
            name2_key = False
        else:
            reset_menu()
            menu_key = False
            solo_key = False

# game functions


def mouse():  # in ham braye mouse e
    global Event, mouse_click, mouse_ready, xmouse1, ymouse1, xmouse2, ymouse2
    try:
        if Event.type == P.MOUSEBUTTONDOWN and mouse_click:  # mouse_click ye sharte ke age test()=True dobare nmizare in shart ok she
            xa, ya = P.mouse.get_pos()
            if test(xa, ya):
                xmouse1, ymouse1 = Player1.x, Player1.y
                mouse_click = False
        if (Event.type == P.MOUSEMOTION) and (not mouse_click):  # dot az inja shoro mishe
            xc, yc = P.mouse.get_pos()
            speed_dots(xmouse1, ymouse1, xc, yc)
        if (Event.type == P.MOUSEBUTTONUP) and (not mouse_click):  # age shart ghabl ok bood miyad to in
            dots.hide()
            xb, yb = P.mouse.get_pos()
            xmouse2 = xb
            ymouse2 = yb
            mouse_click = True
            mouse_ready = True  # in ke True mishe shart baad True mishe
        if mouse_ready:
            mouse_ready = False  # ta dafee baad ke in function call mishe va True in False mimone
            speed(xmouse1, ymouse1, xmouse2, ymouse2)  # coordinates mouse re migire mire braye mohasebe velocity
    except:
        pass


def test(x, y):  # ye square kocholo dor player, age mouse to oon click shod okeye
    global Player1
    if ((x <= (Player1.x + 50)) and (x >= (Player1.x - 50))) and ((y <= (Player1.y + 50)) and (y >= (Player1.y - 50))):
        return True
    return False


def test_out(x, y):  # ye circle bozorg dor player, age mouse to oon clickesh vel shod okeye
    global Player1
    if ((Player1.x-x)**2+(Player1.y-y)**2)**0.5 <= 100:  # age to shoaa ye 100px player bood
        return x, y
    else:
        return circle_interact(x, y)


def circle_interact(x, y):
    global Player1
    gcd = M.gcd((y-Player1.y), (x-Player1.x))
    dy = (y-Player1.y)/gcd/500  # momkene addad aval bashe /500 mikonam
    dx = (x-Player1.x)/gcd/500
    while not ((Player1.x-x)**2+(Player1.y-y)**2)**0.5 <= 100:
        x -= dx
        y -= dy
    return x, y


def speed_dots(x, y, px, py):
    global Player1, Balls, mouse_ball_i, Dots
    px, py = test_out(px, py)
    dots_pos(((px-Player1.x)/5), ((py-Player1.y)/5))


def speed(x, y, px, py):
    global Player1, Balls, mouse_ball_i
    px, py = test_out(px, py)
    Balls[mouse_ball_i].change(((px-Player1.x)/5), ((py-Player1.y)/5))  # mouse_ball_i ke moshakhase on /5 ham test kardam didam okeye
    mouse_ball_i += 1  # age hes mikonin speed bayad bishtar|kamtar she /5 avaz konin

def print_balls():  # har frame ball haro chap mikone
    global Player1, Balls, mouse_ball_i
    for i in range(mouse_ball_i):
        Balls[i].move(toor.lx, toor.rx, toor.ly, Player1.x, Player1.y, 1)


def dots_pos(vx, vy):  # pishbini dot ha ___ aval 20 ta pishbini mikonim vali 10 ta print mikonim
    global Player1, Balls, mouse_ball_i  # baraye behtar run shodam va sangin nashodam mohasebat
    Dots[0].x = Player1.x  # to har fream va ...
    Dots[0].y = Player1.y
    listt = [[Dots[0].x, Dots[0].y]]
    for i in range(1, 20):
        a = listt[i-1][0] - vx
        b = listt[i-1][1] - vy
        vx, vy = gravity(vx, vy, a, b)
        a = test_x(a)
        b = test_y(b)
        listt.append([a, b])
    for i in range(2, 20, 2):
        Dots[i//2].x = listt[i][0]
        Dots[i//2].y = listt[i][1]
    dots.show()


def gravity(x, y, b_x, b_y):
    global display_width, display_height
    y -= 0.4  # gravitymoon
    x += 0.00000001  # ino ghozashtam to line badi (x/x)=0/0 nashe hes raise ghozari nabood :)
    x = (abs(x)-0.03)*(x/abs(x))  # 0.03 kam mikone
    if b_x < 0 or b_x > display_width - 20:
        x = -x * (2/3)
    if b_y < 0 or b_y > 481:  # 480 zamine
        y = -y * (1/2)
        y = 0
    return x, y


def test_x(ball_x):
    if ball_x <= 5:
        return 10
    if ball_x >= 1180:
        return 1179
    return ball_x


def test_y(ball_y):
    if ball_y <= 0:
        return 1
    if ball_y >= 480:
        return 479
    return ball_y


def move_toor(vx, vy):
    toor.move(toor.x+vx, toor.y+vy)


def test_k():
    global kx, ky
    if toor.x < 700:
        kx = -kx
    elif toor.x > 1000:
        kx = -kx
    if toor.y < 100:
        ky = -ky
    elif toor.y > 170:
        ky = -ky


def show_goals(multi_show_time=False, time_up=False):
    global input_boxes, main_display, Data, goals, game_time, Frame
    if time_up:
        P.mixer.music.pause()
        if Mode == 'Solo':
            whistle_sound.play()
            for i in range(400):
                Frame.tick(60)
                Event = P.event.poll()
                main_display.blit(P.image.load(r"Images\time_up.png").convert_alpha(), (display_width//2-300, display_height//2-150))
                if (Event.type == P.MOUSEBUTTONDOWN) or (Event.type == P.KEYDOWN):
                    P.mixer.music.play(-1)
                    return
                main_display.fill((255, 255, 255), (20, display_height-20, round(i*2.9), 10))
                P.display.flip()
            P.mixer.music.play(-1)
            return
        else:
            x, y = display_width//2, display_height//2-100
            if goals[0] > goals[1]:
                text = P.font.SysFont('mvboli', 70).render(f"{str(player_name_box_1.return_text())} Wins!", True, (0, 0, 0))
                text1 = P.font.SysFont('mvboli', 70).render(f"{str(player_name_box_1.return_text())} Wins!", True, Colors[Style])
                x -= (len(str(player_name_box_1.return_text()))+4)*22
            else:
                text = P.font.SysFont('mvboli', 70).render(f"{str(player_name_box_2.return_text())} Wins!", True, (0, 0, 0))
                text1 = P.font.SysFont('mvboli', 70).render(f"{str(player_name_box_2.return_text())} Wins!", True, Colors[Style2])
                x -= (len(str(player_name_box_2.return_text()))+4)*22
            whistle_sound.play()
            for i in range(400):
                Frame.tick(60)
                Event = P.event.poll()
                main_display.blit(text1, (x+3, y+3))
                main_display.blit(text, (x, y))
                if (Event.type == P.MOUSEBUTTONDOWN):
                    P.mixer.music.play(-1)
                    return
                main_display.fill((255, 255, 255), (20, display_height-20, round(i*2.9), 10))
                P.display.flip()
            P.mixer.music.play(-1)
            return
    else:
        if Mode == 'Solo':  # solo player
            text = P.font.SysFont('comicsansms', 28).render(f"Goal: {goals[0]}", True, (0, 0, 0))
            text1 = P.font.SysFont('comicsansms', 28).render(f"Time: {str(game_time)}", True, (0, 0, 0))
            main_display.blit(text, (display_width//2-display_width//3, 25))
            main_display.blit(text1, (display_width//2+display_width//5, 25))
        else:  # multi-player
            text = P.font.SysFont('comicsansms', 28).render(f"{str(player_name_box_1.return_text())}: {goals[0]}", True, Colors[Style])
            text1 = P.font.SysFont('comicsansms', 28).render(f"{str(player_name_box_2.return_text())}: {goals[1]}", True, Colors[Style2])
            text2 = P.font.SysFont('comicsansms', 28).render(f"Time: {str(game_time)}", True, (0, 0, 0))
            main_display.blit(text, (display_width//2-display_width//3, 25))
            main_display.blit(text1, (display_width//2+display_width//5, 25))
            if multi_show_time:
                main_display.blit(text2, (display_width//2-50, 25))


def game_over(mp=False, bg=r"Images\bg.png", FPS=60, pic_size=[300, 95], rotate=False, angle=180, pic_merge=120, text_merge=100, blur_val=80, font=P.font.SysFont('mvboli', 30)):
    global Frame, main_display, mouse_x, mouse_y, player_name_box_1, player_name_box_2, goals, scores, display_width
    x = text_merge
    bg = blur_pic(P.image.load(bg), blur_val)
    temp_pic1 = P.image.load(r"Images\next.png").convert_alpha()
    temp_pic2 = P.image.load(r"Images\next_hover.png").convert_alpha()
    if rotate:
        temp_pic1 = P.transform.rotate(temp_pic1, angle)
        temp_pic2 = P.transform.rotate(temp_pic2, angle)
    temp_pic1 = P.transform.scale(temp_pic1, (pic_size[0], pic_size[1]))
    temp_pic2 = P.transform.scale(temp_pic2, (pic_size[0], pic_size[1]))
    goal_sound[R.randint(0, 2)].play()
    while True:
        Frame.tick(FPS)
        Event = P.event.poll()
        main_display.blit(bg, (0, 0))
        if Event.type == P.QUIT:
            return
        if Event.type == P.MOUSEMOTION:
            mouse_x, mouse_y = Event.pos
        if display_width-(pic_size[0]+pic_merge) <= mouse_x <= display_width-(pic_merge) and display_height-(pic_size[1]+pic_merge) <= mouse_y <= display_height-(pic_merge):
            main_display.blit(temp_pic2, (display_width-(pic_size[0]+pic_merge), display_height-(pic_size[1]+pic_merge)))
            if Event.type == P.MOUSEBUTTONDOWN:
                click_sound.play()
                return
        else:
            main_display.blit(temp_pic1, (display_width-(pic_size[0]+pic_merge), display_height-(pic_size[1]+pic_merge)))
        if not mp:
            username = player_name_box_1.return_text()
            # game result
            main_display.blit(font.render(f"This Game:", True, (0, 0, 0)), (50, 50))
            main_display.blit(font.render(f"Difficulty: {Difficulty_list[Difficulty]}", True, (0, 0, 0)), (50, 50+x*1))
            main_display.blit(font.render(f"Goals: {goals[0]}", True, (0, 0, 0)), (50, 50+x*2))
            main_display.blit(font.render(f"Score: {scores[0]}", True, (0, 0, 0)), (50, 50+x*3))
            # profile
            main_display.blit(font.render(f"{username}:", True, (0, 0, 0)), (display_width//2+50, 50))
            main_display.blit(font.render(f"Name: {Data[username]['Name']}", True, (0, 0, 0)), (display_width//2+50, 50+x))
            main_display.blit(font.render(f"Goals: {Data[username]['Goals']}", True, (0, 0, 0)), (display_width//2+50, 50+x*2))
            main_display.blit(font.render(f"Score: {Data[username]['Score']}", True, (0, 0, 0)), (display_width//2+50, 50+x*3))
            main_display.blit(font.render(f"Remaining Time: {game_time//60}:{game_time%60:02d}", True, (0, 0, 0)), (50, 50+x*4))
        else:
            username = player_name_box_1.return_text()
            username1 = player_name_box_2.return_text()
            # player 1
            main_display.blit(font.render(f"{username}:", True, (0, 0, 0)), (50, 50))
            main_display.blit(font.render(f"Name: {Data[username]['Name']}", True, (0, 0, 0)), (50, 50+x))
            main_display.blit(font.render(f"Goals: {Data[username]['Goals']} + {goals[0]} (this game)", True, (0, 0, 0)), (50, 50+x*2))
            main_display.blit(font.render(f"Score: {Data[username]['Score']} + {scores[0]} (this game)", True, (0, 0, 0)), (50, 50+x*3))
            # player 2
            main_display.blit(font.render(f"{username1}:", True, (0, 0, 0)), (display_width//2+50, 50))
            main_display.blit(font.render(f"Name: {Data[username1]['Name']}", True, (0, 0, 0)), (display_width//2+50, 50+x))
            main_display.blit(font.render(f"Goals: {Data[username1]['Goals']} + {goals[1]} (this game)", True, (0, 0, 0)), (display_width//2+50, 50+x*2))
            main_display.blit(font.render(f"Score: {Data[username1]['Score']} + {scores[1]} (this game)", True, (0, 0, 0)), (display_width//2+50, 50+x*3))
        P.display.flip()


read_data()
P.mixer.music.load(Music[R.randint(0, 2)])
P.mixer.music.play(-1)
while not game_exit:

    # menu
    P.display.set_caption('Welcome To Basketball Game!')  # title
    while True:
        Frame.tick(60)
        Event = P.event.poll()
        if menu_key and solo_key:
            Text = Font.render(f'Selected Mode: {Mode} - {Difficulty_list[Difficulty]} - Time: {list(solo_time.keys())[Difficulty]}', True, (255, 255, 255))
        else:
            Text = Font.render(f'Selected Mode: {Mode}', True, (255, 255, 255))
        # rendering images and texts
        main_display.blit(Menu_Background, (-50, -110))  # background
        main_display.blit(Text, (20, 60))  # Selected Mode ...
        main_display.blit(Text_Hello, (20, 15))  # Hello ...
        if multi_key2:
            main_display.blit(Text_Box_1, (20, 105))
            main_display.blit(Text_Box_2, (20, 390))
        else:
            main_display.blit(Text_Box_1, (20, 140))
            main_display.blit(Text_Box_2, (20, 340))
        if not menu_key:
            main_display.blit(pic_solo, (150, 140))
            main_display.blit(pic_multi, (150, 350))
        if T.time()-time <= 5:  # in vase moghei k error mide 5sec mimone baad mire
            main_display.blit(Text_Help, (400, 0))
        if menu_key:  # rendering text boxes
            for box in input_boxes:
                box.handle_event(Event)
                box.update()
                box.draw()
        if Event.type == P.MOUSEMOTION:
            mouse_x, mouse_y = Event.pos
        # mode menu
        if not menu_key:  # in if vase on menu avaliast k mode entekhab mishe
            if 170 <= mouse_x <= 430 and 160 <= mouse_y <= 320:
                pic_solo = solo_active
                Mode = 'Solo'
                solo_key = True
                main_display.blit(P.image.load(r"Images\solo_describe.png").convert_alpha(), (mouse_x+15, mouse_y+15))  # help text for solo mode (following curser)
                if Event.type == P.MOUSEBUTTONDOWN:
                    click_sound.play()
                    player_name_box_1 = InputBox(240, 150, 200, 35)
                    input_boxes.append(player_name_box_1)
                    Text_Box_1 = Font.render(f'Player Name:', True, (255, 255, 255))
                    Text_Box_2 = Font.render(f'Selected Player: {Sprite_colors[Style]}', True, (255, 255, 255))
                    menu_key = True
            else:
                pic_solo = solo_passive
                solo_key = False
            if 170 <= mouse_x <= 430 and 370 <= mouse_y <= 530:
                pic_multi = multi_active
                Mode = 'Multi-Player'
                multi_key = True
                main_display.blit(P.image.load(r"Images\multi_describe.png").convert_alpha(), (mouse_x+15, mouse_y+15))  # help text for multi-player mode (following curser)
                if Event.type == P.MOUSEBUTTONDOWN:
                    click_sound.play()
                    player_name_box_1 = InputBox(220, 150, 200, 35)
                    player_name_box_2 = InputBox(220, 350, 200, 35)
                    input_boxes.append(player_name_box_1)
                    input_boxes.append(player_name_box_2)
                    Text_Box_1 = Font.render(f'Player 1:', True, (255, 255, 255))
                    Text_Box_2 = Font.render(f'Player 2:', True, (255, 255, 255))
                    menu_key = True
            else:
                pic_multi = multi_passive
                multi_key = False
            if not solo_key and not multi_key and not menu_key:
                Mode = ''
                pic_multi = multi_passive
            if mouse_x <= 50 and display_height//2-125 <= mouse_y <= display_height//2-125+251:  # leaderboard
                main_display.blit(leaderboard_pics[1], (0, display_height//2-125))
                main_display.blit(leaderboard_pics[2], (70, display_height//2-250))
                score_list = []
                for i in Data.keys():  # appending names and scores into a list
                    score_list.append([i, Data[i]['Score']])
                score_list.sort(key=lambda x: x[1], reverse=True)  # sorting score_list by Score
                for i in range(10):  # rendering top-10-score players
                    try:
                        if i % 2 == 0:
                            main_display.blit(P.font.SysFont('Aerial', 22).render(f'{score_list[i][0]}', True, (0, 0, 0)), (471-len(str(score_list[i][0]))*5, 175+i*39))
                            main_display.blit(P.font.SysFont('Aerial', 22).render(f'{score_list[i][1]}', True, (0, 0, 0)), (730-len(str(score_list[i][1]))*5, 175+i*39))
                        else:
                            main_display.blit(P.font.SysFont('Aerial', 22).render(f'{score_list[i][0]}', True, (255, 255, 255)), (465-len(str(score_list[i][0]))*5, 175+i*39))
                            main_display.blit(P.font.SysFont('Aerial', 22).render(f'{score_list[i][1]}', True, (255, 255, 255)), (730-len(str(score_list[i][1]))*5, 175+i*39))
                    except:
                        break
            else:
                main_display.blit(leaderboard_pics[0], (0, display_height//2-125))
        elif menu_key and not multi_key2:  # in shart vase moghei k solo ya multi-player entekhab mishe
            if Mode == 'Solo':
                if player_name_box_1.return_text() in Data.keys():
                    Text_Hello = Font.render(f"Hello {Data[player_name_box_1.return_text()]['Name']}!", True, (255, 255, 255))
                    name1_key = True
                else:
                    Text_Hello = Font.render(f"Hello {player_name_box_1.return_text()}!", True, (255, 255, 255))
                    name1_key = False
                    if 450 <= mouse_x <= 510 and 170 <= mouse_y <= 180:
                        main_display.blit(P.font.SysFont('Aerial', 22).render(f'Sign Up', True, (255, 255, 0)), (450, 170))
                        if Event.type == P.MOUSEBUTTONDOWN:
                            click_sound.play()
                            # sign up menu
                            sign_up_menu()
                    else:
                        main_display.blit(P.font.SysFont('Aerial', 22).render(f'Sign Up', True, (255, 0, 0)), (450, 170))
                main_display.blit(Font.render(f"Select Difficulty:", True, (255, 255, 255)), (20, 200))
                menu_done = True
                # rendering difficulty
                for i in range(3):
                    mokhtasat = [20+(i*120), 270]
                    if mokhtasat[0] <= mouse_x <= mokhtasat[0]+99 and mokhtasat[1] <= mouse_y <= mokhtasat[1]+55 or Difficulty == i:
                        if Event.type == P.MOUSEBUTTONDOWN:
                            click_sound.play()
                            Difficulty = i
                        img = P.image.load(Difficulty_pic[i+3])
                    else:
                        img = P.image.load(Difficulty_pic[i])
                    img = P.transform.scale(img, (99, 55))
                    main_display.blit(img, mokhtasat)
                # rendering sprites
                for i in range(7):
                    if i < 4:
                        mokhtasat = [40+(i*150), 400]
                    else:
                        mokhtasat = [90+((i-4)*150), 550]
                    if mokhtasat[0] <= mouse_x <= mokhtasat[0]+80 and mokhtasat[1] <= mouse_y <= mokhtasat[1]+100 or i == Style:
                        if Event.type == P.MOUSEBUTTONDOWN:
                            click_sound.play()
                            Style = i
                            Text_Box_2 = Font.render(f'Selected Player: {Sprite_colors[Style]}', True, (255, 255, 255))
                        mokhtasat[0] -= 10
                        mokhtasat[1] -= 10
                        img = P.image.load(Sprite_active[i])
                    else:
                        img = P.image.load(Sprite_passive[i])
                    main_display.blit(img, mokhtasat)
            elif Mode == 'Multi-Player':
                if player_name_box_1.return_text() in Data.keys():
                    p1_name = Data[player_name_box_1.return_text()]['Name']
                    name1_key = True
                else:
                    p1_name = player_name_box_1.return_text(default='Player 1')
                    name1_key = False
                    if 430 <= mouse_x <= 490 and 170 <= mouse_y <= 180:
                        main_display.blit(P.font.SysFont('Aerial', 22).render(f'Sign Up', True, (255, 255, 0)), (430, 170))
                        if Event.type == P.MOUSEBUTTONDOWN:
                            click_sound.play()
                            # sign up menu for multi-player p1
                            sign_up_menu(bg="Images\sign_multi.png")
                    else:
                        main_display.blit(P.font.SysFont('Aerial', 22).render(f'Sign Up', True, (255, 0, 0)), (430, 170))
                if (player_name_box_2.return_text() in Data.keys()) and (player_name_box_1.return_text() != player_name_box_2.return_text()):
                    p2_name = Data[player_name_box_2.return_text()]['Name']
                    name2_key = True
                else:
                    p2_name = player_name_box_2.return_text(default='Player 2')
                    name2_key = False
                    if 430 <= mouse_x <= 490 and 370 <= mouse_y <= 380:
                        main_display.blit(P.font.SysFont('Aerial', 22).render(f'Sign Up', True, (255, 255, 0)), (430, 370))
                        if Event.type == P.MOUSEBUTTONDOWN:
                            click_sound.play()
                            # sign up menu for multiplayer p2
                            sign_up_menu(bg="Images\sign_multi.png")
                    else:
                        main_display.blit(P.font.SysFont('Aerial', 22).render(f'Sign Up', True, (255, 0, 0)), (430, 370))
                Text_Hello = Font.render(f"Hello {p1_name} & {p2_name}!", True, (255, 255, 255))
                if 150 <= mouse_x <= 450 and 500 <= mouse_y <= 590 and name1_key and name2_key:  # next button
                    main_display.blit(next_active, (150, 500))
                    if Event.type == P.MOUSEBUTTONDOWN:
                        click_sound.play()
                        Text_Box_1 = Font.render(f'{player_name_box_1.return_text()}: {Sprite_colors[Style]}', True, (255, 255, 255))
                        Text_Box_2 = Font.render(f'{player_name_box_2.return_text()}: {Sprite_colors[Style2]}', True, (255, 255, 255))
                        input_boxes.clear()
                        multi_key2 = True
                elif name1_key and name2_key:
                    main_display.blit(next_passive, (150, 500))
        else:  # if multi_key2
            menu_done = True
            for i in range(7):
                if i < 4:
                    mokhtasat = [40+(i*150), 155]
                else:
                    mokhtasat = [90+((i-4)*150), 255]
                if Style2 == i:
                    continue
                if mokhtasat[0] <= mouse_x <= mokhtasat[0]+80 and mokhtasat[1] <= mouse_y <= mokhtasat[1]+100 or i == Style:
                    if Event.type == P.MOUSEBUTTONDOWN:
                        click_sound.play()
                        Style = i
                        Text_Box_1 = Font.render(f'{player_name_box_1.return_text()}: {Sprite_colors[Style]}', True, (255, 255, 255))
                    mokhtasat[0] -= 10
                    mokhtasat[1] -= 10
                    img = P.image.load(Sprite_active[i])
                else:
                    img = P.image.load(Sprite_passive[i])
                main_display.blit(img, mokhtasat)
            # player 2 sprite
            for i in range(7):
                if i < 4:
                    mokhtasat = [40+(i*150), 450]
                else:
                    mokhtasat = [90+((i-4)*150), 550]
                if Style == i:
                    continue
                if mokhtasat[0] <= mouse_x <= mokhtasat[0]+80 and mokhtasat[1] <= mouse_y <= mokhtasat[1]+100 or i == Style2:
                    if Event.type == P.MOUSEBUTTONDOWN:
                        click_sound.play()
                        Style2 = i
                        Text_Box_2 = Font.render(f'{player_name_box_2.return_text()}: {Sprite_colors[Style2]}', True, (255, 255, 255))
                    mokhtasat[0] -= 10
                    mokhtasat[1] -= 10
                    img = P.image.load(Sprite_active[i])
                else:
                    img = P.image.load(Sprite_passive[i])
                main_display.blit(img, mokhtasat)
        # quiting menu
        if Event.type == P.QUIT:
            P.mixer.music.pause()
            P.display.set_caption('Come Back!')
            main_display.blit(P.image.load(r"Images\credits.jpg").convert_alpha(), (-50, -110))
            P.display.flip()
            T.sleep(3)
            P.quit()
        if Event.type == P.KEYDOWN and Event.key == P.K_RETURN:  # enter key functions on each stage
            if Mode == 'Multi-Player':
                if menu_done and name1_key and name2_key:
                    break
            if not menu_key:
                Text_Help = Font.render(f"   Please Select Game Mode", True, (255, 0, 0))
                time = T.time()
            if multi_key:
                if not name1_key or not name2_key:
                    Text_Help = Font.render(f"Players Must Sign-in or Sign-up", True, (255, 0, 0))
                    time = T.time()
                else:
                    Text_Box_1 = Font.render(f'{player_name_box_1.return_text()}: {Sprite_colors[Style]}', True, (255, 255, 255))
                    Text_Box_2 = Font.render(f'{player_name_box_2.return_text()}: {Sprite_colors[Style2]}', True, (255, 255, 255))
                    input_boxes.clear()
                    multi_key2 = True
            elif Mode == 'Solo':
                if not name1_key:
                    Text_Help = Font.render(f"You Should Sign-in or Sign-up", True, (255, 0, 0))
                    time = T.time()
                else:
                    break
        if (solo_key and name1_key) or (multi_key2):  # start button
            if display_width-290 <= mouse_x <= display_width-50 and display_height-200 <= mouse_y <= display_height-40:
                main_display.blit(P.image.load(r"Images\start2.png").convert_alpha(), (display_width-327, display_height-227))
                if Event.type == P.MOUSEBUTTONDOWN:
                    click_sound.play()
                    break
            else:
                main_display.blit(P.image.load(r"Images\start.png").convert_alpha(), (display_width-300, display_height-200))
        # back key
        if menu_key:
            main_display.blit(back_pic, (display_width-70, 20))  # back picture
            if display_width-70 <= mouse_x <= display_width-20 and 20 <= mouse_y <= 70:
                back_pic = P.image.load(r"Images\back2.png").convert_alpha()
                main_display.blit(P.font.SysFont('Aerial', 18).render(f'Back', True, (255, 255, 255)), (display_width-60, 80))  # freezed help text for back button
                if Event.type == P.MOUSEBUTTONDOWN:
                    click_sound.play()
                    back()
            else:
                back_pic = P.image.load(r"Images\back.png").convert_alpha()
        P.display.flip()

    P.mixer.music.pause()
    loading()
    P.display.set_caption('Basketball Game!')  # title
    game_time = solo_time[list(solo_time.keys())[Difficulty]]  # setting time limit
    Time = T.time()  # time avalie
    P.mixer.music.load(Music[R.randint(0, 2)])
    P.mixer.music.play(-1)

    # solo_levels

    if Mode == 'Solo' and Difficulty == 0:
        setAutoUpdate(False)
        kx = 0
        ky = 0
        Balls = [0] * mouse_ball_num
        for i in range(mouse_ball_num):
            Balls[i] = ball_solo()
        setBackgroundImage(r"Images\bg.png")
        P.display.flip()
        toor = toor_solo(1000, 130)
        moveSprite(toor.sprite, toor.x, toor.y)
        showSprite(toor.sprite)
        Player1 = player(display_width//2-150, display_height-200, 4, False, 0, 0, 0, 0, Sprite_pics[Style], 'left', 'right', 'up', True, 1, Sprite_pics_2[Style])
        moveSprite(Player1.sprite, Player1.x, Player1.y, True)
        moveSprite(Player1.solo_aim, Player1.x, Player1.y, True)
        showSprite(Player1.sprite)
        showSprite(Player1.solo_aim)
        Dots = [0] * 10
        for i in range(10):
            Dots[i] = dots(Player1.x, Player1.y)
        while True:
            if T.time()-Time >= 1:
                game_time -= 1
                Time = T.time()
                setBackgroundImage(r"Images\bg.png")
                show_goals()
                if game_time == 0:
                    Balls[0].dell()
                    dots.dell()
                    hideSprite(toor.sprite)
                    hideSprite(Player1.sprite)
                    hideSprite(Player1.solo_aim)
                    scores[0] = (R.randint(100, 110))*(goals[0])+100
                    show_goals(time_up=True)
                    game_over()
                    break
            i += 1
            Frame.tick(60)
            if i == 10:
                i = 0
                Player_frame += 1
            Event = P.event.poll()
            if Event.type == P.QUIT:
                Balls[0].dell()
                dots.dell()
                hideSprite(toor.sprite)
                hideSprite(Player1.sprite)
                hideSprite(Player1.solo_aim)
                setBackgroundImage(r"Images\bg.png")
                scores[0] = (R.randint(100, 110))*(goals[0])+100
                game_exit = True
                game_over()
                break
            show_goals()
            updateDisplay()

            mouse()
            updateDisplay()
            move_toor(kx, ky)
            updateDisplay()

            print_balls()
            updateDisplay()

            test_k()
            updateDisplay()

            if goal_solo_p == goals[0]:
                goal_solo_p += 1
                setBackgroundImage(r"Images\bg.png")

    if Mode == 'Solo' and Difficulty == 1:
        setAutoUpdate(False)
        kx = -0.3
        ky = 0
        Balls = [0] * mouse_ball_num
        for i in range(mouse_ball_num):
            Balls[i] = ball_solo()
        P.display.flip()
        setBackgroundImage(r"Images\bg.png")
        toor = toor_solo(1000, 130)
        moveSprite(toor.sprite, toor.x, toor.y)
        showSprite(toor.sprite)
        Player1 = player(display_width//2-150, display_height-200, 4, False, 0, 0, 0, 0, Sprite_pics[Style], 'left', 'right', 'up', True, 1, Sprite_pics_2[Style])
        moveSprite(Player1.sprite, Player1.x, Player1.y, True)
        moveSprite(Player1.solo_aim, Player1.x, Player1.y, True)
        showSprite(Player1.sprite)
        showSprite(Player1.solo_aim)
        Dots = [0] * 10
        for i in range(10):
            Dots[i] = dots(Player1.x, Player1.y)
        while True:
            if T.time()-Time >= 1:
                game_time -= 1
                Time = T.time()
                setBackgroundImage(r"Images\bg.png")
                show_goals()
                if game_time == 0:
                    Balls[0].dell()
                    dots.dell()
                    hideSprite(toor.sprite)
                    hideSprite(Player1.sprite)
                    hideSprite(Player1.solo_aim)
                    scores[0] = (R.randint(100, 110))*(goals[0])+100
                    show_goals(time_up=True)
                    game_over()
                    break
            i += 1
            Frame.tick(60)
            if i == 10:
                i = 0
                Player_frame += 1
            Event = P.event.poll()
            if Event.type == P.QUIT:
                Balls[0].dell()
                dots.dell()
                hideSprite(toor.sprite)
                hideSprite(Player1.sprite)
                hideSprite(Player1.solo_aim)
                scores[0] = (R.randint(100, 110))*(goals[0])+100
                game_exit = True
                game_over()
                break
            show_goals()
            updateDisplay()

            mouse()
            updateDisplay()

            move_toor(kx, ky)
            updateDisplay()

            print_balls()
            updateDisplay()

            test_k()
            updateDisplay()

            if goal_solo_p == goals[0]:
                goal_solo_p += 1
                setBackgroundImage(r"Images\bg.png")

    if Mode == 'Solo' and Difficulty == 2:
        setAutoUpdate(False)
        kx = -0.3
        ky = 0.1
        Balls = [0] * mouse_ball_num
        for i in range(mouse_ball_num):
            Balls[i] = ball_solo()
        P.display.flip()
        setBackgroundImage(r"Images\bg.png")
        toor = toor_solo(1000, 130)
        moveSprite(toor.sprite, toor.x, toor.y)
        showSprite(toor.sprite)
        Player1 = player(display_width//2-150, display_height-200, 4, False, 0, 0, 0, 0, Sprite_pics[Style], 'left', 'right', 'up', True, 1, Sprite_pics_2[Style])
        moveSprite(Player1.sprite, Player1.x, Player1.y, True)
        moveSprite(Player1.solo_aim, Player1.x, Player1.y, True)
        showSprite(Player1.sprite)
        showSprite(Player1.solo_aim)
        Dots = [0] * 10
        for i in range(10):
            Dots[i] = dots(Player1.x, Player1.y)
        while True:
            if T.time()-Time >= 1:
                game_time -= 1
                Time = T.time()
                setBackgroundImage(r"Images\bg.png")
                show_goals()
                if game_time == 0:
                    Balls[0].dell()
                    dots.dell()
                    hideSprite(toor.sprite)
                    hideSprite(Player1.sprite)
                    hideSprite(Player1.solo_aim)
                    scores[0] = (R.randint(100, 110))*(goals[0])+100
                    show_goals(time_up=True)
                    game_over()
                    break
            i += 1
            Frame.tick(60)
            if i == 10:
                i = 0
                Player_frame += 1
            Event = P.event.poll()
            if Event.type == P.QUIT:
                Balls[0].dell()
                dots.dell()
                hideSprite(toor.sprite)
                hideSprite(Player1.sprite)
                hideSprite(Player1.solo_aim)
                scores[0] = (R.randint(100, 110))*(goals[0])+100
                game_exit = True
                game_over()
                break
            show_goals()
            updateDisplay()

            mouse()
            updateDisplay()

            move_toor(kx, ky)
            updateDisplay()

            print_balls()
            updateDisplay()

            test_k()
            updateDisplay()

            if goal_solo_p == goals[0]:
                goal_solo_p += 1
                setBackgroundImage(r"Images\bg.png")

    # multi-player
    elif Mode == 'Multi-Player':
        setAutoUpdate(False)
        P.display.flip()
        setBackgroundImage(r"Images\background.png")
        Player1 = player(display_width//2, display_height-200, 4, False, 0, 0, 0, 0, Sprite_pics[Style], 'left', 'right', 'up', False, 1, Sprite_pics_2[Style])
        Player2 = player(display_width//2, display_height-200, 4, False, 0, 0, 0, 0, Sprite_pics[Style2], 'a', 'd', 'w', False, 2, Sprite_pics_2[Style2])
        moveSprite(Player1.sprite, Player1.x, Player1.y, True)
        moveSprite(Player2.sprite, Player2.x, Player2.y, True)
        showSprite(Player1.sprite)
        showSprite(Player2.sprite)
        ball1 = ball(100, 100, 0, 0, False, True, 20, 20, 0, "Images/ball1.png", 1, 'l')
        ball2 = ball(1000, 1000, 0, 0, False, True, 20, 20, 0, "Images/ball2.png", -1, 'v')
        while True:
            if goals[0] == goal_limit or goals[1] == goal_limit:
                scores[0] = (R.randint(100, 110))*(goals[0])+100
                scores[1] = (R.randint(100, 110))*(goals[1])+100
                hideSprite(Player1.sprite)
                hideSprite(Player2.sprite)
                hideSprite(ball1.sprite)
                hideSprite(ball2.sprite)
                show_goals(time_up=True)
                game_over(mp=True)
                break
            i += 1
            Frame.tick(60)
            if i == 10:
                i = 0
                Player_frame += 1
            Event = P.event.poll()
            if Event.type == P.QUIT:
                scores[0] = (R.randint(100, 110))*(goals[0])+100
                scores[1] = (R.randint(100, 110))*(goals[1])+100
                hideSprite(Player1.sprite)
                hideSprite(Player2.sprite)
                hideSprite(ball1.sprite)
                hideSprite(ball2.sprite)
                game_exit = True
                game_over(mp=True)
                break
            show_goals()
            updateDisplay()

            Player1.move(Player_frame)
            updateDisplay()

            ball1.move(x1_sabad_1, x2_sabad_1, y_sabad_1, Player1.x, Player1.y, 1)
            updateDisplay()

            Player2.move(Player_frame)
            updateDisplay()

            ball2.move(x1_sabad_2, x2_sabad_2, y_sabad_1, Player2.x, Player2.y, 2)
            updateDisplay()

            if goal_solo_p == goals[0]:
                goal_solo_p += 1
                setBackgroundImage(r"Images\background.png")

            if goal_solo_p1 == goals[1]:
                goal_solo_p1 += 1
                setBackgroundImage(r"Images\background.png")

            show_goals()
            updateDisplay()

    update_data()
    temp = []
    temp1 = []
    while True:  # try again menu
        Frame.tick(60)
        Event = P.event.poll()
        main_display.blit(Menu_Background, (-50, -110))  # background
        main_display.blit(P.font.SysFont('mvboli', 50).render(f"Do You Want to Play Again?", True, (255, 255, 255)), (display_width//2-340, 100))
        main_display.blit(P.image.load(yes_pic).convert_alpha(), (display_width//2-296, 310))
        main_display.blit(P.image.load(no_pic).convert_alpha(), (display_width//2+50, 310))

        if Mode == 'Solo':
            main_display.blit(P.image.load(r"Images\recent.png").convert_alpha(), (display_width//2-111, display_height-42))
            if display_width//2-111 <= mouse_x <= display_width//2+111 and display_height-42 <= mouse_y <= display_height:
                main_display.blit(P.image.load(r"Images\recent_games.png").convert_alpha(), (display_width//2-360, 85))
                if temp == []:
                    temp = recent_games(player_name_box_1.return_text())
                for i in temp:
                    main_display.blit(i[0], i[1])
        else:
            main_display.blit(P.image.load(r"Images\recent_p1.png").convert_alpha(), (display_width//2-111, display_height-42))
            if display_width//2-111 <= mouse_x <= display_width//2+111 and display_height-42 <= mouse_y <= display_height:
                main_display.blit(P.image.load(r"Images\recent_games.png").convert_alpha(), (display_width//2-360, 85))
                main_display.blit(P.font.SysFont('Arial', 18).render(f"{player_name_box_1.return_text()}", True, (255, 255, 255)), (display_width//2+121, display_height-30))
                if temp1 == []:
                    temp1 = recent_games(player_name_box_1.return_text())
                for i in temp1:
                    main_display.blit(i[0], i[1])
            main_display.blit(P.image.load(r"Images\recent_p2.png").convert_alpha(), (display_width//2-111, -8))
            if display_width//2-111 <= mouse_x <= display_width//2+111 and 0 <= mouse_y <= 42:
                main_display.blit(P.image.load(r"Images\recent_games1.png").convert_alpha(), (display_width//2-360, 46))
                main_display.blit(P.font.SysFont('Arial', 18).render(f"{player_name_box_2.return_text()}", True, (255, 255, 255)), (display_width//2+121, 10))
                if temp == []:
                    temp = recent_games(player_name_box_2.return_text())
                for i in temp:
                    main_display.blit(i[0], i[1])

        if Event.type == P.MOUSEMOTION:
            mouse_x, mouse_y = Event.pos
        if Event.type == P.QUIT:
            P.quit()
        if display_width//2-295 <= mouse_x <= display_width//2-46 and 300 <= mouse_y <= 465:  # yes button
            yes_pic = r"Images\yes_hover.png"
            if Event.type == P.MOUSEBUTTONDOWN:
                click_sound.play()
                game_exit = False
                back()
                reset_menu()
                break
        else:
            yes_pic = r"Images\yes.png"
        if display_width//2+50 <= mouse_x <= display_width//2+300 and 300 <= mouse_y <= 465:  # no button
            no_pic = r"Images\no_hover.png"
            if Event.type == P.MOUSEBUTTONDOWN:
                click_sound.play()
                game_exit = True
                break
        else:
            no_pic = r"Images\no.png"

        P.display.flip()

P.mixer.music.pause()
P.display.set_caption('Come Back!')
main_display.blit(P.image.load(r"Images\credits.jpg").convert_alpha(), (-50, -110))
P.display.flip()
T.sleep(3)
P.quit()  # exit :)
