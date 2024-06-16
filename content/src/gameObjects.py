import os
import monkeglobals as g
import sys
import math
import stage
import pytmx
import random

shadowDict = {}
bulletDict = {}
nextRotatingTimer = 1234.56

def getScreenY(y, z):
    return z + y

def raytrace(x1, y1, z1, x2, y2, z2):
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
    
    for layer in floors:
         if isinstance(layer, pytmx.TiledTileLayer):
            try:
                gid = layer.data[int(res[2] / stage.tilemap.tileheight)][int(res[0] / stage.tilemap.tilewidth)]
            except:
                return (x1, y1, z1)
            p = stage.tilemap.get_tile_properties_by_gid(gid)
            if p and p['colliders']:
                res = (x1, y1, z1)
    return res
    
BulletPlayerImg = None
BulletPlantmanImg = None
BulletGoblinImg = None
BulletSkaterImg = None
BulletSquidImg = None
BulletDinoriderImg = None
BulletSaucerImg = None

def initOnce():
    global shadowDict
    
    img = g.pygame.image.load(os.path.join('img', 'shadow128.png')).convert_alpha(g.screen)
    shadowDict['128'] = img.convert_alpha(g.screen)
    img = g.pygame.image.load(os.path.join('img', 'shadow96.png')).convert_alpha(g.screen)
    shadowDict['96'] = img.convert_alpha(g.screen)
    img = g.pygame.image.load(os.path.join('img', 'shadow64.png')).convert_alpha(g.screen)
    shadowDict['64'] = img.convert_alpha(g.screen)
    img = g.pygame.image.load(os.path.join('img', 'shadow32.png')).convert_alpha(g.screen)
    shadowDict['32'] = img.convert_alpha(g.screen)
    img = g.pygame.image.load(os.path.join('img', 'shadow16.png')).convert_alpha(g.screen)
    shadowDict['16'] = img.convert_alpha(g.screen)
    
    global BulletPlayerImg
    img = g.pygame.image.load(os.path.join('img', 'projectiles.png'))
    subsprite = g.pygame.Surface((12, 12), g.pygame.SRCALPHA)
    subsprite.blit(img, (-118, -23))
    BulletPlayerImg = []
    for i in range(16):
        BulletPlayerImg.append( g.pygame.transform.rotozoom(subsprite, i * 360.0 / 16.0, 6).convert_alpha(g.screen) )
        
    global BulletPlantmanImg
    subsprite = g.pygame.Surface((12, 12), g.pygame.SRCALPHA)
    subsprite.blit(img, (-40, -23))
    BulletPlantmanImg = (g.pygame.transform.scale(subsprite, (subsprite.get_width() * 6, subsprite.get_height() * 6)).convert_alpha(g.screen))
        
    global BulletEnemyBlueImg
    subsprite = g.pygame.Surface((12, 12), g.pygame.SRCALPHA)
    subsprite.blit(img, (-41, -56))
    BulletEnemyBlueImg = (g.pygame.transform.scale(subsprite, (subsprite.get_width() * 6, subsprite.get_height() * 6)).convert_alpha(g.screen))

    global BulletGoblinImg
    subsprite = g.pygame.Surface((11, 11), g.pygame.SRCALPHA)
    subsprite.blit(img, (-111, -63))
    BulletGoblinImg = []
    for i in range(16):
        BulletGoblinImg.append( g.pygame.transform.rotozoom(subsprite, i * 360.0 / 16.0, 6).convert_alpha(g.screen) )

    global BulletSkaterImg
    subsprite = g.pygame.Surface((15, 15), g.pygame.SRCALPHA)
    subsprite.blit(img, (-43, -105))
    BulletSkaterImg = []
    for i in range(16):
        BulletSkaterImg.append( g.pygame.transform.rotozoom(subsprite, i * 360.0 / 16.0, 6).convert_alpha(g.screen) )

    global BulletSquidImg
    subsprite = g.pygame.Surface((12, 12), g.pygame.SRCALPHA)
    subsprite.blit(img, (-114, -101))
    BulletSquidImg = (g.pygame.transform.scale(subsprite, (subsprite.get_width() * 6, subsprite.get_height() * 6)).convert_alpha(g.screen))
    
    global BulletDinoriderImg
    subsprite = g.pygame.Surface((12, 12), g.pygame.SRCALPHA)
    subsprite.blit(img, (-188, -26))
    BulletDinoriderImg = []
    for i in range(16):
        BulletDinoriderImg.append( g.pygame.transform.rotozoom(subsprite, i * 360.0 / 16.0, 6).convert_alpha(g.screen) )

    global BulletSaucerImg
    subsprite = g.pygame.Surface((12, 12), g.pygame.SRCALPHA)
    subsprite.blit(img, (-189, -74))
    BulletSaucerImg = (g.pygame.transform.scale(subsprite, (subsprite.get_width() * 6, subsprite.get_height() * 6)).convert_alpha(g.screen))
    


