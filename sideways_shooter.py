import sys
import pygame
import pygame.font
from random import randint
from pygame.sprite import Sprite, Group


class Settings():
    def __init__(self):
        self.score = 0
        
        self.player_name = input("What is your name: ")
        
        if self.player_name.strip().lower() == "steve":
            print("I am sorry. There is a ban on all players named " + self.player_name + ".")
            sys.exit()
        
        with open("sideways_shooter_score.txt", "r") as document:
            self.contents = document.read()
            self.high_score = self.contents[:4].rstrip()
            self.name = self.contents[4:]
    
        pygame.init()
        self.screen = pygame.display.set_mode((1200,800))
        pygame.display.set_caption("Moving Square")
        self.game_active = False
        self.bg_color = (255,0,0)
    
        self.square = Square()
        self.bullets = Group()
        self.play_button = Button(self.screen, "Play", (0,255,0), 48, True)
        self.target = Target()
        self.road_block = RoadBlock(self.screen)
        self.hole = Hole()
        self.moving_road_block = MovingRoadBlock()
        self.blinking_obstacle = BlinkingObstacle(self.screen)
        self.prev_score = False
        
        self.power_up_timer = 2000
        self.power_up_cool_down = 200
        self.stop_shooting = False
        self.move_on = False
        self.bullet_power_on = False
        self.point_power_on = False
        self.reset_power_on = False
        self.power_start = True
        
        self.score_words = Button(self.screen, "Score: 0", (255,0,0),font_size=50, top=10)
        self.prev_score_words = Button(self.screen, "Previous Score: 0", (255,0,0),font_size=50, top=300, prev_score=True)
        self.power_words = Button(self.screen, "Power Up: 3", (100,100,100), font_size=150, top=50, prev_score=True)
        self.rules_words_1 = Button(self.screen, "How to play:", (255,0,0),font_size=30, top=540, prev_score=True)
        self.rules_words_2 = Button(self.screen, "Use the Up and Down arrow keys to move up and down.", (255,0,0),font_size=20, top=575, prev_score=True)
        self.rules_words_3 = Button(self.screen, "Use the Right Arrow key to shoot bullets at the target.", (255,0,0),font_size=20, top=600, prev_score=True)
        self.rules_words_4 = Button(self.screen, "If you hit the target, you will get a point, and the target size will decrease.", (255,0,0),font_size=20, top=625, prev_score=True)
        self.rules_words_5 = Button(self.screen, "If you miss you lose and must try again.", (255,0,0),font_size=20, top=650, prev_score=True)
        self.rules_words_6 = Button(self.screen, "When the target is hit 4 times, a new difficulty will be introduced.", (255,0,0),font_size=20, top=675, prev_score=True)
        self.rules_words_7 = Button(self.screen, "The new difficulty will be shown in black in the top left.", (255,0,0),font_size=20, top=700, prev_score=True)
        self.rules_words_8 = Button(self.screen, "If you hit the very center of the target you will get a temperary power up.", (255,0,0),font_size=20, top=725, prev_score=True)
        self.high_score_words = Button(self.screen, "High Score: " + self.high_score + "   Held by: " + self.name, (255,0,0), font_size=50, top=250, prev_score=True)
        self.bullet_speed_words = Button(self.screen, "Bullet Speed: 4", (255,0,0), top=40)
        self.target_speed_words = Button(self.screen, "Target Speed: 0.5", (255,0,0), top=70)
        self.hole_obstacle_words = Button(self.screen, "Hole Obstacle: Off", (255,0,0), top=100)
        self.hole_moving_words = Button(self.screen, "Hole Obstacle Moving: Off", (255,0,0), top=130)
        self.moving_box_words = Button(self.screen, "Moving Box Obstacle: Off", (255,0,0), top=160)
        self.moving_box_length_words = Button(self.screen, "Moving Box Length: Short", (255,0,0), top=190)
        self.blinking_obstacle_words = Button(self.screen, "Blinking obstacle: Off", (255,0,0), top=220)
        self.square_distance_words = Button(self.screen, "Distance: Close", (255,0,0), top=250)
        self.square_moving_words = Button(self.screen, "Square Moving: Off", (255,0,0), top=280)
    def reset_score(self):
        self.score = 0

