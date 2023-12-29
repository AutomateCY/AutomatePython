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
            if len(auto['transitions'][states][transition]) > 1:
                return False
    return True


def kill_dupes(used_list):  # kill duplicates in lists used in deter_new_state()
    used_list = set(used_list)
    return list(used_list)


def deter_new_state(automaton, receiver_states, final_list, state_list, treated_state):
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
    #-- creating new state only if not existing, and it's a non_deterministic transition.
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

    # print('automaton:', str(automaton), "\n")

    #-- making sets to avoid duplications
    new_final = set(automaton['final_states'])
    new_states_list = set([])
    todo = list(automaton['initial_states'])
    #-- list of states to process, the rest is generated from deter_new_state

    for state in todo:  # going through new states created
        # print("processing " + str(state) + "...")
        #-- create next states to treat and add in todo list
        for transition in automaton['transitions'][state]:  # going through processed state's transitions
            # print("state" + str(automaton['transitions'][state]) + ":transition " + transition + "...\n")
            #-- create next state
            new_state = deter_new_state(automaton, automaton['transitions'][state][transition], new_final,
                                        new_states_list, state)
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
        if i not in new_states_list:
           automaton['transitions'].pop(i)

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
print(make_deter(automaton3))
#'''
