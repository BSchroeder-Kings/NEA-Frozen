import utils
import pygame

YAXISBUFFER = 30
XAXISBUFFER = 50
GROUNDY = 900 
SCREENHEIGHT = 1000
SCREENWIDTH = 1400
TEXTCOLOUR = (10,10,150)
CONTROLSX = 900

def runsim(results, timeslice):
    
    pygame.init()
    
    win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Free Fall Experiment")
    clock = pygame.time.Clock()
    clockspeed = 1 / float(timeslice)

    x = XAXISBUFFER
    y = YAXISBUFFER
    width = 30
    height = 30

    # main loop
    run = True
    currY= 0+YAXISBUFFER
    timeSlice=1
    scaleFactor = calcScale(results)
    lastDistance = results[len(results)-1][2]
    while run:
        win.fill((120, 155, 250)) #must be at start
        clock.tick(clockspeed)
        distanceDropped=results[timeSlice][2] #0time, 1velocity, 2distance
        currY=distanceDropped * scaleFactor
        time=results[timeSlice][0]
        velocity=results[timeSlice][1]
        CurrHeight = lastDistance - distanceDropped
        CurrHeight = round(CurrHeight, 4)
        velocity = round(velocity, 5)
        utils.windowtextprinter("Height", CurrHeight,"m", 500, 20, win)
        utils.windowtextprinter("time", time,"s", 500, 50, win)
        utils.windowtextprinter("velocity", velocity,"m/s", 500, 80, win)
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
        groundlevel = lastDistance + groundheight
        pygame.draw.rect(win, (75,75,150), (0, GROUNDY, SCREENWIDTH, SCREENHEIGHT - GROUNDY ))
        
        pygame.draw.rect(win, (255, 0, 0), (x, currY, width, height))
        pygame.display.update()
        if (timeSlice < len(results)-1):
            timeSlice=timeSlice+1
        if timeSlice >= len(results):
            run= True

    pygame.quit()
    return

def calcScale(results):
    lastDistance = results[len(results)-1][2]
    firstDistance = results[1][2]
    totaldistance = lastDistance - firstDistance
    fallzone = GROUNDY - YAXISBUFFER
    scalefactor = fallzone / totaldistance
    return scalefactor
    
def run_dummy():
    results=utils.LoadResults("result_fallingobject.txt")
    print(results)
    dummyruntimeslice = 0.025
    runsim(results, dummyruntimeslice)

if __name__=="__main__":
   run_dummy() 