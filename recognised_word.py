from deterministic import make_deter, isdeter

automaton = {
    'name': "automate1",
    'states': ['q0', 'q1', 'q2'],
    'alphabet': ['0', '1'],
    'initial_state': ['q0'],
    'final_states': ['q2'],
    'transitions': {
        'q0': {'0': ['q0'], '1': ['q1']},
        'q1': {'0': ['q0'], '1': ['q2']},
        'q2': {'0': ['q0'], '1': ['q1']},
    }
}


# Function to check if a word is recognized by a deterministic finite automaton (DFA)
def recognised_word(automaton, word):
    # Check if the automaton is deterministic; if not, make it deterministic
    if isdeter(automaton) == False:
        automaton = make_deter(automaton)

    # Initialize the current state with the initial state of the automaton
    tmp = automaton['initial_state'][0]

    # Iterate through each letter in the word
    for i in word:
        # Check if the letter is a valid transition from the current state
        if i in automaton['transitions'][tmp]:
            # Retrieve possible states resulting from the transition
            possible_states = automaton['transitions'][tmp][i]

            # Update the current state
            tmp = possible_states[0]
            print(tmp + "\n")

        else:
            # If the letter is not a valid transition, display a message and exit
            print("The word is not recognised by the language")
            return 1

    # Check if the current state is a final state
    if tmp in automaton['final_states']:
        print("The word is recognised by the language")
        return 0
    else:
        # If the current state is not a final state, the word is not recognized
        print("The word is not recognised by the language")
        return 1



