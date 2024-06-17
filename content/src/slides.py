import os
import monkeglobals as g
import sys
import stage
import title

colorOn = (255, 0, 0)
colorOff = (255, 255, 255)
slideCurrent = None
slideImgDict = {}
slideAlpha = 0
slideFadingIn = True
slideFadingOut = False
slides = [\
    '1', '2', '3', '4', \
    '5', '6', '7',\
    '8', '9', '10', '11', '12', '13',\
    '14', '15', '16', '17', '18', '19', '20']

def goToSlidesStage1():
    global slideCurrent
    slideCurrent = '1'
    #g.pygame.mixer.music.load(os.path.join('music', 'cs127_-_the_destination.ogg'))
    #g.pygame.mixer.music.play(-1)
    g.musicTitle.fadeout(500)
    g.musicGame.play(-1, 0, 0)
    g.musicGame.set_volume(g.volMusic / 100.0)
    initSlides()
    pass
    
def initSlides():
    if 'darkener' not in g.img:
        g.img['darkener'] = g.pygame.Surface((1920, 1080))
    global labelNext
    labelNext = g.fontSmall.render('Z: next', False, colorOff)
    
    global labelClose
    labelClose = g.fontSmall.render('Z: close', False, colorOff)
    
    g.tickFunction = tickSlides
    g.keys['anykey'] = g.dt + 1
    slideFadingIn = True
    slideFadingOut = False
    slideAlpha = 0.0
    tickSlides()
    pass

def goToSlidesStage2():
    global slideCurrent
    slideCurrent = '5'
    initSlides()
    pass

def goToSlidesStage4():
    global slideCurrent
    slideCurrent = '8'
    initSlides()
    pass

def goToSlidesStage5():
    global slideCurrent
    slideCurrent = '10'
    initSlides()
    pass

def goToSlidesEnding():
    global slideCurrent
    slideCurrent = '14'
    initSlides()
    pass

def tickSlides():
    global slideCurrent
    global slideImgDict
    global slideFadingIn
    global slideFadingOut
    global slideAlpha
    
    # check keys 
    if g.keys['anykey'] > 0 and g.keys['anykey'] <= g.dt:
        if not slideFadingOut:
            ow = g.pygame.mixer.Sound(os.path.join('sfx', 'Select8-Bit.ogg'))
            ow.set_volume(g.volSound * 0.01 * 0.5)
            ow.play()
        slideFadingIn = False
        slideFadingOut = True
        
    anyKeyToClose = False
    if \
    slideCurrent == '4' or\
    slideCurrent == '7' or\
    slideCurrent == '9' or\
    slideCurrent == '13' or\
    slideCurrent == '19' or\
    slideCurrent == '20':
        anyKeyToClose = True;
    
    #update fade
    fadeSpeed = 5.0 / 1000.0
    if slideFadingIn:
        slideAlpha += g.dt * fadeSpeed
        if slideAlpha >= 1.0:
            slideAlpha = 1.0
            slideFadingIn = False
    
    if slideFadingOut:
        slideAlpha -= g.dt * fadeSpeed
        if slideAlpha <= 0:
            slideAlpha = 0
            slideFadingOut = False
            slideFadingIn = True
            if slideCurrent == '4':
                stage.goToStage1()
                return
            elif slideCurrent == '7':
                stage.goToStage2()
                return
            elif slideCurrent == '9':
                stage.goToStage4()
            elif slideCurrent == '13':
                stage.goToStage5()
                return
            elif slideCurrent == '20':
                title.goToTitle()
                return
            else:
                curSlideIdx = slides.index(slideCurrent)
                curSlideIdx += 1
                slideCurrent = slides[curSlideIdx]
    
    # draw
    curBG = '1'
    if stage.stage == 2:
        curBG = '2'
    elif stage.stage == 3:
        curBG = '3'
    elif stage.stage == 4:
        curBG = '4' 
    elif stage.stage == 5:
        curBG = '5'
        
    if curBG not in stage.backgroundImgDict:
        fileName = curBG + '.png'
        img = g.pygame.image.load(os.path.join('img', 'background', fileName))
        stage.backgroundImgDict[curBG] = g.pygame.transform.scale(img, (1920, 1080)).convert(g.screen)
    g.screen.blit(stage.backgroundImgDict[curBG], (0, 0))
    
    if slideCurrent not in slideImgDict:
        fileName = slideCurrent + '.png'
        img = g.pygame.image.load(os.path.join('img', 'slides', fileName))
        slideImgDict[slideCurrent] = g.pygame.transform.scale(img, (1920, 1080)).convert(g.screen)
        slideImgDict[slideCurrent].set_colorkey((0, 0, 0))
    g.screen.blit(slideImgDict[slideCurrent], (0, 0))
    
    g.screen.blit(labelClose if anyKeyToClose else labelNext, (1640, 1000))
    
    if slideAlpha != 1:
        darkenerAlpha = 255 * (1 - slideAlpha)
        g.img['darkener'].set_alpha(darkenerAlpha)
        g.screen.blit(g.img['darkener'], (0, 0))
    
    pass