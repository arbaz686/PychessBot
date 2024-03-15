import pygame
import numpy as np
import os

import ChessEngine
import settings
from settings import *


# setting_init()
def pieceval(piece):
    if piece.isupper():
        if piece == 'P':
            return 100
        elif piece == 'N':
            return 302
        elif piece == 'B':
            return 300
        elif piece == 'R':
            return 500
        elif piece == 'Q':
            return 900
        elif piece == 'K':
            return 1000
    else:
        if piece == 'p':
            return -100
        elif piece == 'n':
            return -302
        elif piece == 'b':
            return -300
        elif piece == 'r':
            return -500
        elif piece == 'q':
            return -900
        elif piece == 'k':
            return -1000


def piecetyp(piece):
    if piece > 0:
        if piece == 100:
            return 'P'
        elif piece == 302:
            return 'N'
        elif piece == 300:
            return 'B'
        elif piece == 500 or piece == 501:
            return 'R'
        elif piece == 900:
            return 'Q'
        elif piece == 1000 or piece == 1001:
            return 'K'
    else:
        if piece == -100:
            return 'p'
        elif piece == -302:
            return 'n'
        elif piece == -300:
            return 'b'
        elif piece == -500 or piece == -501:
            return 'r'
        elif piece == -900:
            return 'q'
        elif piece == -1000 or piece == -1001:
            return 'k'


def globalloc(location):
    loc = (
        int(LEFTGAP + BOARDSQ / 2 + ((location[0]) * BOARDSQ)),
        int(BORDER + BOARDSQ / 2 + ((7 - location[1]) * BOARDSQ)))
    return loc


def inbrd(location):
    if (0 <= location[0] < 8) and (0 <= location[1] < 8):
        return True
    else:
        return False


def respriteboard():
    piece_group[0].empty()
    piece_group[1].empty()
    for i in range(8):
        for j in range(8):
            if piecearray[i, j]:
                location = np.array([i, j])
                piece = piecetyp(piecearray[i, j])
                ##print(piece)
                if piece.isupper():
                    piece_group[0].add(typepiece(piece, location))
                else:
                    piece_group[1].add(typepiece(piece, location))


def makepseudomove(locn_old, locn_new):

    temp_attack_array.fill(0)
    pieceval = piecearray[tuple(locn_old)]
    attackval = piecearray[tuple(locn_new)]
    piecearray[tuple(locn_old)] = 0
    piecearray[tuple(locn_new)] = pieceval
    for i in range(8):
        for j in range(8):
            if piecearray[i, j] * np.sign(pieceval) < 0:
                attackCalc(temp_attack_array, np.array([i, j]))
            elif np.sign(piecearray[i, j]) * np.sign(pieceval) > 0 and (
                    abs(piecearray[i, j]) == 1000 or abs(piecearray[i, j]) == 1001):
                king_locn = (i, j)
    # print(piecearray)
    # print(temp_attack_array)
    piecearray[tuple(locn_old)] = pieceval
    piecearray[tuple(locn_new)] = attackval
    # print(piecearray)

    if temp_attack_array[king_locn] != 0:
        return False
    else:
        return True


