import time

from .statusPrinter import StatusPrinter as sp
from .osCommands import OSCommands as osc
from .simplex import (PreProcessor, SimplexAlgorithm, CustomExceptions)

def runCalculation (problemType, objectiveFunction, constraints):
   simplexProblem = None
   try:
      simplexProblem = PreProcessor.preProcess(
         objectiveFunction, constraints, problemType
      )
   except Exception as exception:
      osc.CLEAR()
      print('Simplex Method : Simplex Problem : Calculation\n')
      sp.printRawInputs(
         objectiveFunction, constraints, problemType,
         error=exception
      )
      return None
   
   try:
      SimplexAlgorithm.calculateOptimalSolution(simplexProblem)
   except CustomExceptions.FrameError as exception:
      osc.CLEAR()
      print('Simplex Method : Simplex Problem : Calculation\n')
      sp.printPreFrameProblem(simplexProblem)
      return None
   except CustomExceptions.CalculationError as exception:
      osc.CLEAR()
      print('Simplex Method : Simplex Problem : Calculation\n')
      sp.printPreCalcProblem(simplexProblem)
      return None
   except Exception as error:
      osc.CLEAR()
      print('Simplex Method : Simplex Problem : Calculation\n')
      print(error)
      return None
   
   osc.CLEAR()
   print('Simplex Method : Simplex Problem : Calculation\n')
   sp.printPreCalcProblem(simplexProblem)
   sp.printStatus(simplexProblem)
   
   if (
         simplexProblem.terminationReason in (
            simplexProblem.Terminate.REACHED_OPTIMAL,
            simplexProblem.Terminate.UNBOUNDED_SOLUTION,
         )
      ):
      for iterationTable in simplexProblem.iterationTables:
         sp.printIterationTable(iterationTable)
   
   if (
         simplexProblem.terminationReason == (
            simplexProblem.Terminate.REACHED_OPTIMAL
         )
      ):
      sp.printOptimalSolution(simplexProblem)
   
   return None

def runSimplexMethod ():
   wPress = 0
   problemType = None
   objectiveFunction = None
   constraints = []
   
   while True:
      osc.CLEAR()
      print('Simplex Method : Simplex Problem\n')
      problemType = input('Problem type (*m-min|M-max|q-quit): ')
      
      if (problemType in ('m', '0', '',)):
         problemType = 'min'
         break
      elif (problemType in ('M', '1', ' ')):
         problemType = 'max'
         break
      elif (problemType.lower() == 'min'):
         problemType = 'min'
         break
      elif (problemType.lower() == 'max'):
         problemType = 'max'
         break
      elif (problemType.lower() in ('q', '-1', 'quit', 'no', 'n')):
         print('\nDiscarding problem ...')
         time.sleep(0.5)
         return None
      else:
         wPress += 1
         print('\nInvalid selection!')
         if (wPress < 10):
            time.sleep(0.4)
            continue
         else:
            print('\nDiscarding problem ...')
            time.sleep(0.5)
            return None
   
   wPress = 0
   
   while True:
      osc.CLEAR()
      print('Simplex Method : Simplex Problem\n')
      
      print(
         'Problem: {0} Z'.format(
            'Minimize' if (problemType == 'min') else 'Maximize'
         )
      )
      print('-'*40, '\n')
      
      objectiveFunction = input('Objective function Z (x1-3x2+2x3|q-quit): ')
      
      if (
            objectiveFunction.lower()
            in ('q', '0', '1', '-1', 'quit', 'no', 'n')
         ):
         print('\nDiscarding problem ...')
         time.sleep(0.5)
         return None
      elif (len(objectiveFunction) >= 2):
         break
      else:
         wPress += 1
         print('\nInvalid selection!')
         if (wPress < 10):
            time.sleep(0.4)
            continue
         else:
            print('\nDiscarding problem ...')
            time.sleep(0.5)
            return None
   
   wPress = 0
   
   while True:
      osc.CLEAR()
      print('Simplex Method : Simplex Problem\n')
      
      print(
         'Problem: {0} Z'.format(
            'Minimize' if (problemType == 'min') else 'Maximize'
         )
      )
      
      if (len(constraints) > 0):
         print('\nConstraints::')
         for cS in constraints:
            print(cS)
      
      print('-'*40, '\n')
      
      constraint = input('Constraint (x1-3x2+2x3>=12-x4|c-continue|q-quit): ')
      
      if (
            constraint.lower()
            in ('q', '0', '1', '-1', 'quit', 'no', 'n')
         ):
         wPress = 0
         print('\nDiscarding problem ...')
         time.sleep(0.5)
         return None
      elif (
            constraint.lower()
            in ('c', 'continue', 'p', 'proceed', ' ',)
         ):
         if (len(constraints) < 1):
            wPress += 1
            print('\nNo constraint!')
            time.sleep(0.4)
            continue
         wPress = 0
         print('\nContinuing ...')
         time.sleep(0.4)
         break
      elif (len(constraint) >= 2):
         wPress = 0
         constraints.append(constraint)
         continue
      else:
         wPress += 1
         print('\nInvalid selection!')
         if (wPress < 10):
            time.sleep(0.4)
            continue
         else:
            print('\nDiscarding problem ...')
            time.sleep(0.5)
            return None
   
   runCalculation(problemType, objectiveFunction, constraints)
   
   input('Press [Enter] to continue ...')

def run ():
   wPress = 0
   try:
      while True:
         osc.CLEAR()
         print('Simplex Method\n')
         iKey = input('Calculate a simplex problem? (Y|N|q-quit): ')
         
         iKey = iKey.lower()
         
         if (iKey in  ('1', 'y', 'yes',)):
            wPress = 0
            runSimplexMethod()
         elif (iKey in ('q', 'quit', 'no', 'n', '-1')):
            wPress = 0
            print('\nExiting ...')
            time.sleep(0.6)
            break
         else:
            wPress += 1
            print('\nInvalid selection!')
            if (wPress < 10):
               time.sleep(0.4)
               continue
            else:
               print('\nExiting ...')
               time.sleep(0.6)
               break
   except KeyboardInterrupt:
      print('\n Exiting ...')
   
   osc.CLEAR()
   print('Simplex method LPP solver.\n')
   exit(0)

if __name__ == '__main__':
   run()
