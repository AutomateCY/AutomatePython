automatons = [{
    'name': "automate1",
    'states': ['q0', 'q1', 'q2'],
    'alphabet': ['0', '1'],
    'initial_state': 'q0',
    'final_states': ['q2'],
    'transitions': {
        'q0': {'0': 'q0', '1': 'q1'},
        'q1': {'0': 'q0', '1': 'q2'},
        'q2': {'0': 'q0', '1': 'q1'},
    }
}]


def is_valid_state(state, automaton):
    return state not in automaton['states']

def is_valid_symbol(symbol):
    return symbol.isalpha() and len(symbol) == 1

def print_menu_modify():
    print("Menu :")
    print("1. Add a state")
    print("2. Remove a state")
    print("3. Add a transition")
    print("4. Remove a transition")
    print("5. Change the initial state")
    print("6. Add a final state")
    print("7. Remove a final state")
    print("8. Modify the name")
    print("9. Quit")


def modify_aef(automaton):
    while True:
        print_menu_modify()
        choice = input("Choose an option: ")

        if choice == '1':
            state = input("Name of the state to add: ")
            if is_valid_state(state, automaton):
                automaton['states'].append(state)
            else:
                print(f"State '{state}' already exists.")
        elif choice == '2':
            state = input("Name of the state to remove: ")
            if state in automaton['states']:
                automaton['states'].remove(state)
                if state == automaton["initial_state"]:
                    automaton["initial_state"] = None
                if state in automaton['final_states']:
                    automaton['final_states'].remove(state)
                automaton['transitions'] = {k: v for k, v in automaton['transitions'].items() if k != state}
                for start_state, transition in automaton['transitions'].items():
                    automaton['transitions'][start_state] = {k: v for k, v in transition.items() if v != state}
            else:
                print(f"State '{state}' does not exist.")
        elif choice == '3':
            start_state = input("Starting state: ")
            symbol = input("Transition symbol: ")
            end_state = input("Ending state: ")
            if is_valid_state(start_state, automaton) or is_valid_state(end_state, automaton):
                print("Invalid state name. Both start and end states must already exist.")
            elif not is_valid_symbol(symbol):
                print("Invalid symbol. Please enter a single alphabet character.")
            else:
                if start_state in automaton['transitions']:
                    automaton['transitions'][start_state][symbol] = end_state
                else:
                    automaton['transitions'][start_state] = {symbol: end_state}
                automaton['alphabet'].append(symbol)
        elif choice == '4':
            start_state = input("Starting state: ")
            symbol = input("Transition symbol: ")
            end_state = input("Ending state: ")
            if start_state in automaton['transitions'] and symbol in automaton['transitions'][start_state] and automaton['transitions'][start_state][symbol] == end_state:
                del automaton['transitions'][start_state][symbol]
            else:
                print("The specified transition does not exist.")
        elif choice == '5':
            new_initial_state = input("New initial state: ")
            if new_initial_state in automaton['states']:
                automaton['initial_state'] = new_initial_state
            else:
                print(f"State '{new_initial_state}' does not exist.")
        elif choice == '6':
            final_state = input("Final state to add: ")
            if final_state in automaton['states']:
                automaton['final_states'].append(final_state)
            else:
                print(f"State '{final_state}' does not exist.")
        elif choice == '7':
            final_state = input("Final state to remove: ")
            if final_state in automaton['final_states']:
                automaton['final_states'].remove(final_state)
            else:
                print(f"State '{final_state}' is not a final state.")
        elif choice == "8":
            automaton["name"] = input("enter new name: ")
        elif choice == '9':
            break
        else:
            print("Invalid option. Please choose a valid option.")

    # You can then use the modified automaton as needed.
    print("Modified automaton:", automaton)


modify_aef(automatons[0])
