import pygame 
import random
import copy

from const import *

screen = pygame.display.set_mode((SCREENSIZE, SCREENSIZE))

def readFiles():
    list = []
    with open("input.txt", "r") as my_file:
        for line in my_file:
            str = line.split()
            list.append(str)
        my_file.close()

    startPlayer = list[0]
    flag = list[1]
    boardType = list[2]
    return startPlayer, flag, boardType

# GUI Functions
def drawSign(screen, board, row, col, blockSize):
    if board[row][col] == "O": 
        centerX = blockSize / 2 + blockSize * row
        centerY = blockSize / 2 + blockSize * col
        centerCoor = (centerX, centerY)
        pygame.draw.circle(screen, O_COLOR, (centerX, centerY), RADIUS, 5)
    elif board[row][col] == "X":
        beginX = blockSize / 4 + blockSize * row
        beginY = blockSize / 4 + blockSize * col
        endX = int(blockSize * 0.75) + blockSize * row
        endY = int(blockSize * 0.75) + blockSize * col          
        pygame.draw.line(screen, X_COLOR, (beginX, beginY), (endX, endY), 7)
        pygame.draw.line(screen, X_COLOR, (beginX, endY), (endX, beginY), 7)

# Main functions
def printBoard(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            print(board[j][i], end = " ")
        print()

def checkEmptySqr(board, row, col):
    if (board[row][col] == "EMPTY"):
        return True
    else:
        return False

def checkEmptyBoard(board):
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] == "EMPTY":
                return True
    return False

def emptySqrList(board):
    emptyList = []
    for i in range(len(board)):
        for j in range(len(board[0])):
            if checkEmptySqr(board, i, j) == True:
                emptyList.append((i, j))
    return emptyList

def nextPlayer(player):
    if (player % 2 == 0): 
        player = 1
        return player
    else: 
        player = 0
        return player

def markSquare(board, row, col, player):
    if player == 0:
        board[row][col] = "X"
    else: board[row][col] = "O"

def getRndSqr(board):
    emptyList = emptySqrList(board)
    if (len(emptyList) != 0):
        index = random.randrange(0, len(emptyList))
        solution = emptyList[index]
        return solution
    else:
        return (0, 0)

#for 3x3 board
def evalPoint3(board):
    # check for wins in the rows
    for i in range(0, 3):
        if (board[i][0] == board[i][1] and board[i][1] == board[i][2]):
            if board[i][0] == 'X':
                return 10
            elif board[i][0] == 'O': 
                return -10
    # check for the wins in the cols
    for i in range(0, 3):
        if (board[0][i] == board[1][i] and board[1][i] == board[2][i]):
            if board[0][i] == 'X':
                return 10
            elif board[0][i] == 'O':
                return -10
    # check for the wins in the diags
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        if (board[0][0] == 'X'):
            return 10
        elif (board[0][0] == 'O'):
            return -10
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if (board[1][1] == 'X'):
            return 10
        elif (board[1][1] == 'O'):
            return -10
    return 0;

def drawLines33(screen):
    pygame.draw.line(screen, LINE_COLOR, (SQ1_SIZE, 0), (SQ1_SIZE, SCREENSIZE), GRID)
    pygame.draw.line(screen, LINE_COLOR, (SQ1_SIZE*2, 0), (SQ1_SIZE*2, SCREENSIZE), GRID)
    pygame.draw.line(screen, LINE_COLOR, (0, SQ1_SIZE), (SCREENSIZE, SQ1_SIZE), GRID)
    pygame.draw.line(screen, LINE_COLOR, (0, SQ1_SIZE*2), (SCREENSIZE, SQ1_SIZE*2), GRID)

def drawWinningLine3(board, WINNING_LINE):
    for i in range(0, 3):
        if (board[i][0] == board[i][1] and board[i][1] == board[i][2] and (board[i][0] == 'X' or board[i][0] == 'O')):
            if WINNING_LINE == True:
                pygame.draw.line(screen, WINNING_COLOR, (SQ1_SIZE / 2 + SQ1_SIZE * i, 0), (SQ1_SIZE / 2 + SQ1_SIZE * i, SCREENSIZE), 10)
    for i in range(0, 3):
        if (board[0][i] == board[1][i] and board[1][i] == board[2][i] and (board[0][i] == 'X' or board[0][i] == 'O')):
            if WINNING_LINE == True:
                pygame.draw.line(screen, WINNING_COLOR, (0, SQ1_SIZE / 2 + SQ1_SIZE * i), (SCREENSIZE, SQ1_SIZE / 2 + SQ1_SIZE * i), 10)
    if (board[0][0] == board[1][1] and board[1][1] == board[2][2]):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (0, 0), (SCREENSIZE, SCREENSIZE), 10)
    if (board[0][2] == board[1][1] and board[1][1] == board[2][0]):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SCREENSIZE, 0), (0, SCREENSIZE), 10)

