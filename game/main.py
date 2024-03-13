import pygame

pygame.init()

pygame.display.set_caption("Sonic and the world of python")



screen = pygame.display.set_mode((640,480))
pygame_icon = pygame.image.load("./game/assets/img/logo.png")
pygame.display.set_icon(pygame_icon)

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    clock.tick(60)