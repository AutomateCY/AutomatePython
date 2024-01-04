""" --DOC--

- input_automaton(automaton) -   
    will ask for user to modify automaton in parameter
    if no paramater, it will create a new automaton


"""

def trimNone(l): #remove none while preventing errors.
    try:
        l.remove(None)
    except ValueError:
        pass
  

def cleantrans(auto):#-- clean empty transitions
    
    state_keys=list(auto['transitions'].keys()) #-- to prevent 'dict changed size' errors
    for state in state_keys:
        letter_keys = list(auto['transitions'][state].keys())
        for letter in letter_keys:                                                   
            # if letter has no more transition we delete it
            if len(auto['transitions'][state][letter])==0:
                 auto['transitions'][state].pop(letter)
                
        # if starting state has no more transitions, we delete it.
        if len(auto['transitions'][state])==0:
            auto['transitions'].pop(state)               

def display_automaton(auto):
    print("-----\n Current automaton:{")
    print(" name:",auto["name"])
    print(" states:", auto["states"])
    print(" alphabet:", auto["alphabet"])
    print(" initial_states:",auto["initial_states"])
    print(" final_states:",auto["final_states"])
    for i in auto['transitions']:
        print("     ",i,":", auto['transitions'][i])
    print("-----\n")


def input_choice(min, max, menu='\n'): #-- to make sure the user do not destroy the menu
    print(menu)
    choice = input("your choice:")
    while (not choice.isdigit()) or (int(choice) > max) or (int(choice) < min):
        print("choice invalid, try again")
        print(menu)
        choice = input("your choice:")
    return int(choice)


def modify_list(old, condition = None, condition_name = None, kill = None, alpha = None) :
    # to add and remove elements from list
    # condition is a list where element must be in order to be added
    # for instance, if new transition is in alphabet, it can be added.
    new_list = list(old)
    ans = 0
    while ans != "stop":
        if condition != None:
            print("Condition: New element must be in",condition_name,":", condition)
        if alpha != None:
            print("Condition: letter must be single symbols!")
        ans = input("current list:"+str(new_list)+ '\n type "+element" to add , "-element" to delete , \"mod\" to modify elements from list \ "stop" to stop \n your action:')
        ans=ans.strip()
        if ans=="":
            pass
        elif ans[0] == "+": 
            ans=ans.strip(" +")
            if (condition == None or ans in condition): #-- add if ans is in condition list, if there is a condition list.
                if (alpha == None or (len(ans) == 1 or len(ans) == 0)): #-- if its letter, add only single digits.
                    new_list.append(ans)
                else:
                    print("\n /!\ letter are single symbols!")
            else:
                print("\n /!\ ","'",ans,"' is not in ", condition_name)
        
        elif ans[0] == "-":#-- replace ans with None if ans in list.
            ans=ans.strip(" -")
            if ans in new_list:
                new_list=[x if x != ans else None for x in new_list]
            else:
                print("\n /!\ ","'",ans,"' is not in current list")
        
        elif ans == 'mod' and len(new_list)>0: #modify existing element from list

            for i in range(len(new_list)): # prints list with index for better ergonomy
                print(i,": ",new_list[i])

            i = input_choice(0,len(new_list)-1, "choose element index from list above")
            
            print("remember to meet conditions!")
            ans=input('replace "'+new_list[i]+'" with:')
            while not ((condition == None or ans in condition) and (alpha == None or (len(ans) == 1 or len(ans) == 0))): # enter new element until it satisfies all condition
                print("remember to meet conditions!")
                ans=input('replace "'+new_list[i]+'" with:')
            new_list[i]=ans
            
        elif ans == "stop":
            pass
        else:
            if ans == "mod":
                print("\n /!\ there is no list to modify :(")
            print("\n /!\ did not recognize operation")
        print("\n")
        if kill != None :
            new_list= list(set(new_list))
            trimNone(new_list)
    return new_list


