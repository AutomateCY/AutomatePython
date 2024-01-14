from time import sleep

from deterministic import *
from import_file import *
from input_modify import *
from make_complete import *
from minimal import *
from operations import *
from recognised_word import *
from save import *
from AEFtoREGEX import *

# example of a list with one automaton
# list_automatons = [{
#     'name': "automate1",
#     'states': ['q0', 'q1'],
#     'alphabet': ['0', '1'],
#     'initial_states': ['q0'],
#     'final_states': ['q1'],
#     'transitions': {
#         'q0': {'1': ['q1']},
#         'q1': {'0': ['q1']},
#     }
# }]


list_automatons = []


def main_loop():
    if len(list_automatons) == 0: # if there is no automaton created
        print("You need to create a automaton first. There are 2 options to create one : ")
        print("   1 - enter a FSM")
        print("   2 - import a FSM from a file")
        print("   3 - quit")
        choice = input("What would you like to do ? (choose the number of the option wanted) ")
        match choice:
            case '1':
                print("You have chosen to enter a FSM. \n")
                list_automatons.append(input_automaton())
                main_loop()

            case '2':
                print("You have chosen to import an AEF from a file. \n")
                import_file(list_automatons)
                main_loop()
            case '3':
                return 0
            case _:
                main_loop()
    else: # if there is at least one automaton created
        print("Many options are possible : ")
        print("   1 - enter a FSM")
        print("   2 - import a FSM from a file")
        print("   3 - modify a FSM")
        print("   4 - save a FSM in a file")
        print("   5 - delete a FSM")
        print("   6 - verify if a word is recognized by a FSM")
        print("   7 - check if a FSM is deterministic")
        print("   8 - make a FSM deterministic")
        print("   9 - perform operations on a FSM (mirror, multiplicate ...)")
        print("   10 - show a FSM's regular expression or known language")
        print("   11 - show if 2 FSM are equivalent")
        print("   12 - make a FSM pruned")
        print("   13 - make a FSM minimal")
        print("   14 - check if a FSM is complete")
        print("   15 - make a FSM complete")
        print("   16 - print a automaton")
        print("   17 - quit")
        choice = input("What would you like to do ? (choose the number of the option wanted) ")
        match choice:
            case '1':
                print("You have chosen to enter a FSM. \n")
                list_automatons.append(input_automaton())
                main_loop()

            case '2':
                print("You have chosen to import an AEF from a file. \n")
                import_file(list_automatons)
                main_loop()

            case '3':
                print("You have chosen to modify a FSM. Which one would you like to modify ? \n")
                input_automaton(auto_choice(list_automatons))
                main_loop()

            case '4':
                print("You have chosen to save a FSM in a file. Which automaton would you like to save ? \n")
                saveAutomaton(auto_choice(list_automatons))
                main_loop()

            case '5':
                print("You have chosen to delete a FSM . Which automaton would you like to delete ? \n")
                aut_delete(list_automatons, auto_choice(list_automatons))
                print("New automaton list : \n")
                print_function(list_automatons)
                main_loop()
            case '6':
                print(
                    "You have chosen to verify if a word is recognized by a FSM. Which automaton would you like to choose ? \n")
                chosen_automaton=auto_choice(list_automatons)
                word_to_verify=input("Enter the word you want to verify : ")
                if recognised_word(chosen_automaton,word_to_verify):
                    print("This word is recognized by this automaton.")
                else:
                    print("This word isn't recognized by this automaton.")
                main_loop()
            case '7':
                print(
                    "You have chosen to check if a FSM deterministic. Which automaton would you like to check ? \n")
                if isdeter(auto_choice(list_automatons)):
                    print("This automaton is deterministic.")
                else:
                    print("This automaton isn't deterministic.")
                main_loop()

            case '8':
                print(
                    "You have chosen to make a FSM deterministic. Which automaton would you like to make deterministic ? \n")
                auto_to_save(make_deter(auto_choice(list_automatons)))
                main_loop()

            case '9':
                print(
                    "You have chosen to perform operations on a FSM. On which automaton would you like to perform operations ? \n")
                num = '0'
                while not (num == '1' or num == '2' or num == '3' or num == '4'):
                    num = input("1 for complement | 2 for Mirror | 3 for Product | 4 for concatenation | 5 for quit")
                if num == '1':
                    current_dict = auto_choice(list_automatons)
                    if is_complete(current_dict) == 0:
                        auto_to_save(complement(current_dict))
                    main_loop()
                elif num == '2':
                    auto_to_save(
                        mirror(auto_choice(list_automatons)))
                    main_loop()
                elif num == '3':
                    auto_to_save(product(auto_choice(list_automatons), auto_choice(list_automatons)))
                    main_loop()
                elif num == '4':
                    auto_to_save(concatenation(auto_choice(list_automatons), auto_choice(list_automatons)))
                    main_loop()
                elif num == '5':
                    main_loop()
            case '10':
                print(
                    "You have chosen to show a FSM's regular expression and known language. Which automaton would you "
                    "like to show a FSM's regular expression and known language ? \n")
                print("The regular expression is : ", get_equation(make_deter(auto_choice(list_automatons))))
                sleep(5)
                main_loop()

            case '11':
                print(
                    "You have chosen to show if 2 FSM are equivalent. Which automatons would you like to see their equivalence ? \n")
                choice1 = get_equation(make_deter(auto_choice(list_automatons)))
                choice2 = get_equation(make_deter(auto_choice(list_automatons)))
                if choice1 == choice2:
                    print("These FSM are equivalent")
                    sleep(5)
                main_loop()

            case '12':
                print("You have chosen to make a FSM pruned. Which automaton would you like to make pruned ? \n")
                auto_to_save(pruned(auto_choice(list_automatons)))
                main_loop()

            case '13':
                print("You have chosen to make a FSM minimal. Which automaton would you like to make minimal ? \n")
                auto_to_save(make_minimal(auto_choice(list_automatons)))
                main_loop()

            case '14':
                print("You have chosen to check if a FSM is complete. Which automaton would you like to check ?")
                is_complete(auto_choice(list_automatons))
                sleep(5)
                main_loop()
            case '15':
                print("You have chosen to make a FSM complete. Which automaton would you like to make complete ?")
                auto_to_save(make_complete(auto_choice(list_automatons)))
                main_loop()
            case '16':
                print_automaton(auto_choice(list_automatons))
                main_loop()
            case '17':
                return 0
            case _:
                main_loop()


