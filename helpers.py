import chemparse as cp
from pulp import * 
import streamlit as st

def parse(equation):
    lhs,rhs = equation.split('->')

    lhsCompounds = lhs.split("+")
    rhsCompounds = rhs.split("+")

    lhsCompounds = [e.strip() for e in lhsCompounds]
    rhsCompounds = [e.strip() for e in rhsCompounds]

    allCompounds = []
    uniqueElements= {}

    for compound in lhsCompounds:
        numElements = cp.parse_formula(compound)
        for key in numElements:
            uniqueElements[key] = ''
        allCompounds.append(numElements)

    for compound in rhsCompounds:
        numElements = cp.parse_formula(compound)
        numElements = { key:-val for key,val in numElements.items()}
        allCompounds.append(numElements)
    
    return lhsCompounds,rhsCompounds,uniqueElements, allCompounds


def balance(equation):
    lhsCompounds , rhsCompounds,uniqueElements, allCompounds = parse(equation)

    # Variables
    variables = []

    for idx, item in enumerate(allCompounds):
        variables.append( LpVariable('x'+str(idx),cat='Integer',lowBound = 1) )

    #Problem
    prob = LpProblem("Balance Equation",LpMinimize)
    prob += 0,"Objective Function"

    for element in uniqueElements:
        constraint = None
        for idx,compound in enumerate(allCompounds):
            constraint += variables[idx] * compound.get(element, 0)
        prob += constraint == 0,f'Constraint for {element}'


    st.text(prob)

    prob.solve()

    coeffs= [int(var.value()) for var in variables]

    balancedEquation = ""

    balancedCompounds = []
    for coeff, compound in zip( coeffs , lhsCompounds+rhsCompounds):
        balancedCompounds.append(str(coeff)+compound)

    balancedEquation += '+ '.join(balancedCompounds[:len(lhsCompounds)])
    balancedEquation += ' -> '
    balancedEquation += '+ '.join(balancedCompounds[len(lhsCompounds):])
    st.title("Balanced Equation")
    return balancedEquation

