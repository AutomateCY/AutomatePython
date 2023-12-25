def copy_transitions(transitions):
    """return a copy of the content of the dictionary 'transitions'"""
    new_transitions = {}
    for state_start in transitions:
        for letter in transitions[state_start]:
            new_transitions[state_start] = {letter: transitions[state_start][letter][:]}
    return new_transitions


def pruned(automaton):
    """return a pruned version of 'automaton'"""
    pruned_aut = {'name': automaton["name"],
                  'states': automaton["states"][:],  # copy of the list of states
                  'alphabet': automaton["alphabet"][:],
                  'initial_states': automaton["initial_states"][:],
                  'final_states': automaton["final_states"][:],
                  'transitions': {}}
    list_states = automaton["states"][:]
    list_states_non_co_reachable = []
    list_states_reachable = []
    browse_automaton(automaton, automaton["initial_states"][0], list_states_non_co_reachable, list_states_reachable)
    for s in list_states_reachable:
        list_states.remove(s)
    list_states_to_remove = list_states_non_co_reachable + list_states
    for state in list_states_to_remove:
        pruned_aut["states"].remove(state)
    for state_start in automaton["transitions"]:
        if state_start not in list_states_to_remove:
            pruned_aut["transitions"][state_start] = {}
            for letter in automaton["transitions"][state_start]:
                pruned_aut["transitions"][state_start][letter] = [i for i in
                                                                  automaton["transitions"][state_start][letter] if
                                                                  i not in list_states_to_remove]
                if len(pruned_aut["transitions"][state_start][letter]) == 0:
                    del pruned_aut["transitions"][state_start][letter]
            if len(pruned_aut["transitions"][state_start]) == 0:
                del pruned_aut["transitions"][state_start]
    return pruned_aut


def browse_automaton(automaton, state, list_states_non_co_reachable, list_states_reachable):
    """browse 'automaton' recursively to find the non-reachable and non co-reachable"""
    if state not in list_states_reachable:
        list_states_reachable.append(state)
    if state in automaton["transitions"]:
        for letter in automaton["transitions"][state]:
            for end in automaton["transitions"][state][letter]:
                browse_automaton(automaton, end, list_states_non_co_reachable, list_states_reachable)
    elif state not in automaton["final_states"] and state not in list_states_non_co_reachable:
        list_states_non_co_reachable.append(state)


def complement(automaton):
    aut_complement = automaton.copy()
    final_states = automaton["final_states"]
    aut_complement["final_states"] = [i for i in range(aut_complement['states']) if i not in final_states]
    return aut_complement


def mirror(automaton):
    aut_mirror = {'name': "mirror " + automaton["name"],
                  'states': automaton["states"][:],
                  'alphabet': automaton["alphabet"][:],
                  'initial_states': automaton["initial_states"][:],
                  'final_states': automaton["final_states"][:],
                  'transitions': {}}
    aut_mirror["final_states"] = aut_mirror['initial_states']
    aut_mirror["states"].append("S'0")
    aut_mirror["initial_states"] = ["S'0"]
    aut_mirror["transitions"]["S'0"] = {}
    for state_start in automaton["transitions"]:
        for letter in automaton["transitions"][state_start]:
            for state_end in automaton["transitions"][state_start][letter]:
                if state_end in aut_mirror["transitions"].keys():
                    if letter in aut_mirror["transitions"][state_end]:
                        aut_mirror["transitions"][state_end][letter].append(state_start)
                    else:
                        aut_mirror["transitions"][state_end][letter] = [state_start]
                else:
                    aut_mirror["transitions"][state_end] = {letter: [state_start]}
                if state_end in automaton["final_states"]:
                    if letter in aut_mirror["transitions"]["S'0"]:
                        aut_mirror["transitions"]["S'0"][letter].append(state_start)
                    else:
                        aut_mirror["transitions"]["S'0"][letter] = [state_start]
    return aut_mirror


