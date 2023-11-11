def aut_input():  # to do the input of a new automaton
    # for the name
    name = str(input("What is the name of the automaton ?"))

    # for the alphabet
    pre_alphabet = []
    print("If there are duplicates they will be deleted afterwards.")
    while True:
        al = str(input("What is the alphabet ? Input elements one by one and input automaton when you are finished :"))
        if al == "automaton":
            break
        else:
            pre_alphabet.append(al)
    alphabet = [i for j, i in enumerate(pre_alphabet) if i not in pre_alphabet[:j]]  # deletes duplicates
    print("\n\n")

    # for the states
    pre_state = []
    print("If there are duplicates they will be deleted afterwards.")
    while True:
        st = str(input("What are the states ? Input states one by one and input automaton when you are finished :"))
        if st == "automaton":
            break
        else:
            pre_state.append(st)
    states = [i for j, i in enumerate(pre_state) if i not in pre_state[:j]]  # deletes duplicates
    print("\n\n")

    # for the init state
    while True:
        ini = str(input("What is the init state ? Make sure the state exists :"))
        if ini in states:
            init_state = ini
            break
        else:
            print("The state you entered does not exist. Please try again\n")
    print("\n\n")

    # for the final state
    f_states = []
    while True:
        num = int(input("How many final states ? This numb cannot exceed the number of existing states. Must be > 0"))
        if (num <= len(states)) & (num > 0):
            break
    if num == 1:
        while True:
            fin = str(input("What is the final state ? Make sure the state exists :"))
            if fin in states:
                break
            else:
                print("The state you entered does not exist. Please try again\n")
    else:
        finn_states = []
        print("If there are duplicates they will be deleted afterwards.")
        for k in range(num):
            while True:
                fin = str(input("List your final states one by one. Make sure the state exists. :"))
                if fin in states:
                    finn_states.append(fin)
                    break
                else:
                    print("The state you entered does not exist. Please try again\n")

        f_state = [i for j, i in enumerate(finn_states) if i not in finn_states[:j]]  # deletes duplicates
    print("\n\n")

    # for the transitions
    temp = {}
    transitions = {}
    for state in states:
        while True:
            nbr = int(input("How many transitions for this element? 0 if none, the maximum is the number of states"))
            if (nbr >= 0) & (nbr < len(states)):
                break
        for j in range(nbr):
            while True:
                t1 = str(input("Give the transition from the alphabet : "))
                if t1 in alphabet:
                    break
                else:
                    print("This element isn't in the alphabet. Please try again")
            while True:
                t2 = str(input("Give the state after the transition :"))
                if t2 in alphabet:
                    break
                else:
                    print("This element isn't in the states. Please try again")
            temp[t1] = t2
        transitions[state] = temp
        temp = ''
    print(transitions)

    automaton = {
        'name': name,
        'states': states,
        'alphabet': alphabet,
        'initial_state': init_state,
        'final_states': f_states,
        'transitions': transitions
    }

    return automaton


def aut_delete(list_auto, automaton):
    for i, aut in enumerate(list_auto):
        if aut == automaton:
            del list_auto[i]
            break

    return list_auto
