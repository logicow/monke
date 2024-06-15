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
    '1-1', '1-2', '1-3', '1-4', \
    '2-1', '2-2', '2-3',\
    '3-1', '3-2', '3-3', '3-4', '3-5', '3-6',\
    '4-1', '4-2', '4-3', '4-4', '4-5']

def goToSlidesStage1():
    global slideCurrent
    slideCurrent = '1-1'
    #g.pygame.mixer.music.load(os.path.join('music', 'cs127_-_the_destination.ogg'))
    #g.pygame.mixer.music.play(-1)
    g.musicTitle.fadeout(500)
    g.musicGame.play(-1, 0, 0)
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
    slideCurrent = '2-1'
    initSlides()
    pass

def goToSlidesStage5():
    global slideCurrent
    slideCurrent = '3-1'
    initSlides()
    pass

def goToSlidesEnding():
    global slideCurrent
    slideCurrent = '4-1'
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
        slideFadingIn = False
        slideFadingOut = True
    
    anyKeyToClose = False
    if \
    slideCurrent == '1-4' or\
    slideCurrent == '2-3' or\
    slideCurrent == '3-6' or\
    slideCurrent == '4-5':
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
            if slideCurrent == '1-4':
                stage.goToStage1()
                return
            elif slideCurrent == '2-3':
                stage.goToStage2()
                return
            elif slideCurrent == '3-6':
                stage.goToStage5()
                return
            elif slideCurrent == '4-5':
                title.goToTitle()
                return
            else:
                curSlideIdx = slides.index(slideCurrent)
                curSlideIdx += 1
                slideCurrent = slides[curSlideIdx]
    
    # draw
    if slideCurrent not in slideImgDict:
        fileName = slideCurrent + '.png'
        img = g.pygame.image.load(os.path.join('img', 'slides', fileName))
        slideImgDict[slideCurrent] = g.pygame.transform.scale(img, (1920, 1080)).convert(g.screen)
    g.screen.blit(slideImgDict[slideCurrent], (0, 0))
    
    g.screen.blit(labelClose if anyKeyToClose else labelNext, (1640, 1000))
    
    if slideAlpha != 1:
        darkenerAlpha = 255 * (1 - slideAlpha)
        g.img['darkener'].set_alpha(darkenerAlpha)
        g.screen.blit(g.img['darkener'], (0, 0))
    
    pass