def minimax(board, maximizer):
    currentState = evalPoint3(board)
    if currentState == 10:
        return 1, None
    if currentState == -10:
        return -1, None
    if checkEmptyBoard(board) == False:
        return 0, None

    if maximizer == HUMAN:
        max_evalNum = 999
        emptyList = emptySqrList(board)
        bestMove = None

        for i in range(len(emptyList)):
            tempBoard = copy.deepcopy(board)
            markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
            if (evalPoint3(tempBoard) == -10):
                return -1, (emptyList[i][0], emptyList[i][1])

        for i in range(len(emptyList)):
            tempBoard = copy.deepcopy(board)
            markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
            finalEval = minimax(tempBoard, AI)[0]
            if finalEval < max_evalNum:
                max_evalNum = finalEval
                bestMove = (emptyList[i][0], emptyList[i][1])
        return max_evalNum, bestMove

    elif maximizer == AI:
        min_evalNum = -999
        emptyList = emptySqrList(board)
        bestMove = None
        for i in range(len(emptyList)):
            tempBoard = copy.deepcopy(board)
            markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
            if (evalPoint3(tempBoard) == 10):
                return 1, (emptyList[i][0], emptyList[i][1])
        for i in range(len(emptyList)):
            tempBoard = copy.deepcopy(board)
            markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
            #if (evalPoint(board) == )
            finalEval = minimax(tempBoard, HUMAN)[0]
            if finalEval >= min_evalNum:
                min_evalNum = finalEval
                bestMove = (emptyList[i][0], emptyList[i][1])
        return min_evalNum, bestMove

def AiEval3(board, player):
    return minimax(board, player)[1]
# for 5x5 board
def drawLines55(screen):
    pygame.draw.line(screen, LINE_COLOR, (SQ2_SIZE, 0), (SQ2_SIZE, SCREENSIZE), GRID)
    pygame.draw.line(screen, LINE_COLOR, (SQ2_SIZE*2, 0), (SQ2_SIZE*2, SCREENSIZE), GRID)
    pygame.draw.line(screen, LINE_COLOR, (SQ2_SIZE*3, 0), (SQ2_SIZE*3, SCREENSIZE), GRID)
    pygame.draw.line(screen, LINE_COLOR, (SQ2_SIZE*4, 0), (SQ2_SIZE*4, SCREENSIZE), GRID)

    pygame.draw.line(screen, LINE_COLOR, (0, SQ2_SIZE), (SCREENSIZE, SQ2_SIZE), GRID)
    pygame.draw.line(screen, LINE_COLOR, (0, SQ2_SIZE*2), (SCREENSIZE, SQ2_SIZE*2), GRID)
    pygame.draw.line(screen, LINE_COLOR, (0, SQ2_SIZE*3), (SCREENSIZE, SQ2_SIZE*3), GRID)
    pygame.draw.line(screen, LINE_COLOR, (0, SQ2_SIZE*4), (SCREENSIZE, SQ2_SIZE*4), GRID)

