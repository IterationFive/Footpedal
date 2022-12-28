'''

This file provides a map of non-character keystrokes for conversion to the number
produced by stdscr.getch().

It should be noted that this map was generated under windows 10, running python at
the command prompt.  Perhaps other maps will follow?

A few notes:

F11 should return 275.  It doesn't.  It returns 546.  Also, it starts (or ends) 
fullscreen mode. Alt-Enter and Alt+Padenter do the same (with the same 546).  

Certain keys are do not register as a keystroke, either as a limitation of windows, 
or a limitation of curses.  In some case, windows or another application will take over.
(In the case of Shift+Ins and Ctrl+v, they paste the contents of the keyboard.)

These keys might be available in other environments.  



ctrl+escape
alt+escape
shift+backspace
shift+escape
alt+f1
alt+f2
alt+f3
alt+f4
alt+f5
alt+f6
alt+f7
alt+f8
alt+f9
alt+f10
alt+f11
alt+f12
ctrl+a
ctrl+c
ctrl+f
ctrl+h
ctrl+m
ctrl+v
alt+z
ctrl+home
ctrl+end
ctrl+up
ctrl+down
ctrl+padhome
ctrl+padend
ctrl+padup
ctrl+paddown
shift+insert
shift+delete
shift+home
shift+end
shift+pageup
shift+pagedown
shift+up
shift+down
shift+left
shift+right
shift+padinsert
shift+padhome
shift+padend
shift+padpageup
shift+padpagedown
shift+padup
shift+paddown
shift+padleft
shift+padright


Certain keys produce an identical response to other keys:

ctrl+i* : tab
ctrl+j* : enter
shift+enter :  enter
alt+enter* : f11**
alt+padenter : f11**
ctrl+[ : escape 

*these items appear on the map as well as the item they duplicate.  reverse key lookups
   will return the original key( for example, tab, enter, or F11).
*F11 as it appears in this map, value 546.



Certain keys, for reasons lost to God, history, and the acoustic modem, return 0.  These are as follows:

ctrl+1
ctrl+2
ctrl+3
ctrl+4
ctrl+5
ctrl+6
ctrl+7
ctrl+8
ctrl+9
ctrl+0
ctrl+`
ctrl+-
ctrl+=
ctrl+]
ctrl+,
ctrl+.
ctrl+/
alt+`
alt+-
alt+=
alt+[
alt+]
alt+\
alt+'
alt+,
alt+.
alt+/


Now we can provide the keymap.  It should be noted that certain keystrokes are listed becuase their
order in the sequence was obvious, but are still unavailable, as per above.
'''