class typepiece(pygame.sprite.Sprite):

    def __init__(self, type, location):

        pygame.sprite.Sprite.__init__(self)

        self.location = location
        self.type = type
        if self.type.isupper():
            self.img = pygame.image.load(os.path.join('Images', type + 'W.png'))
        else:
            self.img = pygame.image.load(os.path.join('Images', type + 'B.png'))

        self.image = pygame.transform.scale(self.img, (int(BOARDSQ), int(BOARDSQ)))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = globalloc(self.location)

        if self.type.isupper():
            self.color = 'W'
        else:
            self.color = 'B'

        ## Pawns
        if self.type == 'P':
            self.isInf = False
            self.moves = np.array([[0, 1]])
            self.movespl = np.array([[-1, 1], [1, 1]])
        elif self.type == 'p':
            self.isInf = False
            self.moves = np.array([[0, -1]])
            self.movespl = np.array([[-1, -1], [1, -1]])

        ## Rooks
        elif self.type == 'r' or self.type == 'R':
            self.isInf = True
            self.moves = np.array([[0, -1], [0, 1], [1, 0], [-1, 0]])

        ##Bishops
        elif self.type == 'b' or self.type == 'B':
            self.isInf = True
            self.moves = np.array([[1, 1], [-1, 1], [-1, -1], [1, -1]])

        ##Kings
        elif self.type == 'k' or self.type == 'K':
            self.isInf = False
            self.moves = np.array([
                [1, 1], [-1, 1], [-1, -1], [1, -1], [0, -1], [
                    0, 1], [1, 0], [-1, 0]])


        ##Queens
        elif self.type == 'q' or self.type == 'Q':
            self.isInf = True
            self.moves = np.array([
                [1, 1], [-1, 1], [-1, -1], [1, -1], [0, -1], [
                    0, 1], [1, 0], [-1, 0]])

        ##Knights
        elif self.type == 'n' or self.type == 'N':
            self.isInf = False
            self.moves = np.array([
                [2, 1], [-2, 1], [-2, -1], [2, -1], [
                    1, 2], [-1, 2], [-1, -2], [1, -2]])

    def Castling(self):
        if self.type == 'K' or self.type == 'R':
            temp_attack_array.fill(0)
            for piece in piece_group[(moves + 1) % 2]:
                attackCalc(temp_attack_array, piece.location)
            # print(temp_attack_array)
            if piecearray[4, 0] == 1001:
                if piecearray[0, 0] == 501:
                    if piecearray[1, 0] == 0 and piecearray[2, 0] == 0 and piecearray[3, 0] == 0:
                        if temp_attack_array[2, 0] == 0 and temp_attack_array[3, 0] == 0 and temp_attack_array[
                            4, 0] == 0:
                            return 'Q'
                # if self.location == np.array([7, 0]):
                if piecearray[7, 0] == 501:
                    if piecearray[5, 0] == 0 and piecearray[6, 0] == 0:
                        if temp_attack_array[6, 0] == 0 and temp_attack_array[5, 0] == 0 and temp_attack_array[
                            4, 0] == 0:
                            return 'K'
        elif self.type == 'k' or self.type == 'r':
            temp_attack_array.fill(0)
            for piece in piece_group[(moves + 1) % 2]:
                attackCalc(temp_attack_array, piece.location)

            if piecearray[4, 7] == -1001:
                if piecearray[0, 7] == -501:
                    if piecearray[1, 7] == 0 and piecearray[2, 7] == 0 and piecearray[3, 7] == 0:
                        if temp_attack_array[2, 7] == 0 and temp_attack_array[3, 7] == 0 and temp_attack_array[
                            4, 7] == 0:
                            return 'q'

                if piecearray[7, 7] == -501:
                    if piecearray[5, 7] == 0 and piecearray[6, 7] == 0:
                        if temp_attack_array[6, 7] == 0 and temp_attack_array[5, 7] == 0 and temp_attack_array[
                            4, 7] == 0:
                            return 'k'

        else:
            return False

    def get_moves(self, arr):

        if self.type == 'P':

            move = self.moves[0]
            ## move pawn 1 forward

            if inbrd(self.location + move) and piecearray[tuple(self.location + move)] == 0:
                if makepseudomove(self.location, self.location + move):
                    arr.append(self.location + move)

            ## move 2 forward
            if self.location[1] == 1 and piecearray[tuple(self.location + 2 * move)] == 0 and piecearray[
                tuple(self.location + move)] == 0:
                if makepseudomove(self.location, self.location + 2 * move):
                    arr.append(self.location + 2 * move)

            ## move sideways
            if inbrd(self.location + self.movespl[0]) and piecearray[tuple(self.location + self.movespl[0])] < 0:
                if makepseudomove(self.location, self.location + self.movespl[0]):
                    arr.append(self.location + self.movespl[0])

            ## move sideways
            if inbrd(self.location + self.movespl[1]) and piecearray[tuple(self.location + self.movespl[1])] < 0:
                if makepseudomove(self.location, self.location + self.movespl[1]):
                    arr.append(self.location + self.movespl[1])


        elif self.type == 'p':

            move = self.moves[0]
            ## move pawn 1 forward

            if inbrd(self.location + move) and piecearray[tuple(self.location + move)] == 0:
                if makepseudomove(self.location, self.location + move):
                    arr.append(self.location + move)

            ## move 2 forward
            if self.location[1] == 6 and piecearray[tuple(self.location + 2 * move)] == 0 and \
                    piecearray[
                        tuple(self.location + move)] == 0:
                if makepseudomove(self.location, self.location + 2 * move):
                    arr.append(self.location + 2 * move)

            ## move sideways
            if inbrd(self.location + self.movespl[0]) and piecearray[tuple(self.location + self.movespl[0])] > 0:
                if makepseudomove(self.location, self.location + self.movespl[0]):
                    arr.append(self.location + self.movespl[0])

            ## move sideways
            if inbrd(self.location + self.movespl[1]) and piecearray[tuple(self.location + self.movespl[1])] > 0:
                if makepseudomove(self.location, self.location + self.movespl[1]):
                    arr.append(self.location + self.movespl[1])



        elif self.isInf:
            for move in self.moves:
                ####print(move)
                k = 1
                # print(self.location + k * move)
                # print(piecearray)
                while inbrd(self.location + k * move) and piecearray[tuple(self.location + k * move)] == 0:
                    #####print("Hi")

                    if makepseudomove(self.location, self.location + k * move):
                        arr.append(self.location + k * move)
                    k += 1
                if inbrd(self.location + k * move) and (piecearray[tuple(self.location + k * move)] * pieceval(
                        self.type)) < 0:
                    if makepseudomove(self.location, self.location + k * move):
                        arr.append(self.location + k * move)

        else:
            for move in self.moves:
                #####print(move)
                # print(inbrd(self.location + k*move))
                ####print(self.location + move)
                # print(piecearray[tuple(self.location + k*move)])
                ####print(piecearray)
                if inbrd(self.location + move) and piecearray[tuple(self.location + move)] == 0:
                    if makepseudomove(self.location, self.location + move):
                        arr.append(self.location + move)
                elif inbrd(self.location + move) and (
                        piecearray[tuple(self.location + move)] * pieceval(self.type)) < 0:
                    if makepseudomove(self.location, self.location + move):
                        arr.append(self.location + move)

        castle = self.Castling()

        if castle:
            ###print("Castle")
            if (castle.isupper() and self.type.isupper()) or (castle.islower() and self.type.islower()):
                arr.append(self.type + castle)
                ###print(self.type + castle)

            # if castle == 'Q':
            #     if self.type == 'R':
            #         if makepseudomove()
            #             arr.append('RQ')
            #     elif self.type == 'K':
            #         arr.append('KQ')
            # elif castle == 'K':
            #     if self.type == 'R':
            #         arr.append('RK')
            #     elif self.type == 'K':
            #         arr.append('KK')
            # elif castle == 'q':
            #     if self.type == 'r':
            #         arr.append('rq')
            #     elif self.type == 'k':
            #         arr.append('kq')
            # elif castle == 'k':
            #     if self.type == 'r':
            #         arr.append('rk')
            #     elif self.type == 'k':
            #         arr.append('kk')

    def update(self, location, castletype):

        if type(castletype) == str:
            locn_new = castletype[1]
            if locn_new == 'Q':
                piecearray[0, 0] = 0
                piecearray[4, 0] = 0
                piecearray[2, 0] = 1000
                piecearray[3, 0] = 500
            elif locn_new == 'q':
                piecearray[0, 7] = 0
                piecearray[4, 7] = 0
                piecearray[2, 7] = -1000
                piecearray[3, 7] = -500
            elif locn_new == 'K':
                piecearray[7, 0] = 0
                piecearray[4, 0] = 0
                piecearray[6, 0] = 1000
                piecearray[5, 0] = 500
            elif locn_new == 'k':
                piecearray[7, 7] = 0
                piecearray[4, 7] = 0
                piecearray[6, 7] = -1000
                piecearray[5, 7] = -500
            respriteboard()
        else:
            piecearray[tuple(self.location)] = 0
            self.location = location
            if pieceval(self.type) * piecearray[tuple(location)] < 0:
                piecearray[tuple(self.location)] = pieceval(self.type)
                respriteboard()
            else:
                piecearray[tuple(self.location)] = pieceval(self.type)
            if self.type == 'P' and self.location[1] == 7:
                piecearray[tuple(self.location)] = 9 * pieceval(self.type)
                respriteboard()
            elif self.type == 'p' and self.location[1] == 0:
                piecearray[tuple(self.location)] = 9 * pieceval(self.type)
                respriteboard()

        self.rect.center = globalloc(self.location)


