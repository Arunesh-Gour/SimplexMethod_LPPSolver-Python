class Constraint:
   """Constraint data structure.
   
   Stores Constraint in 3 parts - lhs, equalityType and rhs.
   
   Attributes
   ----------
   lhs: list
      List of tuple terms in format (coefficient, 'variable',).
   equalityType: str
      String containing equality type like '<', '<=', '>', '>=', '='.
   rhs: float
      Constant value indicating RHS of equation.
   
   Methods
   -------
   __init__ ()
      Initializes the data structure.
   """
   
   def __init__ (self):
      """Initializes the data structure.
      """
      
      self.lhs = None # [(coefficient, 'variableName',),].
      self.equalityType = None # str - </>/<=/>=/=.
      self.rhs = None # float - RHS constant.

class AuxillaryConstraint:
   """AuxillaryConstraint data structure.
   
   Stores Constraint in 3 parts - lhs, equalityType and rhs, with
   slackVariable indicating whether slack variable is used and what variable
   it is.
   
   Attributes
   ----------
   lhs: list
      List of tuple terms in format (coefficient, 'variable',).
   equalityType: str
      String containing equality type like '<', '<=', '>', '>=', '='.
   rhs: float
      Constant value indicating RHS of equation.
   slackVariable: str, None
      String denoting which slackVariable is used, else None if no slack
      variable is present.
   
   Methods
   -------
   __init__ ()
      Initializes the data structure.
   """
   
   def __init__ (self):
      """Initializes the data structure.
      """
      
      self.lhs = None # [(coefficient, 'variableName',),].
      self.equalityType = None # </>/<=/>=/=.
      self.rhs = None # RHS constant.
      self.slackVariable = None # str(slackLetter + str(slacks)).

class Row:
   """Row data structure.
   
   Stores a row of IterationTable.
   
   Attributes
   ----------
   i: int
      Row index.
   CB: float
      Corresponding Cj value for B.
   B: str
      aj variable masking XB.
   XB: str
      xj variable, present in basis of current IterationTable for current row.
   b: float
      b value for current row in IterationTable.
   aj: dict
      Dict with key as aj and value as aij.
   zij: dict
      Dict with key as aj and value as zij for current row.
   isKeyRow: bool
      Whether this row is a key row for current iteration table.
   minRatio: float
      b/aij, for i=current column index.
   
   Methods
   -------
   __init__ ()
      Initializes the data structure.
   """
   
   def __init__ (self):
      """Initializes the data structure.
      """
      
      self.i = None # row index.
      self.CB = None # float - cj.
      self.B = None # str - aj.
      self.XB = None # str - xj ~= aj.
      self.b = None # float.
      self.aj = None # {'aj': aij,}.
      self.zij = None # {'aj':zij,}.
      self.isKeyRow = None # True|False.
      self.minRatio = None # float - bi/aij.

class IterationTable:
   """IterationTable data structure.
   
   Stores a table from possible multiple iterations of a SimplexProblem.
   
   Attributes
   ----------
   iteration: int
      Iteration number.
   Cj: dict
      Stores cj values keyed to aj variables.
   aj: list
      List of all aj variables used in table.
   keyRow: Row
      Key row, selected for next iteration.
   keyColumn: str
      aj variable which is selected as key column for next iteration.
   keyElement: float
      Key element value, found at intersection of key row and key column.
   rowi: list
      List of all rows, ordered as last one is latest.
   zj: dict
      zj values per column keyed to aj variables.
   deltaJ: dict
      deltaJ values per column keyed to aj variables.
   
   Methods
   -------
   __init__ ()
      Initializes the data structure.
   """
   
   def __init__ (self):
      """Initializes the data structure.
      """
      
      self.iteration = None # int - 1, 2, 3, ...
      self.Cj = None # {'aj': cj,}
      self.aj = None # ['aj',] - list containing all ajs
      self.keyRow = None # Row - from rowi.
      self.keyColumn = None # str - 'aj'
      self.keyElement = None # float aij
      self.rowi = None # [Row,]
      self.zj = None # {'aj': zj,}
      self.deltaJ = None # {'aj': deltaj,}

