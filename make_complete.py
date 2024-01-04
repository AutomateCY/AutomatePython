automaton = {
    'name': "automate1",
    'states': ['q0', 'q1', 'q2'],
    'alphabet': ['0', '1'],
    'initial_states': ['q0'],
    'final_states': ['q2'],
    'transitions': {
        'q0': {'1': ['q1']},
        'q1': {'0': ['q0'], '1': ['q2']},
        'q2': {'0': ['q0'], '1': ['q1']},
    }
}


# Function to create a copy of the content of the dictionary 'transitions'
def copy_transitions(transitions):
    new_transitions = {}
    # Iterate through each starting state in the original transitions
    for state_start in transitions:
        # Create a new entry for the starting state in the new transitions
        new_transitions[state_start] = {}
        # Iterate through each letter in the transitions from the current starting state
        for letter in transitions[state_start]:
            # Copy the list of states associated with the current letter to the new transitions
            new_transitions[state_start].update({letter: transitions[state_start][letter][:]})
    return new_transitions

# Function to check if an automaton is complete
def is_complete(automaton):
    # Iterate through each state in the automaton's transitions
    for i in automaton['transitions']:
        # Iterate through all letters in the automaton's alphabet
        for n in automaton['alphabet']:
            # If any letter is not in the transitions for a state, the automaton is not complete
            if (n not in automaton['transitions'][i]):
                print('The automaton is not complete')
                return 1
    # If all transitions are defined for each state and letter, the automaton is complete
    print('The automaton is complete')
    return 0

# Function to make an automaton complete by adding 'phi' transitions
def make_complete(automaton):
    # If the automaton is already complete, return it as is
    if is_complete(automaton) == 0:
        return automaton
    else:
        # Create a new automaton with the same structure as the original
        complete_aut = {'name': "complete " + automaton["name"],
                        'states': automaton["states"][:],  # copy of the list of states
                        'alphabet': automaton["alphabet"][:],
                        'initial_states': automaton["initial_states"][:],
                        'final_states': automaton["final_states"][:],
                        'transitions': copy_transitions(automaton["transitions"])}
        # Add a 'phi' transition for each letter in the alphabet to handle missing transitions
        complete_aut['transitions']['phi'] = {}
        for alph in complete_aut['alphabet']:
            complete_aut['transitions']['phi'][alph] = ['phi']
        # Iterate through each state and letter in the transitions and add 'phi' transitions as needed
        for i in complete_aut['transitions']:
            for n in complete_aut['alphabet']:
                if (n not in complete_aut['transitions'][i]):
                    complete_aut['transitions'][i][n] = ['phi']
    return complete_aut