KEYMAP={
'escape' : 27,
'backspace' : 8,
'ctrl+backspace' : 127,
'alt+backspace' : 504,
'enter':10,
'tab' : 9,
'shift+tab': 351,
'ctrl+tab': 482,
'f1' : 265,
'f2' : 266,
'f3' : 267,
'f4' : 268,
'f5' : 269,
'f6' : 270,
'f7' : 271,
'f8' : 272,
'f9' : 273,
'f10' : 274,
'f11' : 546,
'f12' : 276,
'ctrl+f1' : 289,
'ctrl+f2' : 290,
'ctrl+f3' : 291,
'ctrl+f4' : 292,
'ctrl+f5' : 293,
'ctrl+f6' : 294,
'ctrl+f7' : 295,
'ctrl+f8' : 296,
'ctrl+f9' : 297,
'ctrl+f10' : 298,
'ctrl+f11' : 299,
'ctrl+f12' : 300,
'shift+f1' : 277,
'shift+f2' : 278,
'shift+f3' : 279,
'shift+f4' : 280,
'shift+f5' : 281,
'shift+f6' : 282,
'shift+f7' : 283,
'shift+f8' : 284,
'shift+f9' : 285,
'shift+f10' : 286,
'shift+f11' : 287,
'shift+f12' : 288,
'ctrl+a' : 1,
'ctrl+b' : 2,
'ctrl+c' : 3,
'ctrl+d' : 4,
'ctrl+e' : 5,
'ctrl+g' : 7,
'ctrl+h' : 8,
'ctrl+i' : 9,
'ctrl+j' : 10,
'ctrl+k' : 11,
'ctrl+l' : 12,
'ctrl+m' : 13,
'ctrl+n' : 14,
'ctrl+o' : 15,
'ctrl+p' : 16,
'ctrl+q' : 17,
'ctrl+r' : 18,
'ctrl+s' : 19,
'ctrl+t' : 20,
'ctrl+u' : 21,
'ctrl+v' : 22,
'ctrl+w' : 23,
'ctrl+x' : 24,
'ctrl+y' : 25,
'ctrl+z' : 26,
'alt+a' : 417,
'alt+b' : 418,
'alt+c' : 419,
'alt+d' : 420,
'alt+e' : 421,
'alt+f' : 422,
'alt+g' : 423,
'alt+h' : 424,
'alt+i' : 425,
'alt+j' : 426,
'alt+k' : 427,
'alt+l' : 428,
'alt+m' : 429,
'alt+n' : 430,
'alt+o' : 431,
'alt+p' : 432,
'alt+q' : 433,
'alt+r' : 435,
'alt+s' : 436,
'alt+t' : 437,
'alt+u' : 438,
'alt+v' : 439,
'alt+w' : 440,
'alt+x' : 441,
'alt+y' : 442,
'alt+z' : 443,
'insert' : 331,
'delete' : 330,
'home' : 262,
'end' : 358,
'pageup' : 339,
'pagedown' : 338,
'up' : 259,
'down' : 258,
'left' : 260,
'right' : 261,
'padenter' : 459,
'padinsert' : 506,
'paddelete' : 462,
'padhome' : 449,
'padend' : 455,
'padpageup' : 451,
'padpagedown' : 457,
'padup' : 450,
'paddown' : 456,
'padleft' : 452,
'padright' : 45,
'ctrl+enter' : 529,
'ctrl+insert' : 477,
'ctrl+delete' : 527,
'ctrl+pageup' : 445,
'ctrl+pagedown' : 446,
'ctrl+left' : 443,
'ctrl+right' : 444,
'ctrl+padenter' : 460,
'ctrl+padinsert' : 507,
'ctrl+paddelete' : 466,
'ctrl+padpageup' : 516,
'ctrl+padpagedown' : 510,
'ctrl+padleft' : 511,
'ctrl+padright' : 513,
'alt+enter' : 546,
'alt+insert' : 479,
'alt+delete' : 478,
'alt+home' : 486,
'alt+end' : 489,
'alt+pageup' : 487,
'alt+pagedown' : 488,
'alt+up' : 490,
'alt+down' : 491,
'alt+left' : 493,
'alt+right' : 492,
'alt+padinsert' : 517,
'alt+paddelete' : 476,
'alt+padhome' : 524,
'alt+padend' : 518,
'alt+padpageup' : 526,
'alt+padpagedown' : 520,
'alt+padup' : 525,
'alt+paddown' : 519,
'alt+padleft' : 521,
'alt+padright' : 523,
'shift+padenter' : 530,
'shift+paddelete' : 46,
'padcenter' : 453,
'ctrl+padcenter' : 512,
'alt+padcenter' : 522,
'shift+padcenter' : 53,
'ctrl+\\' : 28,
'ctrl+:' : 39,
'ctrl+\'' : 461,
'alt+1' : 408,
'alt+2' : 409,
'alt+3' : 410,
'alt+4' : 411,
'alt+5' : 412,
'alt+6' : 413,
'alt+7' : 414,
'alt+8' : 415,
'alt+9' : 416,
'alt+0' : 407,
'alt+:' : 500
}

PADTRANSLATOR = {
    449:262,
    455:358,
    506:331,
    462:330,
    451:339,
    457:338,
    450:259,
    456:258,
    452:260,
    45:261,
    507:477,
    466:527,
    516:445,
    510:446,
    511:443,
    513:444,
    524:486,
    518:489,
    517:479,
    476:478,
    526:487,
    520:488,
    525:490,
    519:491,
    521:493,
    523:492}