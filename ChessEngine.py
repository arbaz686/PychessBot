import numpy as np
import random
import time
import settings
from ChessPiece import inbrd, makepseudomove, attackCalc
from settings import *

inCheck = False

calc = 0
moves = []

INfinity = 10000

BestMove = None

Depth_Searched = 2


def Evaluation(player):
    val_sum = 0
    attack_sum = 0
    for i in range(8):
        for j in range(8):
            if piecearray[i,j] != 0:
                if piecearray[i,j] > 0:
                    c = j
                    f=1
                else:
                    c = 7-j
                    f=-1
                # 82, 337, 365, 477, 1025, 0
                if abs(piecearray[i,j]) == 100:
                    #val_sum += piecearray[i, j] + 2*f*PawnTable[i,c]
                    val_sum += f*(82+ PawnTable[i,c])
                elif abs(piecearray[i,j]) == 300:
                    # val_sum += piecearray[i, j] + f*BishopTable[i, c]
                    val_sum += f * (337 + BishopTable[i, c])
                elif abs(piecearray[i,j]) == 302:
                    #val_sum += piecearray[i, j] + f*KnightTable[i, c]
                    val_sum += f * (365 + KnightTable[i, c])
                elif abs(piecearray[i,j] )== 500 or abs(piecearray[i,c]) == 501:
                    #val_sum += piecearray[i, j] + f*RookTable[i, c]
                    val_sum += f * (477 + RookTable[i, c])
                elif abs(piecearray[i,j] )== 900:
                    #val_sum += piecearray[i, j] + f*QueenTable[i, c]
                    val_sum += f * (1025 + QueenTable[i, c])
                elif abs(piecearray[i,j] )== 1000 or abs(piecearray[i,j] )== 1001:
                    #val_sum += piecearray[i, j] + f*KingTable[i, c]
                    val_sum += f * (1225 + KingTable[i, c])

            #attack_sum += temp_attack_array[i, j]
    # print(val_sum)
    return val_sum



def CastleMove(move):
    if move[0] == 'Q':
        piecearray[0, 0] = 0
        piecearray[4, 0] = 0
        piecearray[2, 0] = 1000
        piecearray[3, 0] = 500
    elif move[0] == 'q':
        piecearray[0, 7] = 0
        piecearray[4, 7] = 0
        piecearray[2, 7] = -1000
        piecearray[3, 7] = -500
    elif move[0] == 'K':
        piecearray[7, 0] = 0
        piecearray[4, 0] = 0
        piecearray[6, 0] = 1000
        piecearray[5, 0] = 500
    elif move[0] == 'k':
        piecearray[7, 7] = 0
        piecearray[4, 7] = 0
        piecearray[6, 7] = -1000
        piecearray[5, 7] = -500


def UndoCastleMove(move):
    if move[0] == 'Q':
        piecearray[0, 0] = 501
        piecearray[4, 0] = 1001
        piecearray[2, 0] = 0
        piecearray[3, 0] = 0
    elif move[0] == 'q':
        piecearray[0, 7] = -501
        piecearray[4, 7] = -1001
        piecearray[2, 7] = 0
        piecearray[3, 7] = 0
    elif move[0] == 'K':
        piecearray[7, 0] = 501
        piecearray[4, 0] = 1001
        piecearray[6, 0] = 0
        piecearray[5, 0] = 0
    elif move[0] == 'k':
        piecearray[7, 7] = -501
        piecearray[4, 7] = -1001
        piecearray[6, 7] = 0
        piecearray[5, 7] = 0


def do_undo(locn_old, locn_new, depth, alpha, beta, player):
    pieceval = piecearray[tuple(locn_old)]
    attackval = piecearray[tuple(locn_new)]
    piecearray[tuple(locn_old)] = 0
    piecearray[tuple(locn_new)] = pieceval
    player += 1
    # Compute
    gain = -Search(depth - 1, -beta, -alpha, player)
    player -= 1
    # UndoMove
    piecearray[tuple(locn_old)] = pieceval
    piecearray[tuple(locn_new)] = attackval

    return gain


