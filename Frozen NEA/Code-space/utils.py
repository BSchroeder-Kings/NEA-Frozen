FONT = 'freesansbold.ttf'
TEXTCOLOUR = (10,10,150)
FOLDER="."
RED = (170, 40, 40)
BLUE = (40, 40, 170)
GREEN = (170, 40, 40)
FLOATREGEX = "^[0-9]*[.]?[0-9]*$"
REGEX3OPMENU = "^[1-3]$"
REGEX4OPMENU = "^[1-4]$"
import pygame
import math
import re

def printresults(result):
    result = list(result)
    for l in result:
        for c in l:
            print(c,end=" ")
        print()

def LoadResults(fname):
    results=[]
    #open the file
    fh = open(fname, "r")
    title=True
    for line in fh:
        line = line.strip("\n")
        l = line.split(",")
        if title == False:
            for n in range(len(l)):
                l[n]=float(l[n])
        else:
            title = False
        results.append(l)
    fh.close()
    return results

def windowtextprinter(Header, Value, unit, X, Y, win):             
    font = pygame.font.Font(FONT, 22)
    printout = str(Header) + "(" + str(unit) + ")" + ": " + str(Value)
    text= font.render(printout, True, TEXTCOLOUR, None)
    textbox = text.get_rect()
    textbox.x = X
    textbox.y = Y
    win.blit(text, textbox)                                                            
    return

def windowothertextprinter(Text, Colour, X, Y, win):
    font = pygame.font.Font(FONT, 22)
    text= font.render(Text, True, Colour, None)
    textbox = text.get_rect()
    textbox.x = X
    textbox.y = Y
    win.blit(text, textbox)                                                            
    return
    
def printpygamecontrols(CONTROLSX,Y, win):
    font = pygame.font.Font(FONT, 22)
    QuitFunction = "Quit: Q"
    ReplayFunction = "Replay/Play: A"
    text1= font.render(QuitFunction, True, TEXTCOLOUR, None)
    textbox1 = text1.get_rect()
    textbox1.x = CONTROLSX
    textbox1.y = Y
    text2= font.render(ReplayFunction, True, TEXTCOLOUR, None)
    textbox2 = text2.get_rect()
    textbox2.x = CONTROLSX
    textbox2.y = Y+30
    win.blit(text1, textbox1)  
    win.blit(text2, textbox2)                                                          
    return 

def menuinputvalidation(regex):
    userinputvalid = False
    while userinputvalid == False:
        userinput = input (">")
        x = userinput
        if (re.search(regex, x)): #uses regex specified by called thingy to determine whether the if statement should be done or not
            userinputvalid = True
        if x == "9":
            userinputvalid = True
        if userinputvalid == False:
            print ("Please enter a valid input")
    userinput = int(userinput)
    return userinput

def Loadparameters(fname):
    dict={}
    fh = open(FOLDER+"/"+fname)# creates recognisable file name for program to find file attached with program, FOLDER can be changed later if the files are stored outside the program folder
    for l in fh: #goes through each line
        line=l.strip("\n") #strips off the new lines
        tlist=line.split(":") #splits name of variable stored from its value
        dict[tlist[0]]=float(tlist[1]) # turns the variables and values into a dictionary 
    fh.close()
    return dict

def paraminputvalid (paramregex, zero):
    userinputvalid = False
    if zero == False:
        while userinputvalid == False:
            userinput = input (">")
            x = userinput
            if (re.search(paramregex, x)): #uses regex specified by called thingy to determine whether the if statement should be done or not
                xnum = float(x)
                if xnum > 0.0:
                    userinputvalid = True
                else:
                    print ("Please enter a valid input")
            else:
                print ("Please enter a valid input")
    if zero == True:
        while userinputvalid == False:
            userinput = input (">")
            x = userinput
            if (re.search(paramregex, x)): #uses regex specified by called thingy to determine whether the if statement should be done or not
                userinputvalid = True
            else:
                print ("Please enter a valid input")
    userinput = float(userinput)
    return userinput
    

def ChangeParameters(fname):
    
    dict = Loadparameters(fname)
    keylist = list(dict.keys())
    vallist = list(dict.values())
    for n in range(len(keylist)):
        print (keylist[n], ">", vallist[n])
        newval = paraminputvalid(FLOATREGEX, False)
        dict[keylist[n]] = newval
    print (dict)
    vallist = list(dict.values())
    fh = open(FOLDER+"/"+fname,"w")
    for n in range(len(keylist)):
        fh.write(keylist[n]+": "+str(vallist[n])+"\n")
    fh.close()  


def SaveResults(fname, results):
    fh = open(FOLDER+"/"+fname,"w")
    for l in results:
        outline=""
        for idx in range(len(l)-1):
            outline=outline+str(l[idx])+","
        outline=outline+str( l[len(l)-1] )
        fh.write(outline+"\n")
    fh.close()
    return

def degreestoradians(angle):
    if (angle > 0):
        angle = float(angle)
        anglepirad = angle/180
        anglerad = anglepirad*math.pi
        sinangle = math.sin(anglerad)
        sinangle = round(sinangle, 10)
        return sinangle
    else:
        return angle