def tickArrowKeys(self):
    if g.keys['left'] > 0:
        self.accelX -= self.moveAccel
        self.xDir = 0
    elif g.keys['right'] == 0:
        if self.velX < 0:
            self.accelX += self.moveAccel 
            if self.accelX * g.dt + self.velX > 0:
                self.accelX = -self.velX / g.dt
    if g.keys['right'] > 0:
        self.xDir = 1
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

def tickFrictionStop(self):
    self.accelX = 0
    self.accelY = self.gravity
    self.accelZ = 0
    if self.velX < 0:
        self.accelX += self.moveAccel 
        if self.accelX * g.dt + self.velX > 0:
            self.accelX = -self.velX / g.dt
    if self.velX > 0:
        self.accelX -= self.moveAccel 
        if self.accelX * g.dt + self.velX < 0:
           self.accelX = -self.velX / g.dt
    if self.velZ < 0:
        self.accelZ += self.moveAccel 
        if self.accelZ * g.dt + self.velZ > 0:
            self.accelZ = -self.velZ / g.dt
    if self.velZ > 0:        
        self.accelZ -= self.moveAccel 
        if self.accelZ * g.dt + self.velZ < 0:
            self.accelZ = -self.velZ / g.dt

def tickJump(self):
    if g.keys['jump'] > 0 and g.keys['jump'] <= g.dt:
        if self.touchingGround:
            self.velY = self.jumpVel

def tickMove(self):
    for o in g.stageObjects:
        if o != self and o.collide:
            dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
            distInRad = (self.radius + o.radius) - dist
            if distInRad > 0:
                distXZ = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
                pushX = (self.x - o.x) / distXZ
                pushZ = (self.z - o.z) / distXZ
                self.accelX += pushX * 0.06
                self.accelZ += pushZ * 0.06
    
    avgVelX = self.velX + self.accelX * 0.5 * g.dt
    avgVelX = -self.maxVel if avgVelX < -self.maxVel else avgVelX if avgVelX < self.maxVel else self.maxVel
    self.velX += self.accelX * g.dt
    self.velX = -self.maxVel if self.velX < -self.maxVel else self.velX if self.velX < self.maxVel else self.maxVel
    deltaX = avgVelX * g.dt
    
    if self.velY < -3:
        self.velY = -3
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
    
    destination = raytrace(self.x, self.y, self.z, self.x + deltaX, self.y + deltaY, self.z + deltaZ)
    self.x = destination[0]
    self.y = destination[1]
    self.z = destination[2]
    
    self.touchingGround = False
    if self.y >= -self.radius - 0.001:
        self.touchingGround = True
        self.y = -self.radius
    return


def tickPlayerShoot(self):
    self.cooldown -= g.dt
    if self.cooldown > 0:
        return
    if g.keys['attack'] > 0:
        self.cooldown += 100;
        spawnBulletPlayer(self)
    else:
        self.cooldown = 0

playerIdle = None
playerRun = None

