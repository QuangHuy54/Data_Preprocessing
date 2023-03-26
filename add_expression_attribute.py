import pandas as pd
import numpy as np
import argparse


def add_expression_attribute(data: pd.DataFrame, output_path: str, formula: str, new_attribute_name: str) -> pd.DataFrame:
    # Splitting the formula into a list of operands and operators.
    formula = formula.replace('(', '( ')  # Add spaces for splitting
    formula = formula.replace(')', ' )')
    formula = formula.replace('+', ' + ')
    formula = formula.replace('-', ' - ')
    formula = formula.replace('*', ' * ')
    formula = formula.replace('/', ' / ')
    formula = formula.split(' ')
    formula = [x for x in formula if x != '']

    # Get attributes list from the formula
    attributes_list = [x for x in formula if not is_operator(x)]

    # If there are any attribute that doesn't exist, print the error
    if not all(attr in data.columns for attr in attributes_list):
        print("There are invalid attributes in your expression!")
        return data

    new_col = []  # the new attribute
    num_rows = data.shape[0]
    for i in range(num_rows):
        # Replace attributes' name with their values
        row_formula = [x if is_operator(x)
                       else data.loc[i, x] for x in formula]

        # If there are any value that isn't numeric, print error
        if not is_numeric_list([x for x in row_formula if not is_operator(x)]):
            print("Attribute have not numeric type!")
            return data

        # check nan value
        if all(not pd.isna(value) for value in row_formula):
            new_col.append(evaluate(row_formula))
        else:
            new_col.append(np.NAN)

    # Add new attribute and write to output file
    new_data = data
    new_data[new_attribute_name] = new_col
    new_data.to_csv(output_path, index=False)
    print("Saved to", output_path)

    return new_data


def is_operator(x):
    # Check if x is an operand or not
    return x in set(['+', '-', '*', '/', '(', ')'])


def is_numeric_list(lst):
    # Check if all element of lst is_numeric
    # If there are any element that isn't numeric, return false
    for val in lst:
        try:
            float(val)
        except ValueError:
            return False
    return True


def evaluate(formula):
    """
    Evaluate the formula.
    Idea: We iterate through the formula, pushing operands onto the operand stack and operators onto the
    operator stack. When we encounter a closing parenthesis, we pop the operator stack until we find the
    opening parenthesis, and then we evaluate the expression

    Args:
        formula (List): The list of operands and operators from expression
    Return:
        The final result of the formula
    """

    # Define operator precedence
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    # Initialize empty stacks for operators and operands
    operator_stack = []
    operand_stack = []

    for token in formula:
        if token in precedence:
            # If token is +, -, *, /; process the operation until reach '(' or empty stack
            while (len(operator_stack) > 0 and
                   operator_stack[-1] != '(' and
                   precedence[operator_stack[-1]] >= precedence[token]):
                process_operation(operator_stack, operand_stack)
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            # If token is ') process the operation until reach '('
            while operator_stack[-1] != '(':
                process_operation(operator_stack, operand_stack)
            operator_stack.pop()
        else:
            operand_stack.append(float(token))

    # Evaluate the remaining operators
    while len(operator_stack) > 0:
        operator = operator_stack.pop()
        operand2 = operand_stack.pop()
        operand1 = 0
        if len(operand_stack) > 0:
            operand1 = operand_stack.pop()
        result = evaluate_operation(operand1, operand2, operator)
        operand_stack.append(result)

    # Return the final result
    return operand_stack[0]


def process_operation(operator_stack, operand_stack):
    """
    It pops the top operator and operands from the stacks,
    evaluates the operation,
    and pushes the result back onto the operand stack

    :param operator_stack: a list of operators
    :param operand_stack: a list of operands
    """
    operator = operator_stack.pop()
    operand2 = operand_stack.pop()
    operand1 = operand_stack.pop()
    result = evaluate_operation(operand1, operand2, operator)
    operand_stack.append(result)


def evaluate_operation(operand1, operand2, operator):
    """
    It takes two operands and an operator and returns the result of the operation

    :param operand1: The first operand
    :param operand2: The second operand of the operation
    :param operator: The operator to be used in the operation
    :return: The result of the operation
    """
    if operator == '+':
        return operand1 + operand2
    elif operator == '-':
        return operand1 - operand2
    elif operator == '*':
        return operand1 * operand2
    elif operator == '/':
        return operand1 / operand2


if __name__ == '__main__':
    # Parsing the command line arguments
    argParser = argparse.ArgumentParser()
    argParser.add_argument("-i", "--input", help="path of file",
                           required=True)  # Adding input's path argument
    argParser.add_argument("-o", "--output", help="path of output file",
                           required=False)  # Adding output's path argument
    argParser.add_argument("-e", "--expression", help="expression of attributes",
                           required=False)  # Adding expression
    argParser.add_argument("-n", "--name", help="name of the new attribute",
                           required=False)  # Adding the name of the new attribute
    args = vars(argParser.parse_args())

    # Reading the csv file and storing it in a data-frame.
    data = pd.read_csv(args['input'])

    # If user doesn't enter the output file, this will be input name + _add_attribute
    # If user doesn't enter the new attribute's name, it will be newAttr
    add_expression_attribute(data, args['output'] or (
        args['input'][:-4] + "_add_attribute.csv"), args['expression'], args['name'] or "newAttr")
