"""
 This is the program header comment.
 Comments are ignored by python whenthe program runs.
 A triple quote starts and ends a comment block.
 08_final touches
 the starting point for this tutorial sequence is the template from the kids can code tutorial at:
 https://www.youtube.com/watch?v=VO8rTszcW4s&list=PLsk-HSGFjnaH5yghzu7PcOzm9NhsW0Urw%2F
"""
# One line comments start with a # and are also ignored when python runs the program

# import the libraries needed
import pygame
import random           
vec = pygame.math.Vector2

# game constants
WIDTH = 400             
HEIGHT = 600
FPS = 30
GRAV = 0.4
JUMP = 12
PACC = 0.40
PFRIC = 0.10
CATCH = 10              # added these constants
DROP = 2

# colours
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
LEAF_GREEN = (0,150,0)
BLUE = (0,0,255)
SKY_BLUE = (100,150,255)
YELLOW = (255,255,0)
CYAN = (0,255,255)
MAGENTA = (255,0,255)
BROWN = (100,50,50)

# initalise and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PYGAME kids can code")
clock = pygame.time.Clock()
game_font = pygame.font.Font(pygame.font.match_font("arial"), 12)   #Moved this line

# Create the sprite groups and add the sprites
all_sprites = pygame.sprite.Group()
all_platforms = pygame.sprite.Group()
all_balls = pygame.sprite.Group()
all_texts = pygame.sprite.Group()

# player1 sprite
player1 = pygame.sprite.Sprite()
player1.image = pygame.Surface((30, 30))
player1.image.fill(YELLOW)
player1.rect = player1.image.get_rect()
player1.pos = vec(WIDTH/2,HEIGHT - 15)
player1.vel = vec(0.0)
player1.score = 0
player1.on_ground = False
player1.alive = True                    # Added this variable
all_sprites.add(player1)

# starting platforms
# coordinates: [0]=x position [1]=y position, [2]=width [3]=height
# remember 0,0 is top left of screen
platform_coordinates = [(0, HEIGHT-15, WIDTH, 15),
                 (WIDTH/2, HEIGHT*3/4, 100, 20),
                 (125, HEIGHT-350, 100, 20),
                 (175, 100, 50, 20),
                 (300, HEIGHT-450, 50, 20)]
for coordinates in platform_coordinates:
    platform = pygame.sprite.Sprite()
    platform.image = pygame.Surface((coordinates[2],coordinates[3]))
    platform.image.fill(GREEN)
    platform.rect = platform.image.get_rect()
    platform.rect.x = coordinates[0]
    platform.rect.y = coordinates[1]
    all_sprites.add(platform)
    all_platforms.add(platform)

# create a ball
def new_ball():
    ball = platform = pygame.sprite.Sprite()
    ball.image = pygame.Surface((20,20))
    pygame.draw.circle(ball.image, YELLOW, (10,10), 10)
    ball.rect = ball.image.get_rect()
    ball.rect.x = WIDTH/2
    ball.rect.y = HEIGHT/2
    ball.vel = vec(random.randint(-5,5),-10)
    all_sprites.add(ball)
    all_balls.add(ball)
    
# update the ball
def ball_update():
    for ball in all_balls:
        ball.vel.y += GRAV/2
        ball.rect.y += ball.vel.y
        ball.rect.x += ball.vel.x
        if (player1.pos.y < HEIGHT/4) and (player1.vel.y < 0):
            ball.rect.y -= player1.vel.y
        # bounce off sides
        if (ball.rect.x < 0) or (ball.rect.x > WIDTH):
            ball.vel.x = -ball.vel.x
        # off bottom
        if ball.rect.y > HEIGHT:
            player1.score -= DROP
            ball.kill()

# New methods for text floats
# Create a text float sprite
def text_float(the_text, x, y):
    text_fl = platform = pygame.sprite.Sprite()
    textSurf = game_font.render(the_text, True, SKY_BLUE)
    text_fl.image = pygame.Surface((textSurf.get_width(),textSurf.get_height()))
    print("Creating text_float",the_text,(textSurf.get_width(),textSurf.get_height()), x, y)
    text_fl.image.fill(BROWN)
    text_fl.rect = textSurf.get_rect()
    text_fl.rect.center = (x, y)
    text_fl.image.blit(textSurf, (0,0))
    text_fl.age = 0
    all_sprites.add(text_fl)
    all_texts.add(text_fl)
    