def print_automaton(automaton):
    print("Name : ", automaton["name"])
    print("States : ", ", ".join(automaton["states"]))
    print("Alphabet : ", ", ".join(automaton["alphabet"]))
    print("Initial states : ", ", ".join(automaton["initial_states"]))
    print("Final states : ", ", ".join(automaton["final_states"]))
    print("Transitions :")
    for i in automaton["transitions"]:
        for j in automaton["transitions"][i]:
            for k in automaton["transitions"][i][j]:
                print(i, " -> ", j, " -> ", k)
    print("\n")


def print_function(list_auto):
    j = 0
    for i in list_auto:
        print(j, " - ", i["name"], "\n")
        j += 1


def auto_choice(list_fsm):
    print_function(list_fsm)
    number = '€'
    choices = list(range(len(list_fsm)))
    choices = [str(x) for x in choices]
    while not ((number in choices) and (number.isdigit())):
        number = input("Your choice (if stop, you come back to the main menu) : ")
        if number == "stop":
            main_loop()
    return list_fsm[int(number)]


def auto_to_save(automaton, listauto=list_automatons):
    print(automaton)
    choice = '2'
    while not (choice == '0' or choice == '1'):
        choice = input("Would you like to save the automaton in the list ? (0 for Yes and 1 for No) ")
    if choice == '0':
        listauto.append(automaton)


def welcome():
    print("\nWelcome to our finite state machine's (FSM) program ! \n")

    name = input("Please, tell me your name : ")
    print(
        "Welcome " + name + " ! We recommend you to read the 'ReadMe.md' to find out more about how our code works. \n")


welcome()
main_loop()