class Player:
    def __init__(self, pos):
        global playerIdle
        global playerRun
        if playerIdle == None:
            img = g.pygame.image.load(os.path.join('img', 'player', 'idle.png'))
            playerIdle = []
            self.curAnimFrames = 6
            for i in range(0, 6):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                playerIdle.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        if playerRun == None:
            img = g.pygame.image.load(os.path.join('img', 'player', 'run.png'))
            playerRun = []
            self.curAnimFrames = 12
            for i in range(0, 12):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                playerRun.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        
        self.curAnimFrames = 6
        self.curAnim = playerIdle
        self.radius = 52 * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        g.player = self
        self.moveAccel = 0.05
        self.gravity = 0.015
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.maxVel = 1.2
        self.touchingGround = True
        self.jumpVel = -3.0
        self.cooldown = 0.0
        self.xDir = 1
        self.collide = True
        self.curAnimTimer = 0
        self.curAnimDuration = 100.0 * 6.0
        self.isEnemy = False
        self.hp = 3
        targetScroll = (self.x - 960 + 400)
        g.scrollX = targetScroll

    def tick(self):
        
        self.accelX = 0.0
        self.accelY = self.gravity
        self.accelZ = 0.0
        
        tickArrowKeys(self)
        tickJump(self)
        tickMove(self)
        tickPlayerShoot(self)
        
        if self.velX > 1.0 or self.velX < -1 or self.velZ < -1 or self.velZ > 1.0:
            self.curAnim = playerRun
            self.curAnimFrames = 12
            self.curAnimDuration = 100.0 * 12.0
        else:
            self.curAnim = playerIdle
            self.curAnimFrames = 6
            self.curAnimDuration = 100.0 * 6.0
        
        targetScroll = (self.x - 960 + 400)
        g.scrollX += g.dt * 2
        if g.scrollX > targetScroll:
            g.scrollX = targetScroll
        g.scrollY = getScreenY(0, self.z) - self.radius - 540
        
        if(g.bossScrollX > 0 and g.scrollX > g.bossScrollX) :
            g.scrollX = g.bossScrollX
        
        if stage.stage == 1:
            g.scrollY = 100
        if(stage.stage == 5):
            g.scrollY = 100
            
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['128'], self.x, self.y + self.radius, self.z))
        return
        
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            #explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3

def spawnPlayer(obj):
    newObj = Player((obj.x, obj.y))
    g.stageObjects.append(newObj)


class BulletPlayer:
    def __init__(self, pos, xDir):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        self.velX = 0.6 if xDir == 1 else -0.6
        self.velY = -2.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.xDir = xDir
        self.collide = False
        self.isEnemy = False
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        for o in g.stageObjects:
            if o.isEnemy:
                dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
                distInRad = (self.radius + o.radius) - dist
                if distInRad > 0:
                    o.hit((self.x, self.y, self.z))
                    self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        return
        
    def draw(self):
        global BulletPlayerImg
        r = int((self.timer / 20.0) % 16)
        if self.xDir == 1:
            r = 15 - r
        g.sortedSprites.append((BulletPlayerImg[r], self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return
    
def spawnBulletPlayer(player):
    xDir = 1
    posX = player.x
    posY = player.y
    posZ = player.z
    posX += 80 if xDir == 1 else -80
    posY -= 10
    newObj = BulletPlayer((posX, posY, posZ), xDir)
    g.stageObjects.append(newObj)





saucerIdle = None

class Saucer:
    def __init__(self, pos):
        
        global saucerIdle
        if saucerIdle == None:
            img = g.pygame.image.load(os.path.join('img', 'saucer', 'idle.png'))
            saucerIdle = []
            self.curAnimFrames = 5
            for i in range(0, 5):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                saucerIdle.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        self.curAnimFrames = 5
        self.radius = 64  * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        self.curAnim = saucerIdle
        self.curAnimDuration = 100.0 * 5.0
        self.curAnimTimer = 0.0
        self.collide = True
        self.timer = 0
        self.isEnemy = True
        self.hp = 3
        self.gravity = 0.000
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.maxVel = 2.2
        self.moveAccel = 0.05
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
        
    
    def tick(self):
        self.timer += g.dt
        tickFrictionStop(self)
        if not self.attacking:
            self.nextAttack -=  g.dt
            if self.nextAttack <= 0:
                self.attacking = True
                self.nextAttack = random.uniform(100, 1000)
                self.shoot()
                self.attacking = False
        tickMove(self)
        self.y = math.sin(self.timer / 200.0) * 40 - 40 - 120
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['96'], self.x, self.y + self.radius, self.z))
        return
        
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3
        
    def shoot(self):
        if self.x > g.player.x + 1600:
            return;
        newObj = BulletSaucer((self.x, self.y, self.z), self)
        g.stageObjects.append(newObj)

def spawnSaucer(obj):
    newObj = Saucer((obj.x, obj.y))
    g.stageObjects.append(newObj)
    