def product(automaton1, automaton2):
    """return the product of 2 automatons, 'automaton1' and 'automaton2', in a non-recursive way"""
    product_aut = {'name': "product " + automaton1["name"] + " and " + automaton2["name"],
                   'states': [],
                   'alphabet': [],
                   'initial_states': [],
                   'final_states': [],
                   'transitions': {
                   }}
    for state_aut1 in automaton1['states']:
        for state_aut2 in automaton2['states']:
            product_aut["states"].append(state_aut1 + state_aut2)
            if state_aut1 in automaton1["final_states"] and state_aut2 in automaton2["final_states"]:
                product_aut["final_states"].append(state_aut1 + state_aut2)
            if state_aut1 in automaton1["initial_states"] and state_aut2 in automaton2["initial_states"]:
                product_aut["initial_states"].append(state_aut1 + state_aut2)
            if state_aut1 in automaton1["transitions"] and state_aut2 in automaton2["transitions"]:
                list_common_transition = list(set(automaton1["transitions"][state_aut1].keys()) & set(
                    automaton2["transitions"][state_aut2].keys()))
                if len(list_common_transition) > 0:
                    product_aut["transitions"][state_aut1 + state_aut2] = {}
                for transition_name in list_common_transition:
                    if transition_name not in product_aut["alphabet"]:
                        product_aut["alphabet"].append(transition_name)
                    for end_transition_aut1 in automaton1["transitions"][state_aut1][transition_name]:
                        for end_transition_aut2 in automaton2["transitions"][state_aut2][transition_name]:
                            new_end = [end_transition_aut1 + end_transition_aut2]
                            product_aut["transitions"][state_aut1 + state_aut2][
                                transition_name] = new_end if transition_name not in product_aut["transitions"][
                                state_aut1 + state_aut2] else product_aut["transitions"][state_aut1 + state_aut2][
                                                                  transition_name] + new_end
    return pruned(product_aut)


def product2(automaton1, automaton2):
    """return the product of 2 automatons, 'automaton1' and 'automaton2', with a recursive function"""
    automaton_product = {'name': "product " + automaton1["name"] + " and " + automaton2["name"],
                         'states': [],
                         'alphabet': [],
                         'initial_states': [],
                         'final_states': [],
                         'transitions': {
                         }}
    product_recursive(automaton1, automaton2, automaton1["initial_states"][0],
                      automaton2["initial_states"][0], automaton_product)
    # return pruned(automaton_product) #to think : need to make it pruned or does my function makes it already (or make it so)
    return automaton_product


def product_recursive(automaton1, automaton2, state_aut1, state_aut2, automaton_final):
    """browse the automaton to do the product of 'automaton1' and 'automaton2'"""
    fusion_states = state_aut1 + state_aut2
    automaton_final["states"].append(fusion_states)
    if state_aut1 in automaton1["initial_states"] and state_aut2 in automaton2["initial_states"]:
        automaton_final["initial_states"].append(fusion_states)
    if state_aut1 in automaton1["final_states"] and state_aut2 in automaton2["final_states"]:
        automaton_final["final_states"].append(fusion_states)
    if state_aut1 in automaton1["transitions"] and state_aut2 in automaton2["transitions"]:
        list_common_transition = list(set(automaton1["transitions"][state_aut1].keys()) & set(
            automaton2["transitions"][state_aut2].keys()))
        if len(list_common_transition) > 0:
            automaton_final["transitions"][fusion_states] = {}
            for commun_transition in list_common_transition:
                automaton_final["alphabet"].append(commun_transition)
                automaton_final["transitions"][fusion_states][commun_transition] = []
                for end_state_aut1 in automaton1["transitions"][state_aut1][commun_transition]:
                    for end_state_aut2 in automaton2["transitions"][state_aut2][commun_transition]:
                        fusion_end_states = end_state_aut1 + end_state_aut2
                        automaton_final["transitions"][fusion_states][commun_transition].append(fusion_end_states)
                        product_recursive(automaton1, automaton2, end_state_aut1, end_state_aut2, automaton_final)


