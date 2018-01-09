# import
import pygame
import sys
import time
import random
import math

pygame.init()

# init clock
clock = pygame.time.Clock()

# screen
screen = pygame.display.set_mode([640, 359])

# background
background = pygame.Surface(screen.get_size())
bg_image = pygame.image.load('background.jpg')
background.blit(bg_image, [0, 0])


# class
class Ball(pygame.sprite.Sprite):
    def __init__(self, image_file, speed, angle, location):
        self.radius = 6
        pygame.sprite.Sprite.__init__(self)
        surface = pygame.Surface([12, 12])
        surface.set_colorkey([0, 0, 0])
        pygame.draw.circle(surface, [0, 0, 255], (surface.get_rect().centerx, surface.get_rect().centery), 6)
        # self.image = pygame.image.load('ball.jpg')
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.speed = speed
        self.angle = angle
        self.released = False

    # move one step

    def move(self):
        # test edges
        if self.rect.left <= screen.get_rect().left or \
                        self.rect.right >= screen.get_rect().right:
            # self.speed[0] = -self.speed[0]
            self.angle = math.pi - self.angle
            hit_sound.play()

        # test top
        if self.rect.top <= screen.get_rect().top:
            # self.speed[1] = -self.speed[1]
            self.angle = math.pi * 2 - self.angle
            hit_sound.play()
        newpos = self.rect.move((int(self.speed * math.cos(self.angle)), int(self.speed * math.sin(self.angle))))
        self.rect = newpos


