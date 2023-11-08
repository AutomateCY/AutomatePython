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

print("\nWelcome to our finite state machine's (FSM) program ! \n")

#name=input("Please, tell me your name : ")
#print("Welcome "+name+" ! We recommend you to read the 'ReadMe.txt' to find out more about how our code works.")
print("Many options are possible : ")
print("   1 - enter a FSM")
print("   2 - import a FSM from a file")
print("   3 - modify a FSM")
print("   4 - save a FSM in a file")
print("   5 - delete a FSM")
choice=input("What would you like to do ? (chose the number of the option wanted) ")
print(choice) #c'est un test

match choice:
    case '1':
        print("You have choosen to enter a FSM")
        #creation_AEF()
    case '2':
        print("You have choosen to import an AEF from a file")
        path=input("Please, enter your file's path")
        #creation_AEF()
    case '3':
        print("You have choosen to modify a FSM. What would you do ?")
    case '4':
        print("You have choosen to save a FSM in a file.")
        #afficher_liste_FSM
        FSM_to_save=input("Which FSM would you like to save ?")
    case '5':
        print("You have choosen to save a FSM in a file.")
        #afficher_liste_FSM
        FSM_to_delete = input("Which FSM would you like to delete ?")
    case _:
        print('This is not a valid choice. Please, try again.')
        exit(1)