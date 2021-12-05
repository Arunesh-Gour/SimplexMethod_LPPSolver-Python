class StatusPrinter:
   def printRawInputs (objectiveFunction, constraints, problemType,
         error=None
      ):
      print(
         "Problem type: {0}".format(problemType)
         + "Objective function: {0};\n".format(objectiveFunction)
         + "Constraints: {0};\n".format(constraints)
      )
      if (error != None): print(error)
   
   def printPreFrameProblem (simplexProblem):
      objectiveFunction = ' '.join([
         (
            ('+' if (term[0] >= float(0)) else '')
            + str(term[0])
            + ''
            + term[1]
         )
         for term in simplexProblem.objectiveFunction
      ])
      
      constraints = ''
      
      if (len(simplexProblem.constraints) < 1):
         constraints = 'No constraints!'
      elif (len(simplexProblem.constraints) == 1):
         constraints = ' '.join([
            (
               ('+' if (term[0] >= float(0)) else '')
               + str(term[0])
               + ''
               + term[1]
            )
            for term in simplexProblem.constraints[0].lhs
         ])
         constraints += ' ' + simplexProblem.constraints[0].equalityType
         constraints += ' ' + str(simplexProblem.constraints[0].rhs)
      else:
         constraints = ' '.join([
            (
               ('+' if (term[0] >= float(0)) else '')
               + str(term[0])
               + ''
               + term[1]
            )
            for term in simplexProblem.constraints[0].lhs
         ])
         constraints += ' ' + simplexProblem.constraints[0].equalityType
         constraints += ' ' + str(simplexProblem.constraints[0].rhs)
         
         for cSet in simplexProblem.constraints[1:]:
            constraint = ' '.join([
               (
                  ('+' if (term[0] >= float(0)) else '')
                  + str(term[0])
                  + ''
                  + term[1]
               )
               for term in cSet.lhs
            ])
            constraint += ' ' + cSet.equalityType
            constraint += ' ' + str(cSet.rhs)
            
            constraints += '\n' + ' '*13 + constraint
      
      print(
         "Objective function: {0} Z = {1}\n".format(
            (
               'Minimize'
               if (simplexProblem.problemType == 'min')
               else 'Maximize'
            ),
            objectiveFunction,
         )
         + "Constraints: {0}\n".format(constraints)
      )
   
   def printPreCalcProblem (simplexProblem):
      objectiveFunction = ''.join([
         (
            ('+' if (term[0] >= float(0)) else '')
            + str(term[0])
            + ''
            + term[1]
         )
         for term in simplexProblem.auxillaryObjectiveFunction
      ])
      
      constraints = ''
      
      if (len(simplexProblem.auxillaryConstraints) < 1):
         constraints = 'No constraints!'
      elif (len(simplexProblem.auxillaryConstraints) == 1):
         constraints = ''.join([
            (
               ('+' if (term[0] >= float(0)) else '')
               + str(term[0])
               + ''
               + term[1]
            )
            for term in simplexProblem.auxillaryConstraints[0].lhs
         ])
         constraints += (
            ' '
            + simplexProblem.auxillaryConstraints[0].equalityType
         )
         constraints += (
            ' '
            + str(simplexProblem.auxillaryConstraints[0].rhs)
         )
         
         if (simplexProblem.auxillaryConstraints[0].slackVariable != None):
            constraints += ' ; {0}: slack variable'.format(
               simplexProblem.auxillaryConstraints[0].slackVariable,
            )
      else:
         constraints = ''.join([
            (
               ('+' if (term[0] >= float(0)) else '')
               + str(term[0])
               + ''
               + term[1]
            )
            for term in simplexProblem.auxillaryConstraints[0].lhs
         ])
         constraints += (
            ' '
            + simplexProblem.auxillaryConstraints[0].equalityType
         )
         constraints += (
            ' '
            + str(simplexProblem.auxillaryConstraints[0].rhs)
         )
         
         if (simplexProblem.auxillaryConstraints[0].slackVariable != None):
            constraints += ' ; {0}: slack variable'.format(
               simplexProblem.auxillaryConstraints[0].slackVariable,
            )
         
         for cSet in simplexProblem.auxillaryConstraints[1:]:
            constraint = ''.join([
               (
                  ('+' if (term[0] >= float(0)) else '')
                  + str(term[0])
                  + ''
                  + term[1]
               )
               for term in cSet.lhs
            ])
            constraint += ' ' + cSet.equalityType
            constraint += ' ' + str(cSet.rhs)
            
            if (cSet.slackVariable != None):
               constraint += ' ; {0}: slack variable'.format(
                  cSet.slackVariable,
               )
            
            constraints += '\n' + ' '*13 + constraint
      
      print(
         "Objective function: Maximize Z{0} = {1}\n".format(
            (
               "'"
               if (simplexProblem.problemType == 'min')
               else ''
            ),
            objectiveFunction,
         )
         + "Constraints: {0}\n".format(constraints)
      )
   
   def printStatus (simplexProblem):
      statusString = ''
      if (
            simplexProblem.terminationReason == (
               simplexProblem.Terminate.REACHED_OPTIMAL
            )
         ):
         statusString = 'Optimal solution found!'
      elif (
            simplexProblem.terminationReason == (
               simplexProblem.Terminate.UNBOUNDED_SOLUTION
            )
         ):
         statusString = "No solution found, reason - unbounded region."
      else:
         statusString = "Unable to deduce the solution, reason: {0}".format(
            simplexProblem.terminationReason
         )
      
      print("Status: {0}\n".format(statusString))
   
   def printIterationTable (iterationTable):
      aj = iterationTable.aj.copy()
      
      Cj = '\t'.join([
         '{0:04}'.format(round(iterationTable.Cj.get(a_j, float(0)), 2))
         for a_j in aj
      ])
      deltaJ = '\t'.join([
         '{0:04}'.format(round(iterationTable.deltaJ.get(a_j, float(0)), 2))
         for a_j in aj
      ])
      rows = '\n'.join([
         (
            str('\t'.join([
               '{0:04}'.format(round(row.CB, 2)), row.B,
               row.XB, '{0:04}'.format(round(row.b), 2),
               '\t'.join([
                  '{0:04}'.format(round(row.aj.get(a_j, float(0)), 2))
                  for a_j in aj
               ]),
            ]))
            + str(
               (
                  (
                     '\t{0:04}'.format(round(row.minRatio, 2))
                  ) + (
                     (
                        ' <--'
                     ) if (row.isKeyRow) else ''
                  )
               ) if (row.minRatio != None) else ''
            )
         )
         for row in iterationTable.rowi
      ])
      
      print(
         'Iteration: {0}\n\n'.format(iterationTable.iteration)
         + '{0}{1}\t{2}\n'.format('\t'*3, 'Cj', Cj)
         + 'CB\tB\tXB\tb\t{0}\tMinRatio\n'.format('\t'.join(aj))
         + '{0}\n'.format(rows)
         + '{0}{1}\t{2}\n'.format('\t'*3, 'deltaJ', deltaJ)
         + str(
            (
               'Key column: {0}\n'.format(iterationTable.keyColumn)
            ) if (iterationTable.keyColumn != None) else ''
         )
         + '-'*70 + '\n'
      )
      
   
   def printOptimalSolution (simplexProblem):
      solutionString = '; '.join([
         (
            xj
            + ' = '
            + str(round(value, 2))
         )
         for xj, value in simplexProblem.optimalSolution.Xj.items()
         if (xj[0] != simplexProblem.slackLetter)
      ]) or "All variables attain '0' as their value."
      
      print(
         'Optimal solution: {0}\n'.format(solutionString)
         + 'Optimal value: Z {0} = {1}\n'.format(
            simplexProblem.problemType,
            round(simplexProblem.optimalSolution.optimalValue, 2),
         )
      )