class Paddle(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        image_surface = pygame.surface.Surface([100, 20])
        image_surface.fill([0, 0, 0])

        self.image = pygame.image.load('paddle.png')
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class PaddleSide(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        surface = pygame.Surface([20, 20])
        surface.set_colorkey((0, 0, 0))
        pygame.draw.circle(surface, (255, 0, 0), (surface.get_rect().centerx, surface.get_rect().centery), int(surface.get_height()/2))
        # self.image = pygame.image.load('ball.jpg')
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.centerx, self.rect.centery = location
        self.radius = 10


class MyBrickClass(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('brick.jpg')

        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location


class SpeedUp(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        surface = pygame.Surface([15, 15])
        surface.fill([0, 0, 0])
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.name = 'speed_up'

    def move(self):
        newpos = self.rect.move((0, 5))
        self.rect = newpos


class SlowDown(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        surface = pygame.Surface([15, 15])
        surface.fill([255, 255, 255])
        self.image = surface
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.name = 'slow_down'

    def move(self):
        newpos = self.rect.move((0, 5))
        self.rect = newpos


pygame.display.flip()

hit_sound = pygame.mixer.Sound('punch.wav')
hit_sound.set_volume(0.5)

pygame.time.set_timer(pygame.USEREVENT + 1, 5000)

items = pygame.sprite.Group()


def generate_item():
    left = random.randint(0, 600)
    choice = random.choice([1, 2])
    if choice == 1:
        item = SpeedUp((left, 0))
        items.add(item)
    else:
        item = SlowDown((left, 0))
        items.add(item)


def slow_down():
    my_ball.speed = my_ball.speed / 1.5


# object
my_ball = Ball('ball.jpg', 5, math.pi * 1.5, pygame.mouse.get_pos())
# ball_group = pygame.sprite.Group()
# ball_group.add(my_ball)

paddle = Paddle([(640 - 100) / 2, 480 - 135])
left_paddle_side = PaddleSide((paddle.rect.left - 15, paddle.rect.centery))
right_paddle_side = PaddleSide((paddle.rect.left+115, paddle.rect.centery))


paddle_sides = pygame.sprite.Group()
paddle_sides.add(left_paddle_side)
paddle_sides.add(right_paddle_side)


bricks = pygame.sprite.Group()
for row in range(0, 4):
    for column in range(0, 10):
        location = [column * 60 + 10, row * 20 + 10]

        brick = MyBrickClass(location)
        bricks.add(brick)


# score
score = 0

# lives
lives = 3


# animate of every step
def animate():
    global score
    global lives

    screen.blit(background, (0, 0))

    # move ball one step
    my_ball.move()

    # move item
    for item in items:
        item.move()
        screen.blit(item.image, item.rect)

    # detect collision with items
    coll_items = pygame.sprite.spritecollide(paddle, items, True)
    for item in coll_items:
        if item.name == 'speed_up':
            my_ball.speed *= 1.5
        elif item.name == 'slow_down':
            my_ball.speed /= 1.5
    # detect collusion
    if pygame.sprite.collide_rect(paddle, my_ball):
        # my_ball.speed[1] = -my_ball.speed[1]
        my_ball.angle = math.pi * 2 - my_ball.angle
        #score = score + 1
        hit_sound.play()

    # detect hit paddle_side
    side = pygame.sprite.spritecollide(my_ball, paddle_sides, False, collided=pygame.sprite.collide_circle)
    if side:
        side = side[0]
        collision_angle = math.acos((side.rect.centerx - my_ball.rect.centerx) / (side.radius + my_ball.radius))
        my_ball.angle = collision_angle * 2 - my_ball.angle + math.pi
        hit_sound.play()

    # if pygame.sprite.collide_circle(my_ball, left_paddle_side):
    #     collision_angle = math.acos((left_paddle_side.rect.centerx - my_ball.rect.centerx) / (left_paddle_side.radius + my_ball.radius))
    #     my_ball.angle = collision_angle * 2 - my_ball.angle + math.pi

    # detect ball lost
    if my_ball.rect.top > screen.get_rect().bottom:
        lives = lives - 1
        pygame.time.delay(2000)
        my_ball.rect.left, my_ball.rect.top = pygame.mouse.get_pos()
        my_ball.angle = math.pi * 1.5
        my_ball.released = False

    # check hit
    if pygame.sprite.spritecollide(my_ball, bricks, True):
        score += 1
        # my_ball.speed[1] = -my_ball.speed[1]
        my_ball.angle = math.pi * 2 - my_ball.angle
        hit_sound.play()

    screen.blit(my_ball.image, my_ball.rect)
    screen.blit(paddle.image, paddle.rect)
    screen.blit(left_paddle_side.image, left_paddle_side.rect)
    screen.blit(right_paddle_side.image, right_paddle_side.rect)
    for brick in bricks:
        screen.blit(brick.image, brick.rect)

    # draw score
    font = pygame.font.Font(None, 25)
    score_text = font.render("score: %s" % score, 1, [255, 255, 255])
    text_pos = [10, 340]
    screen.blit(score_text, text_pos)

    # draw lives
    font = pygame.font.Font(None, 25)
    lives_text = font.render("lives:", 1, [255, 255, 255])
    screen.blit(lives_text, [550, 340])
    for i in range(lives):
        screen.blit(my_ball.image, [640 - 20 * i, 340])

    pygame.display.flip()

    pass


# main loop
running = True
released = False
while running:

    # process event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEMOTION:
            paddle.rect.centerx = event.pos[0]
            left_paddle_side.rect.centerx = paddle.rect.left - 15
            right_paddle_side.rect.centerx = paddle.rect.left + 115

            if not my_ball.released:
                my_ball.rect.centerx = event.pos[0]
        elif event.type == pygame.USEREVENT + 1:
            generate_item()

    if pygame.mouse.get_pressed()[0]:
        my_ball.released = True

    if not my_ball.released:
        my_ball.rect.centery = screen.get_height() - 20

    if lives == 0 or score == 40:
        screen.blit(background, [0, 0])

        gameover_font = pygame.font.Font(None, 70)
        gameover_text = gameover_font.render("GAME OVER", 1, [0, 0, 0])

        score_font = pygame.font.Font(None, 50)
        score_text = score_font.render("SCORE %d" % score, 1, [0, 0, 0])

        width = screen.get_width()
        screen.blit(gameover_text, [(width - gameover_text.get_width()) / 2, 100])
        screen.blit(score_text, [(width - score_text.get_width()) / 2, 200])

        pygame.display.flip()
    else:
        animate()

    clock.tick(30)

# exit program
pygame.quit()
sys.exit()
