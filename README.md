# AutomatePython

Welcome on our program of finite state machine's (FSM). 
The goal of the program is to define, save, delete, modify, create and import an automaton.
You have to download the code to run the program. You may probably download it in a zip folder, which is important to unzip.
When it's unziped, it is important to have all files in the same directory.
You have 2 (or more) possibilities :
1) open "main.py" and press F5 or the "run" button ;
2) open a terminal, navigate to the folder with "cd" and enter "python main.py" : the program will start. 
When it's done, you will be asked to choose what do you want to do with automatons. 
You have 5 features : create, import, modify, save and delete an automaton.

To interact with the program, you have to follow instructions given in the main menu.

During the automaton's export, you can choose where you want to save it. When you have chosen the path, open the selected folder and you will find the automaton.
Concerning the automaton's import, you have to select the file you want to import, compatible with the following structure and import it :
```python
{
    'name': "automaton1",
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
```
To modify an automaton, select the element you want to interact with and modify it following the dedicated menu.
If you have any question or want more information, ask our service desk at landrysimo@cy-tech.fr.