class OptimalSolution:
   """OptimalSolution data structure.
   
   Stores optimal solution of a SimplexProblem.
   
   Attributes
   ----------
   iterationTable: IterationTable
      Final iteration table from which the optimal solution has been
      calculated.
   Xj: dict
      Optimal solution, with b keyed to xj from iterationTable.
   optimalValue: float
      Optimal value of SimplexProblem, obtained by putting Xj in
      auxillaryObjectiveFunction, i.e., Zmax or Zmin value.
   
   Methods
   -------
   __init__ ()
      Initializes the data structure.
   """
   
   def __init__ (self):
      """Initializes the data structure.
      """
      
      self.iterationTable = None # Final IterationTable.
      self.Xj = None # {'xj': b,}
      self.optimalValue = None # float(z).

class SimplexProblem:
   """SimplexProblem data structure.
   
   Stores a simplex problem.
   
   Attributes
   ----------
   Terminate: class
      Class containing termination reasons.
   problemType: str
      Type of problem - minimization ('min') or maximization ('max').
   objectiveFunction: list
      List of tuple terms in format (coefficient, 'variable',).
   auxillaryObjectiveFunction: list
      Modified objectiveFunction, generated while calculating auxillary
      components.
   constraints: list
      List of Constraint provided.
   auxillaryConstraints: list
      List of AuxillaryConstraint, generated while calculating auxillary
      components.
   slackLetter: str, None
      Slack variable used to denote a slack variable, if used in any
      auxillaryConstraint, else None.
   slacks: int
      Total number of slack variables used.
   netVariables: tuple
      Tuple containing set of all variables used in SimplexProblem.
   AXBMaps: dict
      Maps aj variables to xj variables.
   XABMaps: dict
      Maps xj variables to aj variables.
   iterationTables: list
      List of all IterationTable (s) in order, with latest at end.
   terminated: bool, None
      Whether calculation has been terminated, None if not started.
   terminationReason: str
      Reason for terminating calculation.
   optimalSolution: OptimalSolution
      Optimal solution of problem, if exists.
   
   Methods
   -------
   __init__ ()
      Initializes the data structure.
   """
   
   class Terminate:
      """Termination reasons.
      
      Contains list of termination reasons as CONSTANTs to
      simplify comparison process.
      
      Attributes
      ----------
      REACHED_OPTIMAL: str
         Solution is optimal.
      UNBOUNDED_SOLUTION: str
         Solution is unbounded.
      FRAME_ERROR: str
         Error while framing.
      CALC_ERROR: str
         Error while calculating.
      """
      
      REACHED_OPTIMAL = 'Optimal solution reached for the given problem.'
      UNBOUNDED_SOLUTION = 'Solution is unbounded.'
      FRAME_ERROR = 'Error while framing the problem.'
      CALC_ERROR = 'Error while calculating the solution.'
   
   def __init__ (self):
      """Initializes the data structure.
      """
      
      self.problemType = None # min / max
      self.objectiveFunction = None # [(coefficient, 'variableName',),]
      self.auxillaryObjectiveFunction = None # same or converted.
      self.constraints = None # [Constraint,]
      self.auxillaryConstraints = None # same or converted.
      self.slackLetter = None # str.
      self.slacks = None # int.
      self.netVariables = None # ('x1',)
      self.AXBMaps = None # {'ai': 'xi',}
      self.XABMaps = None # {'xi': 'ai',}
      self.iterationTables = None # [IterationTable,]
      self.terminated = None # True|False - finishedCalculation?|notStarted
      self.terminationReason = None # class.<reason>
      self.optimalSolution = None # OptimalSolution