class BulletSaucer:
    def __init__(self, pos, shooter):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        
        vel = 2.0
        playerDist = math.sqrt((g.player.x - self.x) * (g.player.x - self.x) + (g.player.z - self.z) * (g.player.z - self.z) )
        if playerDist == 0:
            dirX = 1
            dirZ = 0
        else:
            dirX = (g.player.x - self.x) / playerDist
            dirZ = (g.player.z - self.z) / playerDist
        
        self.velX = dirX
        self.velY = 0
        self.velZ = dirZ
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.duration = 10000.0
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        o = g.player
        dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
        distInRad = (self.radius + o.radius) - dist
        if distInRad > 0:
            o.hit((self.x, self.y, self.z))
            self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        
        self.duration -= g.dt
        if self.duration <= 0:
            g.stageObjects.remove(self)
            return
        
        return
        
    def draw(self):
        global BulletSaucerImg
        g.sortedSprites.append((BulletSaucerImg, self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return      
    
    
    
goblinRun = None
class Goblin:
    def __init__(self, pos):
        global goblinRun
        if goblinRun == None:
            img = g.pygame.image.load(os.path.join('img', 'goblin', 'run.png'))
            goblinRun = []
            self.curAnimFrames = 5
            for i in range(0, 5):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                goblinRun.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        self.curAnimFrames = 5
        self.curAnim = goblinRun
        self.radius = 88 * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        self.collide = True
        self.curAnimTimer = 0
        self.curAnimDuration = 100.0 * 5.0
        self.isEnemy = True
        self.hp = 3
        self.gravity = 0.007
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.maxVel = 2.2
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
        self.moveAccel = 0.05
        
    def tick(self):
        #playerDist = math.sqrt(\
        #(g.player.x - self.x) * (g.player.x - self.x) + \
        #(g.player.y - self.y) * (g.player.y - self.y) + \
        #(g.player.z - self.z) * (g.player.z - self.z)) - self.radius - g.player.radius
        #if playerDist <= 0:
        #    g.stageClear = True
        tickFrictionStop(self)
        if not self.attacking:
            self.nextAttack -=  g.dt
            if self.nextAttack <= 0:
                self.attacking = True
                self.nextAttack = random.uniform(100, 1000)
                self.shoot()
                self.attacking = False
        tickMove(self)
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['96'], self.x, self.y + self.radius, self.z))
        return
    
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3
    
    def shoot(self):
        if self.x > g.player.x + 1600:
            return;
        newObj = BulletGoblin((self.x, self.y, self.z), self)
        g.stageObjects.append(newObj)

def spawnGoblin(obj):
    newObj = Goblin((obj.x, obj.y))
    g.stageObjects.append(newObj)


class BulletGoblin:
    def __init__(self, pos, shooter):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        
        vel = 2.0
        playerDist = math.sqrt((g.player.x - self.x) * (g.player.x - self.x) + (g.player.z - self.z) * (g.player.z - self.z) )
        if playerDist == 0:
            dirX = 1
            dirZ = 0
        else:
            dirX = (g.player.x - self.x) / playerDist
            dirZ = (g.player.z - self.z) / playerDist
        
        self.velX = dirX
        self.velY = 0
        self.velZ = dirZ
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.duration = 10000.0
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        o = g.player
        dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
        distInRad = (self.radius + o.radius) - dist
        if distInRad > 0:
            o.hit((self.x, self.y, self.z))
            self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        
        self.duration -= g.dt
        if self.duration <= 0:
            g.stageObjects.remove(self)
            return
        
        return
        
    def draw(self):
        global BulletGoblinImg
        r = int((self.timer / 20.0) % 16)
        g.sortedSprites.append((BulletGoblinImg[r], self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return    


    
dinoriderRun = None
class Dinorider:
    def __init__(self, pos):
        global dinoriderRun
        if dinoriderRun == None:
            img = g.pygame.image.load(os.path.join('img', 'dinorider', 'run.png'))
            dinoriderRun = []
            self.curAnimFrames = 4
            for i in range(0, 4):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                dinoriderRun.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        self.curAnimFrames = 4
        self.curAnim = dinoriderRun
        self.radius = 98 * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        self.collide = True
        self.curAnimTimer = 0
        self.curAnimDuration = 100.0 * 4.0
        self.isEnemy = True
        self.hp = 3
        self.gravity = 0.007
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.maxVel = 2.2
        self.moveAccel = 0.05
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
    
    def tick(self):
        tickFrictionStop(self)
        if not self.attacking:
            self.nextAttack -=  g.dt
            if self.nextAttack <= 0:
                self.attacking = True
                self.nextAttack = random.uniform(100, 1000)
                self.shoot()
                self.attacking = False
        tickMove(self)
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['128'], self.x, self.y + self.radius, self.z))
        return
    
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3
    
    def shoot(self):
        if self.x > g.player.x + 1600:
            return;
        newObj = BulletDinorider((self.x, self.y, self.z), self)
        g.stageObjects.append(newObj)

