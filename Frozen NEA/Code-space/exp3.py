import utils
import pygame
import math

YAXISBUFFER = 30
XAXISBUFFER = 30
GROUNDY = 900 
SCREENHEIGHT = 1000
SCREENWIDTH = 1800
TEXTCOLOUR = (10,10,150)
TEXTX = 800
CONTROLSX = 600

def runsim(results, timeslice):
    
    pygame.init()
    print ("Opening simulation window")
    win = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption("Block sliding down a slope")
    clock = pygame.time.Clock()
    clockspeed = 1 / float(timeslice)

    x = XAXISBUFFER
    y = YAXISBUFFER
    width = 30
    tallness = 30

    # main loop
    run = True
    currY= 0
    timeSlice=1
    scaleFactor = calcScale(results)
    angle = results[0][5]
    angle = float(angle)
    Mass = results[0][6]
    Mass = float(Mass)
    Acceleration = results [0][7]
    Acceleration = float(Acceleration)
    startY = 0 + YAXISBUFFER # REMEMBER TO CHANGE IF SCALE FACTOR WORK PROPER
    anglerad = utils.degreestoradians(angle)
    ENDX = math.cos(anglerad)*results[len(results)-1][3]*scaleFactor
    startline = (0,startY+tallness/2)
    endline = (ENDX-width/2, GROUNDY)
    while run:
        clock.tick(clockspeed)
        win.fill((130, 150, 255))
        distance = results[timeSlice][3] #0time,1BlockSpeed,2Resultantforce,3Distance
        float(distance)
        currY = math.sin(anglerad)*distance*scaleFactor+startY #sine(angle)*distance = adjacent
        currX = math.cos(anglerad)*distance*scaleFactor #cos(angle)*distance = opposite
        pygame.draw.line(win, TEXTCOLOUR, startline, endline,5)
        time=results[timeSlice][0]
        velocity=results[timeSlice][1]
        utils.windowtextprinter("Distance", distance,"m", TEXTX, 20, win)
        utils.windowtextprinter("Speed", velocity,"m/s", TEXTX, 50, win)
        utils.windowtextprinter("Time", time,"s", TEXTX, 80, win)
        utils.windowtextprinter("Mass", Mass,"N", TEXTX, 110, win)
        utils.windowtextprinter("Acceleration", Acceleration,"m/s²", TEXTX, 140, win)
        utils.printpygamecontrols(CONTROLSX, 20, win)
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
        if currY >= GROUNDY-tallness:
            currY=GROUNDY-tallness
            currX=ENDX-width/2
        
        pygame.draw.rect(win, (75,75,150), (0, GROUNDY, SCREENWIDTH, SCREENHEIGHT - GROUNDY ))

        pygame.draw.rect(win, (255, 0, 0), (currX, currY, width, tallness))
        if (timeSlice < len(results)-1):
            timeSlice=timeSlice+1
        if (timeslice >= len(results)-1):
            utils.windowothertextprinter("End of Simulation", utils.RED, SCREENWIDTH/2, SCREENHEIGHT/2, win)
        if timeSlice >= len(results):
            run= True
        pygame.display.update()
    
    pygame.quit()
    return

def calcScale(results):
    lastdist = results[len(results)-1][3]
    angle = results[0][5]
    angle = float(angle)
    anglerad = utils.degreestoradians(angle)
    height = math.sin(anglerad)*lastdist
    width = math.cos(anglerad)*lastdist
    fallzone = GROUNDY - YAXISBUFFER
    widthzone = SCREENWIDTH - XAXISBUFFER
    if angle<45:
        scalefactor = fallzone / height
    elif angle>=45:
        scalefactor = widthzone / width
    return scalefactor
    
def calcYstart(scalefactor, Y):
    if (Y*scalefactor>SCREENHEIGHT):
        placeholder= 0

def run_dummy():
    results=utils.LoadResults("result_blockonaslope.txt")
    print(results)
    dummyruntimeslice = 0.025
    runsim(results, dummyruntimeslice)

if __name__=="__main__":
   run_dummy() 