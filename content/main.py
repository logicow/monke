import asyncio
import sys
import os
sys.path.insert(0, 'src')
import title
import monkeglobals as g
import gameObjects

def initDesktopWindow():
    g.screen = g.pygame.display.set_mode((1920, 1080))
    g.pygame.display.set_caption('Popsicle Pursuit')

def initWeb():
    g.screen = g.pygame.display.set_mode((1920, 1080))
    g.pygame.display.set_caption('Popsicle Pursuit')

def initMonke():
    g.img = {}
    g.pygame.font.init()
    g.fontSmall = g.pygame.font.Font('font/press-start.regular.ttf', 24)
    g.fontBase = g.pygame.font.Font('font/Quicksand_Book.otf', 90)
    g.keys = {}
    g.dt = 0
    g.volSound = 30
    g.volMusic = 30
    g.invulnerability = 0
    g.musicTitle = None
    g.musicGame = None
    g.musicGame2 = None
    g.playerHealthMax = 4
    g.pygame.mixer.init()
    gameObjects.initOnce()
    title.goToTitle()
    pass

def checkEvents():
    for event in g.pygame.event.get():
        if event.type == g.pygame.QUIT:
            g.tickFunction = None
            
def tickKeys():
    pressed = g.pygame.key.get_pressed()
    
    if pressed[g.pygame.K_z]:
        g.keys['jump'] += g.dt
    else:
        g.keys['jump'] = 0
        
    if pressed[g.pygame.K_x]:
        g.keys['attack'] += g.dt
    else:
        g.keys['attack'] = 0
        
    if pressed[g.pygame.K_RETURN] or pressed[g.pygame.K_SPACE]:
        g.keys['start'] += g.dt
    else:
        g.keys['start'] = 0
    
    if g.keys['jump'] > 0 or g.keys['start'] > 0:
        g.keys['anykey'] += g.dt
    else:
        g.keys['anykey'] = 0
    
    if pressed[g.pygame.K_UP]:
        g.keys['up'] += g.dt
    else:
        g.keys['up'] = 0
    
    if pressed[g.pygame.K_DOWN]:
        g.keys['down'] += g.dt
    else:
        g.keys['down'] = 0
    pass
    
    if pressed[g.pygame.K_LEFT]:
        g.keys['left'] += g.dt
    else:
        g.keys['left'] = 0
    
    if pressed[g.pygame.K_RIGHT]:
        g.keys['right'] += g.dt
    else:
        g.keys['right'] = 0
    pass
    
    if pressed[g.pygame.K_ESCAPE]:
        g.keys['escape'] += g.dt
    else:
        g.keys['escape'] = 0
    pass
    
    if g.keys['start'] > 0 or g.keys['jump'] > 0:
        g.keys['menuSelect'] += g.dt
    else:
        g.keys['menuSelect'] = 0
    
    if g.keys['attack'] > 0:
        g.keys['menuBack'] += g.dt
    else:
        g.keys['menuBack'] = 0

async def main():
    g.pygame.init()
    
    # You can initialise pygame here as well
    if sys.platform == "emscripten":
        initWeb()
    else:
        initDesktopWindow()
    initMonke()

    curTime = g.pygame.time.get_ticks()

    while g.tickFunction:
        newTime = g.pygame.time.get_ticks()
        g.dt = newTime - curTime
        curTime = newTime
        tickKeys()
        g.tickFunction()
        #if sys.platform != "emscripten":
        #    scale_window()
        g.pygame.display.update()
        await asyncio.sleep(0)
        checkEvents()
        
    # Closing the game (not strictly required)
    g.pygame.quit()
    sys.exit()
        
if __name__ == "__main__":
    asyncio.run(main())