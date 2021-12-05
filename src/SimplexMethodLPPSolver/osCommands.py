import os

class OSCommands:
   OS = None
   CLEAR = None

if (os.path.sep == '/'):
   OSCommands.OS = 'Linux'
   
   OSCommands.CLEAR = lambda: os.system('clear')
elif (os.path.sep == '\\'):
   OSCommands.OS = 'Windows'
   
   OSCommands.CLEAR = lambda: os.system('cls')

__all__ = [
   'OSCommands',
]
