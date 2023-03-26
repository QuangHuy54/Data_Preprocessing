import pandas as pd
import numpy as np
import argparse


def add_expression_attribute(data: pd.DataFrame, output_path: str, formula: str, new_attribute_name: str) -> pd.DataFrame:
    # Add space between the operators.
    # Then splitting the formula into a list of operands and operators.
    formula = formula.replace('(', '( ')
    formula = formula.replace(')', ' )')
    formula = formula.replace('+', ' + ')
    formula = formula.replace('-', ' - ')
    formula = formula.replace('*', ' * ')
    formula = formula.replace('/', ' / ')

    formula = formula.split(' ')
    formula = [x for x in formula if x != '']

    attributes_list = [x for x in formula if x not in set([
        '+', '-', '*', '/', '(', ')'])]

    if not all(attr in data.columns for attr in attributes_list):
        print("There are invalid attributes in your expression!")
        return data

    num_rows = data.shape[0]
    new_col = []
    for i in range(num_rows):
        row_formula = [x if is_operand(x) else data.loc[i, x] for x in formula]

        # check nan value
        if not is_numeric_list([x for x in row_formula if not is_operand(x)]):
            print("Attribute have not numeric type!")
            return data
        if all(not pd.isna(value) for value in row_formula):
            new_col.append(evaluate(row_formula))
        else:
            new_col.append(np.NAN)

    new_data = data
    new_data[new_attribute_name] = new_col
    new_data.to_csv(output_path, index=False)
    print("Saved to",output_path)
    return new_data


def is_operand(x):
    return x in set([
        '+', '-', '*', '/', '(', ')'])


def is_numeric_list(lst):
    for val in lst:
        try:
            float(val)
        except ValueError:
            return False
    return True


def evaluate(formula):
    # Define operator precedence
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2}

    # Initialize empty stacks for operators and operands
    operator_stack = []
    operand_stack = []

    for token in formula:
        if token in precedence:
            while (len(operator_stack) > 0 and
                   operator_stack[-1] != '(' and
                   precedence[operator_stack[-1]] >= precedence[token]):
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = evaluate_operation(operand1, operand2, operator)
                operand_stack.append(result)
            operator_stack.append(token)
        elif token == '(':
            operator_stack.append(token)
        elif token == ')':
            while operator_stack[-1] != '(':
                operator = operator_stack.pop()
                operand2 = operand_stack.pop()
                operand1 = operand_stack.pop()
                result = evaluate_operation(operand1, operand2, operator)
                operand_stack.append(result)
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


def evaluate_operation(operand1, operand2, operator):
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
                           required=False)  # Adding output's path argument
    argParser.add_argument("-n", "--name", help="name of the new attribute",
                           required=False)  # Adding output's path argument
    args = vars(argParser.parse_args())

    # Reading the csv file and storing it in a data-frame.
    data = pd.read_csv(args['input'])

    # Removing duplicate rows from the data-frame and writing the unique data to a new file.
    add_expression_attribute(data, args['output'] or (
        args['input'][:-4] + "_add_attribute.csv"), args['expression'], args['name'] or "newAttr")

# python3 add_expression_attribute.py -i input.csv -e "A-C*(B+D)"
