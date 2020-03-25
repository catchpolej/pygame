"""
 This is the program header comment.
 Comments are ignored by python whenthe program runs.
 A triple quote starts and ends a comment block.
 Program: 10_jump_hurdle2.py
 Purpose: Completed 2 player jump_hurdle game
 Author: Jeremy Catchpole
 Many ideas taken from Pygame Tutorial #2 Jump Platformer: kidscancode.org/lessons
"""
# One line comments start with a # and are also ignored when python runs the program

# import the libraries needed
import pygame
vec = pygame.math.Vector2

# game constants
WIDTH = 720
HEIGHT = 400
FPS = 30
GRAV = 0.5
JUMP = 12
HURDLE_WIDTH = 30
TARGET = 1                                              # Target is to be more than 1 run ahead

# global game variables
running = True
started = False
ending = False                              # For improved ending/restart
#time_s = 0

# colours
BLACK = (0,0,0)
DARK_GREY = (50,50,50)                                  # Dark grey     
WHITE = (255,255,255)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
SKY_BLUE = (100,150,255)
YELLOW = (255,255,0)

# initalise and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("PYGAME Jump Hurdle")
clock = pygame.time.Clock()

# # Create the sprite group and add the sprites
all_sprites = pygame.sprite.Group()
all_hurdles = pygame.sprite.Group()

# player1 sprite
player1 = pygame.sprite.Sprite()
player1.image = pygame.Surface((30, 30))
player1.image.fill(YELLOW)
player1.rect = player1.image.get_rect()
player1.rect.midbottom = vec(WIDTH / 4, HEIGHT /2)
player1.on_ground = False
player1.jump = False
player1.vel = vec(0,0)
player1.score = 0
all_sprites.add(player1)
# player2 sprite                                 
player2 = pygame.sprite.Sprite()
player2.image = pygame.Surface((30, 30))
player2.image.fill(WHITE)                      
player2.rect = player1.image.get_rect()
player2.rect.midbottom = vec((WIDTH / 4) -5, (HEIGHT /2) + 10)
player2.on_ground = False
player2.jump = False
player2.vel = vec(0,0)
player2.score = 0
all_sprites.add(player2)


# ground
ground = pygame.sprite.Sprite()
ground.image = pygame.Surface((WIDTH,15))
ground.image.fill(GREEN)
ground.rect = ground.image.get_rect()
ground.rect.x = 0
ground.rect.y = HEIGHT-15                 
all_sprites.add(ground)

# ground
ground = pygame.sprite.Sprite()
ground.image = pygame.Surface((WIDTH,15))
ground.image.fill(GREEN)
ground.rect = ground.image.get_rect()
ground.rect.x = 0
ground.rect.y = HEIGHT-15
all_sprites.add(ground)

# hurdles
for i in range(2):
    hurdle = pygame.sprite.Sprite()
    hurdle.image = pygame.Surface((HURDLE_WIDTH, HEIGHT/3))
    hurdle.image.fill(RED)
    hurdle.rect = hurdle.image.get_rect()
    hurdle.rect.x = WIDTH + WIDTH*i/2
    hurdle.rect.bottom = HEIGHT-15
    all_sprites.add(hurdle)
    all_hurdles.add(hurdle)

# This function is updates the position of the player each frame
def hurdle_update():
    for hurdle in all_hurdles:
        hurdle.rect.x -= 5
        if hurdle.rect.x < 0-HURDLE_WIDTH:
            hurdle.rect.x = WIDTH
            hurdle.rect.bottom = HEIGHT-15
        # Did the hurdle hit the player?
        hit = hurdle.rect.colliderect(player1.rect)
        if hit:
            player1.rect.midtop = vec((WIDTH / 4), 10)         # Respawn position
            player1.score -= 1
        # Did the hurdle hit the player?
        hit = hurdle.rect.colliderect(player2.rect)
        if hit:
            player2.rect.midtop = vec((WIDTH / 4), 10)         # Respawn position
            player2.score -= 1

# This function is updates the position of player1 each frame
def player1_update():
    global started
    global ending
    # did we jump ?
    if player1.jump:
        player1.vel.y = -JUMP
        player1.jump = False

    # is a key pressed ?
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player1.vel.x = -5
    elif keys[pygame.K_RIGHT]:
        player1.vel.x = 5
    else:
        player1.vel.x = 0
    if keys[pygame.K_UP]:
        if player1.vel.y > -10:
           player1.vel.y += -GRAV/1.6
    elif keys[pygame.K_DOWN]:
        player1.vel.y += GRAV/1.6

    # move player1
    player1.vel.y += GRAV
    player1.rect.midbottom += player1.vel
    
    # are we on the ground?
    landed = player1.rect.colliderect(ground.rect)
    if landed:
        player1.on_ground = True
        if player1.vel.y > 0:
            player1.rect.bottom = ground.rect.top + 1
            player1.vel.y = 0
    else:
        player1.on_ground = False


    # Are we at the end?
    if player1.rect.x > WIDTH:
        player1.rect.x = 0
        player1.score += 1
        if player1.score > (player2.score + TARGET): 
            ending = True
            started = False


    # Stop us falling off the left edge?
    if player1.rect.x < 0:
        player1.rect.x = 0

