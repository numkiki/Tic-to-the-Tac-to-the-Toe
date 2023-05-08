import pygame 
from const import *
from function import *

starter, flag, board = readFiles()
print(board)
if (board[0] == '3'):
    if starter[0] == 'AI':
        initBoard33(AI, True)
    else:
        initBoard33(HUMAN, False)
else:
    if starter[0] == 'AI':
        initBoard55(AI, False) 
    elif starter[0] == 'HUMAN' and flag[0] == 'True':
        initBoard55(HUMAN, True) 
    else:
        initBoard55(HUMAN, False)