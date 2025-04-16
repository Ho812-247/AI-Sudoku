from csp import *
from copy import deepcopy
import util

def AC3(csp):
    queue = list(csp.constraints)
    while queue:
        (Xi, Xj) = queue.pop(0)
        if revise(csp, Xi, Xj):
            if len(csp.values[Xi]) == 0:
                return False
            for Xk in csp.peers[Xi]:
                if Xk != Xj:
                    queue.append((Xk, Xi))
    return True

def revise(csp, Xi, Xj):
    revised = False
    for x in csp.values[Xi]:
        satisfied = False
        for y in csp.values[Xj]:
            if x != y:
                satisfied = True
                break
        if not satisfied:
            csp.values[Xi] = csp.values[Xi].replace(x, "")
            revised = True
    return revised

def forward_checking(csp, var, value):
    for neighbor in csp.peers[var]:
        if value in csp.values[neighbor]:
            csp.values[neighbor] = csp.values[neighbor].replace(value, "")
            if len(csp.values[neighbor]) == 0:
                return False
    return True


def Backtracking_Search(csp):
    return Recursive_Backtracking({}, csp)

def Recursive_Backtracking(assignment, csp):
    if isComplete(assignment):
        return assignment

    var = Select_Unassigned_Variables(assignment, csp)
    domain_copy = deepcopy(csp.values)


    for value in Order_Domain_Values(var, assignment, csp):
        if isConsistent(var, value, assignment, csp):
            assignment[var] = value
            if forward_checking(csp, var, value): #check for the inference before going deep in recursion

                result = Recursive_Backtracking(assignment, csp)

                if result:
                    return result

            csp.values = deepcopy(domain_copy)  #backtrack
            del assignment[var] # Remove the assigned value before next iteration

    return False


def Select_Unassigned_Variables(assignment, csp):
    unassigned_variables = dict((square, len(csp.values[square])) for square in csp.values if square not in assignment)
    if unassigned_variables:
        mrv = min(unassigned_variables, key=unassigned_variables.get)
        return mrv
    return None




def Order_Domain_Values(var, assignment, csp):
    values = csp.values[var]
    if isinstance(values,list):
        return values

    return sorted(values, key=lambda value: sum(1 for neighbor in csp.peers[var] if neighbor not in assignment and value in csp.values[neighbor]))



def isComplete(assignment):
    return set(assignment.keys()) == set(squares)


def isConsistent(var, value, assignment, csp):
    for neighbor in csp.peers[var]:
        if neighbor in assignment and assignment[neighbor] == value:
            return False
    return True

def display(values):
    for row in rows:
        if row in 'DG':
            print("-------------------------------------------")
        for col in cols:
            if col in '47':
                print(' | ', values[row + col], ' ', end=' ')
            else:
                print(values[row + col], ' ', end=' ')
        print(end='\n')

def write(values):
    output = ""
    for variable in squares:
        output = output + values[variable]
    return output

def solve_sudoku(input_file):
    with open(input_file, 'r') as file:
        puzzles = file.readlines()

    solutions = []
    for puzzle in puzzles:
        grid = puzzle.strip()
        csp_obj = csp(grid=grid)


        if AC3(csp_obj): #call AC3 before backtracking and heuristics
            assignment = Backtracking_Search(csp_obj)

            if assignment:

                solutions.append(write(assignment) + '\n')
            else:
                solutions.append("No solution found.\n")
        else:
            solutions.append("No solution found.\n")


    with open("output.txt", "w") as outfile:
        outfile.writelines(solutions)