def comp(locn_old, locn_new):
    val_old = 8 * locn_old[0] + locn_old[1]
    val_new = 8 * locn_new[0] + locn_new[1]

    return 100 * val_new + val_old


def CanCastle(value):
    if value == 1001 or value == 501:
        temp_attack_array.fill(0)
        for piece in piece_group[1]:
            attackCalc(temp_attack_array, piece.location)
        # print(temp_attack_array)
        if piecearray[4, 0] == 1001:
            if piecearray[0, 0] == 501:
                if piecearray[1, 0] == 0 and piecearray[2, 0] == 0 and piecearray[3, 0] == 0:
                    if temp_attack_array[2, 0] == 0 and temp_attack_array[3, 0] == 0 and temp_attack_array[4, 0] == 0:
                        return 'Q'
            # if self.location == np.array([7, 0]):
            if piecearray[7, 0] == 501:
                if piecearray[5, 0] == 0 and piecearray[6, 0] == 0:
                    if temp_attack_array[6, 0] == 0 and temp_attack_array[5, 0] == 0 and temp_attack_array[4, 0] == 0:
                        return 'K'
    elif value == -1001 or value == -501:
        temp_attack_array.fill(0)
        for piece in piece_group[0]:
            attackCalc(temp_attack_array, piece.location)

        if piecearray[4, 7] == -1001:
            if piecearray[0, 7] == -501:
                if piecearray[1, 7] == 0 and piecearray[2, 7] == 0 and piecearray[3, 7] == 0:
                    if temp_attack_array[2, 7] == 0 and temp_attack_array[3, 7] == 0 and temp_attack_array[4, 7] == 0:
                        return 'q'

            if piecearray[7, 7] == -501:
                if piecearray[5, 7] == 0 and piecearray[6, 7] == 0:
                    if temp_attack_array[6, 7] == 0 and temp_attack_array[5, 7] == 0 and temp_attack_array[4, 7] == 0:
                        return 'k'

    else:
        return False


