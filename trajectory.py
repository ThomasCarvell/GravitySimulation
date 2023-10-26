import pygame
import math as m

class trajectory:

    def __init__(self,bodies,dtime,duration,colour):

        self.dead = True

        self.colour = colour

        self.paths = [[body.pos] for body in bodies]

        time = 0
        while time < duration:
            
            for body in bodies:
                body.update(dtime,bodies)
                
            for body in bodies:
                body.postUpdate()

            for i,body in enumerate(bodies):
                self.paths[i].append([body.pos[0],body.pos[1]])

            time += dtime

    def update(self,dtime,objects):
        return

    def draw(self,root,space):

        width = root.get_width()
        height = root.get_height()

        for path in self.paths:
            points = [[point[0]*width,point[1]*height] for point in [space.veiwPos(p) for p in path]]

            for i,point in list(enumerate(points))[2:]:
                pygame.draw.line(root,self.colour, points[i],points[i-1])
            

            for point in points:

                pygame.draw.circle(root, (255,0,0), point, 3)


