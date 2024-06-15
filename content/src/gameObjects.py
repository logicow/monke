import os
import monkeglobals as g
import sys
import math

def getScreenY(y, z):
    return z/2 - y

class Player:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'player', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.width * 4, img.height * 4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.width  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.height
        g.player = self
       
    
    def tick(self):
        if g.keys['left'] > 0:
            self.x -= 2 * g.dt
        if g.keys['right'] > 0:
            self.x += 2 * g.dt
        if g.keys['up'] > 0:
            self.z -= 2 * g.dt
        if g.keys['down'] > 0:
            self.z += 2 * g.dt
        g.scrollX = self.x - 960
        g.scrollY = getScreenY(self.y, self.z) - 540
        pass
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        pass
        
    def drawShadow(self):
        pass

def spawnPlayer(obj):
    newObj = Player((obj.x, obj.y))
    g.stageObjects.append(newObj)

class Saucer:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'saucer', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.width * 4, img.height * 4)).convert_alpha(g.screen)
        
        self.radius = 128
        self.x = pos[0] + self.image.width  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.height
    
    def tick(self):
        pass
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        pass
        
    def drawShadow(self):
        pass

def spawnSaucer(obj):
    newObj = Saucer((obj.x, obj.y))
    g.stageObjects.append(newObj)
    
    
class Goblin:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'goblin', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.width * 4, img.height * 4)).convert_alpha(g.screen)
    
        self.radius = 128
        self.x = pos[0] + self.image.width  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.height
        
    def tick(self):
        playerDist = math.sqrt(\
        (g.player.x - self.x) * (g.player.x - self.x) + \
        (g.player.y - self.y) * (g.player.y - self.y) + \
        (g.player.z - self.z) * (g.player.z - self.z)) - self.radius - g.player.radius
        if playerDist <= 0:
            g.stageClear = True
        
        pass
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        pass
        
    def drawShadow(self):
        pass

def spawnGoblin(obj):
    newObj = Goblin((obj.x, obj.y))
    g.stageObjects.append(newObj)