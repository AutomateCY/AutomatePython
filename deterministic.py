""" DOC
-isdeter(automaton)-
    will return True if automaton is deterministic
    False otherwise

-make_deter(automaton)-
    will return a deterministic copy of automaton
    if automaton is already deterministic, it will
    return a copy of it.
    Will prune automaton.
"""


def copy_automat(automaton):
    new_transitions = {}

    for state_start in automaton['transitions']:
        new_letter = {}
        for letter in automaton['transitions'][state_start]:
            new_letter[letter] = automaton['transitions'][state_start][letter][:]

        new_transitions[state_start] = new_letter

    return {'name': "new " + automaton["name"],
            'states': automaton["states"][:],  # copy of the list of states
            'alphabet': automaton["alphabet"][:],
            'initial_states': automaton["initial_states"][:],
            'final_states': automaton["final_states"][:],
            'transitions': new_transitions}


def isdeter(auto):
    # Tells if an automaton is deterministic
    # Check lists longer than 1 in transitions = transitions with more than 1 destination

    for states in auto['transitions']:
        for transition in auto['transitions'][states]:
            if len(auto['transitions'][states][transition]) > 1 or transition == "":
                return False
    return True


def kill_dupes(used_list):  # kill duplicates in lists used in deter_new_state()
    used_list = set(used_list)
    return list(used_list)

def kill_Epsilon(auto): #delete all epsilon transition by merging states together.
    edict=[{}] #list of sets of states
    added=0
    if '' in auto['alphabet']:
        auto['alphabet'].remove('')
    else:
        return 0

    #search for states linked epsilon states, group them in sets.
    state_keys=list(auto['transitions'].keys()) #-- to prevent 'dict changed size' errors
    for state in state_keys:
        letter_keys = list(auto['transitions'][state].keys())
        for letter in letter_keys: 
            if letter=="":
                for i in auto['transitions'][state][letter]:
                    added =0
                    for y in edict:
                        if state in y:
                            y.add(i)
                            added = 1
                        elif i in y :
                            y.add(state)
                            added = 1

                    if added == 0:
                        edict.append({i, state})
    edict.remove({})
    #print(edict)
    old_new={} #dict to link old and new state.
    new_dict={} #dict of new states generated
    #-- create new states transitions:
    for sets in edict:
        new_state=""
        trans = {}
        for state in sets:
            new_state += state
            if state in auto['transitions']:
                for letter in auto['transitions'][state]:
                    if letter != "":
                        try:
                            trans[letter] = kill_dupes(trans[letter] + auto['transitions'][state][letter])
                        except KeyError:
                            trans[letter] = auto['transitions'][state][letter]
        new_dict[new_state] = trans
        for state in sets:
            old_new[state] = new_state
        
    #print(new_dict)
    #print(old_new)
    #replace old states by new state generated.
    auto['states']=kill_dupes([old_new[x] if x in old_new else x for x in auto['states']])
    auto['initial_states'] = kill_dupes([old_new[x] if x in old_new else x for x in auto['initial_states']])
    auto['final_states'] = kill_dupes([old_new[x] if x in old_new else x for x in auto['final_states']])
    
    for (state, trans) in new_dict.items(): #-- add state transition if 
        if trans !={}:
            auto['transitions'][state]=trans
    
    keys=list(auto['transitions'].keys())
    for state in keys: #-- delete old state and rename states starting transitions
        if state in old_new:
            auto['transitions'].pop(state)
        else:
            #print(state)
            key_letter=list(auto['transitions'][state].keys())
            for letter in key_letter:
                auto['transitions'][state][letter]=kill_dupes([old_new[x] if x in old_new else x for x in auto['transitions'][state][letter]])
    #print(auto)

def deter_new_state(automaton, receiver_states, final_list, state_list, treated_state, treated_transition):
    # Function used in make_deter()
    # if it detects a list of receiver states longer than 1 i.e.
    # non-deterministic transitions
    # this function creates new receiver state by combining all states
    # pointed by the transition

    # kill dupes if non-deterministic transition points multiple time on the same state
    # sort, that way: same combination of state = same state.
    new_trans = {}
    add = 0
    receiver_states = kill_dupes(receiver_states)
    receiver_states.sort()

    # print("receiver_states", receiver_states)
    # print(state_list)
    #-- creating new state only if not already existing, and it's a non_deterministic transition.
    if len(receiver_states) > 1 and (",".join(receiver_states) != treated_state) and (
            (",".join(receiver_states) not in state_list)):  #

        #-- going through all states in transition
        for s in receiver_states:

            # print("receiver_states", receiver_states)
            # print("s=", s)

            #-- detect if state inherit final state
            if s in final_list:
                # print(s, "in", final_list)
                add = 1

            # inherit all transition
            try:
                for trans in automaton['transitions'][s]:
                    # print('now in', s, ':', automaton['transitions'][s])
                    # print("trans=", trans)

                    #-- create the transition if not existing, else only append
                    try:
                        # print("appending")
                        new_trans[trans] = set(new_trans[trans])
                        for i in automaton['transitions'][s][trans]:
                            new_trans[trans].add(i)
                            # print(new_trans)
                        new_trans[trans] = list(new_trans[trans])

                    except KeyError:
                        # print("creating")
                        new_trans[trans] = automaton['transitions'][s][trans]

                    # print("new trans=", new_trans)
            except KeyError: #receiver state has no transition.
                pass

        #-- create new state name by combining all transition.
        receiver_states = ",".join(receiver_states)
        automaton['transitions'][receiver_states] = new_trans

    else:
        receiver_states = ",".join(receiver_states)
        # print("receiver_states", receiver_states)

    # print("new state generated:" + receiver_states + str(new_trans) + " \n")

    #-- inherit final state
    if add == 1:
        final_list.add(receiver_states)
    return receiver_states


