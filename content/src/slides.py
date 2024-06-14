import os
import monkeglobals as g
import sys
import stage
import title

colorOn = (255, 0, 0)
colorOff = (255, 255, 255)
slideCurrent = None
slideImgDict = {}
slides = [\
    '1-1', '1-2', '1-3', '1-4', \
    '2-1', '2-2', '2-3',\
    '3-1', '3-2', '3-3', '3-4', '3-5', '3-6',\
    '4-1', '4-2', '4-3', '4-4', '4-5']

def goToSlidesStage1():
    global slideCurrent
    slideCurrent = '1-1'
    initSlides()
    pass
    
def initSlides():
    global labelNext
    labelNext = g.fontSmall.render('Z: next', False, colorOff)
    
    global labelClose
    labelClose = g.fontSmall.render('Z: close', False, colorOff)
    
    g.tickFunction = tickSlides
    g.keys['anykey'] = g.dt + 1
    tickSlides()
    pass

def goToSlidesStage2():
    global slideCurrent
    slideCurrent = '2-1'
    initSlides()
    pass

def goToSlidesStage3():
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
    
    # check keys 
    if g.keys['anykey'] > 0 and g.keys['anykey'] <= g.dt:
        if slideCurrent == '1-4':
            stage.goToStage1()
            return
        elif slideCurrent == '2-3':
            stage.goToStage2()
            return
        elif slideCurrent == '3-6':
            stage.goToStage3()
            return
        elif slideCurrent == '4-5':
            title.goToTitle()
            return
        else:
            curSlideIdx = slides.index(slideCurrent)
            curSlideIdx += 1
            slideCurrent = slides[curSlideIdx]
    
    anyKeyToClose = False
    if \
    slideCurrent == '1-4' or\
    slideCurrent == '2-3' or\
    slideCurrent == '3-6' or\
    slideCurrent == '4-5':
        anyKeyToClose = True;
    
    # draw
    if slideCurrent not in slideImgDict:
        fileName = slideCurrent + '.png'
        img = g.pygame.image.load(os.path.join('img', 'slides', fileName))
        slideImgDict[slideCurrent] = g.pygame.transform.scale(img, (1920, 1080))   
    g.screen.blit(slideImgDict[slideCurrent], (0, 0))
    
    
    g.screen.blit(labelClose if anyKeyToClose else labelNext, (1400, 1000))
    pass