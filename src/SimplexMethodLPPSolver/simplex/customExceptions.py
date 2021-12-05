from .dataStructures import SimplexProblem

class CustomExceptions:
   """Contains custom Exceptions and/or handlers.
   
   Attributes
   ----------
   PreProcessError: Exception
      Exception for error occured while pre-processing.
   FrameError: Exception
      Exception for error occured while framing.
   CalculationError: Exception
      Exception for error occured during calculation.
   
   Methods
   -------
   safe_execute (defaultValue, function, *args, exception=None,
         defaultExceptionValue=None, **kwargs)
      Exception handler to safely execute a function.
      Safely executes a function and returns default value if any exception
      occurs.
   
   """
   
   class PreProcessError (Exception):
      """Exception for error occured while pre-processing.
      
      Exception for error occured in pre-processing stage for a
      SimplexProblem.
      
      Methods
      -------
      __init__ ()
         Initializes the exception.
         Initializes the exception with appropriate message.
      
      """
      
      def __init__ (self, objectiveFunction, constraints, problemType):
         """Initializes the exception.
         
         Initializes the exception with appropriate message and puts
         parameters in exception message for debugging purposes.
         
         Parameters
         ----------
         objectiveFunction: str
            str form of objective function.
         constraints: list
            List of constraint in str format.
         problemType: str
            Type of problem - minimization ('min') or maximization ('max').
         
         """
         
         super(CustomExceptions.PreProcessError, self).__init__((
            'Error while pre-processing problem with following inputs::\n'
            + 'Problem Type: {0}'.format(problemType)
            + 'Objective Function: {0}\n'.format(objectiveFunction)
            + 'Constraints: {0}\n'.format(constraints)
         ))
   
   class FrameError (Exception):
      """Exception for error occured while framing.
      
      Exception for error occured in framing stage for a
      SimplexProblem.
      Marks the SimplexProblem as terminated and sets the reason.
      
      Methods
      -------
      __init__ ()
         Initializes the exception.
         Initializes the exception with appropriate message and terminates
         SimplexProblem.
      
      """
      
      def __init__ (self, simplexProblem):
         """Initializes the exception.
         
         Initializes the exception with appropriate message and terminates
         SimplexProblem.
         
         Parameters
         ----------
         simplexProblem: SimplexProblem
            SimplexProblem which generated the exception and has to be
            terminated.
         
         Raises
         ------
         TypeError
            Raises when simplexProblem is not of type SimplexProblem.
         
         """
         
         if (type(simplexProblem) != SimplexProblem):
            raise TypeError((
               'FrameError: Required {0}, '.format(type(SimplexProblem))
               + 'supplied {0}'.format(type(simplexProblem))
            ))
         
         simplexProblem.terminated = True
         simplexProblem.terminationReason = (
            SimplexProblem.Terminate.FRAME_ERROR
         )
         
         super(CustomExceptions.FrameError, self).__init__(
            'Error while framing problem.'
         )
   
   class CalculationError (Exception):
      """Exception for error occured during calculation.
      
      Exception for error occured in calculation stage for a
      SimplexProblem.
      Marks the SimplexProblem as terminated and sets the reason.
      
      Methods
      -------
      __init__ ()
         Initializes the exception.
         Initializes the exception with appropriate message and terminates
         SimplexProblem.
      
      """
      
      def __init__ (self, simplexProblem):
         """Initializes the exception.
         
         Initializes the exception with appropriate message and terminates
         SimplexProblem.
         
         Parameters
         ----------
         simplexProblem: SimplexProblem
            SimplexProblem which generated the exception and has to be
            terminated.
         
         Raises
         ------
         TypeError
            Raises when simplexProblem is not of type SimplexProblem.
         
         """
         
         if (type(simplexProblem) != SimplexProblem):
            raise TypeError((
               'CalculationError: Required {0}, '.format(type(SimplexProblem))
               + 'supplied {0}'.format(type(simplexProblem))
            ))
         
         simplexProblem.terminated = True
         simplexProblem.terminationReason = (
            SimplexProblem.Terminate.CALC_ERROR
         )
         
         super(CustomExceptions.CalculationError, self).__init__(
            'Error during calculation.'
         )
   
   def safe_execute (defaultValue, function, *args, exception=None,
         defaultExceptionValue=None, **kwargs
      ):
      """Exception handler to safely execute a function.
      
      Safely executes a function and returns default value if any exception
      occurs.
      
      Parameters
      ----------
      defaultValue
         Value to return if any exception or provided exception (if provided)
         occurs.
      function: callable
         Function to execute, which might throw exception(s).
      *args
         Arguments to be sent to function.
      exception: Exception, default=None
         Specific exception type to capture.
         If this exception occurs, returns defaultValue.
      defaultExceptionValue, default=None
         Value to return if Exception other than provided exception
         occured.
      **kwargs
         Keyword arguments to be sent to function.
      
      Returns
      -------
      function(*args, **kwargs)
         If no exception occured while function's execution.
      defaultValue
         If an Exception occured (exception==None).
         If provided exception occured (exception!=None).
      defaultExceptionValue
         If Exception occured and Exception!=exception.
      
      """
      
      if (exception == None):
         try:
            return function(*args, **kwargs)
         except:
            return defaultValue
      else:
         try:
            return function(*args, **kwargs)
         except exception:
            return defaultValue
         except:
            return defaultExceptionValue or defaultValue
