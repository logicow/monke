import os
import monkeglobals as g
import sys
import slides

backgroundName = '1'
backgroundImgDict = {}
stage = 1

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
    pass
    
def tickStage():
    global backgroundName
    global backgroundImgDict
    
# check keys
    if g.keys['escape'] > 0 and g.keys['escape'] <= g.dt:
        if stage == 1:
            slides.goToSlidesStage2()
        elif stage == 2:
            slides.goToSlidesStage3()
        elif stage == 3:
            slides.goToSlidesEnding()
        
#draw
    if backgroundName not in backgroundImgDict:
        fileName = backgroundName + '.png'
        img = g.pygame.image.load(os.path.join('img', 'background', fileName))
        backgroundImgDict[backgroundName] = g.pygame.transform.scale(img, (1920, 1080))   
    g.screen.blit(backgroundImgDict[backgroundName], (0, 0))
    pass