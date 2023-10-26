import pygame
import math as m

G = 10

class body():

    def __init__(self,pos,velocity,mass = 1):
        self.pos = pos
        self.vel = velocity

        self.mass = mass

        self.trail = [(self.pos[0],self.pos[1])]

        self.dead = False
    
    def update(self,dtime,objects):

        forces = []

        for obj in objects:

            if obj == self or obj.dead:
                continue

            angle = m.atan2(obj.pos[1]-self.pos[1],obj.pos[0]-self.pos[0])
            force = (G*self.mass*obj.mass)/(m.sqrt((obj.pos[0]-self.pos[0])**2+(obj.pos[1]-self.pos[1])**2)) ** 2
            forces.append([m.cos(angle)*force,m.sin(angle)*force])

        self.forceVector = [sum([force[0] for force in forces]), sum([force[1] for force in forces])]
        self.vel[0] += self.forceVector[0]/self.mass*dtime
        self.vel[1] += self.forceVector[1]/self.mass*dtime

        self.dtime = dtime

    def postUpdate(self):
        self.pos[0] += self.vel[0]*self.dtime
        self.pos[1] += self.vel[1]*self.dtime


        self.trail += [(self.pos[0],self.pos[1])]
        if len(self.trail) > 100:
            del self.trail[0]

    def draw(self,root,space):     

        width = root.get_width()
        height = root.get_height()

        normalisedPos = space.veiwPos(self.pos)

        normalisedPos[0] *= width
        normalisedPos[1] *= height
        
        if -5 <= normalisedPos[0] <= root.get_width()+5 and -5 <= normalisedPos[1] <= root.get_height()+5:
            pygame.draw.circle(root,(255,0,0), normalisedPos, 5)

        linePoint = space.veiwPos([self.pos[0]+self.forceVector[0],self.pos[1]+self.forceVector[1]])
        linePoint[0] *= width
        linePoint[1] *= height

        pygame.draw.aalines(root, (255,0,0), False, [(space.veiwPos(p)[0] * width, space.veiwPos(p)[1] * height) for p in self.trail])

        #pygame.draw.line(root,(0,255,0), normalisedPos, linePoint)