def getallmoves(value, locn,larr, narr,parr):
    if value == 100:
        move = np.array([0, 1])
        if inbrd(locn + move) and piecearray[tuple(locn + move)] == 0:
            if makepseudomove(locn, locn + move):
                if temp_attack_array[tuple(locn + move)] != 0 :
                    larr.append(comp(locn, locn + move))
                else:
                    narr.append(comp(locn, locn + move))

        if locn[1] == 1 and piecearray[tuple(locn + 2 * move)] == 0 and piecearray[tuple(locn + move)] == 0:
            if makepseudomove(locn, locn + 2 * move):
                if temp_attack_array[tuple(locn + 2* move)] != 0:
                    larr.append(comp(locn, locn + 2*move))
                else:
                    narr.append(comp(locn, locn + 2*move))
        move = np.array([1, 1])
        if inbrd(locn + move) and piecearray[tuple(locn + move)] < 0:
            if makepseudomove(locn, locn + move):
                parr.append(comp(locn, locn + move))
        move = np.array([-1, 1])
        if inbrd(locn + move) and piecearray[tuple(locn + move)] < 0:
            if makepseudomove(locn, locn + move):
                parr.append(comp(locn, locn + move))
    elif value == -100:
        move = np.array([0, -1])
        if inbrd(locn + move) and piecearray[tuple(locn + move)] == 0:
            if makepseudomove(locn, locn + move):
                if temp_attack_array[tuple(locn + move)] != 0:
                    larr.append(comp(locn, locn + move))
                else:
                    narr.append(comp(locn, locn + move))

        if locn[1] == 6 and piecearray[tuple(locn + 2 * move)] == 0 and piecearray[tuple(locn + move)] == 0:
            if makepseudomove(locn, locn + 2 * move):
                if temp_attack_array[tuple(locn + 2 * move)] != 0:
                    larr.append(comp(locn, locn + 2 * move))
                else:
                    narr.append(comp(locn, locn + 2 * move))
        move = np.array([1, -1])
        if inbrd(locn + move) and piecearray[tuple(locn + move)] > 0:
            if makepseudomove(locn, locn + move):
                parr.append(comp(locn, locn + move))
        move = np.array([-1, -1])
        if inbrd(locn + move) and piecearray[tuple(locn + move)] > 0:
            if makepseudomove(locn, locn + move):
                parr.append(comp(locn, locn + move))



    elif value == 302 or value == -302:
        moves = np.array([
            [2, 1], [-2, 1], [-2, -1], [2, -1], [
                1, 2], [-1, 2], [-1, -2], [1, -2]])
        for move in moves:
            if inbrd(locn + move) and piecearray[tuple(locn + move)] * np.sign(value) <= 0:
                if makepseudomove(locn, locn + move):
                    if piecearray[tuple(locn + move)] * np.sign(value) < 0:
                        parr.append(comp(locn, locn + move))
                    elif temp_attack_array[tuple(locn +  move)] != 0:
                        larr.append(comp(locn, locn + move))
                    else:
                        narr.append(comp(locn, locn + move))


    elif value == 300 or value == -300:
        moves = np.array([
            [1, 1], [-1, 1], [-1, -1], [1, -1]])
        for move in moves:
            for k in range(1, 8):

                if inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] == 0:
                    if makepseudomove(locn, locn + k * move):
                        if temp_attack_array[tuple(locn + k* move)] != 0:
                            larr.append(comp(locn, locn + k * move))
                        else:
                            narr.append(comp(locn, locn + k * move))
                elif inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] * np.sign(value) < 0:
                    if makepseudomove(locn, locn + k * move):
                        parr.append(comp(locn, locn + k * move))
                    break
                else:
                    break
                # elif inbrd(locn + k*move) and piecearray[tuple(locn + k*move)] * value > 0:
                #     break
    elif value == 500 or value == -500 or value == 501 or value == -501:
        moves = np.array([
            [1, 0], [-1, 0], [0, -1], [0, 1]])
        for move in moves:
            for k in range(1, 8):
                if inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] == 0:
                    if makepseudomove(locn, locn + k * move):
                        if temp_attack_array[tuple(locn + k * move)] != 0:
                            larr.append(comp(locn, locn + k * move))
                        else:
                            narr.append(comp(locn, locn + k * move))
                elif inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] * np.sign(value) < 0:
                    if makepseudomove(locn, locn + k * move):
                        parr.append(comp(locn, locn + k * move))
                    break
                else:
                    break
                # elif inbrd(locn + k*move) and piecearray[tuple(locn + k*move)] * value > 0:
                #     break
    elif value == 900 or value == -900:
        moves = np.array([
            [1, 1], [-1, 1], [-1, -1], [1, -1], [0, -1], [
                0, 1], [1, 0], [-1, 0]])
        for move in moves:
            for k in range(1, 8):
                if inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] == 0:
                    if makepseudomove(locn, locn + k * move):
                        if temp_attack_array[tuple(locn + k * move)] != 0:
                            larr.append(comp(locn, locn + k * move))
                        else:
                            narr.append(comp(locn, locn + k * move))
                elif inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] * np.sign(value) < 0:
                    if makepseudomove(locn, locn + k * move):
                        parr.append(comp(locn, locn + k * move))
                    break
                else:
                    break
                # elif inbrd(locn + k*move) and piecearray[tuple(locn +k* move)] * value > 0:
                #     break

    elif value == 1000 or value == -1000 or value == 1001 or value == -1001:
        moves = np.array([
            [1, 1], [-1, 1], [-1, -1], [1, -1], [0, -1], [
                0, 1], [1, 0], [-1, 0]])
        for move in moves:
            if inbrd(locn + move) and piecearray[tuple(locn + move)] * np.sign(value) <= 0:
                if makepseudomove(locn, locn + move):
                    narr.append(comp(locn, locn + move))

    Castlable = CanCastle(value)
    if Castlable:
        narr.append(Castlable)





