import os
import monkeglobals as g
import sys
import math
import stage
import pytmx

def getScreenY(y, z):
    return z + y

def raytrace(x1, y1, z1, x2, y2, z2, obj):
    dirX = 1 if x2 >= x1 else -1
    dirZ = 1 if z2 >= z1 else -1
    res = (x2, y2, z2)
    
    floors = []
    for layer in stage.tilemap.visible_layers:
        if layer.name == 'floor':
            floors.append(layer)
    
    for x in range(int(x2 / stage.tilemap.tilewidth), int(x1 / stage.tilemap.tilewidth), -dirX):
        #z = ((z2 * x) + (z1 * (x2 - x1 - x))) / (x2 - x1)
        z = z1
        for layer in floors:
            if isinstance(layer, pytmx.TiledTileLayer):
                gid = layer.data[int(z / stage.tilemap.tileheight)][x]
                p = stage.tilemap.get_tile_properties_by_gid(gid)
                if p and p['colliders']:
                    #solid tile, return intersection
                    #print('hit bg')
                    #print((x * stage.tilemap.tilewidth if dirX > 0 else (x + 1) * stage.tilemap.tilewidth, 0, z))
                    res = ((x - 0.001) * stage.tilemap.tilewidth if dirX > 0 else (x + 1) * stage.tilemap.tilewidth, res[1], res[2])
                    break
        
    
    for z in range(int(z2 / stage.tilemap.tileheight), int(z1 / stage.tilemap.tileheight), -dirZ):
        x = ((res[0] * z) + (x1 * (z2 - z1 - z))) / (z2 - z1)
        for layer in floors:
            if isinstance(layer, pytmx.TiledTileLayer):
                gid = layer.data[z][int(x / stage.tilemap.tilewidth)]
                p = stage.tilemap.get_tile_properties_by_gid(gid)
                if p and p['colliders']:
                    #solid tile, return intersection
                    res = (res[0], res[1], (z - 0.001) * stage.tilemap.tileheight if dirZ > 0 else (z + 1) * stage.tilemap.tileheight)
                    break
    return res


def tickArrowKeys(self):
    if g.keys['left'] > 0:
        self.accelX -= self.moveAccel
    elif g.keys['right'] == 0:
        if self.velX < 0:
            self.accelX += self.moveAccel 
            if self.accelX * g.dt + self.velX > 0:
                self.accelX = -self.velX / g.dt
    if g.keys['right'] > 0:
        self.accelX += self.moveAccel
    elif g.keys['left'] == 0:
        if self.velX > 0:
            self.accelX -= self.moveAccel 
            if self.accelX * g.dt + self.velX < 0:
                self.accelX = -self.velX / g.dt
    if g.keys['up'] > 0:
        self.accelZ -= self.moveAccel
    elif g.keys['down'] == 0:
        if self.velZ < 0:
            self.accelZ += self.moveAccel 
            if self.accelZ * g.dt + self.velZ > 0:
                self.accelZ = -self.velZ / g.dt
    if g.keys['down'] > 0:
        self.accelZ += self.moveAccel
    elif g.keys['up'] == 0:
        if self.velZ > 0:        
            self.accelZ -= self.moveAccel 
            if self.accelZ * g.dt + self.velZ < 0:
                self.accelZ = -self.velZ / g.dt
                
    accelLen = math.sqrt(self.accelX * self.accelX + self.accelZ * self.accelZ)
    if accelLen > self.moveAccel:
        self.accelX *= self.moveAccel / accelLen
        self.accelY *= self.moveAccel / accelLen

def tickJump(self):
    if g.keys['jump'] > 0 and g.keys['jump'] <= g.dt:
        if self.touchingGround:
            self.velY = self.jumpVel

def tickMove(self):
    for o in g.stageObjects:
        if o != self:
            dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z)))
            distInRad = (self.radius + o.radius) - dist
            if distInRad > 0:
                pushX = (self.x - o.x) / dist
                pushY = (self.y - o.y) / dist
                pushZ = (self.z - o.z) / dist
                self.accelX += pushX * 0.06
                self.accelY += pushY * 0.01
                self.accelZ += pushZ * 0.06
    
    avgVelX = self.velX + self.accelX * 0.5 * g.dt
    avgVelX = -self.maxVel if avgVelX < -self.maxVel else avgVelX if avgVelX < self.maxVel else self.maxVel
    self.velX += self.accelX * g.dt
    self.velX = -self.maxVel if self.velX < -self.maxVel else self.velX if self.velX < self.maxVel else self.maxVel
    deltaX = avgVelX * g.dt
    
    avgVelY = self.velY + self.accelY * 0.5 * g.dt
    self.velY += self.accelY * g.dt
    deltaY = avgVelY * g.dt
    
    if self.y + deltaY > - self.radius:
        deltaY = -self.y - self.radius
        self.velY = 0
    
    avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
    avgVelZ = -self.maxVel if avgVelZ < -self.maxVel else avgVelZ if avgVelZ < self.maxVel else self.maxVel
    self.velZ += self.accelZ * g.dt
    self.velZ = -self.maxVel if self.velZ < -self.maxVel else self.velZ if self.velZ < self.maxVel else self.maxVel
    deltaZ = avgVelZ * g.dt
    
    destination = raytrace(self.x, self.y, self.z, self.x + deltaX, self.y + deltaY, self.z + deltaZ, self)
    self.x = destination[0]
    self.y = destination[1]
    self.z = destination[2]
    
    self.touchingGround = False
    if self.y >= -self.radius - 0.001:
        self.touchingGround = True
        self.y = -self.radius
    return


class Player:
    def __init__(self, pos):
        img = g.pygame.image.load(os.path.join('img', 'player', 'idle1.png'))
        self.image = g.pygame.transform.scale(img, (img.get_width()*4, img.get_height()*4)).convert_alpha(g.screen)
        self.radius = 128
        self.x = pos[0] + self.image.get_width()  / 2
        self.y = -self.radius
        self.z = pos[1] * 1 + self.image.get_height()
        g.player = self
        self.moveAccel = 0.05
        self.gravity = 0.015
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.maxVel = 1.2
        self.touchingGround = True
        self.jumpVel = -3.0

    def tick(self):
        
        self.accelX = 0.0
        self.accelY = self.gravity
        self.accelZ = 0.0
        
        tickArrowKeys(self)
        tickJump(self)
        tickMove(self)
            
        g.scrollX = self.x - 960
        g.scrollY = getScreenY(0, self.z) - self.radius - 540
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
        img = g.pygame.image.load(os.path.join('img', 'saucer', 'idle.png'))
        self.idle = []
        self.curAnimFrames = 5
        for i in range(0, 5):
            singleWidth = img.get_width() / self.curAnimFrames;
            frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
            frame.blit(img, (singleWidth * -i, 0))
            self.idle.append(\
            g.pygame.transform.scale(frame, (frame.get_width() * 4, frame.get_height() * 4)).convert_alpha(g.screen))
        self.radius = 128
        self.x = pos[0] + self.idle[0].get_width()  / 2
        self.y = -self.radius
        self.z = pos[1] * 1 + self.idle[0].get_height()
        self.curAnim = self.idle
        self.curAnimDuration = 100.0 * 5.0
        self.curAnimTimer = 0.0
    
    def tick(self):
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.idle[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
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
        self.y = -self.radius
        self.z = pos[1] * 1 + self.image.get_height()
        
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
        self.z = pos[1] * 1 + self.image.get_height()
    
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
        self.y = -self.radius
        self.z = pos[1] * 1 + self.image.get_height()
    
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
        self.z = pos[1] * 1 + self.image.get_height()
    
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