def make_deter(automaton):
    if isdeter(automaton):
        # print("already deterministic.")
        return copy_automat(automaton)


    # print("Deterministic Conversion...")  # debug print
    automaton = copy_automat(automaton)
    kill_Epsilon(automaton) #-- merge states linked by epsilon transitions
    # print('automaton:', str(automaton), "\n")

    #-- making sets to avoid duplications
    new_final = set(automaton['final_states'])
    new_states_list = set([])
    todo = list(automaton['initial_states'])
    #-- list of states to process, the rest is generated from deter_new_state

    for state in todo:  # going through new states created
        # print("processing " + str(state) + "...")
        #-- create next states to treat and add in todo list
        if state in automaton['transitions']:
            for transition in automaton['transitions'][state]:  # going through processed state's transitions
                # print("state" + str(automaton['transitions'][state]) + ":transition " + transition + "...\n")
                #-- create next state
                new_state = deter_new_state(automaton, automaton['transitions'][state][transition], new_final,
                                            new_states_list, state, transition)
                # print('new=', new_state)

                if new_state in todo:
                    pass
                else:
                    todo.append(new_state)

                automaton['transitions'][state][transition] = [new_state]
                # print(automaton['transitions'][state][transition])
        # print(todo)
        # print("state finished \n")
        new_states_list.add(state)
        # print('automaton:', str(automaton['transitions']), "\n")
    

    #-- update automaton.
    # print('automaton:', str(automaton['transitions']), "\n")
    automaton['final_states'] = list(new_final)
        #-- prune non treated states.
    for i in automaton['states']:
        if i not in new_states_list and i in automaton['transitions']:
           automaton['transitions'].pop(i)
        if i not in new_states_list and i in automaton['initial_states']:
           automaton['initial_states'].remove(i)
        if i not in new_states_list and i in automaton['final_states']:
           automaton['final_states'].remove(i)

    automaton['states'] = list(new_states_list)
    automaton['states'].sort()  #-- for better legibility
    automaton['final_states'].sort()
    return automaton


# ##############################-TEST RUN-#######################################
'''
automaton1 = {
    'name': "automaton1",
    'states': ['q0', 'q1', 'q2'],
    'alphabet': ['0', '1'],
    'initial_states': ['q0'],
    'final_states': ['q2'],
    'transitions': {
        'q0': {'0': ['q0', 'q1'], '1': ['q1']},
        'q1': {'0': ['q0', 'q1'], '1': ['q2', 'q2']},
        'q2': {'0': ['q0'], '1': ['q1']},
    }
}

automaton3 = {
    'name': "automaton1",
    'states': ['q0', 'q1', 'q2'],
    'alphabet': ['0', '1', '2'],
    'initial_states': ['q0'],
    'final_states': ['q2'],
    'transitions': {
        'q0': {'0': ['q0', 'q1'], '1': ['q1']},
        'q1': {'0': ['q0', 'q1'], '2': ['q2', 'q2', 'q2', 'q1']},
        'q2': {'0': ['q0'], '1': ['q1']},
    }
}

automaton2 = {
    'name': "automaton2",
    'states': ['q0', 'q1', 'q2', 'q3'],
    'alphabet': ['a', 'b'],
    'initial_states': ['q0'],
    'final_states': ['q2'],
    'transitions': {
        'q0': {'a': ['q1', 'q3'], 'b': ['q1']},
        'q1': {'a': ['q2'], 'b': ['q1']},
        'q2': {'a': ['q2']},
        'q3': {'a': ['q3']},

    }
}

automaton4 = {
    'name': "automaton2",
    'states': ['q0', 'q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7'],
    'alphabet': ['a', 'b', ''],
    'initial_states': ['q0'],
    'final_states': ['q7'],
    'transitions': {
        'q0': {'': ['q1', 'q4']},
        'q1': {'a': ['q2']},
        'q2': {'a': ['q2', 'q3'], 'b':['q2']},
        'q3': {'':['q7']},
        'q4': {'b':['q5']},
        'q5': {'a':['q5'], 'b':['q5','q6']},
        'q6': {'':['q7']}

    }
}

print(make_deter(automaton4))
#'''
