automaton = {
    'states': {'q0', 'q1', 'q2'},
    'alphabet': {'0', '1'},
    'initial_state': 'q0',
    'final_states': {'q2'},
    'transitions': {
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q0', '1': 'q1'},
    }
}

print("hello word")