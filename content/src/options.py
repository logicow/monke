import pygame
import os
import monkeglobals as g
import sys

colorOn = (255, 255, 255)
colorOff = (0xab, 0x51, 0x30)
optionsSelection = 0
returnTo = None

def goToOptions():
    global returnTo
    returnTo = g.tickFunction
    
    if 'options' not in g.img:
        img = pygame.image.load(os.path.join('img', 'options.png'))
        g.img['options'] = pygame.transform.scale(img, (1920, 1080)).convert(g.screen)

    global labelAccept
    labelAccept = g.fontSmall.render('Z: select   X: back', False, (255, 255, 255))
    
    g.tickFunction = options
    g.keys['menuSelect'] = g.dt + 1
    optionsSelection = 0
    options()
    pass

def options():
    global returnTo
    global optionsSelection
    # check keys 
    if g.keys['menuBack']:
        g.tickFunction = returnTo
        g.tickFunction()
        ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Cancel8-Bit.ogg'))
        ow.set_volume(g.volSound * 0.01 * 0.5)
        ow.play()
        return
    
    if g.keys['up'] <= g.dt and g.keys['up'] > 0:
        optionsSelection -= 1
        ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Select8-Bit.ogg'))
        ow.set_volume(g.volSound * 0.01 * 0.5)
        ow.play()
        if optionsSelection < 0:
            optionsSelection = 3
            
    if g.keys['down'] <= g.dt and g.keys['down'] > 0:
        optionsSelection += 1
        ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Select8-Bit.ogg'))
        ow.set_volume(g.volSound * 0.01 * 0.5)
        ow.play()
        if optionsSelection >= 4:
            optionsSelection = 0
    
    if g.keys['left'] <= g.dt and g.keys['left'] > 0:
        if optionsSelection == 0:
            g.volSound -= 10
            if g.volSound < 0:
                g.volSound = 0
        if optionsSelection == 1:
            g.volMusic -= 10
            if g.volMusic < 0:
                g.volMusic = 0
        if optionsSelection == 2:
            g.invulnerability = not g.invulnerability
    
    if g.keys['right'] <= g.dt and g.keys['right'] > 0:
        if optionsSelection == 0:
            g.volSound += 10
            if g.volSound > 100:
                g.volSound = 100
        if optionsSelection == 1:
            g.volMusic += 10
            if g.volMusic > 100:
                g.volMusic = 100
        if optionsSelection == 2:
            g.invulnerability = not g.invulnerability
    
    if g.keys['menuSelect'] <= g.dt and g.keys['menuSelect'] > 0:
        g.keys['menuSelect'] = g.dt + 1
        if optionsSelection == 2:
            g.invulnerability = not g.invulnerability
        if optionsSelection == 3:
            g.tickFunction = returnTo
            g.tickFunction()
            ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Confirm8-Bit.ogg'))
            ow.set_volume(g.volSound * 0.01 * 0.5)
            ow.play()
            return
    
    g.musicTitle.set_volume(g.volMusic / 100.0)
    g.musicGame.set_volume(g.volMusic / 100.0)
    g.musicGame2.set_volume(g.volMusic / 100.0)
    
    # draw
    g.screen.blit(g.img['options'], (0, 0))
    
    volSoundString = 'Sound Volume: '
    volSoundString += str(g.volSound)
    labelVolSound = g.fontSmall.render(volSoundString, False, colorOn if optionsSelection == 0 else colorOff)
    g.screen.blit(labelVolSound, (950, 450))
    
    volMusicString = 'Music Volume: '
    volMusicString += str(g.volMusic)
    labelVolMusic = g.fontSmall.render(volMusicString, False, colorOn if optionsSelection == 1 else colorOff)
    g.screen.blit(labelVolMusic, (950, 500))
    
    invulString = 'Invulnerability: '
    invulString += 'On' if g.invulnerability else 'Off'
    labelInvul = g.fontSmall.render(invulString, False, colorOn if optionsSelection == 2 else colorOff)
    g.screen.blit(labelInvul, (950, 550))
    
    backString = 'Back'
    labelBack = g.fontSmall.render(backString, False, colorOn if optionsSelection == 3 else colorOff)
    g.screen.blit(labelBack, (950, 650))
    
    g.screen.blit(labelAccept, (1400, 1000))
    pass