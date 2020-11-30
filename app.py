import pygame
import time
import random

pygame.init()

display_x = 800
display_y = 600

gameDisplay = pygame.display.set_mode((display_x,display_y))
pygame.display.set_caption('Game')

clock = pygame.time.Clock()

# colors
white = (255,255,255)
black = (0,0,0)
red = (255,0,0)
bright_red = (200,0,0)
green = (0,255,0)
bright_green = (0,200,0)
blue = (0,0,255)

# Images for the game
planeImg = pygame.image.load('paper-plane.png')

# Parametres for some things
plane_x = 64

def message_display(message):
    font = pygame.font.Font('freesansbold.ttf', 32)
    text = font.render(message, True, black)
    textRect = text.get_rect()
    textRect.center = (display_x // 2, display_y // 2)
    gameDisplay.blit(text, textRect)
    pygame.display.update()

# Draw plane
def plane(x,y):
    gameDisplay.blit(planeImg, (x,y))

# Draw obstacles
def obstacle(start_x, start_y, width, height, color):
    pygame.draw.rect(gameDisplay, color, [start_x,start_y,width,height])

# Show score
def score(count):
    font = pygame.font.SysFont(None, 25)
    text = font.render("Score: " + str(count), True, black)
    gameDisplay.blit(text,(10,10))

#####################
## Draw the button ##
#############################################
#############################################
### msg    - text on button               ###
### x      - the X location of the button ###
### y      - the Y location of the button ###
### w      - button width                 ### 
### h      - button height                ###
### ic     - inactive color               ### 
### ac     - active color                 ###  
### action - what this button have to do  ###      
#############################################
#############################################
def button(msg,x,y,w,h,ic,ac,action=None):

    # Get position of the cursor (x, y)
    mouse = pygame.mouse.get_pos()

    # What button on mouse has been clicked
    click = pygame.mouse.get_pressed()

    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac, (x,y,w,h))

        if click[0] == True and action != None:
            action()

    else:  
        pygame.draw.rect(gameDisplay, ic, (x,y,w,h))

    smallText = pygame.font.Font('freesansbold.ttf', 20)
    text = smallText.render(msg, True, black)
    textRect = text.get_rect()
    textRect.center = ( (x+(w/2)), (y+(h/2)))
    gameDisplay.blit(text, textRect)

def quitgame():
    pygame.quit()
    quit()

def game_intro():

    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s:
                    main()
                
        gameDisplay.fill(white)
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render("Plane escape", True, black)
        textRect = text.get_rect()
        textRect.center = (display_x // 2, display_y // 2)
        gameDisplay.blit(text, textRect)


        button('Go!', 150, 450, 100, 50, green, bright_green, main)
        button('Quit', 550, 450, 100, 50, red, bright_red, quitgame)

        pygame.display.update()

def main():

    # stats for plane
    x = display_x * 0.47
    y = display_y * 0.8
    x_change = 0
    plane_speed = 0

    # stats for obstacles
    obs_start_x = random.randrange(0, display_x)
    obs_start_y = -100
    obs_speed = 10
    obs_width = 100
    obs_height = 100

    dodged = 0

    close = False

    while not close:

        # close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            # move left, right
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -5 - plane_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = 5 + plane_speed
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0 

        # Window color
        gameDisplay.fill(white)

        # Show plane on the window
        x += x_change
        plane(x,y)

        # Show score
        score(dodged)

        # Show obstacles on the window
        ''' obstacle(start_x, start_y, width, height, color) '''
        obstacle(obs_start_x, obs_start_y, obs_width, obs_height, red)
        obs_start_y += obs_speed
        if obs_start_y >= display_y + obs_height:
            obs_start_x = random.randrange(0, display_x)
            obs_start_y = -100
            obstacle(obs_start_x, obs_start_y, obs_width, obs_height, red)
            obs_start_y += obs_speed
            dodged += 1
            obs_speed += 0.2
            plane_speed += 0.2

        # Collision with obstacles
        if obs_start_y - 32 < y < obs_start_y + obs_height and obs_start_x - 64 < x < obs_start_x + obs_width:
            message_display("Game Over your score is: {}".format(dodged))
            time.sleep(2)
            game_intro()

        # Plane can't get out from the window
        if x > display_x - plane_x or x < 0:
            x_change = 0
            
        # Update the window
        pygame.display.update()
        clock.tick(60)

game_intro()
main()
pygame.quit()
quit()