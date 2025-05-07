
# All time related vars are in seconds unless commented otherwise
import re
import math
import utils
import exp1
import exp2
import exp3
import exp4

P_FALLOBJ="param_fallingobject.txt"
P_PROJMOT="param_projectilemotion.txt"
P_SLOPE="param_blockonaslope.txt"
P_COLLISION="param_inelasticcollision.txt"
TIMESLICE=0.025
RUNTIMEMAX=20
TIMESEGMENTS=int(RUNTIMEMAX/TIMESLICE) # how many counts the program can run for, determined by: Runtime lim (s)/ seconds per reading
SCREENSIZE = (720, 720)
NICEBLUE = (60, 100, 170)
REGEXFLOATORINTMAYBEZERO = "[1-9]?.[1-9]?"
REGEXFLOATORINT = "[1-9]+.[1-9]?"

# Base SI units are used
# Experiments

def Exp_FallingObj(param):
    elapsedtime=0.0 #time since start of simulation
    velocity=0.0 
    falldistance=0.0 #distance travelled from start point
    height = param["height"] # loads start height from file
    gravity = param["gravity"] # loads gravitational acceleration from file
    if gravity == 0:
        gravity = 9.81
    results=[] 
    results.append(["time", "velocity", "distance"]) #initial values to table
    for i in range (1, TIMESEGMENTS):
        elapsedtime = i*TIMESLICE #loop 
        elapsedtime = round(elapsedtime, 10)       
        velocity = gravity*elapsedtime # speed = acceleration*time
        velocity = round(velocity, 5)

        falldistance = velocity*elapsedtime # distance = speed*time
        falldistance = round(falldistance, 5)
 
        if (falldistance > height): #End condition, fix results
            falldistance = height
            velocity=0.0
        results.append([elapsedtime, velocity, falldistance]) #Sends results to list

        if (falldistance == height): #End Condition
            break
    utils.SaveResults("result_fallingobject.txt", results)    
    return results

# airresistance is modelled as a deceleration (in m/s) that doesn't effect gravity, however the value of gravity could be made to account for air resistance

def Exp_ProjectileMotion(param):
    totalvelocity = 0
    elapsedtime = 0
    distance = 0
    verticaldisplacement = 0 # Distance from start height # how many counts the program can run for, determined by: Runtime lim (s)/ the readings per second
    fallheight = param["height"] # start height
    height = fallheight # Current height
    gravity = param["gravity"] # gravitational acceleration
    if gravity == 0:
        gravity = 9.81
    forwardvelocity = param["forwardvelocity"] # forward speed
    fallvelocity = param["fallvelocity"] # downward speed
    fallvelocity = fallvelocity
    airresistance = param["airresistance"] # deceleration due to air resistance
    if airresistance > gravity:
        airresistance = 0
    totalvelocity = forwardvelocity + fallvelocity # sum of fall and forward velocities
    results=[]
    results.append(["elapsedtime", "totalvelocity", "forwardvelocity", "fallvelocity", "height", "distance",]) #init val to table
    for i in range (1, TIMESEGMENTS): # main loop
        elapsedtime = i*TIMESLICE #time
        elapsedtime = round(elapsedtime, 10) # removes binary rounding errors

        if (airresistance > 0 and height > 0): # air resistance deceleration calculations
            forwardvelocity = forwardvelocity - airresistance*TIMESLICE
            feltacceleration = gravity - airresistance
            height = fallheight - 0.5*feltacceleration*elapsedtime*elapsedtime
            fallvelocity = gravity*elapsedtime - airresistance*elapsedtime
            if (forwardvelocity < 0): # stops forward velocity from becoming a negative value
                forwardvelocity = 0

        if (airresistance == 0 and height > 0):
            fallvelocity = elapsedtime * gravity
            height = fallheight - 0.5*gravity*elapsedtime*elapsedtime # s=ut+0.5at^2 from the start of the experiment to increase accuracy
            totalvelocity = fallvelocity + forwardvelocity
            
        if (height > 0 and forwardvelocity > 0):
            distance = distance + forwardvelocity*TIMESLICE
        height = round(height, 5)
        forwardvelocity = round(forwardvelocity, 5)
        verticaldisplacement = round(verticaldisplacement, 5)
        fallvelocity = round(fallvelocity, 5)
        totalvelocity = round(totalvelocity, 5)
        distance = round(distance, 5)
        
        # end loop
        if (height < 0):
            height = 0
            fallvelocity = 0
            forwardvelocity = 0
        results.append([elapsedtime, totalvelocity, forwardvelocity, fallvelocity, height, distance])
        if (height == 0):
            break
    utils.SaveResults("result_projectilemotion.txt", results)  
    return results

