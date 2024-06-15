import os
import monkeglobals as g
import sys
import math

def getScreenY(y, z):
    return z/2 - y

class Player:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'player', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.get_width()*4, img.get_height()*4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.get_width()  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.get_height()
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
        return
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        return

def spawnPlayer(obj):
    newObj = Player((obj.x, obj.y))
    g.stageObjects.append(newObj)

class Saucer:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'saucer', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.get_width()  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.get_height()
    
    def tick(self):
        return
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        return

def spawnSaucer(obj):
    newObj = Saucer((obj.x, obj.y))
    g.stageObjects.append(newObj)
    
    
class Goblin:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'goblin', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.get_width()  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.get_height()
        
    def tick(self):
        playerDist = math.sqrt(\
        (g.player.x - self.x) * (g.player.x - self.x) + \
        (g.player.y - self.y) * (g.player.y - self.y) + \
        (g.player.z - self.z) * (g.player.z - self.z)) - self.radius - g.player.radius
        if playerDist <= 0:
            g.stageClear = True
        return
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        return

def spawnGoblin(obj):
    newObj = Goblin((obj.x, obj.y))
    g.stageObjects.append(newObj)
    
    

class Dinorider:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'dinorider', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.get_width()  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.get_height()
    
    def tick(self):
        return
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        return

def spawnDinorider(obj):
    newObj = Dinorider((obj.x, obj.y))
    g.stageObjects.append(newObj)
    
    

class Plantman:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'plantman', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.get_width()  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.get_height()
    
    def tick(self):
        return
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        return

def spawnPlantman(obj):
    newObj = Plantman((obj.x, obj.y))
    g.stageObjects.append(newObj)
    
    
    
class EnemyBlue:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'enemyblue', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.get_width() * 4, img.get_height() * 4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.get_width()  / 2
        self.y = self.radius
        self.z = pos[1] * 2 + self.image.get_height()
    
    def tick(self):
        return
    
    def draw(self):
        g.sortedSprites.append((self.image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        return

def spawnEnemyBlue(obj):
    newObj = EnemyBlue((obj.x, obj.y))
    g.stageObjects.append(newObj)