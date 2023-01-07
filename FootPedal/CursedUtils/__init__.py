'''
configuration variables

Note that TOP and UP are synonyms, as are BOTTOM and DOWN.  CENTER, CENTRE, and MIDDLE are likewise interchangeable.

'''

LEFT  = -1
CENTER =  0
CENTRE =  0
RIGHT = 1

TOP=-1
UP=-1
MIDDLE = 0
BOTTOM = 1
DOWN = 1

AUTO = -2

from CursedUtils.tools import *
from CursedUtils.Screen import Screen
from CursedUtils.Window import Window
from CursedUtils.ColumnHandler import ColumnHandler
from CursedUtils.KeyResponder import KeyResponder
from CursedUtils.keymaps import KEYMAP, PADTRANSLATOR