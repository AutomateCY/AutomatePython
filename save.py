import json
import os






def intRes(text): #Function to avoid NaN error on inputs. 
    res=input(text)
    while(not res.isdigit()):
        res=input(text)
        print("NaN please enter a number\n")
    return int(res)


def numFile(saveDir,automaton,filename, mode=1): # /!\mode=1 changes name of automaton/!\ search for the right number to add to save file name. 
    num=1 #number to add
    filename= saveDir+"/"+automaton["name"]+" ("+str(num)+").json" #name generation: 'saveDir/automaton (num).json'
    
    while (os.path.exists(filename)): #while the name exists we add 1.
        num+=1
        filename= saveDir+"/"+automaton["name"]+" ("+str(num)+").json"
    
    if mode==1:#rename automaton
        automaton["name"]=filename.split(".json")[0].split(saveDir+"/")[1]

    return filename

def nameFile(automaton, saveDir, mode, filename=""): #fonction used in saveAutomation(). generates filename and handles name conflicts.

    filename= saveDir+"/"+automaton["name"]+".json" #generate name of json file using automaton name.

    if os.path.exists(filename): #testing if file exists.
        
        if mode==0: #default mode, asks for user decision.
            
            mode=intRes("'"+filename+"' already exists \n (1) replace it \n (2) keep both files \n (3) Rename my automaton\n (1, 2 or 3)?: ")
            
        if mode==1: #replace it
                #do nothing since open(filename,"w") will replace it.
                pass

        elif mode==3: #rename the automaton until the name is unique
                automaton["name"]=input(" new name: ")
                filename= saveDir+"/"+automaton["name"]+".json"
                
                while(os.path.exists(filename) or automaton["name"]==""):
                    print(automaton["name"]+' already exists!\n')
                    automaton["name"]=input(" new name: ")
                    filename= saveDir+"/"+automaton["name"]+".json"

        else: #keep both files.
                filename=numFile(saveDir,automaton,filename)
    return filename          


def saveAutomaton(automaton, mode=0): 
    '''
    take an automaton dict as parameter and write it down in save folder, 
    saveAutomation(dict) or saveAutomation(dict, 0) asks for user to replace, rename or keep the two files.
    saveAutomaton(dict, 1) to automatically replace file without asking.
    saveAutomaton(dict, 2) to automatically keep the two files, adds "(1), (2), (3)..." to filename without changing automaton name.
    saveAutomaton(dict, 3) will ask you to rename the file.
    saveAutomaton('return saveDir') to get save directory name
    '''



    saveDir= "save" #save folder, can be modified here if needed
    
    if automaton=="return saveDir": #so the rest of the code can use saveDir.
        return saveDir
        


    if not os.path.exists(saveDir): #create save folder if it doesn't exist
        os.makedirs(saveDir)


    try: automaton["name"]

    except KeyError: automaton["name"]= None

    while(automaton["name"]=="" or (automaton["name"] is None)): #test if name exists
        if mode==3 or mode==0:
            automaton["name"]=input("no name detected \n enter new name: ")
        else:
            automaton["name"]="myAutomaton"

    filename= nameFile(automaton, saveDir, mode)
    
            
    
    with open(filename, "w") as savefile: #saving.
        json.dump(automaton, savefile, indent=4)


def allSave(): #return a list of all files in saveDir
    saveDir=saveAutomaton("return saveDir")

    return os.listdir(saveDir)

def deleteSave(filename=0):
    """
    delete a file in save directory
    deleteSave() or deleteSave(0) will ask user which file to delete.

    with string automaton name as argument.
    example: deleteSave("MyAutomaton") or delete(automaton["name"])
    will delete automaton.json file without user intervention.
    """
    saveDir=saveAutomaton("return saveDir")

    if not os.path.exists(saveDir): #check for save directory existence.
        print("no save directory found")


    
    if filename==0: 
        save=allSave() #make a list with all saves

        for i in range(len(save)): # print all saves so the user can see them.
            print('save n°'+str(i+1)+'-- '+save[i])
        
        res=intRes("which will you delete? (enter save number or save name, 0 to cancel):")

        if res>0 and res<len(save): #test if the number is valid.
            filename=saveDir+"/"+save[res-1] #remove the file.
            os.remove(filename) 
        else:
            print("did nothing")
    
    
    else:#remove a file if specified in arguments
        filename=saveDir+"/"+str(filename)+".json"
        if os.path.exists(filename):
            os.remove(filename)
        else:    
            print(filename+" doesn't exist")
    

#-----------------test run--------------------#
"""
test= {
    'states': ['q0', 'q1', 'q2'],
    'alphabet': ['0', '1'],
    'initial_state': 'q0',
    'final_states': ['q2'],
    'transitions': {
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q0', '1': 'q1'},
    }
}
saveAutomaton(test,2)
deleteSave()
"""