class Square():
    def __init__(self):
        self.x = 830
        self.y = 400
        self.moving_up = False
        self.moving_down = False
        self.bullet_speed = 4
        self.square_moving_true = False
        self.direction = 1
        
    def input_move_square(self, event, game_active):
        if event.type == pygame.KEYDOWN and game_active:
            if event.key == pygame.K_UP:
                self.moving_up = True
            if event.key == pygame.K_DOWN:
                self.moving_down = True
                
        if event.type == pygame.KEYUP and game_active:
            if event.key == pygame.K_UP:
                self.moving_up = False
            if event.key == pygame.K_DOWN:
                self.moving_down = False
    
    def move_square(self):
        if self.moving_up and self.y > 0:
            if not self.square_moving_true:
                self.y -= 2
            self.direction = -1
        if self.moving_down and self.y < 750:
            if not self.square_moving_true:
                self.y += 2
            self.direction = 1
            
        if self.square_moving_true:
            if self.y >= 800:
                self.direction = -1
            if self.y <= 0:
                self.direction = 1
            
            self.y += self.direction

class Target():
    def __init__(self):
        self.x = 1120
        self.y_number = 0
        self.y = 0
        self.direction = 1
        self.size = 800
        self.rect = pygame.Rect(self.x, self.y, 50, self.size)
        self.power_rect = pygame.Rect(self.x, self.rect.centery - 2, 50, 4)
        self.speed = 0.5
        self.color = (255,255,255)
        
    def change(self, settings):
        self.size /= 2
        if settings.bullet_power_on or settings.point_power_on:
            self.y_number = randint(0, 750)
            self.size = 100
        self.rect = pygame.Rect(self.x, self.y, 50, self.size)
        
        settings.hole.y = randint(0, 700)
        settings.hole.rect = pygame.Rect(settings.hole.x, settings.hole.y, 50, 100)
        
    def update_target(self, settings):
        if self.rect.bottom >= 800:
            self.direction = -1
        if self.rect.top <= 0:
            self.direction = 1
        
        if self.size <= 50 and not settings.bullet_power_on and not settings.point_power_on and not settings.reset_power_on:
            get_new_difficulty(settings)
        elif self.size <= 50:
            settings.target.new_speed = settings.target.speed
            settings.target.__init__()
            settings.target.speed = settings.target.new_speed
            
        self.y_number += float(self.direction * self.speed)
        self.y = self.y_number
        self.rect = pygame.Rect(self.x, self.y, 50, self.size)
        
        for bullet in settings.bullets:
            if self.rect.top <= bullet.rect.bottom and self.rect.bottom >= bullet.rect.top:
                if self.rect.left <= bullet.rect.right and self.rect.right >= bullet.rect.left:
                    
                    if self.power_rect.top <= bullet.rect.bottom and self.power_rect.bottom >= bullet.rect.top:
                        if not settings.bullet_power_on and not settings.point_power_on and not settings.reset_power_on and self.size != 800:
                            start_power(settings)
                    
                    settings.bullets.remove(bullet)
                    if settings.point_power_on:
                        settings.score += 5
                    else:
                        settings.score += 1
                    settings.score_words.prep_msg("Score: " + str(settings.score))
                    self.change(settings)
        
    def draw_target(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
        self.power_rect = pygame.Rect(self.x, self.rect.centery - 2, 50, 4)

class Bullet(Sprite):
    def __init__(self, screen, square):
        super(Bullet, self).__init__()
        self.screen = screen
        
        self.rect = pygame.Rect(0, 0, 20, 10)
        self.rect.centery = square.y + 25
        self.rect.right = square.x + 50
        
    def update(self, settings):
        self.rect.centerx += settings.square.bullet_speed
        
    def draw_bullet(self, settings):
        pygame.draw.rect(self.screen, (0,255,0), self.rect)
        
class Button():
    def __init__(self, screen, msg, bg_color, font_size=20, button=False, top=0, prev_score=False, color=(255,255,255)):
        """initialize button attributes"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.button = button
        self.prev_score = prev_score
        
        #Set the dimensions and properties of the button
        self.width, self.height = 200, 50
        self.button_color = bg_color
        self.text_color = color
        self.font = pygame.font.SysFont(None,font_size)
        
        #Build the button's rect object and center it.
        self.rect = pygame.Rect(0,0, self.width, self.height)
        self.rect.left = 10
        self.rect.top = top
        if self.prev_score:
            self.rect.center = self.screen_rect.center
            self.rect.top = top
        if self.button:
            self.rect.center = self.screen_rect.center
        
        #The button message needs to be prepped only once.
        self.prep_msg(msg)
        
    def prep_msg(self, msg):
        """Turn msg into a rendered image and center text on the button"""
        
        self.msg = msg
        self.msg_image = self.font.render(msg, True, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
        if not self.button:
            self.msg_image_rect.centery = self.rect.centery - 10
        
    def draw_button(self):
        #Draw blank button and then draw message.
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        
    def check_button(self, game_active):
        if self.button:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            button_clicked = self.rect.collidepoint(mouse_x, mouse_y)
            if button_clicked and not game_active:
                game_active = True
                return game_active

class RoadBlock():
    def __init__(self, screen):
        self.x = 980
        self.y = 0
        self.rect = pygame.Rect(self.x, self.y, 50, 800)
    def draw_road_block(self, screen, hole):
        if hole.true:
            pygame.draw.rect(screen, (0,0,0), self.rect)
        
class Hole():
    def __init__(self):
        self.x = 980
        self.y_holder = randint(0,700)
        self.y = self.y_holder
        self.rect = pygame.Rect(self.x, self.y, 50, 100)
        self.true = False
        self.moving_true = False
        self.direction = 1
        
    def draw_hole(self, screen, bullets, road_block, target, square, settings):
        if self.moving_true:
            if self.rect.bottom >= 800:
                self.direction = -1
            elif self.rect.top <= 0:
                self.direction = 1
            self.y_holder += float(0.25 * self.direction)
            self.y = self.y_holder
            self.rect = pygame.Rect(self.x, self.y, 50, 100)
        if self.true:
            pygame.draw.rect(screen, settings.bg_color, self.rect)
    
class MovingRoadBlock():
    def __init__(self):
        self.x = 910
        self.y_number = randint(0,750)
        self.y = self.y_number
        self.length = 50
        self.rect = pygame.Rect(self.x, self.y, 50, self.length)
        self.true = False
        self.direction = 1
        self.speed = 0.5
        
    def draw_moving_road_block(self, screen):
        if self.true:
            pygame.draw.rect(screen, (0,0,0), self.rect)
            
    def update_moving_road_block(self):
        if self.rect.bottom >= 800:
            self.direction = -1
        if self.rect.top <= 0:
            self.direction = 1
        
        if self.true:
            self.y_number += float(self.direction * self.speed)
            self.y = self.y_number
            self.rect = pygame.Rect(self.x, self.y, 50, self.length)

class BlinkingObstacle():
    def __init__(self, screen):
        self.x = 1050
        self.y = 0
        self.screen = screen
        self.rect = pygame.Rect(self.x, self.y, 50, 800)
        self.true = False
        self.timer = 600
        self.on = True
        
    def draw_blinking_obstacle(self):
        if self.true:
            self.timer -= 1
            if self.timer <= 0:
                if self.on:
                    self.on = False
                elif not self.on:
                    self.on = True
                self.timer = 600
            if self.on:
                pygame.draw.rect(self.screen, (0,0,0), self.rect)

def start_power(settings):
    settings.power_start = True
    n = randint(1,3)
    if n == 1:
        turn_off_obstacles_for_power(settings)
        settings.bullet_power_on = True
    elif n == 2:
        turn_off_obstacles_for_power(settings)
        settings.point_power_on = True
    elif n == 3:
        settings.reset_power_on = True

def turn_off_obstacles_for_power(settings):
    if settings.moving_road_block.true:
        settings.moving_road_block.true_holder = True
        settings.moving_road_block.true = False
    else :
        settings.moving_road_block.true_holder = False
    if settings.hole.true:
        settings.hole.true_holder = True
        settings.hole.true = False
    else:
        settings.hole.true_holder = False
    if settings.blinking_obstacle.true:
        settings.blinking_obstacle.true_holder = True
        settings.blinking_obstacle.true = False
    else:
        settings.blinking_obstacle.true_holder = False

def turn_on_obstacles_after_power(settings):
    if settings.moving_road_block.true_holder:
        settings.moving_road_block.true_holder = False
        settings.moving_road_block.true = True
    if settings.hole.true_holder:
        settings.hole.true_holder = False
        settings.hole.true = True
    if settings.blinking_obstacle.true_holder:
        settings.blinking_obstacle.true_holder = False
        settings.blinking_obstacle.true = True

def draw_point_power(settings):
    if settings.point_power_on:
        if settings.power_start:
            settings.move_on = False
            settings.power_up_timer = 2000
            settings.power_up_cool_down = 200
            settings.power_start = False
            
        settings.power_words.draw_button()
        settings.target.color = (0,255,0)
        settings.bg_color = (100,100,100)
        update_word_colors(settings)
        
        if settings.power_up_timer <= 2000:
            settings.power_words.prep_msg("X5 Points: 5")
        if settings.power_up_timer < 1600:
            settings.power_words.prep_msg("X5 Points: 4")
        if settings.power_up_timer < 1200:
            settings.power_words.prep_msg("X5 Points: 3")
        if settings.power_up_timer < 800:
            settings.power_words.prep_msg("X5 Points: 2")
        if settings.power_up_timer < 400:
            settings.power_words.prep_msg("X5 Points: 1")
            
        settings.power_up_timer -= 1
        settings.move_on = False
        if settings.power_up_timer <= 0:
            settings.power_up_timer = 1500
            settings.move_on = True
            
        if settings.move_on:
            settings.point_power_on = False
            settings.move_on = False
            settings.stop_shooting = False
            settings.power_up_timer = 1500
            settings.power_up_cool_down = 200
            settings.power_start = True
            turn_on_obstacles_after_power(settings)
            settings.bg_color = (255,0,0)
            update_word_colors(settings)
    else:
        settings.target.color = (255,255,255)

def draw_bullet_power(settings):
    if settings.bullet_power_on:
        
        settings.power_words.draw_button()
        
        settings.bg_color = (100,100,100)
        update_word_colors(settings)
        if settings.power_start:
            
            settings.move_on = False
            settings.stop_shooting = False
            settings.power_up_timer = 2000
            settings.power_up_cool_down = 200
            settings.power_start = False
        if not settings.stop_shooting:
            
            if settings.power_up_timer <= 2000:
                settings.power_words.prep_msg("Rapid Fire: 5")
            if settings.power_up_timer < 1600:
                settings.power_words.prep_msg("Rapid Fire: 4")
            if settings.power_up_timer < 1200:
                settings.power_words.prep_msg("Rapid Fire: 3")
            if settings.power_up_timer < 800:
                settings.power_words.prep_msg("Rapid Fire: 2")
            if settings.power_up_timer < 400:
                settings.power_words.prep_msg("Rapid Fire: 1")
            
            settings.power_up_timer -= 1
            settings.move_on = False
            if settings.power_up_timer <= 0:
                settings.power_up_timer = 1500
                settings.move_on = True
                settings.stop_shooting = True
                settings.power_up_cool_down = 200
            
            if settings.power_up_timer % 25 == 0:
                new_bullet = Bullet(settings.screen, settings.square)
                settings.bullets.add(new_bullet)
            
        if settings.move_on:
            settings.power_up_cool_down -= 1
            if settings.power_up_cool_down <= 0:
                settings.bullet_power_on = False
                settings.move_on = False
                settings.stop_shooting = False
                settings.power_up_timer = 1500
                settings.power_up_cool_down = 200
                settings.power_start = True
                turn_on_obstacles_after_power(settings)
                settings.bg_color = (255,0,0)
                update_word_colors(settings)

def draw_reset_power(settings):
    if settings.reset_power_on:
        if settings.power_start:
            update_word_colors(settings)
            settings.target.__init__()
            settings.square.__init__()
            settings.hole.__init__()
            settings.road_block.__init__(settings.screen)
            settings.blinking_obstacle.__init__(settings.screen)
            settings.moving_road_block.__init__()
            settings.bullet_speed_words.prep_msg("Bullet Speed: 4")
            settings.target_speed_words.prep_msg("Target Speed: 0.5")
            settings.hole_obstacle_words.prep_msg("Hole Obstacle: Off")
            settings.hole_moving_words.prep_msg("Hole Moving: Off")
            settings.moving_box_words.prep_msg("Moving Box Obstacle: Off")
            settings.blinking_obstacle_words.prep_msg("Blinking Obstacle: Off")
            settings.square_distance_words.prep_msg("Distance: Close")
            settings.square_moving_words.prep_msg("Square Moving: Off")
            
            settings.move_on = False
            settings.power_up_timer = 1000
            settings.power_start = False
        
        settings.power_words.prep_msg("Reset Power!")
        settings.power_words.draw_button()
        settings.bg_color = (100,100,100)
        update_word_colors(settings)
        
            
        settings.power_up_timer -= 1
        settings.move_on = False
        if settings.power_up_timer <= 0:
            settings.power_up_timer = 2000
            settings.move_on = True
            
        if settings.move_on:
            settings.reset_power_on = False
            settings.move_on = False
            settings.power_up_timer = 2000
            settings.power_start = True
            settings.bg_color = (255,0,0)
            update_word_colors(settings)

def make_high_score(settings):
    with open("sideways_shooter_score.txt", "r") as document:
        contents = document.read()
        high_score = contents[:4].rstrip()
        name = contents[4:]
        if settings.score > int(high_score):
            settings.high_score_words.prep_msg("High Score: " + str(settings.score) + "   Held By: " + settings.player_name)
            with open("sideways_shooter_score.txt", "w") as document:
                if settings.score < 10:
                    document.write(str(settings.score) + "   " + settings.player_name)
                elif settings.score < 100:
                    document.write(str(settings.score) + "  " + settings.player_name)
                elif settings.score < 1000:
                    document.write(str(settings.score) + " " + settings.player_name)
                elif settings.score < 10000:
                    document.write(str(settings.score) + settings.player_name)

def get_new_difficulty(settings):
    searching_for_number = True
    while searching_for_number:
        n = randint(0,6)
        searching_for_number = False
        if settings.square.x <= 30 and n == 1:
            searching_for_number = True
        if settings.hole.true and settings.hole.moving_true and n == 2:
            searching_for_number = True
        if settings.moving_road_block.true and settings.moving_road_block.length >= 400 and n == 3:
            searching_for_number = True
        if settings.square.bullet_speed <= 1 and n == 4:
            searching_for_number = True
        if settings.square.square_moving_true and n == 5:
            searching_for_number = True
        if settings.blinking_obstacle.true and n == 6:
            searching_for_number = True
            
    if n == 0:
        settings.target.new_speed = settings.target.speed * 2
        settings.target.__init__()
        settings.target.speed = settings.target.new_speed
        
        update_word_colors(settings)
        settings.target_speed_words.text_color = (0,0,0)
        settings.target_speed_words.prep_msg("Target Speed: " + str(settings.target.speed))
                
    elif n == 1:
        settings.square.x -= 200
        update_word_colors(settings)
        settings.square_distance_words.text_color = (0,0,0)
                
        if settings.square.x == 630:
            settings.square_distance_words.prep_msg("Distance: Medium")
        if settings.square.x == 430:
            settings.square_distance_words.prep_msg("Distance: Far")
        if settings.square.x == 230:
            settings.square_distance_words.prep_msg("Distance: Really Far")
        if settings.square.x == 30:
            settings.square_distance_words.prep_msg("Distance: Unbelievably Far")
        speed_holder = settings.target.speed
        settings.target.__init__()
        settings.target.speed = speed_holder

    elif n == 2:
        if not settings.hole.true:
            settings.hole.true = True
                    
            update_word_colors(settings)
            settings.hole_obstacle_words.text_color = (0,0,0)
            settings.hole_obstacle_words.prep_msg("Hole Obstace: On")
                
        elif not settings.hole.moving_true:
            settings.hole.moving_true = True
                    
            update_word_colors(settings)
            settings.hole_moving_words.text_color = (0,0,0)
            settings.hole_moving_words.prep_msg("Hole Obstacle Moving: On")
                    
        settings.target.new_speed = settings.target.speed
        settings.target.__init__()
        settings.target.speed = settings.target.new_speed

    elif n == 3:
        if not settings.moving_road_block.true:
            settings.moving_road_block.true = True
            
            update_word_colors(settings)
            settings.moving_box_words.text_color = (0,0,0)
            settings.moving_box_words.prep_msg("Moving Box Obstacle: On")
        else:
            settings.moving_road_block.length *= 2
                    
            update_word_colors(settings)
            settings.moving_box_length_words.text_color = (0,0,0)
            
            if settings.moving_road_block.length == 100:
                settings.moving_box_length_words.prep_msg("Moving Box Length: Medium")
            if settings.moving_road_block.length == 200:
                settings.moving_box_length_words.prep_msg("Moving Box Length: Large")
            if settings.moving_road_block.length == 400:
                settings.moving_box_length_words.prep_msg("Moving Box Length: Huge")
                    
        settings.target.new_speed = settings.target.speed
        settings.target.__init__()
        settings.target.speed = settings.target.new_speed
                
    elif n == 4:
        settings.square.bullet_speed -= 1
        update_word_colors(settings)
                
        settings.bullet_speed_words.text_color = (0,0,0)
        settings.bullet_speed_words.prep_msg("Bullet Speed: " + str(settings.square.bullet_speed))
                
        settings.target.new_speed = settings.target.speed
        settings.target.__init__()
        settings.target.speed = settings.target.new_speed
        
    elif n == 5:
        settings.square.square_moving_true = True
        update_word_colors(settings)
        
        settings.square_moving_words.text_color = (0,0,0)
        settings.square_moving_words.prep_msg("Square Moving: On")
        
        settings.target.new_speed = settings.target.speed
        settings.target.__init__()
        settings.target.speed = settings.target.new_speed
        
    elif n == 6:
        settings.blinking_obstacle.true = True
        
        update_word_colors(settings)
        
        settings.blinking_obstacle_words.text_color = (0,0,0)
        settings.blinking_obstacle_words.prep_msg("Blinking Obstacle: On")
        
        settings.target.new_speed = settings.target.speed
        settings.target.__init__()
        settings.target.speed = settings.target.new_speed

def update_word_colors(settings):
    settings.bullet_speed_words.text_color = (255,255,255)
    settings.target_speed_words.text_color = (255,255,255)
    settings.hole_obstacle_words.text_color = (255,255,255)
    settings.hole_moving_words.text_color = (255,255,255)
    settings.moving_box_words.text_color = (255,255,255)
    settings.moving_box_length_words.text_color = (255,255,255)
    settings.blinking_obstacle_words.text_color = (255,255,255)
    settings.square_distance_words.text_color = (255,255,255)
    settings.square_moving_words.text_color = (255,255,255)
    
    settings.score_words.button_color = settings.bg_color
    settings.bullet_speed_words.button_color = settings.bg_color
    settings.target_speed_words.button_color = settings.bg_color
    settings.hole_obstacle_words.button_color = settings.bg_color
    settings.hole_moving_words.button_color = settings.bg_color
    settings.square_distance_words.button_color = settings.bg_color
    settings.moving_box_words.button_color = settings.bg_color
    settings.blinking_obstacle_words.button_color = settings.bg_color
    settings.moving_box_length_words.button_color = settings.bg_color
    settings.square_moving_words.button_color = settings.bg_color
                
    settings.score_words.prep_msg(settings.score_words.msg)
    settings.bullet_speed_words.prep_msg(settings.bullet_speed_words.msg)
    settings.target_speed_words.prep_msg(settings.target_speed_words.msg)
    settings.hole_obstacle_words.prep_msg(settings.hole_obstacle_words.msg)
    settings.hole_moving_words.prep_msg(settings.hole_moving_words.msg)
    settings.square_distance_words.prep_msg(settings.square_distance_words.msg)
    settings.moving_box_words.prep_msg(settings.moving_box_words.msg)
    settings.blinking_obstacle_words.prep_msg(settings.blinking_obstacle_words.msg)
    settings.moving_box_length_words.prep_msg(settings.moving_box_length_words.msg)
    settings.square_moving_words.prep_msg(settings.square_moving_words.msg)

def end_game(settings, bullet):
    settings.bg_color = (255,0,0)
    update_word_colors(settings)
    settings.power_up_timer = 1500
    settings.power_up_cool_down = 200
    settings.stop_shooting = False
    settings.move_on = False
    settings.bullet_power_on = False
    settings.point_power_on = False
    settings.bullets.remove(bullet)
    settings.game_active = False
    settings.target.__init__()
    settings.square.__init__()
    settings.hole.__init__()
    settings.road_block.__init__(settings.screen)
    settings.blinking_obstacle.__init__(settings.screen)
    settings.moving_road_block.__init__()
    print("Score: " + str(settings.score))
    settings.prev_score_words.prep_msg("Previous Score: " + str(settings.score))
    make_high_score(settings)
    settings.reset_score()
    settings.bullet_speed_words.text_color = (255,255,255)
    settings.target_speed_words.text_color = (255,255,255)
    settings.hole_obstacle_words.text_color = (255,255,255)
    settings.hole_moving_words.text_color = (255,255,255)
    settings.moving_box_words.text_color = (255,255,255)
    settings.blinking_obstacle_words.text_color = (255,255,255)
    settings.square_distance_words.text_color = (255,255,255)
    settings.square_moving_words.text_color = (255,255,255)
    settings.score_words.prep_msg("Score: 0") 
    settings.bullet_speed_words.prep_msg("Bullet Speed: 4")
    settings.target_speed_words.prep_msg("Target Speed: 0.5")
    settings.hole_obstacle_words.prep_msg("Hole Obstacle: Off")
    settings.hole_moving_words.prep_msg("Hole Moving: Off")
    settings.moving_box_words.prep_msg("Moving Box Obstacle: Off")
    settings.blinking_obstacle_words.prep_msg("Blinking Obstacle: Off")
    settings.square_distance_words.prep_msg("Distance: Close")
    settings.square_moving_words.prep_msg("Square Moving: Off")

def check_for_bullet_collisions(settings):
    for bullet in settings.bullets:
        if bullet.rect.left >= 1220:
            settings.bullets.remove(bullet)
            if not settings.bullet_power_on:
                end_game(settings, bullet)
                    
        if settings.hole.true:
            if settings.hole.rect.top > bullet.rect.top or settings.hole.rect.bottom < bullet.rect.bottom:
                if settings.hole.rect.left <= bullet.rect.right and settings.hole.rect.right >= bullet.rect.left:
                    settings.bullets.remove(bullet)
                    if not settings.bullet_power_on:
                        end_game(settings, bullet)
                            
        if settings.moving_road_block.true:
            if settings.moving_road_block.rect.top <= bullet.rect.bottom and settings.moving_road_block.rect.bottom >= bullet.rect.top:
                if settings.moving_road_block.rect.left <= bullet.rect.right and settings.moving_road_block.rect.right >= bullet.rect.left:
                    settings.bullets.remove(bullet)
                    if not settings.bullet_power_on:
                        end_game(settings, bullet)
                    
        if settings.blinking_obstacle.true and settings.blinking_obstacle.on:
            if settings.blinking_obstacle.rect.top <= bullet.rect.bottom and settings.blinking_obstacle.rect.bottom >= bullet.rect.top:
                if settings.blinking_obstacle.rect.left <= bullet.rect.right and settings.blinking_obstacle.rect.right >= bullet.rect.left:
                    settings.bullets.remove(bullet)
                    if not settings.bullet_power_on:
                        end_game(settings, bullet)
        
        bullet.update(settings)
        bullet.draw_bullet(settings)
    draw_point_power(settings)
    draw_bullet_power(settings)
    draw_reset_power(settings)

def active_game_loop(settings):
    pygame.mouse.set_visible(False)
    settings.prev_score = True
    settings.square.move_square()
    
    settings.score_words.draw_button()
    settings.bullet_speed_words.draw_button()
    settings.target_speed_words.draw_button()
    settings.hole_obstacle_words.draw_button()
    settings.hole_moving_words.draw_button()
    settings.moving_box_words.draw_button()
    settings.moving_box_length_words.draw_button()
    settings.blinking_obstacle_words.draw_button()
    settings.square_distance_words.draw_button()
    settings.square_moving_words.draw_button()
    
    settings.target.update_target(settings)
    settings.target.draw_target(settings.screen)
    pygame.draw.rect(settings.screen, (0,0,255), (settings.square.x , settings.square.y , 50,50))
    settings.road_block.draw_road_block(settings.screen, settings.hole)
    settings.hole.draw_hole(settings.screen, settings.bullets, settings.road_block, settings.target, settings.square, settings)
    settings.moving_road_block.update_moving_road_block()
    settings.moving_road_block.draw_moving_road_block(settings.screen)
    settings.blinking_obstacle.draw_blinking_obstacle()
            
    check_for_bullet_collisions(settings)

def non_active_game_loop(settings):
    pygame.mouse.set_visible(True)
    if settings.prev_score:
        settings.prev_score_words.draw_button()
        
    settings.high_score_words.draw_button()
    settings.play_button.draw_button()
    
    settings.rules_words_1.draw_button()
    settings.rules_words_2.draw_button()
    settings.rules_words_3.draw_button()
    settings.rules_words_4.draw_button()
    settings.rules_words_5.draw_button()
    settings.rules_words_6.draw_button()
    settings.rules_words_7.draw_button()
    settings.rules_words_8.draw_button()

def check_for_input(settings):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            settings.game_active = settings.play_button.check_button(settings.game_active)
        if event.type == pygame.KEYDOWN and settings.game_active:
            if event.key == pygame.K_RIGHT and len(settings.bullets) == 0 and not settings.reset_power_on:
                new_bullet = Bullet(settings.screen, settings.square)
                settings.bullets.add(new_bullet)
    
        settings.square.input_move_square(event, settings.game_active)

def run_game():
    settings = Settings()
        
    while True:
        settings.screen.fill(settings.bg_color)
        check_for_input(settings)
        
        if settings.game_active:
            active_game_loop(settings)
            
        else:
            non_active_game_loop(settings)
        pygame.display.flip()

run_game()

