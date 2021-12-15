import re

params = []
functions = []
constants = []
rules = []
rules_size = {}
text = []

def extract_params(line):
    res = ['']
    balance = 0
    for c in line:
        if balance > 0:
            print("Wrong terms syntax with brackets at " + line)
            quit()
        if c == ',' and balance == 0:
            res.append('')
        else:
            res[-1] += c

            if c == '(':
                balance -= 1
            elif c == ')':
                balance += 1
    return res


def parse_term(line):
    # print(str)
    regexp = r'([a-zA-Z]+|([a-zA-Z]+\(.*\)))'
    if not re.fullmatch(regexp, line):
        print("Wrong terms syntax at " + line)
        quit()
    if "(" and ")" not in line:
        if line not in params and line not in constants:
            constants.append(line)
        return [line]

    if (line.find("(") == -1 and line.find(")") != -1) or (line.find("(") != -1 and line.find(")") == -1):
        print("Wrong brackets at " + line)
        quit()

    if line.find("(") > line.find(")"):
        print("Wrong brackets at " + line)
        quit()

    open_ind = line.find("(")
    close_ind = line.rfind(")")
    terms = [parse_term(term) for term in extract_params(line[open_ind+1:close_ind])]

    functions.append(line[:open_ind])
    if line[:open_ind] not in rules_size.keys():
        rules_size[line[:open_ind]] = len(terms)
    elif len(terms) != rules_size[line[:open_ind]]:
        print("Error with count of arguments of " + line[:open_ind])
        quit()

    return [line[:open_ind]] + terms


def parse_terms(line):
    line = line.replace(' ', '')
    if "->" not in line:
        print("Error in " + line)
        quit()
    term1 = parse_term(line.split('->')[0])
    term2 = parse_term(line.split("->")[1])
    # print(str(term1) + "->" + str(term2))
    rules.append([term1, term2])


def parse(path):
    global params
    with open(path) as file:
        lines = file.read().split('\n')
        text = file.read().split('\n')
        print(lines)

        if len(lines) < 2:
            print("Error")
            quit()

        params_r = r'\[([a-zA-Z])+(,[a-zA-Z])*\]'
        if not re.fullmatch(params_r, lines[0].strip()):
            print("Error in first line")
            quit()
        params = lines[0].strip()[1:-1].split(",")
        for line in lines[1:]:
            if line.strip() != "":
                parse_terms(line)
        return lines


def check_functions_and_const(functions, constants):
    for func in functions:
        if func in constants:
            print("Error, " + func + " is function and constant")
            quit()


text = parse("hahaton.txt")[1:]
if len(rules) == 0:
    print("there no rules")
    quit()
check_functions_and_const(functions, constants)


# def unificate(term1, term2):
#     pass
#
#
# for rule1 in rules:
#     term1 = rule1[1]
#     for rule2 in rules:
#         term2 = rule2[1]
#         if unificate(term1, term2):
#             print("False")
#             quit()




print(text)
# print(params)
#print(functions)
# print(constants)