class possible_move(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)

        if type(location) == str:
            self.castletype = location

            if location == 'RQ' or location == 'RK':
                self.location = np.array([4, 0])
            elif location == 'KQ':
                self.location = np.array([0, 0])
            elif location == 'KK':
                self.location = np.array([7, 0])
            elif location == 'rq' or location == 'rk':
                self.location = np.array([4, 7])
            elif location == 'kq':
                self.location = np.array([0, 7])
            elif location == 'kk':
                self.location = np.array([7, 7])
        else:
            self.castletype = None
            self.location = location

        if piecearray[tuple(self.location)] != 0:
            self.img = pygame.image.load(os.path.join('Images', 'Attack.png'))
        else:
            self.img = pygame.image.load(os.path.join('Images', 'SelectedSq.png'))
        self.image = pygame.transform.scale(self.img, (int(BOARDSQ), int(BOARDSQ)))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = globalloc(self.location)


def attackCalc(arr, locn):
    value = piecearray[tuple(locn)]
    if value == 100:
        if inbrd(locn + np.array([1, 1])) and piecearray[tuple(locn + np.array([1, 1]))] <= 0:
            arr[tuple(locn + np.array([1, 1]))] += 2
        if inbrd(locn + np.array([-1, 1])) and piecearray[tuple(locn + np.array([-1, 1]))] <= 0:
            arr[tuple(locn + np.array([-1, 1]))] += 2
    elif value == -100:
        if inbrd(locn + np.array([1, -1])) and piecearray[tuple(locn + np.array([1, -1]))] >= 0:
            arr[tuple(locn + np.array([1, -1]))] += 5
        if inbrd(locn + np.array([-1, -1])) and piecearray[tuple(locn + np.array([-1, -1]))] >= 0:
            arr[tuple(locn + np.array([-1, -1]))] += 5


    elif value == 302 or value == -302:
        moves = np.array([
            [2, 1], [-2, 1], [-2, -1], [2, -1], [
                1, 2], [-1, 2], [-1, -2], [1, -2]])
        for move in moves:
            if inbrd(locn + move):  # and piecearray[tuple(locn + move)]*value <= 0:
                arr[tuple(locn + move)] += 3

    elif value == 300 or value == -300:
        moves = np.array([
            [1, 1], [-1, 1], [-1, -1], [1, -1]])
        for move in moves:
            for k in range(1, 8):
                if inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] == 0:
                    arr[tuple(locn + k * move)] += 2
                elif inbrd(locn + k * move):  # and piecearray[tuple(locn + k*move)] * value < 0:
                    arr[tuple(locn + k * move)] += 5
                    break
                # elif inbrd(locn + k*move) and piecearray[tuple(locn + k*move)] * value > 0:
                #     break
    elif value == 500 or value == -500 or value == 501 or value == -501:
        moves = np.array([
            [1, 0], [-1, 0], [0, -1], [0, 1]])
        for move in moves:
            for k in range(1, 8):
                if inbrd(locn + k * move) and piecearray[tuple(locn + k * move)] == 0:
                    arr[tuple(locn + k * move)] += 2
                elif inbrd(locn + k * move):  # and piecearray[tuple(locn + k*move)] * value < 0:
                    arr[tuple(locn + k * move)] += 5
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
                    arr[tuple(locn + k * move)] += 2
                elif inbrd(locn + k * move):  # and piecearray[tuple(locn +k* move)] * value < 0:
                    arr[tuple(locn + k * move)] += 5
                    break
                # elif inbrd(locn + k*move) and piecearray[tuple(locn +k* move)] * value > 0:
                #     break

    elif value == 1000 or value == -1000 or value == 1001 or value == -1001:
        moves = np.array([
            [1, 1], [-1, 1], [-1, -1], [1, -1], [0, -1], [
                0, 1], [1, 0], [-1, 0]])
        for move in moves:
            if inbrd(locn + move):  # and piecearray[tuple(locn + move)] * value <= 0
                arr[tuple(locn + move)] += 3