def spawnDinorider(obj):
    newObj = Dinorider((obj.x, obj.y))
    g.stageObjects.append(newObj)
    
class BulletDinorider:
    def __init__(self, pos, shooter):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        
        vel = 2.0
        playerDist = math.sqrt((g.player.x - self.x) * (g.player.x - self.x) + (g.player.z - self.z) * (g.player.z - self.z) )
        if playerDist == 0:
            dirX = 1
            dirZ = 0
        else:
            dirX = (g.player.x - self.x) / playerDist
            dirZ = (g.player.z - self.z) / playerDist
        
        self.velX = dirX
        self.velY = 0
        self.velZ = dirZ
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.duration = 10000.0
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        o = g.player
        dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
        distInRad = (self.radius + o.radius) - dist
        if distInRad > 0:
            o.hit((self.x, self.y, self.z))
            self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        
        self.duration -= g.dt
        if self.duration <= 0:
            g.stageObjects.remove(self)
            return
        
        return
        
    def draw(self):
        global BulletDinoriderImg
        r = int((self.timer / 20.0) % 16)
        g.sortedSprites.append((BulletDinoriderImg[r], self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return    
    
    
    
    
    
plantmanRun = None
class Plantman:
    def __init__(self, pos):
        global plantmanRun
        if plantmanRun == None:
            img = g.pygame.image.load(os.path.join('img', 'plantman', 'run.png'))
            plantmanRun = []
            self.curAnimFrames = 6
            for i in range(0, 6):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                plantmanRun.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        self.curAnimFrames = 6
        self.curAnim = plantmanRun
        self.radius = 60 * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        self.collide = True
        self.curAnimTimer = 0
        self.curAnimDuration = 100.0 * 6.0
        self.isEnemy = True
        self.hp = 3
        self.gravity = 0.007
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.maxVel = 2.2
        self.moveAccel = 0.05
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
    
    def tick(self):
        tickFrictionStop(self)
        if not self.attacking:
            self.nextAttack -=  g.dt
            if self.nextAttack <= 0:
                self.attacking = True
                self.nextAttack = random.uniform(100, 1000)
                self.shoot()
                self.attacking = False
        tickMove(self)
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['96'], self.x, self.y + self.radius, self.z))
        return
        
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3
        
    def shoot(self):
        if self.x > g.player.x + 1600:
            return;
        newObj = BulletPlantman((self.x, self.y, self.z), self)
        g.stageObjects.append(newObj)
        

def spawnPlantman(obj):
    newObj = Plantman((obj.x, obj.y))
    g.stageObjects.append(newObj)

class BulletPlantman:
    def __init__(self, pos, shooter):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        
        vel = 2.0
        playerDist = math.sqrt((g.player.x - self.x) * (g.player.x - self.x) + (g.player.z - self.z) * (g.player.z - self.z) )
        if playerDist == 0:
            dirX = 1
            dirZ = 0
        else:
            dirX = (g.player.x - self.x) / playerDist
            dirZ = (g.player.z - self.z) / playerDist
        
        self.velX = dirX
        self.velY = 0
        self.velZ = dirZ
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.duration = 10000.0
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        o = g.player
        dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
        distInRad = (self.radius + o.radius) - dist
        if distInRad > 0:
            o.hit((self.x, self.y, self.z))
            self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        
        self.duration -= g.dt
        if self.duration <= 0:
            g.stageObjects.remove(self)
            return
        
        return
        
    def draw(self):
        global BulletPlantmanImg
        g.sortedSprites.append((BulletPlantmanImg, self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return


    
enemyblueRun = None
class EnemyBlue:
    def __init__(self, pos):
        global enemyblueRun
        if enemyblueRun == None:
            img = g.pygame.image.load(os.path.join('img', 'enemyblue', 'run.png'))
            enemyblueRun = []
            self.curAnimFrames = 3
            for i in range(0, 3):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                enemyblueRun.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        self.curAnimFrames = 3
        self.curAnim = enemyblueRun
        self.radius = 70 * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        self.collide = True
        self.curAnimTimer = 0
        self.curAnimDuration = 100.0 * 3.0
        self.isEnemy = True
        self.hp = 3
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
        self.gravity = 0.007
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.maxVel = 2.2
        self.moveAccel = 0.05
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
    
    def tick(self):
        tickFrictionStop(self)
        if not self.attacking:
            self.nextAttack -=  g.dt
            if self.nextAttack <= 0:
                self.attacking = True
                self.nextAttack = random.uniform(100, 1000)
                self.shoot()
                self.attacking = False
        tickMove(self)
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['96'], self.x, self.y + self.radius, self.z))
        return
        
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3
            
    def shoot(self):
        if self.x > g.player.x + 1600:
            return;    
        newObj = BulletEnemyBlue((self.x, self.y, self.z), self)
        g.stageObjects.append(newObj)

