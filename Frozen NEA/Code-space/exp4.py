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
    pygame.display.set_caption("Inelastic Collision Simulation")
    clock = pygame.time.Clock()
    clockspeed = 1 / float(timeslice)

    x = XAXISBUFFER
    y = YAXISBUFFER
    width1 = 30
    width2 = 30
    tallness1 = 30
    tallness2 = 30

    # main loop
    run = True
    currY= 0+YAXISBUFFER
    timeslice = int(timeslice)
    timeslice = 1
    scaleFactor = calcScale(results, width2)
    mass1 = results[0][6]
    mass2 = results[0][7]
    x1 = 0
    distance = results[0][5]
    distance = float(distance)
    x2 = distance
    floor1 = GROUNDY - tallness1
    floor2 = GROUNDY - tallness2
    pygame.draw.rect(win, utils.BLUE, (x1, floor1, width1, tallness1))
    pygame.draw.rect(win, utils.GREEN, (x2+width1, floor2, width2, tallness2))
    pygame.draw.rect(win, (75,75,150), (0, GROUNDY, SCREENWIDTH, SCREENHEIGHT - GROUNDY ))
    pygame.display.update()
    while run:
        clock.tick(clockspeed)
        win.fill((130, 150, 255))
        speed1 = results[timeslice][1]
        speed2 = results[timeslice][2]
        x1str = results[timeslice][3]
        x1str = float(x1str)
        x1 = x1str * scaleFactor
        x2str = results[timeslice][4]
        x2str = float(x2str)
        x2 = x2str * scaleFactor
        time=results[timeslice][0]
        utils.windowtextprinter("Block 1 Speed", speed1,"m/s", TEXTX, 20, win)
        utils.windowtextprinter("Block 2 Speed", speed2,"m/s", TEXTX, 50, win)
        utils.windowtextprinter("Time", time,"s", TEXTX, 80, win)
        utils.windowtextprinter("Mass1", mass1,"N", TEXTX, 110, win)
        utils.windowtextprinter("Mass2", mass2,"N", TEXTX, 140, win)
        utils.printpygamecontrols(CONTROLSX, 20,win)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
                    print("leaving simulation window")
                if event.key == pygame.K_a: 
                    timeslice = 0 #returns to 1 by next loop
                    print("replaying experiment")
        if currY >= GROUNDY:
            currY=GROUNDY
        pygame.draw.rect(win, (75,75,150), (0, GROUNDY, SCREENWIDTH, SCREENHEIGHT - GROUNDY ))
        pygame.draw.rect(win, utils.BLUE, (x1, floor1, width1, tallness1))
        pygame.draw.rect(win, utils.GREEN, (x2+width1, floor2, width2, tallness2))

        if (timeslice < len(results)-1):
            timeslice=timeslice+1
        if (timeslice >= len(results)-1):
            utils.windowothertextprinter("End of Simulation", utils.RED, SCREENWIDTH/2, SCREENHEIGHT/2, win)
        if (timeslice >= len(results)):
            run= True
        pygame.display.update()
    pygame.quit()
    return

def calcScale(results, width2):
    Distance = results[1][4]
    Screenwidthzone = SCREENWIDTH - XAXISBUFFER - width2*2
    scalefactor = Screenwidthzone / Distance
    return scalefactor
    
def run_dummy():
    results=utils.LoadResults("result_inelasticcollision.txt")
    print(results)
    dummyruntimeslice = 0.025
    runsim(results, dummyruntimeslice)

if __name__=="__main__":
   run_dummy() 