import pygame
#testing


pygame.init()

gameDisplay = pygame.display.set_mode((1200,800))
pygame.display.set_caption("cool pool")


poolImg = pygame.image.load("coolpool.png")


green = (0,128,0)
lime = (0,255,0)
blue = (0,128,128)
cyan = (0,255,255)
red = (255,0,0)
lightRed = (220,20,60)
white = (255,255,255)
PT = (175,238,238)

def message_display(text):
    largeText = pygame.font.Font("freesansbold.ttf",115)
    textSurf, textRect = text_objects(text,largeText)
    textRect.center = ()


def text_objects(text,font):
    textSurface = font.render(text,True,(0,0,0))
    return textSurface, textSurface.get_rect()

def button(msg,x,y,w,h,activeColor,inactiveColor,action=None):
    '''This is the basic button function template'''
    mouse = pygame.mouse.get_pos()

    click = pygame.mouse.get_pressed()

    #checking if mouse is on button
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, activeColor, (x, y, w, h))
        if click[0] == 1 and action!= None:
            action()

    else:
        pygame.draw.rect(gameDisplay, inactiveColor, (x, y, w, h))

    smallText = pygame.font.Font("freesansbold.ttf", 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = (x + (w / 2), y + (h / 2))
    gameDisplay.blit(textSurf, textRect)


def mainMultiplayer():

    classic = True

    while classic:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            import game


        pygame.display.update()


def mainSingleplayer():
    import singleplayer


def intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill(white)
        gameDisplay.blit(poolImg, (500, 200))


        button("Multiplayer",150,450,200,100,lime,green,mainMultiplayer)

        button("Singleplayer",850,450,200,100,lightRed,red,mainSingleplayer)


        pygame.display.update()



intro()