def spawnEnemyBlue(obj):
    newObj = EnemyBlue((obj.x, obj.y))
    g.stageObjects.append(newObj)

class BulletEnemyBlue:
    def __init__(self, pos, shooter):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        
        vel = 2.0
        playerDist = math.sqrt((g.player.x - self.x) * (g.player.x - self.x) + (g.player.z - self.z) * (g.player.z - self.z) )
        if playerDist == 0:
            dirX = 1
            dirZ = 0
        else:
            dirX = (g.player.x - self.x) / playerDist
            dirZ = (g.player.z - self.z) / playerDist
        
        self.velX = dirX
        self.velY = 0
        self.velZ = dirZ
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.duration = 10000.0
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        o = g.player
        dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
        distInRad = (self.radius + o.radius) - dist
        if distInRad > 0:
            o.hit((self.x, self.y, self.z))
            self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        
        self.duration -= g.dt
        if self.duration <= 0:
            g.stageObjects.remove(self)
            return
        
        return
        
    def draw(self):
        global BulletEnemyBlueImg
        g.sortedSprites.append((BulletEnemyBlueImg, self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return




class HitStar:
    def __init__(self, pos):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 8
        self.moveAccel = 0.05
        self.gravity = 0.005
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.duration = 1000
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.color = (255, nextRotatingTimer % 256, 0)
        return
    
    def tick(self):
        self.timer += g.dt
        self.duration -= g.dt
        if self.duration < 0:
            g.stageCosmetic.remove(self)
            return
        return
        
    def draw(self):
        points = []
        for i in range(10):
            ptRad = (i % 2) * 10 + 10
            ptAngle = math.radians(i * 360.0 / 10)
            ptAngle += self.timer * 0.005
            points.append([math.cos(ptAngle) * ptRad - g.scrollX + self.x, math.sin(ptAngle) * ptRad - g.scrollY + self.y + self.z])
        g.pygame.draw.polygon(g.screen, self.color, points, 0)
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['16'], self.x, self.y + self.radius, self.z))
        return

def spawnHitStar(self, hitPos):
    newObj = HitStar(hitPos)
    g.stageCosmetic.append(newObj)
    return



class HitSpark:
    def __init__(self, x, y, z):
        global nextRotatingTimer
        self.x = x
        self.y = y
        self.z = z
        self.radius = 8
        self.moveAccel = 0.05
        self.gravity = 0.002
        self.velX = random.uniform(-.4, .4)
        self.velY = random.uniform(-.8, .4)
        self.velZ = random.uniform(-.4, .4)
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.duration = 5000
        self.color = (255, nextRotatingTimer % 256, 0)
        nextRotatingTimer += 456.789
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            g.stageCosmetic.remove(self)
            return
            
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
        
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
            
        self.duration -= g.dt
        if self.duration < 0:
            g.stageCosmetic.remove(self)
            return
        return
        
    def draw(self):
        center = (self.x - g.scrollX, self.y + self.z - g.scrollY)
        g.pygame.draw.circle(g.screen, self.color, center, 4)
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['16'], self.x, self.y + self.radius, self.z))
        return

