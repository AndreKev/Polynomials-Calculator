# the defined module for text manipulation
from text_splitting import tokenizer,evaluate_postfix, infix_to_postfix 

# Function to evaluate a strinf in infix natation
def evaluate(string):
    infix = []
    for token in tokenizer(string):
        infix.append(token)
    print(infix)
    postfix = infix_to_postfix(infix)
    result = evaluate_postfix(postfix)
    return result

# www.ictinovationwork.com

""" In order to handle the different errors in the code,
I must catch the inside code of the polynomial evaluator.

try: setting evaluator value
except: getting the error message and printing the error message on the alert frame
"""
