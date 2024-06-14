import pygame
import os
import monkeglobals as g
import sys

pressStartTimer = 0
colorOn = (255, 0, 0)
colorOff = (255, 255, 255)
mainMenuSelection = 0

def goToTitle():
    g.title = {}
    if 'title' not in g.img:
        imgTitle = pygame.image.load(os.path.join('img', 'title.png'))
        g.img['title'] = pygame.transform.scale(imgTitle, (1920, 1080))
    
    fontBase = pygame.font.SysFont('Comic Sans MS', 90)
    
    global titlePressStart
    titlePressStart = fontBase.render('Press Start', False, (255, 255, 255))
    
    global titlePlayOn
    global titlePlayOff
    titlePlayOn = fontBase.render('Play', False, colorOn)
    titlePlayOff = fontBase.render('Play', False, colorOff)
    
    global titleOptionsOn
    global titleOptionsOff
    titleOptionsOn = fontBase.render('Options', False, colorOn)
    titleOptionsOff = fontBase.render('Options', False, colorOff)
    
    global titleQuitOn
    global titleQuitOff
    titleQuitOn = fontBase.render('Quit', False, colorOn)
    titleQuitOff = fontBase.render('Quit', False, colorOff)
    
    g.tickFunction = title

def title():
    # check keys
    if(g.keys['anykey'] > 0):
        g.tickFunction = titleMenu
        titleMenu()
        return
        
    if g.keys['escape']:
        if sys.platform != "emscripten":
            g.tickFunction = None

    # draw
    global pressStartTimer
    g.screen.blit(g.img['title'], (0, 0))
    
    pressStartTimer += g.dt
    pressStartVisible = (pressStartTimer / 300.0) % 2
    if pressStartVisible >= 1:
        g.screen.blit(titlePressStart, (700,820))
    
    pass
    
def titleMenu():
    global mainMenuSelection
    global titlePlayOn
    global titlePlayOff
    global titleOptionsOn
    global titleOptionsOff
    global titleQuitOn
    global titleQuitOff
    
    numMenuOptions = 3
    if sys.platform == "emscripten":
        numMenuOptions = 2
    
    # check keys
    if g.keys['up'] <= g.dt and g.keys['up'] > 0:
        mainMenuSelection -= 1
        if mainMenuSelection < 0:
            mainMenuSelection = 2
            
    if g.keys['down'] <= g.dt and g.keys['down'] > 0:
        mainMenuSelection += 1
        if mainMenuSelection >= numMenuOptions:
            mainMenuSelection = 0
    
    if g.keys['escape']:
        if sys.platform != "emscripten":
            g.tickFunction = None
    
    if g.keys['menuSelect']:
        if mainMenuSelection == 2:
            g.tickFunction = None
    
    # draw
    g.screen.blit(g.img['title'], (0, 0))
    g.screen.blit(titlePlayOn if mainMenuSelection == 0 else titlePlayOff, (800,700))
    g.screen.blit(titleOptionsOn if mainMenuSelection == 1 else titleOptionsOff, (800,800))
    if numMenuOptions >= 3:
        g.screen.blit(titleQuitOn if mainMenuSelection == 2 else titleQuitOff, (800,900))
    pass