def explode(self):
    for i in range(30):
        randAngle = random.uniform(0, 360)
        randRadius = random.uniform(0, self.radius)
        randX = math.cos(randAngle) * randRadius
        randY = random.uniform(0, self.radius)
        randZ = math.sin(randAngle) * randRadius
        newObj = HitSpark(self.x + randX, self.y + randY, self.z + randZ)
        g.stageCosmetic.append(newObj)
    g.stageObjects.remove(self)
    return

def explodeSmall(self):
    for i in range(4):
        newObj = HitSpark(self.x, self.y, self.z)
        g.stageCosmetic.append(newObj)
    g.stageObjects.remove(self)
    return




skaterRun = None
class Skater:
    def __init__(self, pos):
        global skaterRun
        if skaterRun == None:
            img = g.pygame.image.load(os.path.join('img', 'skater', 'run.png'))
            skaterRun = []
            self.curAnimFrames = 14
            for i in range(0, 14):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                skaterRun.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        self.curAnimFrames = 14
        self.curAnim = skaterRun
        self.radius = 58 * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        self.collide = True
        self.curAnimTimer = 0
        self.curAnimDuration = 100.0 * 14.0
        self.isEnemy = True
        self.hp = 3
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
        self.gravity = 0.007
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.maxVel = 2.2
        self.moveAccel = 0.05
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
    
    def tick(self):
        tickFrictionStop(self)
        if not self.attacking:
            self.nextAttack -=  g.dt
            if self.nextAttack <= 0:
                self.attacking = True
                self.nextAttack = random.uniform(100, 1000)
                self.shoot()
                self.attacking = False
        tickMove(self)
        
                
        if g.bossScrollX == -1 :
            g.bossScrollX = self.x - 1200    
        
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['64'], self.x, self.y + self.radius, self.z))
        return
        
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            g.startStageClear = True
            explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3
            
    def shoot(self):
        if self.x > g.player.x + 1600:
            return;
        newObj = BulletSkater((self.x, self.y, self.z), self)
        g.stageObjects.append(newObj)

def spawnSkater(obj):
    newObj = Skater((obj.x, obj.y))
    g.stageObjects.append(newObj)

class BulletSkater:
    def __init__(self, pos, shooter):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        
        vel = 2.0
        playerDist = math.sqrt((g.player.x - self.x) * (g.player.x - self.x) + (g.player.z - self.z) * (g.player.z - self.z) )
        if playerDist == 0:
            dirX = 1
            dirZ = 0
        else:
            dirX = (g.player.x - self.x) / playerDist
            dirZ = (g.player.z - self.z) / playerDist
        
        self.velX = dirX
        self.velY = 0
        self.velZ = dirZ
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.duration = 10000.0
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        o = g.player
        dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
        distInRad = (self.radius + o.radius) - dist
        if distInRad > 0:
            o.hit((self.x, self.y, self.z))
            self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        
        self.duration -= g.dt
        if self.duration <= 0:
            g.stageObjects.remove(self)
            return
        return
        
    def draw(self):
        global BulletSkaterImg
        r = int((self.timer / 20.0) % 16)
        g.sortedSprites.append((BulletSkaterImg[r], self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return



squidRun = None
class Squid:
    def __init__(self, pos):
        global squidRun
        if squidRun == None:
            img = g.pygame.image.load(os.path.join('img', 'squid', 'run.png'))
            squidRun = []
            self.curAnimFrames = 8
            for i in range(0, 8):
                singleWidth = img.get_width() / self.curAnimFrames;
                frame = g.pygame.Surface((singleWidth, img.get_height()), g.pygame.SRCALPHA)
                frame.blit(img, (singleWidth * -i, 0))
                squidRun.append(\
                g.pygame.transform.scale(frame, (frame.get_width() * 6, frame.get_height() * 6)).convert_alpha(g.screen))
        self.curAnimFrames = 8
        self.curAnim = squidRun
        self.radius = 66 * 3/2
        self.x = pos[0]
        self.y = -self.radius
        self.z = pos[1]
        self.collide = True
        self.curAnimTimer = 0
        self.curAnimDuration = 100.0 * 8.0
        self.isEnemy = True
        self.hp = 3
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
        self.gravity = 0.007
        self.velX = 0.0
        self.velY = 0.0
        self.velZ = 0.0
        self.accelX = 0
        self.accelY = self.gravity
        self.accelZ = 0
        self.maxVel = 2.2
        self.moveAccel = 0.05
        self.attacking = False
        self.nextAttack = random.uniform(100, 1000)
        g.bossScrollX = self.x - 1400
    
    def tick(self):
        tickFrictionStop(self)
        if not self.attacking:
            self.nextAttack -=  g.dt
            if self.nextAttack <= 0:
                self.attacking = True
                self.nextAttack = random.uniform(100, 1000)
                self.shoot()
                self.attacking = False
        tickMove(self)
        return
    
    def draw(self):
        self.curAnimTimer += g.dt
        frameIdx = math.floor((self.curAnimTimer % self.curAnimDuration) * self.curAnimFrames / self.curAnimDuration)
        image = self.curAnim[frameIdx]
        g.sortedSprites.append((image, self.x, self.y, self.z))
        return
        
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['128'], self.x, self.y + self.radius, self.z))
        return
        
    def hit(self, hitPos):
        self.hp -= 1
        if self.hp <= 0:
            spawnHitStar(self, hitPos)
            g.bossScrollX = -1
            g.startStageClear = True
            explode(self)
        else:
            spawnHitStar(self, hitPos)
        pushDist = math.sqrt((self.x - hitPos[0]) * (self.x - hitPos[0]) + (self.z - hitPos[2]) * (self.z - hitPos[2]))
        pushX = (self.x - hitPos[0]) / pushDist
        pushZ = (self.z - hitPos[2]) / pushDist
        self.velX += pushX * 3
        self.velZ += pushZ * 3
            
    def shoot(self):
        if self.x > g.player.x + 1600:
            return;
        newObj = BulletSquid((self.x, self.y, self.z), self)
        g.stageObjects.append(newObj)