def Exp_BlockOnASlope(param):
    elapsedtime=0
    angle = param ["Angle"]
    gravity = param ["Gravity"]
    resistance = param ["Resistance"]
    mass = param ["Mass"]
    distancetotravel = param ["Distancetotravel"]
    results=[]
    sinangle = utils.degreestoradians(angle)
    force = gravity*mass*sinangle
    resultantforce = force - resistance
    resultantforce = round(resultantforce, 6)
    distance = 0
    if resultantforce <= 0:
        resultantforce = 0
    Acceleration = resultantforce / mass
    results.append(["time", "BlockSpeed", "Resultantforce", "Distance", "Extra info->", angle, mass,Acceleration]) # adds names to params
    for i in range (1, TIMESEGMENTS):
        elapsedtime = i*TIMESLICE #loop 
        elapsedtime = round(elapsedtime, 10)
        speed = Acceleration*elapsedtime
        speed = round(speed, 6)
        distance = distance+speed*TIMESLICE
        distance = round(distance, 6)
        results.append([elapsedtime, speed, resultantforce, distance])
        if distance >= distancetotravel:
            utils.SaveResults("result_blockonaslope.txt", results)
            return results
        if resultantforce == 0:
            utils.SaveResults("result_blockonaslope.txt", results)
            return results
    utils.SaveResults("result_blockonaslope.txt", results)  
    return results

def Exp_InelasticCollision(param):
    elapsedtime=0
    mass1 = param["Mass1"]
    mass2 = param["Mass2"]
    speed1 = param["Speed1"]
    speed2 = param["Speed2"]
    distance = 2 * speed1 + 2 * speed2 #3 seconds till collision
    speedtotal = speed1 + speed2
    speedratio = speed1 / speedtotal
    inertia1 = mass1*speed1*speed1
    inertia2 = mass2*speed2*speed2
    speed2 = 0 - speed2
    x1 = 0  #x axis of block 1
    x2=distance #x axis of block 2,
    #^(referenced from the part of the block that will collide with the other block)
    # maybe calculate exact point of collision: x1/(x1+x2)*D
    collisionpoint = distance*speedratio
    results=[]
    results.append(["time", "Speed1", "Speed2", "x1", "x2", distance, mass1, mass2])
    collision = False
    timesincecollision = 0.0
    for i in range (1, TIMESEGMENTS):
        elapsedtime = i*TIMESLICE #loop 
        elapsedtime = round(elapsedtime, 10)
        x1 = x1 + speed1*TIMESLICE
        x2 = x2 + speed2*TIMESLICE# speed2 is negative for first bit
        x1 = round(x1, 5)
        x2 = round(x2, 5)
        if (collision == False and x1>=x2):
            collision = True
            x1 = collisionpoint
            x2 = collisionpoint
            speedcalc = inertia1 - inertia2
            masstotal = mass1+mass2
            speedcalc2 = speedcalc/masstotal
            speed1 = speedcalc2 / speed1 
            speed1 = round (speed1, 5)
            speed2 = speed1

        if collision == True:
            timesincecollision = timesincecollision + TIMESLICE
            if timesincecollision >= 3:
                results.append([elapsedtime, speed1, speed2, x1, x2])
                utils.SaveResults("result_inelasticcollision.txt", results) 
                return results
        results.append([elapsedtime, speed1, speed2, x1, x2])
        utils.SaveResults("result_inelasticcollision.txt", results) 


def Menu_FallingObjSEL():
    print()
    numint = 0
    while numint == 0:
        para = utils.Loadparameters(P_FALLOBJ)
        Menu_FallingObj()
        back = False
        numint = utils.menuinputvalidation(utils.REGEX3OPMENU)
        if numint == 1:
            para = utils.Loadparameters(P_FALLOBJ)
            results = Exp_FallingObj(para)
            back = False
            while back == False:
                simnum = post1stinstanceoptionsSEL() #numbers compile then options come up
                if simnum == 1: # loads pygame simulation model
                    exp1.runsim(results,TIMESLICE)
                if simnum == 2: # prints result table
                    utils.printresults(results)
                if simnum == 3: # back
                    back = True
                    numint = 0
                if simnum == 9: # quits program
                    numint = 9
                    back = True

        if numint == 2: #change paras
            utils.ChangeParameters(P_FALLOBJ)
            numint = 0
        if numint == 3: #back
            return False
        if numint == 9:
            return True

def Menu_ProjectileMotionSEL():
    numint = 0
    while numint == 0:
        Menu_ProjectileMotion()
        para=utils.Loadparameters(P_PROJMOT)
        results=Exp_ProjectileMotion(para)
        back = False
        numint = utils.menuinputvalidation(utils.REGEX3OPMENU)
        if numint == 1:
            while back == False:
                simnum = post1stinstanceoptionsSEL() #numbers compile then options come up
                if simnum == 1: # loads pygame simulation model
                    exp2.runsim(results, TIMESLICE)
                if simnum == 2: # prints result table
                    utils.printresults(results)
                if simnum == 3: # back
                    back = True
                    numint = 0
                elif simnum == 9: # quits program
                    numint = 9
                    back = True

        if numint == 2: #change paras
            utils.ChangeParameters(P_PROJMOT)
            numint=0
        if numint == 3: #back
            return False
        if numint == 9:
            return True

