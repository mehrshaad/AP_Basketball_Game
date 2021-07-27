import random as R

import pygame as P

from Basketball_variable import *


class InputBox():
    def __init__(self, x, y, w, h, text='Username!', limit=14, active_color='GREENYELLOW', inactive_color='PALEGREEN', text_color='LIGHTCYAN', font_style='comicsansms', font_size=20, text_filter='alphabet-digit-line'):
        self.COLOR_ACTIVE = P.Color(active_color)
        self.COLOR_INACTIVE = P.Color(inactive_color)
        self.COLOR_TEXT = P.Color(text_color)
        self.FONT = P.font.SysFont(font_style, font_size)
        self.color = P.Color(inactive_color)
        self.rect = P.Rect(x, y, w, h)
        self.text = text
        self.text_default = text
        self.txt_surface = self.FONT.render(text, True, self.color)
        self.active = False
        self.key = True
        self.limit = limit
        self.text_filter = []
        if 'digit' in text_filter.lower():
            self.text_filter += ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        if 'alphabet' in text_filter.lower():
            self.text_filter += ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        if 'line' in text_filter.lower():
            self.text_filter += ['-', '_']
        if 'up' in text_filter.lower():
            self.text_filter += ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                                 'U', 'V', 'W', 'X', 'Y', 'Z']
        if 'space' in text_filter.lower():
            self.text_filter += [' ']
        if 'low' in text_filter.lower():
            self.text_filter += ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

    def handle_event(self, event):
        if event.type == P.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                if self.key:
                    self.key = False
                    self.text = ''
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE
        if event.type == P.KEYDOWN:
            if event.key == P.K_ESCAPE:
                self.active = False
                self.color = self.COLOR_INACTIVE
            if self.active:
                if event.key == P.K_RETURN:
                    # self.key = True
                    self.color = self.COLOR_INACTIVE
                    self.active = False
                    # self.text = self.text_default
                elif event.key == P.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode in self.text_filter:
                        self.text += event.unicode
                        keyboard_sound.play()
                    if len(self.text) > self.limit:
                        self.text = self.text[1:]
                # Re-render the text.
                self.txt_surface = self.FONT.render(self.text, True, self.COLOR_TEXT)
            self.color = self.COLOR_ACTIVE if self.active else self.COLOR_INACTIVE

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen=main_display):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        P.draw.rect(screen, self.color, self.rect, 2)

    def return_text(self, default='Guest'):
        if self.text == self.text_default or self.text == '':
            return default
        return self.text


class ball():
    def __init__(self, x, y, px, py, bol, have, vx, vy, lock, image, side, keyprs):
        self.x = x
        self.y = y
        self.px = px
        self.py = py
        self.bool = bol
        self.have = have
        self.vx = vx
        self.vy = vy
        self.lock = lock
        self.sprite = makeSprite(image)
        self.side = side
        self.keyprs = keyprs

    def move(self, x1, x2, y, plx, ply, num):
        global ball_animation_frame, goal_p1, goal_p2, goals
        if (((self.px <= x1 and self.x >= x2) or (self.px >= x1 and self.x <= x2) or
             (self.px <= x2 and self.x >= x2) or (self.px <= x1 and self.x >= x1))
                and ((self.py <= y and self.y >= y)) and (self.py < self.y)) and (self.px != 0 and self.px != 100):
            # mehrshad inja goal mishe
            goal_sound[R.randint(0, 2)].play()
            if num == 1:
                goals[0] += 1
            elif num == 2:
                goals[1] += 1
        self.px, self.py = self.x, self.y
        if self.lock > 0:
            self.lock -= 1
            self.x -= self.vx
            self.y -= self.vy
            self.vx, self.vy = self.gravity(self.vx, self.vy, self.x, self.y)
            self.x = self.test_x(self.x)
            self.y = self.test_y(self.y)
            moveSprite(self.sprite, self.x, self.y, True)
        if self.lock == 0:
            self.bool = False
        if not self.have:
            if (plx <= self.x+10 and plx >= self.x-10) and (ply <= self.y+10 and ply >= self.y-10):
                hideSprite(self.sprite)
                self.have = True
        if keyPressed(self.keyprs) and self.have:
            self.have = False
            self.vx = 5 * self.side
            self.vy = 18
            self.bool = True
            self.lock = ball_animation_frame
            showSprite(self.sprite)
            self.x = plx
            self.y = ply
            moveSprite(self.sprite, self.x, self.y, True)

    def gravity(self, x, y, b_x, b_y):
        global display_width, display_height, display_ground
        y -= 0.4  # gravitymoon
        x += 0.00000001  # ino ghozashtam to line badi (x/x)=0/0 nashe hes raise ghozari nabood :)
        x = (abs(x)-0.03)*(x/abs(x))  # 0.03 kam mikone
        if b_x < 5 or b_x > display_width - 20:
            x = -x * (2/3)
        if b_y < 0 or b_y > display_ground - 1:  # 480 zamine
            y = -y * (1/2)
        if (b_y > display_ground - 3) and abs(y) < 0.9:  # age in nabashe ball milarze
            self.y = 479
            y = 0
        return x, y

    def test_x(self, ball_x):
        if ball_x <= 5:
            ball_sound[R.randint(0, 1)].play()
            return 10
        if ball_x >= 1180:
            ball_sound[R.randint(0, 1)].play()
            return 1179
        return ball_x

    def test_y(self, ball_y):
        if ball_y <= 0:
            ball_sound[R.randint(0, 1)].play()
            return 1
        if ball_y >= 480:
            ball_sound[R.randint(0, 1)].play()
            return 479
        return ball_y


