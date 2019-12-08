import pygame

pygame.init()

gameDisplay = pygame.display.set_mode((1200,800))
pygame.display.set_caption("cool pool")

running = True

poolImg = pygame.image.load("coolpool.png")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    gameDisplay.fill((255,255,255))
    gameDisplay.blit(poolImg, (500, 200))
    pygame.display.update()