def evalPoint5(board):
    # check for wins in the rows
    for i in range(0, 5):
        if ((board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][2] == board[i][3])
        or (board[i][1] == board[i][2] and board[i][2] == board[i][3] and board[i][3] == board[i][4])):
            if board[i][1] == 'X':
                return 10
            elif board[i][1] == 'O': 
                return -10
    # check for the wins in the cols
    for i in range(0, 5):
        if ((board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[2][i] == board[3][i])
        or (board[1][i] == board[2][i] and board[2][i] == board[3][i] and board[3][i] == board[4][i])):
            if board[1][i] == 'X':
                return 10
            elif board[1][i] == 'O':
                return -10
    # check for the wins in the diags
    if ((board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == board[3][3])
    or (board[1][1] == board[2][2] and board[2][2] == board[3][3] and board[3][3] == board[4][4])):
        if (board[1][1] == 'X'):
            return 10
        elif (board[1][1] == 'O'):
            return -10

    if ((board[0][4] == board[1][3] and board[1][3] == board[2][2] and board[2][2] == board[3][1])
    or (board[1][3] == board[2][2] and board[2][2] == board[3][1] and board[3][1] == board[4][0])):
        if (board[1][3] == 'X'):
            return 10
        elif (board[1][3] == 'O'):
            return -10

    if (board[0][1] == board[1][2] and board[1][2] == board[2][3] and board[2][3] == board[3][4]):
        if (board[0][1] == 'X'):
            return 10
        elif (board[0][1] == 'O'):
            return -10
    if (board[1][0] == board[2][1] and board[2][1] == board[3][2] and board[3][2] == board[4][3]):
        if (board[1][0] == 'X'):
            return 10
        elif (board[1][0] == 'O'):
            return -10

    if (board[3][0] == board[2][1] and board[2][1] == board[1][2] and board[1][2] == board[0][3]):
        if (board[3][0] == 'X'):
            return 10
        elif (board[3][0] == 'O'):
            return -10
    
    if (board[4][1] == board[3][2] and board[3][2] == board[2][3] and board[1][4] == board[2][3]):
        if (board[4][1] == 'X'):
            return 10
        elif (board[4][1] == 'O'):
            return -10
    return 0;

def drawWinningLine5(board, WINNING_LINE):
    # for type-1 row
    for i in range(0, 5):
        if ((board[i][0] == board[i][1] and board[i][1] == board[i][2] and board[i][2] == board[i][3])
        and (board[i][1] == 'X' or board[i][1] == 'O')):
            if WINNING_LINE == True:
                pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2, SQ2_SIZE / 2 + SQ2_SIZE * i), (SQ2_SIZE / 2 + SQ2_SIZE * i, SQ2_SIZE / 2 + SQ2_SIZE * 3), 10)
    #for type-2 row
    for i in range(0, 5):
        if ((board[i][1] == board[i][2] and board[i][2] == board[i][3] and board[i][3] == board[i][4])
        and (board[i][1] == 'X' or board[i][1] == 'O')):
            if WINNING_LINE == True:
                pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2 + SQ2_SIZE, SQ2_SIZE / 2 + SQ2_SIZE * i), (SCREENSIZE - SQ2_SIZE / 2, SQ2_SIZE / 2 + SQ2_SIZE * i), 10)

    # for type-1 col
    for i in range(0, 5):
        if ((board[0][i] == board[1][i] and board[1][i] == board[2][i] and board[2][i] == board[3][i]) and
        (board[0][i] == 'X' or board[0][i] == 'O')):
            if WINNING_LINE == True:
                pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2 + SQ2_SIZE * i, SQ2_SIZE / 2 + SQ2_SIZE), (SQ2_SIZE / 2 + SQ2_SIZE * i, SCREENSIZE - SQ2_SIZE / 2), 10)
                #pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2, SQ2_SIZE / 2 + SQ2_SIZE * i), (SQ2_SIZE / 2 + SQ2_SIZE * i, SQ2_SIZE / 2 + SQ2_SIZE * 3), 10)

    # for type-2 col
    for i in range(0, 5):
        if ((board[1][i] == board[2][i] and board[2][i] == board[3][i] and board[3][i] == board[4][i]) and
        (board[1][i] == 'X' or board[1][i] == 'O')):
            if WINNING_LINE == True:
                pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2 + SQ2_SIZE * i, SQ2_SIZE / 2 + SQ2_SIZE), (SQ2_SIZE / 2 + SQ2_SIZE * i, SQ2_SIZE / 2 + SQ2_SIZE * 4), 10)
                #pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2 + SQ2_SIZE, SQ2_SIZE / 2 + SQ2_SIZE * i), (SQ2_SIZE / 2 + SQ2_SIZE * i, SCREENSIZE - SQ2_SIZE / 2), 10)

    # for type-1 diag
    if ((board[0][0] == board[1][1] and board[1][1] == board[2][2] and board[2][2] == board[3][3]) and
        (board[1][1] == 'X' or board[1][1] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2, SQ2_SIZE / 2), (SQ2_SIZE / 2 + SQ2_SIZE * 3 , SQ2_SIZE / 2 + SQ2_SIZE * 3), 10)
    # for type-2 diag
    if ((board[1][1] == board[2][2] and board[2][2] == board[3][3] and board[3][3] == board[4][4]) and
        (board[1][1] == 'X' or board[1][1] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE + SQ2_SIZE / 2, SQ2_SIZE + SQ2_SIZE / 2), (SQ2_SIZE / 2 + SQ2_SIZE * 4 , SQ2_SIZE / 2 + SQ2_SIZE * 4), 10)
    # for type-3 diag
    if ((board[0][4] == board[1][3] and board[1][3] == board[2][2] and board[2][2] == board[3][1]) and
        (board[0][4] == 'X' or board[0][4] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2, SCREENSIZE - SQ2_SIZE / 2), (SQ2_SIZE / 2 + SQ2_SIZE * 3 , SQ2_SIZE / 2 + SQ2_SIZE), 10)
    # for type-4 diag
    if ((board[1][3] == board[2][2] and board[2][2] == board[3][1] and board[3][1] == board[4][0]) and
        (board[1][3] == 'X' or board[1][3] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2 + SQ2_SIZE, SQ2_SIZE / 2 + SQ2_SIZE * 3), (SQ2_SIZE / 2 + SQ2_SIZE * 4 , SQ2_SIZE / 2), 10)
    
    # for type-5 diag
    if ((board[0][1] == board[1][2] and board[1][2] == board[2][3] and board[2][3] == board[3][4]) and
        (board[0][1] == 'X' or board[0][1] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2 + SQ2_SIZE, SQ2_SIZE / 2), (SQ2_SIZE / 2 + SQ2_SIZE * 4, SQ2_SIZE / 2 + SQ2_SIZE * 3), 10)
    # for type-6 diag
    if ((board[1][0] == board[2][1] and board[2][1] == board[3][2] and board[3][2] == board[4][3]) and
        (board[1][0] == 'X' or board[1][0] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2, SQ2_SIZE / 2 + SQ2_SIZE), (SQ2_SIZE / 2 + SQ2_SIZE * 3, SQ2_SIZE / 2 + SQ2_SIZE * 4), 10)
    # for type-7 diag
    if ((board[3][0] == board[2][1] and board[2][1] == board[1][2] and board[1][2] == board[0][3]) and
        (board[3][0] == 'X' or board[3][0] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2, SQ2_SIZE / 2 + SQ2_SIZE * 3), (SQ2_SIZE / 2 + SQ2_SIZE * 3, SQ2_SIZE / 2), 10)
    # for type-8 diag
    if ((board[4][1] == board[3][2] and board[3][2] == board[2][3] and board[2][3] == board[1][4]) and
        (board[4][1] == 'X' or board[4][1] == 'O')):
        if WINNING_LINE == True:
            pygame.draw.line(screen, WINNING_COLOR, (SQ2_SIZE / 2 + SQ2_SIZE, SQ2_SIZE / 2 + SQ2_SIZE * 4), (SQ2_SIZE / 2 + SQ2_SIZE * 4, SQ2_SIZE / 2 + SQ2_SIZE), 10)

