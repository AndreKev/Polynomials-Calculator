# We will create a syntaxic analyser that returns $ if a word is recognised,
# else the position where the error happens
premiers = {
    "E" : ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X", "+", "-"],
    "E'": ["+", "-"],
    "T" : ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X"],
    "T'": ["*", "/"],
    "F" : ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X", "+", "-"],
    "F'": ["^"],
    "H" : ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X", "+", "-"],
    "H'": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "X", "+", "-"]
}

expexted_message = {
    "E" : "Expected a number, variable or +, - ",
    "E'": "Expected + or -",
    "T" : "Expected a number or variable",
    "T'": "Expected * or /",
    "F" : "Expected a number, variable or +, - ",
    "F'": "Expected exponentiation ^ ",
    "H" : "Expected a number, variable or +, - ",
    "H'": "Expected a number, variable or +, - "
}

def expectation(result):
    if result[0] == "$":
        if result[2] in ["E", "T", "F", "H", "H'"]:
            return expexted_message[result[2]] + "at the end"
    return expexted_message[result[2]] + " at position " + str(result[1])

class Pile(object):
    def __init__(self):
        self.pile = ["$"]
        self.sommet = 0

    def goup(self, value=None):
        self.pile.append(value)
        self.sommet += 1

    def godown(self):
        del self.pile[self.sommet]
        self.sommet -= 1

    def settop(self, value):
        self.pile[self.sommet] = value

    def gettop(self):
        return self.pile[self.sommet]

# Analyser for complex infix notations
def analysepol(infix_text):
    if not isinstance(infix_text, str):
        return -1
    else: # If the word is a string
        # Adding $ to word
        word = infix_text.replace(" ", "") + "$"
        # Creating our stack
        pile = Pile()
        pile.goup("E")
        # Our variables for testing
        error = False
        recognised = False
        current = 0
        # Trying to recognise a word
        while not error and not recognised:
            print("The stack is",pile.pile, "and the word is", word)
            match pile.gettop():
                case "E":
                    match word[0]:
                        case "+"|"-"|".":
                            pile.goup(word[0])
                        case _:
                            pile.settop("E'")
                            pile.goup("T")
                case "E'":
                    match word[0]:
                        case "+"|"-":
                            pile.settop("E")
                            pile.goup(word[0])
                        case "$"|")"|".":
                            pile.godown()
                        case _:
                            error = True
                case "T":
                    pile.settop("T'")
                    pile.goup("F")
                case "T'":
                    match word[0]:
                        case "*"|"/":
                            pile.settop("T")
                            pile.goup(word[0])
                        case "+"|"-"|"$"|")"|".":
                            pile.godown()
                        case _:
                            error = True
                case "F":
                    pile.settop("F'")
                    pile.goup("H")
                case "F'":
                    match word[0]:
                        case "^":
                            pile.settop("F")
                            pile.goup("^")
                        case "*"|"/"|"$"|"+"|"-"|")"|".":
                            pile.godown()
                        case _:
                            error = True
                case "H":
                    match word[0]:
                        case "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"X":
                            pile.settop("H'")
                            pile.goup(word[0])
                        case "+"|"-"|".":
                            pile.settop("H")
                            pile.goup(word[0])
                        case "(":
                            pile.settop("H'")
                            pile.goup(")")
                            pile.goup("E")
                            pile.goup("(")
                        case _:
                            error = True
                case "H'":
                    match word[0]:
                        case "("|"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"X"|".":
                            pile.settop("H")
                        case "*"|"/"|"^"|"$"|"+"|"-"|")":
                            pile.godown()
                        case _:
                            error = True
                case "("|")"|"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"X"|"+"|"-"|"*"|"/"|"^"|".":
                    if pile.gettop() == word[0]:
                        pile.godown()
                        word = word[1:]
                        current+=1
                    else:
                        error = True
                case "$":
                    if word[0] == pile.gettop():
                        recognised = True
                    else:
                        error = True
                case _:
                    error = True
        return [word, current, pile.gettop(), recognised]

# Analyser for simple infix notations
def analyse(infix_text):
    if not isinstance(infix_text, str):
        return -1
    else: # If the word is a string
        # Adding $ to word
        word = infix_text + "$"
        # Creating our stack
        pile = Pile()
        pile.goup("E")
        # Our variables for testing
        error = False
        recognised = False
        current = 0
        # Trying to recognise a word
        while not error and not recognised:
            print("The stack is",pile.pile, "and the word is", word)
            match pile.gettop():
                case "E":
                    pile.settop("G")
                    pile.goup("F")
                case "G":
                    if word[0] in ["+", "-", "*", "/"]:
                        pile.settop("E")
                        pile.goup(word[0])
                    elif word[0] in ["$", ")"]:
                        pile.godown()
                    else:
                        error = True
                case "F":
                    match word[0]:
                        case "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"X":
                            pile.settop(word[0])
                        case "+"|"-":
                            pile.goup(word[0])
                        case "(":
                            pile.settop(")")
                            pile.goup("E")
                            pile.goup("(")
                        case _:
                            error = True
                case "("|")"|"0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"|"X"|"+"|"-"|"*"|"/":
                    if pile.gettop() == word[0]:
                        pile.godown()
                        word = word[1:]
                        current+=1
                    else:
                        error = True
                case "$":
                    if word[0] == pile.gettop():
                        recognised = True
                    else:
                        error = True
                case _:
                    error = True
        return [word, current, pile.gettop(), recognised]
