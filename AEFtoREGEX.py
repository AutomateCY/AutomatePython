def resolve_equations(initial_state, start: str, equations: dict[str, list[str]], passed_states: list[str],
                      states_to_not_aiden):
    passed_states.append(start)
    if len(equations[start]) > 1:
        if start not in equations[start] or start in states_to_not_aiden:
            for i in range(len(equations[start]) // 2):
                state = equations[start][i * 2 + 1]
                if state not in states_to_not_aiden and state != "€":
                    if state in passed_states:  # Replace + factorisation
                        # start remplace
                        value_state = equations[start][i * 2]
                        del equations[start][i * 2 + 1]
                        del equations[start][i * 2]
                        index = i * 2
                        for j in range(len(equations[state]) // 2):
                            new_value = value_state + equations[state][j * 2]
                            equations[start].insert(index, new_value)
                            equations[start].insert(index + 1, equations[state][j * 2 + 1])
                            index += 2
                        # end remplace
                        # start factorisation
                        states = [equations[start][k * 2 + 1] for k in range(len(equations[start]) // 2)]
                        duplicate = {}
                        for e in range(len(states)):
                            if states.count(states[e]) > 1:
                                if states[e] in duplicate:
                                    duplicate[states[e]].append(equations[start][e * 2])
                                else:
                                    duplicate[states[e]] = [equations[start][e * 2]]
                        for d in duplicate.keys():
                            index1 = equations[start].index(duplicate[d][0])
                            del equations[start][index1]
                            del equations[start][index1]
                            index2 = equations[start].index(duplicate[d][1])
                            del equations[start][index2]
                            del equations[start][index2]
                            new_value = duplicate[d][0] + "+" + duplicate[d][1]
                            equations[start].append(new_value)
                            equations[start].append(d)
                        # end factorisation
                        resolve_equations(initial_state, start, equations, passed_states, states_to_not_aiden)
                        break
                    else:
                        if len(equations[state]) == 2 and state not in equations[state]:  # When state=language state
                            equations[start][i * 2] = equations[start][i * 2] + equations[state][0]
                            equations[start][i * 2 + 1] = equations[state][1]
                            if start in equations[start]:
                                resolve_equations(initial_state, start, equations, passed_states, states_to_not_aiden)
                        elif len(equations[state]) == 4 and state not in equations[state]:
                            if (equations[state][3] == "€"):  # When state=language state + language epsilon
                                v = equations[start][i * 2]
                                equations[start][i * 2] = v + equations[state][0]
                                equations[start][i * 2 + 1] = equations[state][1]
                                equations[start].insert((i + 1) * 2, v + equations[state][2])
                                equations[start].insert((i + 1) * 2 + 1, "€")
                                if start in equations[start]:
                                    resolve_equations(initial_state, start, equations, passed_states,
                                                      states_to_not_aiden)
                            else:
                                resolve_equations(initial_state, state, equations, passed_states, states_to_not_aiden)
                        else:
                            resolve_equations(initial_state, state, equations, passed_states, states_to_not_aiden)
        elif start != initial_state:
            # ARDEN
            index_value_state = equations[start].index(start) - 1
            value_start = equations[start][index_value_state]
            new_exp = []
            for i in range(len(equations[start]) // 2):
                if i * 2 != index_value_state:
                    if len(equations[start][i * 2]) > 0:
                        e1 = "(" + value_start + ")*(" + equations[start][i * 2] + ")"
                    else:
                        e1 = "(" + value_start + ")*"
                    new_exp.append(e1)
                    new_exp.append(equations[start][i * 2 + 1])
            equations[start] = new_exp
            # Replace "start" in every equation it appears
            for l in equations.values():
                while start in l:
                    index = l.index(start) - 1
                    v = l[index]
                    del l[index]
                    del l[index]
                    for p in range(len(new_exp)):
                        if (p % 2 == 0):
                            l.insert(index + p, v + new_exp[p])
                        else:
                            l.insert(index + p, new_exp[p])


def regular_expression(equations, start):
    equations_not_changed_yet = {i: equations[i][:] for i in equations}
    resolve_equations(start, start, equations, [], [])
    while equations[start].count(start) + equations[start].count("€") != len(
            equations[start]) // 2 and equations_not_changed_yet != equations:
        equations_not_changed_yet = {i: equations[i][:] for i in equations}
        resolve_equations(start, start, equations, [], [start])
    if equations[start].count(start) + equations[start].count("€") == len(
            equations[start]) // 2:  # if the function found the expression
        count_start = equations[start].count(start)
        count_epsilon = equations[start].count("€")
        if count_epsilon > 1:  # if there are more than one epsilon -> factorisation
            index_start = equations[start].index("€") - 1
            index_to_del = []
            total_value = ""
            for i in range(len(equations[start]) // 2):
                if equations[start][i * 2 + 1] == "€":
                    value = equations[start][i * 2]
                    total_value = total_value + "+" + value
                    if i * 2 != index_start:
                        index_to_del.append(i * 2)
            equations[start][index_start] = total_value[1:]
            for i in range(len(index_to_del)):
                del equations[start][index_to_del[i] - i * 2 + 1]
                del equations[start][index_to_del[i] - i * 2]
        if count_start > 1:  # if there are more than one "start" -> factorisation
            index_start = equations[start].index(start) - 1
            index_to_del = []
            total_value = ""
            for i in range(len(equations[start]) // 2):
                if equations[start][i * 2 + 1] == start:
                    value = equations[start][i * 2]
                    total_value = total_value + "+" + value
                    if i * 2 != index_start:
                        index_to_del.append(i * 2)
            equations[start][index_start] = total_value[1:]
            for i in range(len(index_to_del)):
                del equations[start][index_to_del[i] - i * 2 + 1]
                del equations[start][index_to_del[i] - i * 2]
        # AIDEN
        value_start = ""
        value_epsilon = ""
        if start in equations[start]:
            value_start = "(" + equations[start][equations[start].index(start) - 1] + ")*"
        if "€" in equations[start]:
            value_epsilon = "(" + equations[start][equations[start].index("€") - 1] + ")"
        return value_start + value_epsilon
    else:  # if the function can't find the expression
        return "Oops, there was a problem while trying to find the expression."


def get_equation(dict):
    if dict["initial_states"][0] in dict['transitions']:
        equation = {}
        final = dict["final_states"][0]
        start = dict["initial_states"][0]
        dict = dict["transitions"]
        for key, values in dict.items():
            temp = []
            for key2, values2 in values.items():
                for item in values2:
                    temp.append(key2)
                    temp.append(item)
                if key == final:
                    temp.append('')
                    temp.append("€")
                equation[key] = temp
        if final not in dict:
            equation[final]=["","€"]
        return regular_expression(equation, start)
    else:
        return ""

# Tests#
# e = {"1": ["a", "2", "b", "3"], "2": ["b", "1", "a", "3"], "3": ["a", "1", "b", "2","","€"]}
# e = {"1": ["a", "2", "b", "3"], "2": ["b", "1"], "3": ["a", "2","","€"]}
# print(regular_expression(e, '1'))
# e = {'q0': ['1', 'q1'], 'q1': ['0', 'q1', '', '€']}
# print(regular_expression(e, 'q0'))
