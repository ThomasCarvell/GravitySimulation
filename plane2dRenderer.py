import pygame
import math as m

pygame.init()

fontSize = 24
font = pygame.font.SysFont('Ariel', fontSize)

textPadding = 6

class space2d:

    def __init__(self,camX,camY):
        self.topLeft = [camX-16,camY-9]
        self.bottomRight = [camX+16,camY+9]

        self.objects = []

        self.time = 0
        self.timeRate = 1

    def translate(self,x,y):

        camWidth = self.bottomRight[0]-self.topLeft[0]

        self.topLeft[0] += x*camWidth
        self.topLeft[1] += y*camWidth

        self.bottomRight[0] += x*camWidth
        self.bottomRight[1] += y*camWidth

    def zoom(self, multiplier, center = None):
        if not center:
            center = (
                (self.topLeft[0]+self.bottomRight[0])*0.5,
                (self.topLeft[1]+self.bottomRight[1])*0.5)

        self.topLeft[0] -= center[0]
        self.topLeft[1] -= center[1]
        self.topLeft[0] *= multiplier
        self.topLeft[1] *= multiplier
        self.topLeft[0] += center[0]
        self.topLeft[1] += center[1]

        self.bottomRight[0] -= center[0]
        self.bottomRight[1] -= center[1]
        self.bottomRight[0] *= multiplier
        self.bottomRight[1] *= multiplier
        self.bottomRight[0] += center[0]
        self.bottomRight[1] += center[1]

    def unzoom(self, multiplier, center = None):
        if not center:
            center = (
                (self.topLeft[0]+self.bottomRight[0])*0.5,
                (self.topLeft[1]+self.bottomRight[1])*0.5)

        self.topLeft[0] -= center[0]
        self.topLeft[1] -= center[1]
        self.topLeft[0] /= multiplier
        self.topLeft[1] /= multiplier
        self.topLeft[0] += center[0]
        self.topLeft[1] += center[1]

        self.bottomRight[0] -= center[0]
        self.bottomRight[1] -= center[1]
        self.bottomRight[0] /= multiplier
        self.bottomRight[1] /= multiplier
        self.bottomRight[0] += center[0]
        self.bottomRight[1] += center[1]

    def reset(self):
        self.topLeft = [-16,-9]
        self.bottomRight = [16,9]

    def renderGrid(self,root):

        width = root.get_width()
        height = root.get_height()
        
        startX = self.topLeft[0]
        stopX = self.bottomRight[0]
        camWidth = stopX-startX

        startY = self.topLeft[1]
        stopY = self.bottomRight[1]
        camHeight = stopY-startY

        scaleX = 1
        while width/(int(camWidth)/scaleX) < 50:
            scaleX *= 2

        scaleY = 1
        while height/(int(camHeight)/scaleY) < 50:
            scaleY *= 2

        x = 1
        while x > startX:
            x -= scaleX

        while x < stopX+1:
            x += scaleX

            xValue = int(x)-1
            
            if xValue != 0:
                pygame.draw.line(
                    root,(100,100,100),
                    (int(width*((int(x)-1-startX)/camWidth)),0),
                    (int(width*((int(x)-1-startX)/camWidth)),height)
                )
            else:
                pygame.draw.line(
                    root,(255,255,255),
                    (int(width*((int(x)-1-startX)/camWidth)),0),
                    (int(width*((int(x)-1-startX)/camWidth)),height)
                )
            

            location0 = (0-startY)/camHeight

            textSurface = font.render(str(xValue),True,(200,200,200),(0,0,0))
            textRect = textSurface.get_rect()

            surfHeight = textSurface.get_height()

            if location0 >= 1:
                textRect.center = (int(width*((int(x)-1-startX)/camWidth)),height-surfHeight//2-textPadding)
            elif location0 <= 0:
                textRect.center = (int(width*((int(x)-1-startX)/camWidth)),surfHeight//2+textPadding)
            else:
                textRect.center = (int(width*((int(x)-1-startX)/camWidth)),int(location0*height)+textPadding+surfHeight//2)

            if xValue != 0:
                root.blit(textSurface, textRect)

        y = 1
        while y > startY:
            y -= scaleY

        while y < stopY+1:
            y += scaleY

            yValue = 1-int(y)

            if yValue != 0:
                pygame.draw.line(
                    root,(100,100,100),
                    (0,int(height*((int(y)-1-startY)/camHeight))),
                    (width,int(height*((int(y)-1-startY)/camHeight)))
                )
            else:
                pygame.draw.line(
                    root,(255,255,255),
                    (0,int(height*((int(y)-1-startY)/camHeight))),
                    (width,int(height*((int(y)-1-startY)/camHeight)))
                )

            location0 = (0-startX)/camWidth

            textSurface = font.render(str(yValue),True,(200,200,200),(0,0,0))
            textRect = textSurface.get_rect()

            surfWidth = textSurface.get_width()

            if location0 >= 1:
                textRect.center = (width-surfWidth//2-textPadding,int(height*((int(y)-1-startY)/camHeight)))
            elif location0 <= 0:
                textRect.center = (surfWidth//2+textPadding,int(height*((int(y)-1-startY)/camHeight)))
            else:
                if yValue == 0:
                    textRect.center = (int(location0*width)-textPadding-surfWidth//2,int(height*((int(y)-1-startY)/camHeight))+textPadding+5)
                else:
                    textRect.center = (int(location0*width)-textPadding-surfWidth//2,int(height*((int(y)-1-startY)/camHeight)))

            if yValue != 0 or (0 <= location0 <= 1):
                root.blit(textSurface, textRect)
    
    def addObject(self,obj):
        self.objects.append(obj)

    def updateSpace(self,dtime):

        keys = pygame.key.get_pressed()

        if keys[pygame.K_d]: self.translate(0.25*dtime,0)
        if keys[pygame.K_a]: self.translate(-0.25*dtime,0)
        if keys[pygame.K_w]: self.translate(0,-0.25*dtime)
        if keys[pygame.K_s]: self.translate(0,0.25*dtime)

        if keys[pygame.K_e]: self.zoom(1+(1*dtime))
        if keys[pygame.K_q]: self.unzoom(1+(1*dtime))

        if keys[pygame.K_c]: self.reset()

        if keys[pygame.K_x]:
            self.timeRate *= 1+(1*dtime)
        if keys[pygame.K_z]:
            self.timeRate /= 1+(1*dtime)

        self.time += dtime*self.timeRate
        for obj in self.objects:
            obj.update(dtime*self.timeRate,self.objects)

        for obj in self.objects:
            obj.postUpdate()
    
    def renderObjects(self,root):
        for obj in self.objects:
            obj.draw(root,self)

        timeSurf = font.render(str(round(self.time,5)), True, (200,200,200))
        timeRect = timeSurf.get_rect()

        timeRect.topleft = (textPadding,textPadding)
        root.blit(timeSurf,timeRect)

    def veiwPos(self,pos):
        return [(pos[0]-self.topLeft[0])/(self.bottomRight[0]-self.topLeft[0]),(-pos[1]-self.topLeft[1])/(self.bottomRight[1]-self.topLeft[1])]


class graph(space2d):

    def __init__(self,numValues = 0):
        super().__init__(self,0,0)

        self.values = {}
        self.topLeft = [0,10]
        self.bottomRight = [25,-10]

    def addValues(x,values):
        self.values[x] = values

    def renderGraph(self,root):
        
        for key in sorted(self.values.keys(), key = lambda x:x):
            pass




