import os
import monkeglobals as g
import sys
import slides
import options
import title
import pytmx
from util_pygame import load_pygame
import gameObjects

colorOn = (255, 0, 0)
colorOff = (255, 255, 255)
backgroundName = '1'
backgroundImgDict = {}
stage = 1
escapeMenu = False
escapeMenuCursorPos = 0
stageAlpha = 0
stageFadingIn = True
stageFadingOut = False
tilemap = None

def getScreenY(y, z):
    return z/2 - y

def loadTilemap(filename):
    global tilemap
    tilemap = load_pygame(filename)
    
    #scale images 4x
    tilemap.tilewidth *= 4
    tilemap.tileheight *= 4
        
    for idx, image in enumerate(tilemap.images):
        if image != None:
            scaledImage = g.pygame.transform.scale(image, (image.get_width() * 4, image.get_height() * 4))
            tilemap.images[idx] = scaledImage

    pass

def goToStage1():
    global backgroundName
    global stage
    backgroundName = '1'
    stage = 1
    loadTilemap(os.path.join('tilemap', 'stage1.tmx'))
    initStage()
    pass

def goToStage2():
    global stage
    global backgroundName
    backgroundName = '2'
    stage = 2
    loadTilemap(os.path.join('tilemap', 'stage2.tmx'))
    initStage()
    pass
    
def goToStage3():
    global stage
    global backgroundName
    stage = 3
    backgroundName = '3'
    loadTilemap(os.path.join('tilemap', 'stage3.tmx'))
    initStage()
    pass
    
def drawTilemapBackground():
    global tilemap
    for layer in tilemap.visible_layers:
        if isinstance(layer, pytmx.TiledTileLayer):
            drawTileLayer(layer)
        elif isinstance(layer, pytmx.TiledObjectGroup):
            #drawObjectLayer(layer)
            pass
        elif isinstance(layer, pytmx.TiledImageLayer):
            drawImageLayer(layer)
    pass

def drawTileLayer(layer):
    global tilemap
    tw = tilemap.tilewidth
    th = tilemap.tileheight
    for x, y, image in layer.tiles():
        dstX = x * tw - g.scrollX
        dstY = y * th - g.scrollY
        g.screen.blit(image, (dstX, dstY))
        
    pass
    
def drawTilemapForeground():
    pass

def initStage():
    global tilemap
    g.tickFunction = tickStage
    if 'darkener' not in g.img:
        g.img['darkener'] = g.pygame.Surface((1920, 1080))
    global labelReturnOff
    global labelReturnOn
    labelReturnOff = g.fontSmall.render('Return to game', False, colorOff)
    labelReturnOn = g.fontSmall.render('Return to game', False, colorOn)
    
    global labelOptionsOff
    global labelOptionsOn
    labelOptionsOff = g.fontSmall.render('Options', False, colorOff)
    labelOptionsOn = g.fontSmall.render('Options', False, colorOn)
    
    global labelBackToMainOff
    global labelBackToMainOn
    labelBackToMainOff = g.fontSmall.render('Back to Main Menu', False, colorOff)
    labelBackToMainOn = g.fontSmall.render('Back to Main Menu', False, colorOn)
    
    g.keys['menuSelect'] = g.dt + 1
    escapeMenu = False
    stageFadingIn = True
    stageFadingOut = False
    stageAlpha = 0
    g.stageClear = False
    
    g.stageObjects = []
    
    spawnType = {}
    spawnType['player'] = gameObjects.spawnPlayer
    spawnType['saucer'] = gameObjects.spawnSaucer
    spawnType['goblin'] = gameObjects.spawnGoblin
    
    for layer in tilemap.visible_layers:
        if isinstance(layer, pytmx.TiledObjectGroup):
            for obj in layer:
                if obj.name in spawnType:
                    obj.x *= 4
                    obj.y *= 4
                    spawnType[obj.name](obj)
                else:
                    print(obj.name + ' not in spawner list')
    pass