def Search(depth, alpha, beta, player,prevBest = None):

    settings.calc += 1

    if depth == 0:
      return Evaluation(player)


    AI_normal_moves_array = []
    AI_moves_array = []
    Low_Priority_AI_Move_array = []

    for i in range(8):
        for j in range(8):
            if piecearray[i, j] * (-1 ** player) > 0:
                getallmoves(piecearray[i, j], np.array([i, j]),Low_Priority_AI_Move_array,AI_normal_moves_array,AI_moves_array)

    # random.shuffle(Low_Priority_AI_Move_array)
    # random.shuffle(AI_normal_moves_array)
    # random.shuffle(AI_moves_array)

    AI_moves_array = AI_moves_array + AI_normal_moves_array + Low_Priority_AI_Move_array
    if prevBest != None:
        AI_moves_array = [prevBest] + AI_moves_array

    # random.shuffle(AI_moves_array)


    if len(AI_moves_array) == 0:
        return -INfinity

    random.shuffle(AI_moves_array)
    if player%2 == 1:
        maxEval = -INfinity
        for move_val in AI_moves_array:
            if type(move_val) == str:
                CastleMove(move_val)
                player += 1
                gain = Search(depth - 1, alpha, beta, player)
                player -= 1
                UndoCastleMove(move_val)
            else:
                    # MakeMove
                locn_new = ((move_val // 100) // 8, (move_val // 100) % 8)
                locn_old = ((move_val % 100) // 8, (move_val % 100) % 8)
                pieceval = piecearray[tuple(locn_old)]
                attackval = piecearray[tuple(locn_new)]
                piecearray[tuple(locn_old)] = 0
                piecearray[tuple(locn_new)] = pieceval
                if pieceval == 100 and locn_new[1] == 7:
                    piecearray[tuple(locn_new)] = 900
                elif pieceval == -100 and locn_new[1] == 0:
                    piecearray[tuple(locn_new)] = -900
                player += 1
                # Compute
                gain = Search(depth - 1, alpha, beta, player)
                player -= 1
                # UndoMove
                piecearray[tuple(locn_old)] = pieceval
                piecearray[tuple(locn_new)] = attackval

            # maxEval = max(maxEval,gain)
            if gain >= maxEval:
                maxEval = gain
                if player == 1:
                    BestMove = move_val
            alpha = max(alpha,gain)
            if beta <= alpha:
                break
        if player == 1:
            # print(maxEval , alpha , beta)
            return BestMove

        return maxEval

    else:
        minEval = INfinity
        for move_val in AI_moves_array:
            if type(move_val) == str:
                CastleMove(move_val)
                player += 1
                gain = Search(depth - 1, alpha, beta, player)
                player -= 1
                UndoCastleMove(move_val)
            else:
                # MakeMove
                locn_new = ((move_val // 100) // 8, (move_val // 100) % 8)
                locn_old = ((move_val % 100) // 8, (move_val % 100) % 8)
                pieceval = piecearray[tuple(locn_old)]
                attackval = piecearray[tuple(locn_new)]
                piecearray[tuple(locn_old)] = 0
                piecearray[tuple(locn_new)] = pieceval

                player += 1
                # Compute
                gain = Search(depth - 1, alpha, beta, player)
                player -= 1
                # UndoMove
                piecearray[tuple(locn_old)] = pieceval
                piecearray[tuple(locn_new)] = attackval

            minEval = min(minEval, gain)
            beta = min(beta, gain)
            if beta <= alpha:
                break
        return minEval



def MoveGetterAI():

    print("HEllo")
    print(settings.calc)

    seconds = time.time()
    # if settings.moves < 8:
    #     return Search(2, -INfinity, INfinity, 1)
    # else:
    i = 3
    times = time.time()
    bstmv = Search(i, -INfinity, INfinity, 1)
    timeend = time.time()
    print(timeend-times)
    while time.time() - seconds < 2:
        if bstmv == -INfinity:
            break
        i+=1
        times = time.time()
        newbstmv = Search(i, -INfinity, INfinity, 1,bstmv)
        timeend = time.time()
        print(timeend - times)
        bstmv = newbstmv


    return bstmv