def AIEval5_Real(board, player):
    return minimax_ABPruning(board, player, -999, 999, 6)[1]

def minimax_ABPruning(board, maximizer, alpha, beta, depth):
    currentState = evalPoint5(board)
    if currentState == 10:
        return 1, None
    if currentState == -10:
        return -1, None
    if checkEmptyBoard(board) == False or depth == 0:
        return 0, None

    if maximizer == HUMAN:
        max_evalNum = 999
        emptyList = emptySqrList(board)
        bestMove = None

        if (len(emptyList) <= 20):
            for i in range(len(emptyList)):
                tempBoard = copy.deepcopy(board)
                markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
                if (evalPoint5(tempBoard) == -10):
                    return -1, (emptyList[i][0], emptyList[i][1])

        for i in range(len(emptyList)):
            tempBoard = copy.deepcopy(board)
            markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
            finalEval = minimax_ABPruning(tempBoard, AI, alpha, beta, depth - 1)[0]
            
            if finalEval < max_evalNum:
                max_evalNum = finalEval
                bestMove = (emptyList[i][0], emptyList[i][1])
            beta = min(beta, finalEval)
            if (beta <= alpha):
                break
        return max_evalNum, bestMove

    elif maximizer == AI:
        min_evalNum = -999
        emptyList = emptySqrList(board)
        bestMove = None

        if (len(emptyList) <= 20):
            for i in range(len(emptyList)):
                tempBoard = copy.deepcopy(board)
                markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
                if (evalPoint5(tempBoard) == 10):
                    return 1, (emptyList[i][0], emptyList[i][1])

        for i in range(len(emptyList)):
            tempBoard = copy.deepcopy(board)
            markSquare(tempBoard, emptyList[i][0], emptyList[i][1], maximizer)
            # finalEval = minimax(tempBoard, HUMAN)[0]
            # min_evalNum = max(min_evalNum, finalEval, alpha, beta)
            finalEval = minimax_ABPruning(tempBoard, HUMAN, alpha, beta, depth - 1)[0]
            if finalEval > min_evalNum:
                min_evalNum = finalEval
                bestMove = (emptyList[i][0], emptyList[i][1])
            alpha = max(alpha, finalEval)
            if beta <= alpha:
                break
        return min_evalNum, bestMove