def text_float_update():
    for text_fl in all_texts:
        text_fl.rect.y -= 4
        # last for 60 frames
        text_fl.age += 1
        if text_fl.age > 60:
            text_fl.kill()

# update platform positions           
def platform_update():
    # if player is in top 1/4 of screen and moving up move all objects downwards
    if (player1.pos.y < HEIGHT/4) and (player1.vel.y < 0):
        for platform in all_platforms:
            platform.rect.y -= player1.vel.y
            # if platform is off screen respawn it
            if platform.rect.y > HEIGHT:
                #platform = pygame.sprite.Sprite()
                w = random.randint(10, 100)     # width of platform
                x = random.randint(0, WIDTH-w)  # x position
                coordinates = (x, 0, w, 20)
                print("Respawning", coordinates)
                platform.image = pygame.Surface((coordinates[2],coordinates[3]))
                platform.image.fill(GREEN)
                platform.rect = platform.image.get_rect()
                platform.rect.x = coordinates[0]
                platform.rect.y = coordinates[1]
                # create a ball to catch
                new_ball()
        player1.pos.y -= player1.vel.y

# update the player   
def player_update():
    player1.acc = vec(0, GRAV)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player1.acc.x += -PACC
    elif keys[pygame.K_RIGHT]:
        player1.acc.x += PACC
    if keys[pygame.K_UP]:
        if player1.vel.y > -10:
            player1.vel.y += -GRAV/1.6
    elif keys[pygame.K_DOWN]:
        player1.vel.y += GRAV/1.6
    
    #Friction
    player1.acc.x -= player1.vel.x * PFRIC
    #print(player_acc)
    #Motion
    player1.vel += player1.acc
    player1.pos += player1.vel
    #Wrap around
    if player1.pos.x > WIDTH:
        player1.pos.x = 0
    if player1.pos.x < 0:
        player1.pos.x = WIDTH
    #Place rectangle at new position of player
    player1.rect.midbottom = player1.pos

    # Are we on a platform?
    landed = pygame.sprite.spritecollide(player1, all_platforms, False)
    if landed:
        player1.on_ground = True
        if player1.vel.y > 0:
            player1.pos.y = landed[0].rect.top + 1
            player1.vel.y = 0
    else:
        player1.on_ground = False

    # Did we catch a ball?
    caught = pygame.sprite.spritecollide(player1, all_balls, True)
    if caught:
        # create text float sprite
        text_float(str(CATCH), player1.pos.x, (player1.pos.y-10))   
        player1.score += CATCH

# Return true to keep running unless we lost
    if player1.pos.y > HEIGHT:
        return(False)
    else:
        return(True)

def draw_score(surf):
    text_surface = game_font.render("Score: "+str(player1.score), True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 10)
    surf.blit(text_surface, text_rect)

def restart():
    player1.pos = vec(WIDTH/2, 20)
    player1.vel = vec(0.0)
    
# game loop
running = True
while running:
    # Pause till next clock tick
    clock.tick(FPS)
    
    # Process inputs / events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # if UP is pressed and player is on the ground jump
            if event.key == pygame.K_UP:
                if player1.on_ground:
                    player1.vel.y = -JUMP
        # This can be commented out but it shows the events in the shell
        #print(event)
            if player1.alive == False:
                if event.key == pygame.K_SPACE:             ### space to restart
                    restart()
                else:
                    running = False

   
    # update
    player1.alive = player_update()       # Changed to set alive flag
    if player1.alive:                      # added this logic
        platform_update()
        ball_update()
        all_sprites.update()
        text_float_update()
    
    # draw / render
    screen.fill(BLACK)
    if player1.alive:                       # added this logic
        all_sprites.draw(screen)
        draw_score(screen)
    else:              # added this section        message = "GAME OVER: SCORE is "+str(player1.score)
        message = "GAME OVER: SCORE is "+str(player1.score)
        text_surface = game_font.render(message, True, SKY_BLUE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH/2, HEIGHT/2)
        screen.blit(text_surface, text_rect)
        text_surface = game_font.render("Press SPACE to continue", True, SKY_BLUE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (WIDTH/2, (HEIGHT/2 + 20))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()
    
pygame.quit()
quit()
