import numpy as np

from .customExceptions import CustomExceptions
from .dataStructures import (
   Constraint, AuxillaryConstraint, Row, IterationTable,
   OptimalSolution, SimplexProblem
)

class SimplexAlgorithm:
   """Algorithm to calculate optimal solution for simplex LPP problem.
   
   Contains simplex algorithm steps divided into functions.
   Each step can be invoked manually by calling separate functions or
   invoke multiple steps from just one function, automatically (almost).
   
   Methods
   -------
   frameAuxillary (SimplexProblem)
      Frames auxillary components.
      Frames auxillary objective function and constraints which
      are required for further steps.
   frameInitialSimplexTable (SimplexProblem)
      Frames initial simplex table.
      Creates initial simplex table and forms initial basis.
   calculateDeltaJ (SimplexProblem)
      Calculates deltaJ.
      Calculates Zj, deltaJ = Zj-Cj for/from last IterationTable.
   calculateKeys (SimplexProblem)
      Calculates key values.
      Calculates key row, column, element for/from last IterationTable,
      minimum ratio for/from Row, only if SimplexProblem is not terminated
      and optimal solution hasn't been found.
   calculateNewIterationTable (SimplexProblem)
      Calculates new iteration table.
      Calculates new IterationTable, succeeding last IterationTable only
      if calculation has started and SimplexProblem is not terminated.
   frameOptimalSolution (SimplexProblem)
      Frames optimal feasible solution.
      Frames optimal solution from last IterationTable only if calculation
      has been terminated and optimal solution has been reached.
   calculateOptimalSolution (SimplexProblem)
      Calculates optimal solution, automatically.
      Runs all steps of simplex algorithm automatically to reach optimal
      solution, if exists.
   
   """
   
   def frameAuxillary (simplexProblem):
      """Frames auxillary components.

      Frames auxillary objective function and constraints which
      are required for further steps.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         SimplexProblem whose auxillary components has to be framed.
      
      """
      
      if (type(simplexProblem) != SimplexProblem):
         return None
      
      if (None in (
            simplexProblem.problemType,
            simplexProblem.objectiveFunction,
            simplexProblem.constraints,
         )):
         return None
      
      if (simplexProblem.problemType == 'min'):
         simplexProblem.auxillaryObjectiveFunction = [
            (0-float(term[0]), term[1],)
            for term in simplexProblem.objectiveFunction
         ]
      elif (simplexProblem.problemType == 'max'):
         simplexProblem.auxillaryObjectiveFunction = \
         simplexProblem.objectiveFunction.copy()
      
      simplexProblem.auxillaryConstraints = []
      variableList = [
         str(term[1])
         for term in simplexProblem.objectiveFunction
      ]
      [
         None
         for constraint in simplexProblem.constraints
         if (variableList.extend(
            list(np.array(constraint.lhs)[:, 1])
         ) != None)
      ]
      variableList = set([
         variable[0]
         for variable in variableList
      ])
      slackLetter = None
      
      for i in range(0, 25):
         if (chr(ord('d') + i) not in variableList):
            slackLetter = chr(ord('d') + i)
            break
         elif (chr(ord('D') + i) not in variableList):
            slackLetter = chr(ord('D') + i)
            break
      
      if (slackLetter == None):
         return None
      
      simplexProblem.slackLetter = slackLetter
      slacks = 0
      
      for constraint, cIndex in zip(
            simplexProblem.constraints,
            range(0, len(simplexProblem.constraints))
         ):
         if (constraint.equalityType == '>='):
            lhs = [
               (0-float(term[0]), term[1],)
               for term in constraint.lhs
            ]
            equalityType = '<='
            rhs = 0-float(constraint.rhs)
         elif (constraint.equalityType == '<='):
            lhs = constraint.lhs.copy()
            equalityType = '<='
            rhs = float(constraint.rhs)
         elif (constraint.equalityType == '='):
            lhs = constraint.lhs.copy()
            equalityType = '='
            rhs = float(constraint.rhs)
         elif (constraint.equalityType == '>'):
            lhs = [
               (0-float(term[0]), term[1],)
               for term in constraint.lhs
            ]
            equalityType = '<'
            rhs = 0-float(constraint.rhs)
         elif (constraint.equalityType == '<'):
            lhs = constraint.lhs.copy()
            equalityType = '<'
            rhs = float(constraint.rhs)
         else:
            return None
         
         auxillaryConstraint = AuxillaryConstraint()
         
         if (equalityType in ('<', '<=')):
            slacks += 1
            lhs.append((float(1), (slackLetter + str(slacks)),))
            auxillaryConstraint.slackVariable = (
               slackLetter + str(slacks)
            )
            equalityType = '='
            simplexProblem.auxillaryObjectiveFunction.append(
               (float(0), (slackLetter + str(slacks)),)
            )
         
         auxillaryConstraint.lhs = lhs
         auxillaryConstraint.equalityType = '='
         auxillaryConstraint.rhs = rhs
         simplexProblem.auxillaryConstraints.append(auxillaryConstraint)
      
      simplexProblem.slacks = slacks
   
   def frameInitialSimplexTable (simplexProblem):
      """Frames initial simplex table.
      
      Creates initial simplex table and forms initial basis.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         SimplexProblem whose initial simplex table has to be framed.
      
      """
      
      if (type(simplexProblem) != SimplexProblem):
         return None
      
      if (None in (
            simplexProblem.problemType,
            simplexProblem.objectiveFunction,
            simplexProblem.constraints,
            simplexProblem.auxillaryObjectiveFunction,
            simplexProblem.auxillaryConstraints,
         )):
         return None
      
      iterationTable = IterationTable()
      iterationTable.iteration = 1
      iterationTable.Cj = dict([
         term[::-1]
         for term in simplexProblem.auxillaryObjectiveFunction
      ])
      netVariables = list(iterationTable.Cj.keys())
      
      iterationTable.rowi = []
      
      for constraint, i in zip(
            simplexProblem.auxillaryConstraints,
            range(0, len(simplexProblem.auxillaryConstraints))
         ):
         row = Row()
         row.i = i
         row.aj = dict([
            term[::-1]
            for term in constraint.lhs
         ])
         row.b = float(constraint.rhs)
         if (constraint.slackVariable != None):
            row.B = constraint.slackVariable
            row.XB = constraint.slackVariable
            row.CB = float(0)
         else:
            row.B = constraint.lhs[-1][1]
            row.XB = constraint.lhs[-1][1]
            row.CB = float(iterationTable.Cj.get(row.XB, float(0)))
         
         netVariables.extend(list(row.aj.keys()))
         iterationTable.rowi.append(row)
      
      netVariables = tuple(set(netVariables))
      simplexProblem.netVariables = netVariables
      
      simplexProblem.AXBMaps = dict([
         ((str('a') + str(i + 1)), str(variable))
         for variable, i in zip(
            netVariables,
            range(0, len(netVariables))
         )
      ])
      simplexProblem.XABMaps = dict([
         (str(variable), (str('a') + str(i + 1)))
         for variable, i in zip(
            netVariables,
            range(0, len(netVariables))
         )
      ])
      
      iterationTable.Cj = dict([
         (simplexProblem.XABMaps[key], value)
         for key, value in iterationTable.Cj.items()
      ])
      iterationTable.Cj.update([
         (variable, float(0))
         for variable in
         list(set(
            set(simplexProblem.AXBMaps.keys())
            - set(iterationTable.Cj.keys())
         ))
      ])
      
      for row in iterationTable.rowi:
         row.B = simplexProblem.XABMaps[row.B]
         row.aj = dict([
            (simplexProblem.XABMaps[key], value)
            for key, value in row.aj.items()
         ])
         row.aj.update([
            (variable, float(0))
            for variable in
            list(set(set(simplexProblem.AXBMaps.keys()) - set(row.aj.keys())))
         ])
         row.CB = float(iterationTable.Cj[row.B])
      
      iterationTable.aj = list(simplexProblem.AXBMaps.keys())
      simplexProblem.iterationTables = [iterationTable,]
   
   def calculateDeltaJ (simplexProblem):
      """Calculates deltaJ.
      
      Calculates Zj, deltaJ = Zj-Cj for/from last IterationTable.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         SimplexProblem whose last IterationTable's Zj, deltaJ has to be
         calculated.
      
      """
      
      if (type(simplexProblem) != SimplexProblem):
         return None
      
      if (None in (
            simplexProblem.problemType,
            simplexProblem.objectiveFunction,
            simplexProblem.constraints,
            simplexProblem.auxillaryObjectiveFunction,
            simplexProblem.auxillaryConstraints,
            simplexProblem.iterationTables,
         )):
         return None
      
      simplexProblem.iterationTables[-1].zj = {}
      
      for row in simplexProblem.iterationTables[-1].rowi:
         row.zij = dict([
            (aj, float(row.CB * row.aj[aj]))
            for aj in row.aj.keys()
         ])
         
         simplexProblem.iterationTables[-1].zj.update([
            (
               aj,
               float(
                  float(
                     simplexProblem.iterationTables[-1].zj.get(aj, float(0))
                  )
                  + float(row.zij.get(aj, float(0)))
               ),
            )
            for aj in row.aj.keys()
         ])
      
      simplexProblem.iterationTables[-1].deltaJ = dict([
         (
            aj,
            float(
               simplexProblem.iterationTables[-1].zj.get(aj, float(0))
               - simplexProblem.iterationTables[-1].Cj.get(aj, float(0))
            ),
         )
         for aj in simplexProblem.iterationTables[-1].aj
      ])
   
   def calculateKeys (simplexProblem):
      """Calculates key values.
      
      Calculates key row, column, element for/from last IterationTable,
      minimum ratio for/from Row, only if SimplexProblem is not terminated
      and optimal solution hasn't been found.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         SimplexProblem whose last IterationTable's key components are
         to be calculated.
      
      """
      
      if (type(simplexProblem) != SimplexProblem):
         return None
      
      if (None in (
            simplexProblem.terminated,
            simplexProblem.iterationTables,
            simplexProblem.iterationTables[-1].deltaJ,
         )):
         return None
      
      if (simplexProblem.terminated == True):
         return None
      
      keyColumn = None
      mostNegativeDeltaJ = float(0)
      for aj, deltaj in simplexProblem.iterationTables[-1].deltaJ.items():
         if (deltaj < mostNegativeDeltaJ):
            keyColumn = aj
            mostNegativeDeltaJ = deltaj
      
      if (mostNegativeDeltaJ >= float(0)):
         simplexProblem.terminated = True
         simplexProblem.terminationReason = (
            SimplexProblem.Terminate.REACHED_OPTIMAL
         )
         
         return None
      
      simplexProblem.iterationTables[-1].keyColumn = keyColumn
      
      keyRow = None
      leastPositiveRatio = float('inf')
      
      for row in simplexProblem.iterationTables[-1].rowi:
         row.minRatio = float(CustomExceptions.safe_execute(
            float('inf'), lambda: (row.b / row.aj.get(keyColumn, float(0))),
         ))
         
         row.isKeyRow = False
         
         if (
               (row.minRatio < leastPositiveRatio)
               and (row.minRatio > float(0))
            ):
            keyRow = row
            leastPositiveRatio = row.minRatio
      
      if (
            (keyRow == None)
            or (leastPositiveRatio == float('inf'))
         ):
         simplexProblem.terminated = True
         simplexProblem.terminationReason = (
            SimplexProblem.Terminate.UNBOUNDED_SOLUTION
         )
         
         return None
      
      simplexProblem.iterationTables[-1].keyRow = keyRow
      keyRow.isKeyRow = True
      simplexProblem.iterationTables[-1].keyElement = keyRow.aj.get(
         keyColumn, float(0)
      )
      
      simplexProblem.terminated = False
   
   def calculateNewIterationTable (simplexProblem):
      """Calculates new iteration table.
      
      Calculates new IterationTable, succeeding last IterationTable only
      if calculation has started and SimplexProblem is not terminated.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         SimplexProblem whose new IterationTable is to be calculated.
      
      """
      
      if (type(simplexProblem) != SimplexProblem):
         return None
      
      if (None in (
            simplexProblem.terminated,
            simplexProblem.iterationTables,
            simplexProblem.iterationTables[-1].keyRow,
            simplexProblem.iterationTables[-1].keyColumn,
            simplexProblem.iterationTables[-1].keyElement,
         )):
         return None
      
      if (simplexProblem.terminated == True):
         return None
      
      oldIterationTable = simplexProblem.iterationTables[-1]
      newIterationTable = IterationTable()
      
      newIterationTable.iteration = oldIterationTable.iteration + 1
      newIterationTable.Cj = oldIterationTable.Cj.copy()
      newIterationTable.aj = oldIterationTable.aj.copy()
      newIterationTable.rowi = []
      
      for oldRow in oldIterationTable.rowi:
         newRow = Row()
         newRow.i = oldRow.i
         
         if (oldRow.isKeyRow == True):
            newRow.B = oldIterationTable.keyColumn
            newRow.XB = simplexProblem.AXBMaps[newRow.B]
            newRow.CB = newIterationTable.Cj.get(newRow.B, float(0))
            
            newRow.b = CustomExceptions.safe_execute(
               float(oldRow.b * float('inf')),
               lambda: (oldRow.b / oldIterationTable.keyElement)
            )
            
            newRow.aj = dict([
               (
                  aj,
                  float(1)
                  if (aj == oldIterationTable.keyColumn)
                  else CustomExceptions.safe_execute(
                     float(oldRow.aj[aj] * float('inf')),
                     lambda: (oldRow.aj[aj] / oldIterationTable.keyElement)
                  )
               )
               for aj, aij in oldRow.aj.items()
            ])
         else:
            newRow.B = oldRow.B
            newRow.XB = oldRow.XB
            newRow.CB = oldRow.CB
            
            newRow.b = (
               oldRow.b
               - CustomExceptions.safe_execute(
                  float(0),
                  lambda: (
                     (
                        (oldIterationTable.keyRow.b)
                        * (oldRow.aj.get(oldIterationTable.keyColumn, float(0)))
                     )
                     / (oldIterationTable.keyElement)
                  ),
               )
            )
            
            newRow.aj = dict([
               (
                  aj,
                  float(0)
                  if (aj == oldIterationTable.keyColumn)
                  else float(
                     aij
                     - CustomExceptions.safe_execute(
                        float(0),
                        lambda: (
                           (
                              (oldIterationTable.keyRow.aj.get(aj, float(0)))
                              * (
                                 oldRow.aj.get(
                                    oldIterationTable.keyColumn, float(0)
                                 )
                              )
                           )
                           / (oldIterationTable.keyElement)
                        ),
                     )
                  )
               )
               for aj, aij in oldRow.aj.items()
            ])
         
         newIterationTable.rowi.append(newRow)
      
      simplexProblem.iterationTables.append(newIterationTable)
   
   def frameOptimalSolution (simplexProblem):
      """Frames optimal feasible solution.
      
      Frames optimal solution from last IterationTable only if calculation
      has been terminated and optimal solution has been reached.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         SimplexProblem whose optimal solution has to be framed.
      
      """
      
      if (type(simplexProblem) != SimplexProblem):
         return None
      
      if (None in (
            simplexProblem.terminated,
            simplexProblem.iterationTables,
         )):
         return None
      
      if (
            (simplexProblem.terminated == False)
            or (simplexProblem.terminationReason
               != SimplexProblem.Terminate.REACHED_OPTIMAL
            )
         ):
         return None
      
      iterationTable = simplexProblem.iterationTables[-1]
      
      optimalSolution = OptimalSolution()
      optimalSolution.iterationTable = simplexProblem.iterationTables[-1]
      
      optimalSolution.Xj = dict([
         (row.XB, float(row.b),)
         for row in simplexProblem.iterationTables[-1].rowi
      ])
      
      optimalValue = sum([
         (
            term[0]
            * optimalSolution.Xj.get(term[1], float(0))
         )
         for term in simplexProblem.auxillaryObjectiveFunction
      ])
      
      optimalSolution.optimalValue = (
         optimalValue
         if (simplexProblem.problemType == 'max')
         else
         (float(0) - optimalValue)
      )
      
      simplexProblem.optimalSolution = optimalSolution
   
   def calculateOptimalSolution (simplexProblem):
      """Calculates optimal solution, automatically.
      
      Runs all steps of simplex algorithm automatically to reach optimal
      solution, if exists.
      
      Raises
      ------
      FrameError
         Raises when there is an error in framing process.
      CalculationError
         Raises when there is an error in calculation process.
      
      Parameters
      ----------
      simplexProblem: SimplexProblem
         SimplexProblem whose optimal solution has to be calculated.
      
      """
      
      if (type(simplexProblem) != SimplexProblem):
         return None
      
      if (None in (
            simplexProblem.problemType,
            simplexProblem.objectiveFunction,
            simplexProblem.constraints,
         )):
         return None
      
      SimplexAlgorithm.frameAuxillary(simplexProblem)
      
      if (
            (simplexProblem.auxillaryConstraints == None)
            or (len(simplexProblem.auxillaryConstraints) < 1)
            or (simplexProblem.auxillaryObjectiveFunction == None)
            or (len(simplexProblem.auxillaryObjectiveFunction) < 1)
            or (simplexProblem.slackLetter == None)
         ):
         raise CustomExceptions.FrameError(simplexProblem)
      
      SimplexAlgorithm.frameInitialSimplexTable(simplexProblem)
      
      if (
            (simplexProblem.AXBMaps == None)
            or (len(simplexProblem.AXBMaps) < 1)
            or (simplexProblem.XABMaps == None)
            or (len(simplexProblem.XABMaps) < 1)
            or (simplexProblem.iterationTables == None)
            or (len(simplexProblem.iterationTables) < 1)
         ):
         raise CustomExceptions.FrameError(simplexProblem)
      
      while True:
         SimplexAlgorithm.calculateDeltaJ(simplexProblem)
         
         if (simplexProblem.iterationTables[-1].deltaJ == None):
            raise CustomExceptions.CalculationError(simplexProblem)
         
         simplexProblem.terminated = False
         
         SimplexAlgorithm.calculateKeys(simplexProblem)
         
         if (simplexProblem.terminated == False):
            oldIteration = simplexProblem.iterationTables[-1].iteration
            
            SimplexAlgorithm.calculateNewIterationTable(simplexProblem)
            
            if (simplexProblem.iterationTables[-1].iteration <= oldIteration):
               raise CustomExceptions.CalculationError(simplexProblem)
            
            continue
         else:
            if (
                  simplexProblem.terminationReason == (
                     SimplexProblem.Terminate.REACHED_OPTIMAL
                  )
               ):
               SimplexAlgorithm.frameOptimalSolution(simplexProblem)
            
            break