def concatenation(automaton1, automaton2):
    """concatenate the 2 automatons 'automaton1' and 'automaton2' and return the result"""
    concatenation_aut = {'name': "concatenation " + automaton1["name"] + " and " + automaton2["name"],
                         'states': automaton1["states"] + automaton2["states"],
                         'alphabet': automaton1["alphabet"] + automaton2["alphabet"],
                         'initial_states': automaton1["initial_states"],
                         'final_states': automaton2["final_states"],
                         'transitions': {
                         }}
    for t in automaton1["transitions"]:
        concatenation_aut["transitions"][t] = automaton1["transitions"][t]
    for t in automaton2["transitions"]:
        concatenation_aut["transitions"][t] = automaton2["transitions"][t]
    for state in automaton1["final_states"]:
        if state in concatenation_aut["transitions"]:
            concatenation_aut["transitions"][state].update(automaton2["transitions"][automaton2["initial_states"][0]])
        else:
            concatenation_aut["transitions"][state] = automaton2["transitions"][automaton2["initial_states"][0]]
        if automaton2["initial_states"] in automaton2["final_states"]:
            concatenation_aut['final_states'].append(state)
    return concatenation_aut


# TEST AREA
test = False
if test:
    automatons_to_multiply = [
        {
            'name': "automate1",
            'states': ['q0', 'q1', ],
            'alphabet': ['0', '1'],
            'initial_states': ['q0'],
            'final_states': ['q1'],
            'transitions': {
                'q0': {'0': ['q0'], '1': ['q1']},
                'q1': {'0': ['q1']}
            }
        },
        {
            'name': "automate2",
            'states': ['t0', 't1', 't2'],
            'alphabet': ['0', '1'],
            'initial_states': ['t0'],
            'final_states': ['t2'],
            'transitions': {
                't0': {'0': ['t1']},
                't1': {'1': ['t2']}
            }
        }
    ]

    print(product(automatons_to_multiply[0], automatons_to_multiply[1]))
    print(product2(automatons_to_multiply[0], automatons_to_multiply[1]))

    aut_to_mirror = {
        'name': "automate1",
        'states': ['q1', 'q2', 'q3', 'q4'],
        'alphabet': ['a', 'b', 'c'],
        'initial_states': ['q1'],
        'final_states': ['q3', 'q4'],
        'transitions': {
            'q1': {'a': ['q2']},
            'q2': {'b': ['q3'], 'c': ['q4']}
        }
    }
    print(mirror(aut_to_mirror))

    aut_to_concatenate = [
        {
            'name': "automate1",
            'states': ['q1', 'q2', 'q3', 'q4'],
            'alphabet': ['a', 'b', 'c'],
            'initial_states': ['q1'],
            'final_states': ['q3', 'q4'],
            'transitions': {
                'q1': {'a': ['q2']},
                'q2': {'b': ['q3'], 'c': ['q4']}
            }
        },
        {
            'name': "automate1",
            'states': ['t1', 't2', 'q3'],
            'alphabet': ['d', 'e'],
            'initial_states': ['t1'],
            'final_states': ['t2', 't3'],
            'transitions': {
                't1': {'d': ['t2'], 'e': ['t3']}
            }
        }
    ]

    print(concatenation(aut_to_concatenate[0], aut_to_concatenate[1]))

    aut_to_pruned = {
        'name': "automate1",
        'states': ["A", "B", "C", "D", "E", "F"],
        'alphabet': ['0', '1', '2', '3', '4', '5'],
        'initial_states': ['A'],
        'final_states': ['E'],
        'transitions': {
            'A': {'0': ['B']},
            'B': {'1': ['C'], '2': ['D']},
            'D': {'3': ['E']},
            'F': {'4': ['E']},
            'E': {'5': ['C']}
        }
    }
    print("pruned_aut : ", pruned(aut_to_pruned))
