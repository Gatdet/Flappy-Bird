import random

import pygame



pygame.init()
clock = pygame.time.Clock()
fps = 60
screen = pygame.display.set_mode((470, 685))

bird_flap = pygame.mixer.Sound("Flap_sound.mp3")
bird_flap.set_volume(0.4)
bird_collision = pygame.mixer.Sound("collision_sound.mp3")
bird_collision.set_volume(0.4)


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) #allows us to inherit functinallity
        fly_straight = pygame.image.load("bird_straight.png")
        fly_up = pygame.image.load("bird_up.png")
        fly_down = pygame.image.load("bird_down.png")

        self.flying_motion = [fly_straight, fly_up, fly_down]
        self.index = 0 #will tell which image is showing
        self.image = self.flying_motion[self.index]
        self.rect = self.image.get_rect(center = (100,342)) #creates boundaries around image
        self.gravity = 0
        self.add_gravity = 0.7
        self.pressed = False


    def apply_gravity(self):
        self.rect.y+=self.gravity
        self.gravity += self.add_gravity
        if self.rect.bottom >= 590:  # if the bird hits the bottom
            self.add_gravity = 0
            self.gravity = 0
            self.rect.y = 560


    def animations(self):
        self.index+=0.1
        if self.index >=len(self.flying_motion):
            self.index=0
        self.image = self.flying_motion[int(self.index)]
        self.image = pygame.transform.rotate(self.flying_motion[int(self.index)], self.gravity*-2) #this makes the bird rotate

    def collision(self):
        pass

    def update(self):
        self.animations()
        self.apply_gravity()

#Sprites
bird_group = pygame.sprite.Group()# will keep count of the sprits I add
bird= Bird()
bird_group.add(bird) #adding to the sprite to the group


class Pipe(pygame.sprite.Sprite):
    def __init__(self, position,y):
        pygame.sprite.Sprite.__init__(self)  # allows us to inherit functinallity
        self.scroll_speed = 4
        self.image = pygame.image.load("pipe.png")
        self.rect = self.image.get_rect(topleft=(370, 430))

        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True) #flip the image
            self.rect.bottomleft = (500,y) #spawn at top      #range  50-530
        if position == -1:
            self.rect.topleft= (500,y+165) #spawn at bottom       #range  50-530     #keep 160 space in between


    def movement(self):
        self.rect.x -= self.scroll_speed
        if self.rect.x <= -200: #this makes the bottom move
            self.kill()

    def update(self):
        self.movement()

#Sprite/Timer
pipe_group = (pygame.sprite.Group())
spawn_pipe = pygame.USEREVENT +1
pygame.time.set_timer(spawn_pipe, 1300)

#Button
button = pygame.image.load("restart.png")
button_rect = button.get_rect(topleft = (180, 200))



#title and icon
pygame.display.set_caption("Flappy Birds")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)

#background/floor
background = pygame.image.load("background.png")
floor = pygame.image.load("ground.png")
ground_scroll = 0
scroll_speed = 4


#bird
fly_straight = pygame.image.load("bird_up.png")
fly_up = pygame.image.load("bird_up.png")
fly_down = pygame.image.load("bird_down.png")
flying_motion = [fly_straight,fly_up,fly_down]
flying_index =0
flying = flying_motion[flying_index]
flying_rect = flying.get_rect(center = (100,342))

#Score
counter = 0
score_font = pygame.font.SysFont("impact", 80)
score = score_font.render(f"{counter}", True, "White")
score_sound = pygame.mixer.Sound("score_sound.mp3")     #audio for score
score_sound.set_volume(0.4)

def Score():
    global counter, score

    if len(pipe_group)>0:
        if pipe_group.sprites()[0].rect.x == -4:
            counter+=1
            score_sound.play()
    score = score_font.render(f"{counter}", True, "White")

    screen.blit(score, (210,50))

def collisions():
    global game_active, pressed, scroll_speed

    if pygame.sprite.groupcollide(bird_group,pipe_group, False, False):     #pygame.sprite.spritecollide(bird, pipe_group, False):    #if the bird hits the pipe
        game_active = False
        pressed = True   #stop the player from interupting the collision
        bird.apply_gravity()
        bird_collision.play()


    if bird.rect.top<=-400:     #if the bird goes too high off the screen
        game_active = False
        bird_collision.play()

def start_game():
    global game_active, bird, running

    if game_active == None:
        screen.blit(background, (0, 0))  # showing background on screen
        bird_group.draw(screen)
        bird.animations()
        screen.blit(floor, (ground_scroll, 600))
        Score()



        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key== pygame.K_SPACE:
                    game_active = True
                    bird.gravity -=10
                    bird_flap.play()
            if event.type == pygame.QUIT:
                running = False

pressed = False     #check if the space bar is pressed
clicked = False     #check if the mouse is clicked
num = random.randint(50,580)    #generates a random number so the pipe can have random spawn heights
game_active = None  #starts out with 'NONE' so that the game isnt started or ended yet

running = True
while running:

    pos = pygame.mouse.get_pos()    #get the current mouse pos the entire game so dont put in game_active loop
    #Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running=False

        #Game Active
        if game_active:
            if event.type == pygame.KEYDOWN and pressed == False:
                if event.key== pygame.K_SPACE:
                    bird.gravity =-10
                    pressed = True
                    bird_flap.play()

            if event.type== pygame.KEYUP and pressed==True:
                pressed= False

            if event.type == spawn_pipe:
                num = random.randint(50, 400)
                btm_pipe = Pipe(-1, num)
                top_pipe = Pipe(1, num)
                pipe_group.add(btm_pipe, top_pipe)

    #if game_active == None:
    start_game()

    #Game Active
    if game_active:
        #Blits/Draw/Update
        screen.blit(background,(0,0)) #showing background on screen
        pipe_group.draw(screen)
        pipe_group.update()
        bird_group.draw(screen)
        bird_group.update()
        screen.blit(floor,(ground_scroll,600)) #showing bottom on screen
        ground_scroll -= scroll_speed  #making the background move

        Score()
        collisions()

        #Scroll/End
        if abs(ground_scroll) > 35: #this makes the bottom move
            ground_scroll = 0 #this loops the bottom image

        if bird.rect.bottom>=590:
            scroll_speed=0
            game_active=False
            bird.rect.y= 560
            bird_collision.play()
        else:
            scroll_speed = 4

    if game_active == False:
        screen.blit(background, (0, 0))
        bird.apply_gravity()
        pipe_group.draw(screen)
        screen.blit(floor, (ground_scroll, 600))
        bird_group.draw(screen)
        Score()

        if bird.rect.bottom>=590:
            screen.blit(button,button_rect)
            if pygame.mouse.get_pressed()[0] == 0:
                clicked = False
            if button_rect.collidepoint(pos):
                if pygame.mouse.get_pressed()[0]==1 and clicked ==False:
                    clicked = True
                    game_active = None
                    pipe_group.empty()
                    bird.rect.y = 342
                    counter = 0

    if game_active== None and bird.add_gravity ==0 and bird.gravity == 0:
         bird.add_gravity = 0.7
         bird.gravity = 0

    clock.tick(fps)
    pygame.display.update()