def spawnSquid(obj):
    newObj = Squid((obj.x, obj.y))
    g.stageObjects.append(newObj)

class BulletSquid:
    def __init__(self, pos, shooter):
        global nextRotatingTimer
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
        self.radius = 16
        self.moveAccel = 0.05
        self.gravity = 0.005
        
        vel = 2.0
        playerDist = math.sqrt((g.player.x - self.x) * (g.player.x - self.x) + (g.player.z - self.z) * (g.player.z - self.z) )
        if playerDist == 0:
            dirX = 1
            dirZ = 0
        else:
            dirX = (g.player.x - self.x) / playerDist
            dirZ = (g.player.z - self.z) / playerDist
        
        self.velX = dirX
        self.velY = 0
        self.velZ = dirZ
        self.accelX = 0
        self.accelY = 0
        self.accelZ = 0
        self.timer = nextRotatingTimer
        nextRotatingTimer += 456.789
        self.collide = False
        self.isEnemy = False
        self.duration = 10000.0
        return
    
    def breakBullet(self):
        explodeSmall(self)
        return
    
    def tick(self):
        avgVelX = self.velX + self.accelX * 0.5 * g.dt
        self.velX += self.accelX * g.dt
        deltaX = avgVelX * g.dt
        
        avgVelY = self.velY + self.accelY * 0.5 * g.dt
        self.velY += self.accelY * g.dt
        deltaY = avgVelY * g.dt
        
        if self.y + deltaY > - self.radius:
            deltaY = -self.y - self.radius
            self.velY = 0
            self.breakBullet()
            return
        
        o = g.player
        dist = math.sqrt(((self.x - o.x) * (self.x - o.x)) + ((self.y - o.y) * (self.y - o.y)) + ((self.z - o.z) * (self.z - o.z) * 2.0))
        distInRad = (self.radius + o.radius) - dist
        if distInRad > 0:
            o.hit((self.x, self.y, self.z))
            self.breakBullet()
        
        avgVelZ = self.velZ + self.accelZ * 0.5 * g.dt
        self.velZ += self.accelZ * g.dt
        deltaZ = avgVelZ * g.dt
    
        self.x += deltaX
        self.y += deltaY
        self.z += deltaZ
        self.timer += g.dt
        
        self.duration -= g.dt
        if self.duration <= 0:
            g.stageObjects.remove(self)
            return
        
        return
        
    def draw(self):
        global BulletSquidImg
        g.sortedSprites.append((BulletSquidImg, self.x, self.y, self.z))
        return
    
    def drawShadow(self):
        global shadowDict
        g.shadowSprites.append((shadowDict['32'], self.x, self.y + self.radius, self.z))
        return