# Initialize board
def initBoard33(starter, startAI):
    board = BOARD_33
    player = starter
    pygame.init()
    pygame.display.set_caption("TIC TAC TOE")
    flag = True
    screen.fill(BACKGROUND_COLOR)
    drawLines33(screen)
    startAI = startAI  
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = event.pos
                rowBoard = result[0] // SQ1_SIZE
                colBoard = result[1] // SQ1_SIZE 
                if (checkEmptyBoard(board) == False):
                    print("Board is full")
                else:
                    if (checkEmptySqr(board, rowBoard, colBoard) == True):
                        markSquare(board, rowBoard, colBoard, player)
                        drawSign(screen, board, rowBoard, colBoard, SQ1_SIZE)
                        print(rowBoard, colBoard)
                        printBoard(board)
                        player = nextPlayer(player)
                    else:
                        print("Already filled")   
            if (player == AI):
                if startAI == True:
                    #getRndSqr(board)
                    row, col = getRndSqr(board)
                    markSquare(board, row, col, player)
                    print(board)
                    drawSign(screen, board, row, col, SQ1_SIZE)
                    startAI = False
                    player = nextPlayer(player)
                else:
                    if (len(emptySqrList(board)) != 0):
                        row, col = AiEval3(board, player)
                        print(row, col)
                        if (checkEmptyBoard(board) == False):
                            print("Board is full")
                        else:
                            markSquare(board, row, col, player)
                            drawSign(screen, board, row, col, SQ1_SIZE)
                            print(row, col)
                            printBoard(board)
                            player = nextPlayer(player)
                        print(emptySqrList(board))
                    else:
                        print("Board is full") 
            if (evalPoint3(board) == 0):
                drawWinningLine3(board, False)
            elif (evalPoint3(board) == 10 or evalPoint3(board) == -10):
                drawWinningLine3(board, True)
        pygame.display.update() 
    pygame.quit()

def initBoard55(starter, startAI):
    board = BOARD_55
    player = starter
    startAI = startAI
    pygame.init()
    pygame.display.set_caption("TIC TAC TOE")
    flag = True
    screen.fill(BACKGROUND_COLOR)
    drawLines55(screen)
    counterFlag = 1
    while flag:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                flag = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                result = event.pos
                rowBoard = result[0] // SQ2_SIZE
                colBoard = result[1] // SQ2_SIZE
                if (checkEmptyBoard(board) == False):
                    print("Board is full")
                else:
                    if (checkEmptySqr(board, rowBoard, colBoard) == True):
                        markSquare(board, rowBoard, colBoard, player)
                        drawSign(screen, board, rowBoard, colBoard, SQ2_SIZE)
                        print(rowBoard, colBoard)
                        print(board)
                        player = nextPlayer(player)
                    else:
                        print("Already filled")
            if (player == AI):
                if startAI == True:
                    counterFlag = counterFlag - 1
                    row, col = getRndSqr(board)
                    markSquare(board, row, col, player)
                    print(board)
                    drawSign(screen, board, row, col, SQ2_SIZE)
                    player = nextPlayer(player)
                    if (counterFlag == 0):
                        startAI = False        
                else:
                    if (len(emptySqrList(board)) != 0):
                        row, col = AIEval5_Real(board, player)
                        if (checkEmptyBoard(board) == False):
                            print("Board is full")
                        else:
                            markSquare(board, row, col, player)
                            drawSign(screen, board, row, col, SQ2_SIZE)
                            player = nextPlayer(player)
                        print(emptySqrList(board))
                    else:
                        print("Board is full")     
            if (evalPoint5(board) == 0):
                drawWinningLine5(board, False)
            elif (evalPoint5(board) == 10 or evalPoint5(board) == -10):
                drawWinningLine5(board, True)
        pygame.display.update() 
    pygame.quit()  