# This function is updates the position of player2 each frame          # NEW
def player2_update():
    global started
    global ending
        # did we jump ?
    if player2.jump:
        player2.vel.y = -JUMP
        player2.jump = False

    keys = pygame.key.get_pressed()
    if keys[ord('a')]:
        player2.vel.x = -5
    elif keys[ord('d')]:
        player2.vel.x = 5
    else:
        player2.vel.x = 0
    if keys[ord('w')]:
        if player2.vel.y > -10:
            player2.vel.y += -GRAV/1.6
    elif keys[ord('s')]:
        player2.vel.y += GRAV/1.6
    player2.vel.y += GRAV
    player2.rect.midbottom += player2.vel
    
    # Are we on a the ground?
    landed = player2.rect.colliderect(ground.rect)
    if landed:
        player2.on_ground = True
        if player2.vel.y > 0:
            player2.rect.bottom = ground.rect.top + 1
            player2.vel.y = 0
    else:
        player2.on_ground = False


    # Are we at the end?
    if player2.rect.x > WIDTH:
        player2.rect.x = 0
        player2.score += 1
        if player2.score > (player1.score + TARGET):
            ending = True
            started = False

    # Stop us falling off the left edge?
    if player2.rect.x < 0:
        player2.rect.x = 0

        
def player_update():
    player1_update()
    player2_update()
        
def draw_race_instructions(surf):               # Added draw_race_instructions
    font= pygame.font.Font(pygame.font.match_font("arial"), 14)
    text_surface = font.render("P1 Use arrows keys: UP to jump and decrease gravity", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 10)
    surf.blit(text_surface, text_rect)
    text_surface = font.render("Down to increase gravity, Left and Right to move", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 30)
    surf.blit(text_surface, text_rect)
    text_surface = font.render("P2 Use 'w','a','s','d'", True, WHITE)       # Altered instructions
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 50)
    surf.blit(text_surface, text_rect)
    text_surface = font.render("Press up arrow to start", True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 70)
    surf.blit(text_surface, text_rect)
    
def draw_score(surf):
    font= pygame.font.Font(pygame.font.match_font("arial"), 14)
    text_surface = font.render("P1: "+str(player1.score)+"  P2:"+str(player2.score), True, WHITE)     # Altered
    text_rect = text_surface.get_rect()
    text_rect.midtop = (WIDTH/2, 10)
    surf.blit(text_surface, text_rect)

def restart():
    # Reset variables
    global ending
    global started
    ending = False
    started = True
    player1.score = 10
    player2.score = 10
    player2.rect.midbottom = vec((WIDTH / 4) -5, (HEIGHT /2) + 10)         # Start position
    player1.rect.midbottom = vec(WIDTH / 4, HEIGHT /2)
    for i in range(2):
        hurdle.rect.x = WIDTH + WIDTH*i/2


# game loop
while running:
    # Pause till next clock tick
    clock.tick(FPS)
    #time_s += 1/FPS                                   # Added time increment
    
    # Process inputs / events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # if UP is pressed and player is on the ground jump
            if event.key == pygame.K_UP:
                started = True                          # Start the game with up arrow
                if player1.on_ground:
                    player1.jump = True
            # if 'w' is pressed and player2 is on the ground jump
            if event.key == ord('w'):
                if player2.on_ground:
                    player2.jump = True
            if ending:
                if event.key == pygame.K_SPACE:             ### space to restart
                    restart()
                else:
                    running = False


    if started:                                         
        # update
        hurdle_update()
        player_update()
        all_sprites.update()
         # draw / render
        screen.fill(BLACK)
        all_sprites.draw(screen)
        draw_score(screen)
    else:
        screen.fill(BLACK)
        if ending:
            # Moved this section to here
            # game over                                     ### IMPROVED TO COMPLETE GAME
            screen.fill(BLACK)
            draw_score(screen)
            font= pygame.font.Font(pygame.font.match_font("arial"), 20)
            if player1.score > player2.score:
                message = "P1 wins:  "
            else:
                message = "P2 wins:  "
            message = message + "P1: "+str(player1.score)+"  P2: "+str(player2.score)
            text_surface = font.render(message, True, SKY_BLUE)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (WIDTH/2, HEIGHT/2)
            screen.blit(text_surface, text_rect)
            text_surface = font.render("Press SPACE to play again", True, SKY_BLUE)
            text_rect = text_surface.get_rect()
            text_rect.midtop = (WIDTH/2, (HEIGHT/2 + 20))
            screen.blit(text_surface, text_rect)
        else:
            all_sprites.draw(screen)
            draw_race_instructions(screen)
   
        
    pygame.display.flip()
        
pygame.quit()
quit()