def Menu_BlockOnASlopeSEL():
    numint = 0
    while numint == 0:
        Menu_BlockOnASlope()
        para=utils.Loadparameters(P_SLOPE)
        results=Exp_BlockOnASlope(para)
        back = False
        numint = utils.menuinputvalidation(utils.REGEX3OPMENU)
        if numint == 1:
            while back == False:
                simnum = post1stinstanceoptionsSEL() #numbers compile then options come up
                if simnum == 1: # loads pygame simulation model
                    exp3.runsim(results ,TIMESLICE)
                if simnum == 2: # prints result table
                    utils.printresults(results)
                if simnum == 3: # back
                    back = True
                    numint = 0
                if simnum == 9: # quits program
                    numint = 9
                    back = True

        if numint == 2: #change paras
            utils.ChangeParameters(P_SLOPE)
            numint=0
        if numint == 3: #back
            return False
        if numint == 9:
            return True

def Menu_InelasticCollisionSEL():
    numint = 0
    while numint == 0:
        Menu_InelasticCollision()
        para=utils.Loadparameters(P_COLLISION)
        results=Exp_InelasticCollision(para)
        back = False
        numint = utils.menuinputvalidation(utils.REGEX3OPMENU)
        if numint == 1:
            while back == False:
                simnum = post1stinstanceoptionsSEL() #numbers compile then options come up
                if simnum == 1: # loads pygame simulation model
                    exp4.runsim(results,TIMESLICE)
                if simnum == 2: # prints result table
                    utils.printresults(results)
                if simnum == 3: # back
                    back = True
                    numint = 0
                elif simnum == 9: # quits program
                    numint = 9
                    back = True

        if numint == 2: #change paras
            utils.ChangeParameters(P_COLLISION)
            numint=0
        if numint == 3: #back
            return False
        if numint == 9:
            return True

def paramprint(file):
    para = []
    para = utils.Loadparameters(file)
    print (para)
    

def mainmenu():
    print ("-----=====-----")
    print ("Experiments:")
    print ("(1) Free Fall")
    print ("(2) Projectile Motion")
    print ("(3) Block on a slope") 
    print ("(4) Inelastic Collision")

    print ("(9) Quit")
    print ("-----=====-----")

def post1stinstanceoptions():
    print ("-----=====-----")
    print("Options:")
    print("(1) Continue To Model")
    print("(2) Results Table")
    print("(3) Back")
    print("")
    print("(9) Quit ")
    print ("-----=====-----")

def post1stinstanceoptionsSEL():
    post1stinstanceoptions()
    numint = 0
    numint = utils.menuinputvalidation(utils.REGEX3OPMENU)
    numcorrect = False
    while numcorrect == False:
        if (numint == 1):
            return 1
        if (numint == 2):
            return 2
        if (numint == 3):
            return 3
        if (numint == 9):
            return 9
        else:
            print("input validation error")
            numcorrect = True
            return 3



def PracticalMenuOptions():
    print("Options:")
    print("(1) Continue To Simulation")
    print("(2) Change Parameters")
    print("(3) Back")
    print("")
    print("(9) Quit")

def Menu_FallingObj():
    print ("-----=====-----")
    print("A model of a Free Falling block which accelerates toward the ground under gravity.")
    print("")
    print("Parameters:")
    paramprint(P_FALLOBJ)
    print("")
    PracticalMenuOptions()
    print ("-----=====-----")


def Menu_ProjectileMotion():
    print ("-----=====-----")
    print("A model of a block being launched under gravity from a height.")
    print("")
    print("Parameters:")
    paramprint(P_PROJMOT)
    print("")
    PracticalMenuOptions()
    print ("-----=====-----")

def Menu_BlockOnASlope():
    print ("-----=====-----")
    print("A model of a Block sliding down a slope under the force of gravity.")
    print("")
    print("Parameters:")
    paramprint(P_SLOPE)
    print("")
    PracticalMenuOptions()
    print ("-----=====-----")



def Menu_InelasticCollision():
    print ("-----=====-----")
    print("A model of Two masses colliding on a plane.")
    print("")
    print("Parameters:")
    paramprint(P_COLLISION)
    print("")
    PracticalMenuOptions()
    print ("-----=====-----")

def main():
    mainloop = True
    Exit = False
    while mainloop == True:
        mainmenu()
        numint = utils.menuinputvalidation(utils.REGEX4OPMENU)

        if numint == 1:
            Exit = Menu_FallingObjSEL()
        if numint == 2:
            Exit = Menu_ProjectileMotionSEL()
        if numint == 3:
            Exit = Menu_BlockOnASlopeSEL()
        if numint == 4:
            Exit = Menu_InelasticCollisionSEL()
        if Exit == True:
            numint = 9
        if numint == 9:
            mainloop = False

    print("End of program. Bye!")

main()
