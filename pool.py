import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((1200,800))
pygame.display.set_caption("cool pool")


poolImg = pygame.image.load("coolpool.png")

green = (0,128,0)
blue = (0,0,255)

def text_objects(text,font):
    textSurface = font.render(text,True,(0,0,0))
    return textSurface, textSurface.get_rect()

#testing
def intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        gameDisplay.fill((255,255,255))
        gameDisplay.blit(poolImg, (500, 200))


        mouse = pygame.mouse.get_pos()
        print(mouse)


        #Mouse hover onto button will change the color
        if 150+200 > mouse[0] > 150 and 450 + 100 > mouse[1] > 450:
            pygame.draw.rect(gameDisplay, (0,255,0), (150, 450, 200, 100))
        else:
            pygame.draw.rect(gameDisplay, green, (150, 450, 200, 100))


        if 500+200>mouse[0]>500 and 450+100> mouse[1]>450:
            pygame.draw.rect(gameDisplay, (255,0,255), (500, 450, 200, 100))
        else:
            pygame.draw.rect(gameDisplay, (255,0,0), (500, 450, 200, 100))

        if 850+200 > mouse[0] > 850 and 450 + 100 > mouse[1] > 450:
            pygame.draw.rect(gameDisplay, (0,255,255), (850, 450, 200, 100))
        else:
            pygame.draw.rect(gameDisplay, (0,128,128), (850, 450, 200, 100))


        smallText = pygame.font.Font("freesansbold.ttf",20)
        textSurf, textRect = text_objects("Classic", smallText)
        textRect.center = ( 150+(200/2), 450+(100/2))
        gameDisplay.blit(textSurf,textRect)

        textSurf, textRect = text_objects("Circle", smallText)
        textRect.center = (500 + (200 / 2), 450 + (100 / 2))
        gameDisplay.blit(textSurf, textRect)

        textSurf, textRect = text_objects("Triangle", smallText)
        textRect.center = (850 + (200 / 2), 450 + (100 / 2))
        gameDisplay.blit(textSurf, textRect)

        pygame.display.update()



intro()