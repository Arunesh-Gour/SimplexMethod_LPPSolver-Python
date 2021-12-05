import re
import numpy as np

from .dataStructures import (SimplexProblem, Constraint,)
from .customExceptions import CustomExceptions

class PreProcessor:
   """Pre-processes simplex LPP problem and frames as SimplexProblem.
   
   Contains pre-processors to process simplex LPP problems and frames
   them as SimplexProblem before being passed to SimplexAlgorithm.
   Each step can be invoked manually by calling separate functions or
   invoke multiple steps from just one function, automatically (almost).
   
   Methods
   -------
   processExpression (expression)
      Processes single expression.
      Converts expression string into list of tuples containing
      variables and coefficients in format (coefficient, 'variable').
   objectiveFunction (objFunc, simplexProblem=None, problemType='min')
      Processes objective function of a simplex problem.
      Processes objective function and generates a SimplexProblem
      if not provided.
   processConstraints (simplexProblem, constraints)
      Processes set of constraints for SimplexProblem.
   preProcess (objectiveFunction, constraints, problemType=None)
      Runs pre-processor's all steps, automatically (almost).
      Pre-processes simplex problem and generates a SimplexProblem.
   
   """
   
   def processExpression (expression):
      """Processes single expression.
      
      Converts expression string into list of tuples containing
      variables and coefficients in format (coefficient, 'variable').
      For constants, tuple will take the form (coefficient, '').
      
      Parameters
      ----------
      expression: str
         Single expression string.
         str containing terms in format 'coefficientVariable',
         where coefficient is a number (int, float, exponential, etc),
         followed by an alpha-numeric variable name followed by
         (+|-) another term.
      
      Returns
      -------
      NoneType
         If expression is invalid.
      list
         List of tuples of term in format (coefficient, 'variable').
         Coefficient is of type float, while variable is of type str.
      
      """
      if ((type(expression).__name__ != 'str') or (len(expression) < 1)):
         return None
      
      terms = []
      
      while expression != '':
         coefficient = re.findall(
            '^([+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?)[a-zA-Z]*',
            expression,
         )
         
         if (len(coefficient) < 1):
            if (expression[0] in ('-', '+',)):
               coefficient = expression[0] + '1'
               expression = expression[1:]
            else:
               coefficient = '1'
         else:
            coefficient = coefficient[0]
            expression = expression[(
               expression.index(coefficient) + len(coefficient)
            ):]
         
         if (len(expression) < 1):
            terms.append((float(coefficient), '',))
            break
         
         variable = re.findall(
            '^(\w+)[+-]?',
            expression,
         )
         
         if (len(variable) < 1):
            terms.append((float(coefficient), '',))
            continue
         
         variable = variable[0]
         
         expression = expression[(
            expression.index(variable) + len(variable)
         ):]
         
         terms.append((float(coefficient), str(variable),))
      
      return terms
   
   def objectiveFunction (objFunc, simplexProblem=None, problemType='min'):
      """Processes objective function of a simplex problem.
      
      Processes objective function and generates a SimplexProblem
      if not provided.
      
      Parameters
      ----------
      objFunc: str
         Objective function for simplex problem.
      simplexProblem: SimplexProblem, default=None
         SimplexProblem data structure, if created manually.
      problemType: str, default='min'
         Type of problem - minimization ('min') or maximization ('max').
      
      Returns
      -------
      NoneType
         If any of objFunc, simplexProblem, problemType is invalid.
      SimplexProblem
         Framed simplex problem.
      
      """
      
      if (problemType.lower() not in ('min', 'max',)):
         return None
      
      if (
            (simplexProblem != None)
            and (type(simplexProblem) != SimplexProblem)
         ):
         return None
      
      if (simplexProblem == None):
         simplexProblem = SimplexProblem()
      
      simplexProblem.problemType = problemType.lower()
      
      objFunc.replace(' ', '')
      objFunc = PreProcessor.processExpression(objFunc)
      if (objFunc in (None, '', [],)):
         return None
      
      simplexProblem.objectiveFunction = objFunc
      
      return simplexProblem
   
   def processConstraints (simplexProblem, constraints):
      """Processes set of constraints for SimplexProblem.
      
      Processes all constraints provided and attaches them in
      simplexProblem as new constraints.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         Framed simplex problem.
      constraints: list, str
         List of str constraint.
         str if there is only one constraint, but it will be upgraded to a
         list containing single constraint.
         Each constraint is of str containing terms in format
         'coefficientVariables' followed by multiple (if any) (+|-) terms
         or constants followed by equality sign ('<', '>', '=', '<=', '>=')
         followed by another set of terms or constants.
      
      Returns
      -------
      NoneType
         If error occured.
         On success.
      
      """
      
      if (type(constraints).__name__ == 'str'):
         constraints = [constraints,]
      
      if (type(constraints).__name__ not in ('list', 'tuple',)):
         return None
      
      if (simplexProblem.constraints == None):
         simplexProblem.constraints = []
      
      for constraint in constraints:
         constraintSet = Constraint()
         
         constraint = re.split(
            '(<=|>=|<|>|=)',
            constraint,
            1,
         )
         
         if (len(constraint) != 3):
            return None
         
         if (
               (len(re.findall('^(>|<|=)', constraint[0])) > 0)
               or (len(re.findall('^(>|<|=)', constraint[2])) > 0)
            ):
            return None
         
         lhs = PreProcessor.processExpression(
            constraint[0].replace(' ', '')
         )
         
         if (lhs in (None, [],)):
            return None
         
         lhsConstraints = [term
            for term in lhs
            if (term[1] != '')
         ]
         
         lhsConstant = sum([term[0]
            for term in lhs
            if (term[1] == '')
         ])
         constraintSet.equalityType = constraint[1]
         
         rhs = PreProcessor.processExpression(
            constraint[2].replace(' ', '')
         )
         
         if (rhs in (None, [],)):
            return None
         
         rhsConstraints = [
            ((0-float(term[0])), str(term[1]),)
            for term in rhs
            if (term[1] != '')
         ]
         
         rhsConstant = sum([term[0]
            for term in rhs
            if (term[1] == '')
         ])
         
         constraintSet.rhs = rhsConstant - lhsConstant
         
         lhsConstraints.extend(rhsConstraints)
         
         cVars = np.array([lhsConstraints[0],])
         
         for lhsConstraint in lhsConstraints[1:]:
            if (lhsConstraint[1] in cVars[:, 1]):
               cVIndex = np.where(cVars[:, 1] == lhsConstraint[1])[0][0]
               cVars[cVIndex][0] = float(cVars[cVIndex][0]) + lhsConstraint[0]
            else:
               cVars = list(cVars)
               cVars.append(lhsConstraint)
               cVars = np.array(cVars)
         
         constraintSet.lhs = [
            (float(list(term)[0]), str(list(term)[1]),)
            for term in list(cVars)
            if (float(list(term)[0]) != 0)
         ]
         
         simplexProblem.constraints.append(constraintSet)
   
   def preProcess (objectiveFunction, constraints, problemType=None):
      """Runs pre-processor's all steps, automatically (almost).
      
      Pre-processes simplex problem and generates a SimplexProblem.
      
      Parameters
      ----------
      objectiveFunction: str
         Objective function for simplex problem.
      constraints: list, str
         List of str constraint.
         str if there is only one constraint, but it will be upgraded to a
         list containing single constraint.
         Each constraint is of str containing terms in format
         'coefficientVariables' followed by multiple (if any) (+|-) terms
         or constants followed by equality sign ('<', '>', '=', '<=', '>=')
         followed by another set of terms or constants.
      problemType: str, default=None
         Type of problem - minimization ('min') or maximization ('max').
         Defaults to minimization ('min') type.
      
      Raises
      ------
      PreProcessError
         If there is an error during pre-processing.
      
      Returns
      -------
      SimplexProblem
         Framed simplex problem.
      
      """
      
      if (problemType == None):
         problemType = 'min'
      
      simplexProblem = PreProcessor.objectiveFunction(
         objectiveFunction,
         None,
         problemType,
      )
      
      if (simplexProblem == None):
         raise CustomExceptions.PreProcessError(
            objectiveFunction,
            constraints, problemType
         )
      
      PreProcessor.processConstraints(simplexProblem, constraints)
      
      if (
            (simplexProblem.constraints == None)
            or (len(simplexProblem.constraints) < 1)
         ):
         raise CustomExceptions.PreProcessError(
            objectiveFunction,
            constraints, problemType
         )
      
      return simplexProblem
