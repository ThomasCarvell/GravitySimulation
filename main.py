import pygame
from plane2dRenderer import *
from body import *
from trajectory import *
import random as r

pygame.init()

dis = (1920,1080)
root = pygame.display.set_mode(dis, pygame.RESIZABLE)

clock = pygame.time.Clock()
FPS = 0

def main():

    space = space2d(0, 0)

    particles = 10

    positions = [[r.randint(-1000,1000)/100,r.randint(-1000,1000)/100] for i in range(particles)]
    masses = [r.randint(1,100)/10 for i in range(particles)]
    velocities = [[r.randint(-100,100)/10,r.randint(-100,100)/10] for i in range(particles-1)]

    residualMomentum = [0,0]
    for mass,velocity in zip(masses,velocities):
        residualMomentum[0] += velocity[0]*mass
        residualMomentum[1] += velocity[1]*mass

    velocities.append([-(residualMomentum[0]/masses[-1]),-(residualMomentum[1]/masses[-1])])

    #scene = [
    #    body([1.5,0],[-1,-1]),
    #    body([0,0],[1,0]),
    #    body([-1.5,0],[0,1]),
    #]

    scene = [body(positions[i],velocities[i],masses[i]) for i in range(particles)]

    for obj in scene:
        space.addObject(obj)
    
    dtime = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return

        space.updateSpace(dtime/1000)

        root.fill((0,0,0))

        space.renderGrid(root)
        space.renderObjects(root)

        pygame.display.update()
        dtime = clock.tick(FPS)

    return


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        pygame.quit()
        raise e