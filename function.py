import pygame
def button (screen, msg, x, y, w, h, ic, ac, action=None):
    mouse =pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    print(click)
    if x + w > mouse[0] > x and y + h > mouse[1] > y:
        pygame.draw.rect(screen, ac, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(screen, ic, (x,y,w,h))
    smallText = pygame.font.SysFont('comicsansms', 20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)))
    screen.blit(textSurf, textRect)