def isCheckStaleMate():
    ###print(moves)
    checkmatearray = []
    king_locn = np.array([0, 0])
    temp_attack_array.fill(0)

    if len(piece_group[0]) == 1 and len(piece_group[1]) == 1:
        return 2

    for piece in piece_group[moves % 2]:
        piece.get_moves(checkmatearray)
        if len(checkmatearray) > 0:
            return False
        attackCalc(temp_attack_array, piece.location)
        ###print("wwwwwwwwwwwwwwwwwwwwwwww")
        ###print(temp_attack_array)
        if moves % 2 == 0 and piece.type == 'K':
            king_locn = piece.location
        elif moves % 2 == 1 and piece.type == 'k':
            king_locn = piece.location

    if temp_attack_array[tuple(king_locn)] != 0:
        return 10
    else:
        return 2


def make_png(locn_old,locn_new,castle):
    if settings.moves%2 == 0:
        settings.PGN += str(int(settings.moves/2 + 1)) + "."
    if type(castle) == str:
        if castle == 'k' or  castle == 'K':
            settings.PGN += "O-O "
        elif castle == 'q' or  castle == 'Q':
            settings.PGN += "O-O-O "

    else:
        pice_type = piecetyp(abs(piecearray[tuple(locn_old)]))
        char = 'a'
        move_to_rank  = chr(ord(char[0]) + locn_new[0])
        move_to_file = str(locn_new[1] + 1)
        if pice_type == 'P' or pice_type == 'p':
            if piecearray[tuple(locn_new)] != 0:
                old_rank = chr(ord(char[0]) + locn_old[0])
                settings.PGN += old_rank + "x" + move_to_rank + move_to_file + " "
            else:
                settings.PGN += move_to_rank + move_to_file + " "
        else:
            if piecearray[tuple(locn_new)] != 0:
                settings.PGN += pice_type + "x" + move_to_rank + move_to_file + " "
            else:
                settings.PGN += pice_type +  move_to_rank + move_to_file + " "