def input_automaton(auto=None):
    #-- No automaton in parameter means, we create one
    #-- activate create mode
    if auto == None:
        auto = {
            'name': "toto the automaton",
            'states': [],
            'alphabet': [],
            'initial_states': [],
            'final_states': [],
            'transitions': {
            }
        }
        create = 1
    else:
        create = 0


    choice = 0
    while choice != 7: 
        display_automaton(auto)
        if create == 0: # in modify mode = you show the menu, else you go through creating steps.
            choice = input_choice(1,7,"Menu : \n    1. Modify the name \n    2. Change Alphabet \n    3. Modify states\n    4. Change the initial states \n    5. Change the final states \n    6. modify transitions \n    7. quit")
        else: 
            choice+=1
            if choice  == 7:
                choice +=1
                create = 0
        
        
        
        
        if choice == 1: #change name
            if create == 1:
                print("new name for automaton...")
            auto['name']=input("new name:")
        
        elif choice == 2: #change the alphabet, same as modify_list() function, but with more condition for adding.
            if create == 1:
                print("now creating alphabet...")
                auto['alphabet'] = modify_list(auto['alphabet'], None, None, 1, 1) #add letters, no conditions , kill duplicates, letter are single symbols
            
            else:
                new_alphabet = modify_list(auto['alphabet'], None, None, None, 1) #add letters, letter are single symbols
                
                choice = input_choice(1,2,"1: rename letters \n2: delete old transitions")
                

                if choice == 2: #-- goes through automaton and keep only transitions with letter in new alphabet.
                    auto['alphabet']=list(set(new_alphabet)) #-- kill dupes + removes None 
                    trimNone(auto['alphabet'])
                    
                    for state in auto['transitions']: 
                        keys=list(auto['transitions'][state].keys()) #to prevent 'dict changed size' error
                        for letter in keys:
                            if letter not in auto['alphabet']:
                                auto['transitions'][state].pop(letter)
                
                else: #-- goes through automaton and rename 
                    #-- create dict to have link old and new name, None means they has been deleted.
                    letter_dict ={}
                    for i in range(len(auto['alphabet'])): # new list is always bigger than old list since we didn't remove None in modify_list()
                        letter_dict.setdefault(auto['alphabet'][i], new_alphabet[i])
                    
                    auto['alphabet']=list(set(new_alphabet)) #-- kill dupes + removes None 
                    trimNone(auto['alphabet'])
                    
                    #-- if letter are paired with None it means they need to be removed. else we rename
                    for state in auto['transitions']: #-- delete and rename letter starting transitions
                        keys=list(auto['transitions'][state].keys())
                        for letter in keys:
                            if letter_dict[letter] == None: #-- delete letter
                                auto['transitions'][state].pop(letter)
                            else: #-- rename letter
                                if letter not in new_alphabet:
                                    auto['transitions'][state][letter_dict[letter]] = auto['transitions'][state][letter]
                                    auto['transitions'][state].pop(letter)
            
            #-- cleaning empty lists and dicts:
            cleantrans(auto)             


        elif choice == 3: 
            #-- in modify mode, you either destroy every state no longer in automaton's states list.
            #-- or you can rename them.
            #-- in create mode you just create new states
            if create == 1:
                print("now enter the states of your automaton...")
                auto['states'] = modify_list(auto["states"], None, None, 1)
            
            
            if create != 1: #-- if not in create mode = if in modify mode
                new_state_list = modify_list(auto["states"])
                choice = input_choice(1,2,"1: rename states \n2: delete old states")

                if choice == 2: #-- goes through automaton and keep only states that are in new state list.
                    auto['states']=list(set(new_state_list))  #-- kill dupes + removes None
                    trimNone(auto['states'])

                    #--keep state only if it's in new state list
                    auto['initial_states'] = [x for x in auto['initial_states'] if x in auto['states']]
                    auto['final_states'] = [x for x in auto['final_states'] if x in auto['states']]
                    
                    keys=list(auto['transitions'].keys()) #to prevent 'dict changed size' error
                    for state in keys: 
                        if state not in auto['states']:
                            auto['transitions'].pop(state)
                        else:
                            letter_keys=list(auto['transitions'][state].keys())
                            for letter in letter_keys:
                                auto['transitions'][state][letter] = [x for x in auto['transitions'][state][letter] if x in auto['states']]
                
                else: #-- goes through automaton and rename 
                    #-- create dict to have link old and new name, None means they has been deleted.
                    state_dict ={}
                    for i in range(len(auto['states'])): # new list is always bigger than old list since we didn't remove None in modify_list()
                        state_dict.setdefault(auto['states'][i], new_state_list[i])
                    print(state_dict)
                    
                    auto['states']=list(set(new_state_list)) #-- kill dupes
                    trimNone(auto['states'])#-- Remove none in list

                    #-- if state are paired with None it means they need to be removed. else we rename
                    auto['initial_states'] = [state_dict[x] for x in auto['initial_states'] if state_dict[x] != None]
                    auto['final_states'] = [state_dict[x] for x in auto['final_states'] if state_dict[x] != None]

                    keys=list(auto['transitions'].keys()) #to prevent 'dict changed size' error
                    for state in keys: #-- delete and rename states starting transitions
                        if state_dict[state] == None: 
                            auto['transitions'].pop(state)
                        else:
                            letter_keys=list(auto['transitions'][state].keys())
                            for letter in letter_keys:#-- delete and rename end states in letter lists
                                auto['transitions'][state][letter] = [state_dict[x] for x in auto['transitions'][state][letter] if state_dict[x] != None]
                                # if letter has no more transition we delete it
                            if state not in new_state_list: #-- rename starting state if needed
                                auto['transitions'][state_dict[state]] = auto['transitions'][state] 
                                auto['transitions'].pop(state)
            #-- cleaning empty lists and dicts:
            cleantrans(auto)                
                                        

        elif choice == 4: #-- modify initial states
            if create == 1:
                print("now defining initial_states...")
            auto['initial_states']=modify_list(auto['initial_states'], auto['states'], 'state list', 1)
        elif choice == 5: #-- modify final states
            if create == 1:
                print("now defining final_states...")
            auto['final_states']=modify_list(auto['final_states'], auto['states'], 'state list', 1)
            
        
        elif choice == 6: 
            #-- input transition
            #-- chose to delete or create it
            if create == 1:
                print("now defining transitions...")
            while True:
                print("current transitions:")
                for i in auto['transitions']:
                    print("     ",i,":", auto['transitions'][i])
                new_trans={
                    'start': '',
                    'end' : [],
                    'letter' : None
                }
                #-- starting state
                while new_trans['start'] not in auto['states']:
                    new_trans['start']=input('choose state to start from in states list:'+str(auto['states'])+'\n "stop" to stop\n your starting state:')
                    if new_trans['start'] == 'stop':
                        break
                if new_trans['start'] == 'stop':
                        break
                
                #-- ending state must be in states list
                print('\nchoose states to end in, stop to stop')
                new_trans['end']=modify_list(new_trans['end'], auto['states'], "states list", 1)
                if new_trans['end'] == []:
                    break

                #-- letter must be in alphabet
                while new_trans['letter'] not in auto['alphabet']:
                    new_trans['letter']=input('choose letter from alphabet:'+str(auto['alphabet'])+'\n "stop" to stop\n your letter:')
                    if new_trans['letter'] == 'stop':
                        break
                if new_trans['letter'] == 'stop':
                        break
                
                choice = input_choice(1,3, "1/create specified trans 2/delete specified trans 3/Cancel")
                
                if choice == 1:
                    #-- create
                        # if new starting state is not in transition, create it
                    if new_trans['start'] not in auto['transitions']:
                        auto['transitions'][new_trans['start']]= {new_trans['letter']:new_trans['end']}
                        # if new starting state is in transition, but has not the specified letter, create the letter.
                    elif new_trans['letter'] not in auto['transitions'][new_trans['start']]:
                        auto['transitions'][new_trans['start']][new_trans['letter']]= new_trans['end']
                        # if start and letter already exist, merge the two lists while killing duplicates.
                    else:
                        auto['transitions'][new_trans['start']][new_trans['letter']]= list(set(new_trans['end']+auto['transitions'][new_trans['start']][new_trans['letter']]))
                
                if choice == 2:
                    #-- DELETE
                        # test if new starting state is in transition, else 'not found'
                    if new_trans['start'] in auto['transitions']:
                        # search for letter, else not found
                        if new_trans['letter'] in auto['transitions'][new_trans['start']]:
                            # search for ending states and delete them, else not found
                            for i in new_trans['end']:
                                if i in auto['transitions'][new_trans['start']][new_trans['letter']]:
                                    auto['transitions'][new_trans['start']][new_trans['letter']].remove(i)
                                
                            # if letter has no more transition we delete it
                            if len(auto['transitions'][new_trans['start']][new_trans['letter']])==0:
                                auto['transitions'][new_trans['start']].pop(new_trans['letter'])
                            # if starting state has no more transitions, we delete it.
                            if len(auto['transitions'][new_trans['start']])==0:
                                auto['transitions'].pop(new_trans['start'])
                        else:
                            print("transition not found :(")
                    else:
                        print("transition not found :(")
                choice = 6 # to allow create mode to continue.
        
        elif choice==7: #-- stop loop
            pass
        elif choice==8: #-- stop creating mode
            print("do you wish to change something?")
        else:
            print("did not recognize operation")
    
    return auto

            
            



# ##############################-TEST RUN-#######################################
'''
automaton1 = {
    'name': "automaton1",
    'states': ['q0', 'q1', 'q2'],
    'alphabet': ['0', '1', ''],
    'initial_states': ['q0'],
    'final_states': ['q2'],
    'transitions': {
        'q0': {'0': ['q0', 'q1'], '': ['q1']},
        'q1': {'0': ['q0', 'q1'], '1': ['q2', 'q1']},
        'q2': {'': ['q0'], '1': ['q1']},
    }
}
input_automaton(automaton1)
'''