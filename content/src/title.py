import pygame
import os
import monkeglobals as g
import sys
import options
import slides

pressStartTimer = 0
colorOn = (0, 0, 196)
colorOff = (255, 255, 255)
mainMenuSelection = 0
titleMusicTimer = 0

def goToTitle():
    if 'title' not in g.img:
        imgTitle = pygame.image.load(os.path.join('img', 'title.png'))
        g.img['title'] = pygame.transform.scale(imgTitle, (1920, 1080)).convert(g.screen)
    
    global titlePressStart
    titlePressStart = g.fontBase.render('Press Start', False, (255, 255, 255))
    
    global titlePlayOn
    global titlePlayOff
    labelPlayOnTemp = g.fontBase.render('Play', False, colorOn)
    titlePlayOn = g.pygame.Surface((labelPlayOnTemp.get_width(), labelPlayOnTemp.get_height()))
    titlePlayOn.fill((255, 255, 255))
    titlePlayOn.blit(labelPlayOnTemp, (0, 0))
    titlePlayOff = g.fontBase.render('Play', False, colorOff)
    
    global titleOptionsOn
    global titleOptionsOff
    labelOptionsOnTemp = g.fontBase.render('Settings', False, colorOn)
    titleOptionsOn = g.pygame.Surface((labelOptionsOnTemp.get_width(), labelOptionsOnTemp.get_height()))
    titleOptionsOn.fill((255, 255, 255))
    titleOptionsOn.blit(labelOptionsOnTemp, (0, 0))
    titleOptionsOff = g.fontBase.render('Settings', False, colorOff)
    
    global titleQuitOn
    global titleQuitOff
    titleQuitOnTemp = g.fontBase.render('Quit', False, colorOn)
    titleQuitOn = g.pygame.Surface((titleQuitOnTemp.get_width(), titleQuitOnTemp.get_height()))
    titleQuitOn.fill((255, 255, 255))
    titleQuitOn.blit(titleQuitOnTemp, (0, 0))
    titleQuitOff = g.fontBase.render('Quit', False, colorOff)
    
    global labelAccept
    labelAccept = g.fontSmall.render('Z: select', False, colorOff)
    
    g.tickFunction = title
    g.debugString = None
    
    global titleMusicTimer
    if(g.musicGame):
        g.musicGame.fadeout(1000)
    else:
        g.musicGame = g.pygame.mixer.Sound(os.path.join('sfx', 'cs127_-_the_destination.ogg'))
    if(g.musicGame2):
        g.musicGame2.fadeout(1000)
    else:
        g.musicGame2 = g.pygame.mixer.Sound(os.path.join('sfx', 'DOPE.ogg'))
    if not g.musicTitle:
        g.musicTitle = g.pygame.mixer.Sound(os.path.join('sfx', 'biker_mice_from_mars_-_circuit.ogg'))
    titleMusicTimer = 0

def title():
    global titleMusicTimer
    titleMusicTimerOld = titleMusicTimer
    titleMusicTimer += g.dt
    if(titleMusicTimer >= 200 and titleMusicTimerOld < 200):
        print("playing music")
        g.musicTitle.play(-1, 0, 0)
        g.musicTitle.set_volume(g.volMusic / 100.0)

    # check keys
    if g.keys['anykey'] > 0 and g.keys['anykey'] <= g.dt:
        g.tickFunction = titleMenu
        g.keys['menuSelect'] = g.dt + 1
        titleMenu()
        ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Confirm8-Bit.ogg'))
        ow.set_volume(g.volSound * 0.01 * 0.5)
        ow.play()
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
        g.screen.blit(titlePressStart, (700,860))
    
    pass
    
def titleMenu():
    global mainMenuSelection
    global titlePlayOn
    global titlePlayOff
    global titleOptionsOn
    global titleOptionsOff
    global titleQuitOn
    global titleQuitOff
    global titleMusicTimer
    
    numMenuOptions = 3
    if sys.platform == "emscripten":
        numMenuOptions = 2
    
    # check keys
    if g.keys['up'] <= g.dt and g.keys['up'] > 0:
        mainMenuSelection -= 1
        ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Select8-Bit.ogg'))
        ow.set_volume(g.volSound * 0.01 * 0.5)
        ow.play()
        if mainMenuSelection < 0:
            mainMenuSelection = 2
            
    if g.keys['down'] <= g.dt and g.keys['down'] > 0:
        mainMenuSelection += 1
        ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Select8-Bit.ogg'))
        ow.set_volume(g.volSound * 0.01 * 0.5)
        ow.play()
        if mainMenuSelection >= numMenuOptions:
            mainMenuSelection = 0
    
    if g.keys['escape']:
        if sys.platform != "emscripten":
            g.tickFunction = None
            return
    
    if g.keys['menuSelect'] <= g.dt and g.keys['menuSelect'] > 0:
        ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Confirm8-Bit.ogg'))
        ow.set_volume(g.volSound * 0.01 * 0.5)
        ow.play()
        if mainMenuSelection == 0:
            slides.goToSlidesStage1()
        if mainMenuSelection == 1:
            options.goToOptions()
            return
        if mainMenuSelection == 2:
            g.tickFunction = None
    
    # draw
    g.screen.blit(g.img['title'], (0, 0))
    g.screen.blit(titlePlayOn if mainMenuSelection == 0 else titlePlayOff, (1300,400))
    g.screen.blit(titleOptionsOn if mainMenuSelection == 1 else titleOptionsOff, (1300,500))
    if numMenuOptions >= 3:
        g.screen.blit(titleQuitOn if mainMenuSelection == 2 else titleQuitOff, (1300,600))
        
    g.screen.blit(labelAccept, (1640, 1000))
    pass