class player():
    def __init__(self, x, y, ln, bol, lock, side, loop, le, pic, keyleft, keyright, keyjump, solo, num, pic2):
        self.x = x
        self.y = y
        self.ln = ln
        self.bool = bol
        self.lock = lock
        self.side = side
        self.loop = loop
        self.le = le
        self.sprite = makeSprite(pic, 15)
        self.kl = keyleft
        self.kr = keyright
        self.kj = keyjump
        self.solo = solo
        self.num = num
        self.goal = 0
        addSpriteImage(self.sprite, pic2)
        if solo:
            self.solo_aim = makeSprite(r"Images\aim.png")

    def move(self, Player_frame):
        if self.lock == 0:
            self.bool = False
        else:
            self.jump()
        if keyPressed(self.kr):
            self.le = 'right'
            if self.bool:
                return
            if self.x <= display_width:
                self.x += 5
            changeSpriteImage(self.sprite, 1+Player_frame % 6)
            moveSprite(self.sprite, self.x, self.y, True)
            if self.solo:
                moveSprite(self.solo_aim, self.x, self.y, True)
        elif keyPressed(self.kl):
            self.le = 'left'
            if self.bool:
                return
            if self.x >= 0:
                self.x -= 5
            changeSpriteImage(self.sprite, 7+Player_frame % 6)
            moveSprite(self.sprite, self.x, self.y, True)
            if self.solo:
                moveSprite(self.solo_aim, self.x, self.y, True)
        elif keyPressed(self.kj):
            if self.bool:
                return
            self.jump()
        elif not self.bool:
            if self.le == 'right':
                changeSpriteImage(self.sprite, 0)
            elif self.le == 'left':
                changeSpriteImage(self.sprite, 15)

    def jump(self):
        global mid_jump
        if self.bool:
            if self.lock == mid_jump:
                moveSprite(self.sprite, self.x, self.y, True)
                if self.solo:
                    moveSprite(self.solo_aim, self.x, self.y, True)
                self.lock -= 1
                return
            elif self.lock < mid_jump:
                if self.x <= 1150 and self.x >= 60:
                    self.x += self.side
                self.y += self.ln
                moveSprite(self.sprite, self.x, self.y, True)
                if self.solo:
                    moveSprite(self.solo_aim, self.x, self.y, True)
                self.lock -= 1
                return
            elif self.lock > mid_jump:
                if self.x <= 1150 and self.x >= 60:
                    self.x += self.side
                self.y -= self.ln
                moveSprite(self.sprite, self.x, self.y, True)
                if self.solo:
                    moveSprite(self.solo_aim, self.x, self.y, True)
                self.lock -= 1
                return
        if self.le == 'right':
            self.bool = True
            self.lock = mid_jump*2-1
            self.side = 3
            self.loop = 1
            changeSpriteImage(self.sprite, 13)
            moveSprite(self.sprite, self.x, self.y, True)
            if self.solo:
                moveSprite(self.solo_aim, self.x, self.y, True)
        elif self.le == 'left':
            self.bool = True
            self.lock = mid_jump*2-1
            self.side = -3
            self.loop = 1
            changeSpriteImage(self.sprite, 14)
            moveSprite(self.sprite, self.x, self.y, True)
            if self.solo:
                moveSprite(self.solo_aim, self.x, self.y, True)
        else:
            self.bool = True
            self.lock = mid_jump*2-1
            self.side = 0
            self.loop = 1
            changeSpriteImage(self.sprite, 13)
            moveSprite(self.sprite, self.x, self.y, True)
            if self.solo:
                moveSprite(self.solo_aim, self.x, self.y, True)