def tickStage():
    global backgroundName
    global backgroundImgDict
    global escapeMenu
    global escapeMenuCursorPos
    global stageAlpha
    global stageFadingIn
    global stageFadingOut
    
#update fade
    if g.stageClear == True:
        stageFadingOut = True
    
    doTransition = False
    fadeSpeed = 1.0 / 1000.0
    if stageFadingIn:
        stageAlpha += g.dt * fadeSpeed
        if stageAlpha >= 1.0:
            stageAlpha = 1.0
            stageFadingIn = False
            
    if stageFadingOut:
        stageAlpha -= g.dt * fadeSpeed
        if stageAlpha <= 0:
            stageAlpha = 0
            stageFadingOut = False
            stageFadingIn = True
            doTransition = True
    
# check keys
    if g.keys['escape'] > 0 and g.keys['escape'] <= g.dt:
        escapeMenu = not escapeMenu
        escapeMenuCursorPos = 0
    
    if doTransition:
        if stage == 1:
            slides.goToSlidesStage2()
        elif stage == 2:
            slides.goToSlidesStage3()
        elif stage == 3:
            slides.goToSlidesEnding()
    
    if escapeMenu:
        if g.keys['up'] <= g.dt and g.keys['up'] > 0:
            escapeMenuCursorPos -= 1
            if escapeMenuCursorPos < 0:
                escapeMenuCursorPos = 2
                
        if g.keys['down'] <= g.dt and g.keys['down'] > 0:
            escapeMenuCursorPos += 1
            if escapeMenuCursorPos >= 3:
                escapeMenuCursorPos = 0
                
        if g.keys['menuSelect'] <= g.dt and g.keys['menuSelect'] > 0:
            if escapeMenuCursorPos == 0:
                escapeMenu = False
            elif escapeMenuCursorPos == 1:
                options.goToOptions()
                escapeMenu = False
                return
            elif escapeMenuCursorPos == 2:
                escapeMenu = False
                title.goToTitle()
                
    #if g.keys['jump'] > 0 and g.keys['jump'] <= g.dt:
    #    stageFadingIn = False
    #    stageFadingOut = True
    
    if not escapeMenu:
        for o in g.stageObjects:
            o.tick()

#draw
    

    if backgroundName not in backgroundImgDict:
        fileName = backgroundName + '.png'
        img = g.pygame.image.load(os.path.join('img', 'background', fileName))
        backgroundImgDict[backgroundName] = g.pygame.transform.scale(img, (1920, 1080)).convert(g.screen)
    g.screen.blit(backgroundImgDict[backgroundName], (0, 0))
    
    drawTilemapBackground()
    
#draw objects
    g.shadowSprites = []
    g.sortedSprites = []
    
    for o in g.stageObjects:
        o.drawShadow()
    for o in g.stageObjects:
        o.draw()
    
    g.sortedSprites.sort(key = lambda x: x[3])
    
    for s in g.shadowSprites:
        g.screen.blit(s[0], (s[1] - g.scrollX - s[0].width/2, getScreenY(s[2], s[3]) - g.scrollY - s[0].height / 2))
    for s in g.sortedSprites:
        g.screen.blit(s[0], (s[1] - g.scrollX - s[0].width/2, getScreenY(s[2], s[3]) - g.scrollY - s[0].height / 2))
    
    drawTilemapForeground()
    
#draw game UI
    
    if stageAlpha != 1:
        darkenerAlpha = 255 * (1 - stageAlpha)
        g.img['darkener'].set_alpha(darkenerAlpha)
        g.screen.blit(g.img['darkener'], (0, 0))
    
    if escapeMenu:
        g.img['darkener'].set_alpha(128)
        g.screen.blit(g.img['darkener'], (0, 0))
        g.screen.blit(labelReturnOn if escapeMenuCursorPos == 0 else labelReturnOff, (760, 450))
        g.screen.blit(labelOptionsOn if escapeMenuCursorPos == 1 else labelOptionsOff, (760, 500))
        g.screen.blit(labelBackToMainOn if escapeMenuCursorPos == 2 else labelBackToMainOff, (760, 550))
    
    pass