def makebookmove(move):
    if move == "O-O":
        ChessEngine.CastleMove('k')
        return True
    elif move == "O-O-O":
        ChessEngine.CastleMove('q')
        return True
    elif move[0].isupper():
        pic = pieceval(move[0])
        t = 1
        if move[t] == "x" or move[t+1].islower():
            t+=1
        rank  = move[t]
        file = move[t+1]
        char = 'a'
        rank_int = int(ord(rank)-ord(char[0]))
        file_int = int(file)-1
        print(piecearray)
        loc_new = 8*rank_int + file_int


        for i in range(8):
            for j in range(8):
                if abs(piecearray[i,j] + pic) < 2:
                    move_pgn = []
                    ChessEngine.getallmoves(piecearray[i,j],np.array([i,j]),move_pgn,move_pgn,move_pgn)
                    for move in move_pgn:
                        if type(move) != str and move//100 == loc_new:
                            locn_old = ((move % 100) // 8, (move % 100) % 8)
                            locn_new = ((move // 100) // 8, (move // 100) % 8)
                            val_old = piecearray[locn_old]
                            piecearray[locn_old] = 0
                            piecearray[locn_new] = val_old
                            print(piecearray)
                            return True

    elif move[0].islower():
        if move[1] == "x":
            ranko = move[0]
            rankn = move[2]
            file = move[3]
            char = 'a'
            rank_old = int(ord(ranko) - ord(char[0]))
            rank_new = int(ord(rankn) - ord(char[0]))

            file_new = int(file) - 1
            file_old = int(file)
            if piecearray[rank_new,file_new]==0:
                #En-pessant
                piecearray[rank_new, file_new] = piecearray[rank_old,file_old]
                piecearray[rank_old, file_old] = 0
                piecearray[rank_new, file_old] = 0
            else:
                piecearray[rank_new, file_new] = piecearray[rank_old, file_old]
                piecearray[rank_old, file_old] = 0
            return True
        else:
            rank = move[0]
            file = move[1]
            char = 'a'
            rank_o= int(ord(rank) - ord(char[0]))
            file_o = int(file) - 1
            print(piecearray[rank_o, 6])
            if file_o == 4 and piecearray[rank_o,5] == 0:
                piecearray[rank_o, 4] = piecearray[rank_o, 6]
                piecearray[rank_o, 6] = 0
                print(piecearray)
                return True
            else:
                piecearray[rank_o, file_o] = piecearray[rank_o, file_o+1]
                piecearray[rank_o, file_o+1] = 0
                return True
    return False



class playbutton(pygame.sprite.Sprite):
    def __init__(self,location):
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.img = pygame.image.load(os.path.join('Images', 'Chess_Play.png'))
        self.image = pygame.transform.scale(self.img, (314,314))
        self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.center = self.location
    