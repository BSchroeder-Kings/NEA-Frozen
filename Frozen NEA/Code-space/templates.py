
# Experiment subroutine shell program thing
'''
def newpractical(param):
    elapsedtime=0
    # variable initialisation
    results=[]
    results.append(["time", "variable1", "variable2"])
    for i in range (1, TIMESEGMENTS):
        elapsedtime = i*TIMESLICE #loop 
        elapsedtime = round(elapsedtime, 10)

        if #end condition = true
            break
    pygame.display.set_caption("Exp Name")
    return results
'''
# menu shell
'''
    
def newMenu_practical():
    print()
    numint = 0
    while numint == 0:
        para = Loadparameters(paramfile)
        Menutext()
        back = False
        num = inputvalidation(REGEX1TO3AND9)
        numint = int(num)
        if numint == 1:
            para = Loadparameters(paramfile)
            results = exp(para)
            back = False
            while back == False:
                simnum = post1stinstanceoptionsSEL() #numbers compile then options come up
                if simnum == 1: # loads pygame simulation model
                    practicalrun(results)
                if simnum == 2: # prints result table
                    utils.printresults(results)
                if simnum == 3: # back
                    back = True
                    numint = 0
                if simnum == 9: # quits program
                    numint = 9

        if numint == 2: #change paras
            ChangeParameters(paramfile)
            numint = 0
        if numint == 3: #back
            return False
        if numint == 9:
            return True
'''