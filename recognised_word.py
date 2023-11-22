def recognised_word(automaton,word):
    tmp = automaton['initial_state']
    for i in word:
        tmp = automaton['transitions'][tmp][i]
        print(tmp+"\n")

    if tmp in automaton['final_states']:
        print("The word is recognised by the language")
        return 0

    print("The word is not recognised by the language")
    return 1