class ball_solo():
    All = []

    def __init__(self, x=100, y=100, px=0, py=0, bol=False, have=True, vx=0, vy=0, lock=0, image="Images/ball1.png"):
        ball_solo.All.append(self)
        self.x = x  # x of ball
        self.y = y  # y of ball
        self.px = px  # previous x of ball # jenab aghaye eskandari sakht nagir lotfan ;)
        self.py = py  # previous y of ball # sakht nagir :)
        self.bool = bol  # bool for ball? ye hamchenin chizi
        self.have = have  # age ball dast player bood = True age nabood ham nist :/
        self.vx = vx  # velocity of ball
        self.vy = vy  # velocity of ball
        self.lock = lock  # ye joori animation ball be in rabt dare
        self.sprite = makeSprite(image)  # sprite ball
        self.key = True  # age in dorost bashe ball harkat mikone
        self.goal = True

    def move(self, x1, x2, y, plx, ply, p):
        global ball_animation_frame, goal_solo, goals
        if self.key == False:  # ta vaghti be ball speed nadim in injori mimone
            if (((self.px <= x1 and self.x >= x2) or (self.px >= x1 and self.x <= x2) or
                 (self.px <= x2 and self.x >= x2) or (self.px <= x1 and self.x >= x1))
                    and ((self.py <= y and self.y >= y)) and (self.py < self.y)) and self.px != 100 and self.goal:  # in shart baraye ine ke age ball raft to sabad
                # True beshe... kolan 3 halat dare 1-ball az bala vared sabad beshe 2- previous coordinate ball az coordinate ball
                # mehrshad inja goal mishe
                goal_sound[R.randint(0, 2)].play()
                self.goal = False
                goals[0] += 1
            self.px, self.py = self.x, self.y
            if self.lock > 0:  # in lock to mode solo ziad jedi nist
                goals[1] += 1
                self.lock -= 1
                self.x -= self.vx  # velocity ball az coordinate ball kam mishe
                self.y -= self.vy  # velocity ball az coordinate ball kam mishe
                self.vx, self.vy = self.gravity(self.vx, self.vy, self.x, self.y)  # inja jazebe ro velocity asar mizare
                self.x = self.test_x(self.x)  # test mishe x az screen nazane biroon
                self.y = self.test_y(self.y)  # test mishe y az screen nazane biroon
                moveSprite(self.sprite, self.x, self.y, True)  # dar akhar toop tekon mikhore
            if self.lock == 0:  # ino nmidonam to solo chera neveshtam vaghti az multi copy kardam ino dasht
                # age didin be dard nmikhore paakesh konin
                self.bool = False
            if self.have:  # to solo hamishe in shart doroste
                self.have = False  # dige dorost nist :/
                self.bool = True  # inam to copy kardan bood age didin be dard nmikhore paakesh konin
                self.lock = ball_animation_frame  # be toop ejaze mide 400 jaye mokhtalef to screen bashe
                showSprite(self.sprite)  # ball shoro be namayesh mikone
                self.x = plx  # plx & ply hamoon coordinate player e
                self.y = ply
                moveSprite(self.sprite, self.x, self.y, True)  # dar akhar toop tekon mikhore

    def goal(self):
        global main_display

    def gravity(self, x, y, b_x, b_y):
        global display_width, display_height
        y -= 0.4  # gravitymoon
        x -= 0.00000001  # ino ghozashtam to line badi (x/x)=0/0 nashe hes raise ghozari nabood :)
        x = (abs(x)-0.03)*(x/abs(x))  # 0.03 kam mikone
        if b_x < 5 or b_x > display_width - 20:
            x = -x * (2/3)
        if b_y < 0 or b_y > 479:  # 480 zamine
            y = -y * (1/2)
        if (b_y > 477) and abs(y) < 0.9:  # age in nabashe ball milarze
            self.y = 479
            y = 0
        return x, y

    def test_x(self, ball_x):
        if ball_x <= 5:
            ball_sound[R.randint(0, 1)].play()
            return 10
        if ball_x >= 1180:
            ball_sound[R.randint(0, 1)].play()
            return 1179
        return ball_x

    def test_y(self, ball_y):
        if ball_y <= 0:
            ball_sound[R.randint(0, 1)].play()
            return 1
        if ball_y >= 480:
            ball_sound[R.randint(0, 1)].play()
            return 479
        return ball_y

    def change(self, x, y):  # vx,vy ro nmishe 2baar avaz kard tabe zadam
        if self.key:
            self.key = False
            self.vx = x
            self.vy = y

    def dell(self):
        for i in ball_solo.All:
            hideSprite(i.sprite)


class dots():
    all_member = []

    def __init__(self, x, y):
        dots.all_member.append(self)
        self.x = x
        self.y = y
        self.sprite = makeSprite(r"Images\dot.png")

    def show():
        for i in dots.all_member:
            moveSprite(i.sprite, i.x, i.y, True)
            showSprite(i.sprite)

    def hide():
        for i in dots.all_member:
            hideSprite(i.sprite)

    def dell():
        for i in dots.all_member:
            hideSprite(i.sprite)
        dots.all_member = []


class toor_solo():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.lx = self.x+5
        self.ly = self.y+75
        self.rx = self.x+80
        self.ry = self.y+75
        self.takhte = self.x + 88
        self.sprite = makeSprite(r"Images\sabad_solo.png")

    def move(self, x, y):
        self.x = x
        self.y = y
        self.lx = self.x+5
        self.ly = self.y+75
        self.rx = self.x+80
        moveSprite(self.sprite, self.x, self.y)
