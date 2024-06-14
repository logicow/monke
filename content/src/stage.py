import os
import monkeglobals as g
import sys
import slides
import options
import title

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

def goToStage1():
    global backgroundName
    global stage
    backgroundName = '1'
    stage = 1
    initStage()
    pass

def goToStage2():
    global stage
    global backgroundName
    backgroundName = '2'
    stage = 2
    initStage()
    pass
    
def goToStage3():
    global stage
    global backgroundName
    stage = 3
    backgroundName = '3'
    initStage()
    pass

def initStage():
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
    stageClear = False
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
            stageClear = True
    
# check keys
    if g.keys['escape'] > 0 and g.keys['escape'] <= g.dt:
        escapeMenu = not escapeMenu
        escapeMenuCursorPos = 0
    
    if stageClear:
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

#draw
    if backgroundName not in backgroundImgDict:
        fileName = backgroundName + '.png'
        img = g.pygame.image.load(os.path.join('img', 'background', fileName))
        backgroundImgDict[backgroundName] = g.pygame.transform.scale(img, (1920, 1080))   
    g.screen.blit(backgroundImgDict[backgroundName], (0, 0))
    
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