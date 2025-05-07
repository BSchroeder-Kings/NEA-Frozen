import utils
import pygame

YAXISBUFFER = 30
XAXISBUFFER = 0
GROUNDY = 900 
SCREENHEIGHT = 1000
SCREENWIDTH = 1400
TEXTCOLOUR = (10,10,150)
TEXTX = 800
CONTROLSX = 600

def runsim(results, timeslice):
    
    pygame.init()
    print ("Opening simulation window")
    win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Projectile Motion Experiment")
    clock = pygame.time.Clock()
    clockspeed = 1 / float(timeslice)

    x = XAXISBUFFER
    y = YAXISBUFFER
    width = 30
    tallness = 30

    # main loop
    run = True
    currY= 0+YAXISBUFFER
    timeSlice=1
    scaleFactor = calcScale(results)
    height = results[1][4]
    float(height)
    startheight = height
    while run:
        clock.tick(clockspeed)
        win.fill((130, 150, 255))
        height = results[timeSlice][4] #0elapsedtime,1totalvelocity,2forwardvelocity,3fallvelocity,4height,5distance
        float(height)
        heightcalc = startheight - height
        currY = heightcalc * scaleFactor
        distancetravelled = results[timeSlice][5]
        currX = distancetravelled * scaleFactor
        time=results[timeSlice][0]
        velocity=results[timeSlice][1]
        utils.windowtextprinter("Height", height,"m", TEXTX, 20, win)
        utils.windowtextprinter("Distance", distancetravelled,"m", TEXTX, 50, win)
        utils.windowtextprinter("Time", time,"s", TEXTX, 80, win)
        utils.windowtextprinter("Velocity", velocity,"m/s", TEXTX, 110, win)
        utils.printpygamecontrols(CONTROLSX, 20,win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    print("leaving simulation window")
                if event.key == pygame.K_a: 
                    timeSlice = 0 #returns to 1 by next loop
                    print("replaying experiment")
        if currY >= GROUNDY:
            currY=GROUNDY
        groundheight = 500
        groundlevel = startheight + groundheight
        pygame.draw.rect(win, (75,75,150), (0, GROUNDY, SCREENWIDTH, SCREENHEIGHT - GROUNDY ))

        pygame.draw.rect(win, (255, 0, 0), (currX, currY, width, tallness))
        pygame.display.update()
        if (timeSlice < len(results)-1):
            timeSlice=timeSlice+1
        if timeSlice >= len(results):
            run= True
        pygame.display.update()
    pygame.quit()
    return

def calcScale(results):
    lastHeight = results[1][4]
    fallzone = GROUNDY - YAXISBUFFER
    scalefactor = fallzone / lastHeight
    return scalefactor
    
def run_dummy():
    results=utils.LoadResults("result_projectilemotion.txt")
    print(results)
    dummyruntimeslice = 0.025
    runsim(results, dummyruntimeslice)

if __name__=="__main__":
   run_dummy() 