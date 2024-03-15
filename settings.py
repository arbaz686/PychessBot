import numpy as np
import pygame

def setting_init():
    global moves
    global HEIGHT
    global WIDTH
    global BORDER
    global BOARDL
    global BOARDSQ
    global LEFTGAP
    global FEN
    global piecearray
    global attack_array_b
    global attack_array_w
    global  whiteincheck
    global blackincheck
    global CHECKMATE
    global buttongrp
    CHECKMATE = False


    

#Make sure Boardl%8 == 0, else weird tearing issues

whiteincheck  = False
blackincheck  = False

whitekinglocn = np.array([0,4])
blackkinglocn = np.array([7,4])


moves = 0



HEIGHT = 720
WIDTH = 1080
BORDER = 64
BOARDL = HEIGHT - 2*BORDER
BOARDSQ = BOARDL/8         
LEFTGAP = (WIDTH-BOARDL)/2

#FEN = list('1r3rk1/p1pq1ppp/1b4n1/6B1/3P4/2P3P1/PPQ2PbP/RN3RK1')
FEN = list('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
#FEN = list('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQK2R')
piecearray = np.zeros((8,8),dtype=np.int16)

attack_array = np.zeros((2,8,8),dtype=np.int8)
temp_attack_array = np.zeros((8,8),dtype=np.int8)

white_pieces = pygame.sprite.Group()
black_pieces = pygame.sprite.Group()    

piece_group = [white_pieces,black_pieces]

selectionbrd = pygame.sprite.Group()

buttongrp = pygame.sprite.Group()

calc = 0

moves_array = []

screen = pygame.display.set_mode((WIDTH,HEIGHT))

move_is_castle = False

CHECKMATE = False
GAMEOVER = False
LOSS = str()

PGN = str()

PawnTable = np.array([[ 100,50,10,5,0,5,5,0],
                        [ 100,50,10,5,0,-5,10,0],
                        [ 100,50,20,10,0,-10,10,0],
                        [ 100,50,30,27,40,0,-25,0],
                        [ 100,50,30,27,40,0,-25,0],
                        [ 100,50,20,10,0,-10,10,0],
                        [ 100,50,10,5,0,-5,10,0],
                        [ 100,50,10,5,0,5,5,0] ])


KnightTable = np.array([[ -50,-40,-30,-30,-30,-30,-40,-50],
                        [ -40,-20,0,5,0,5,-20,-40],
                        [ -30,0,10,15,15,10,0,-20],
                        [ -30,0,15,20,20,15,5,-30],
                        [ -30,0,15,20,20,15,5,-30],
                        [ -30,0,10,15,15,10,0,-20],
                        [ -40,-20,0,5,0,5,-20,-40],
                        [ -50,-40,-30,-30,-30,-30,-40,-50]])

BishopTable = np.array([[ -20,-10,-10,-10,-10,-10,-10,-20],
                        [ -10,0,0,5,0,10,5,-10],
                        [ -10,0,5,5,10,10,0,-40],
                        [ -10,0,10,10,10,10,0,-10],
                        [ -10,0,10,10,10,10,0,-10],
                        [ -10,0,5,5,10,10,0,-40],
                        [ -10,0,0,5,0,10,5,-10],
                        [ -20,-10,-10,-10,-10,-10,-10,-20],])

RookTable = np.array([[ 0,5,-5,-5,-5,-5,-5,0],
                        [ 0,10,0,0,0,0,0,-10],
                        [ 0,10,0,0,0,0,0,-10],
                        [ 0,10,0,0,0,0,0,5],
                        [ 0,10,0,0,0,0,0,5],
                        [ 0,10,0,0,0,0,0,-10],
                        [ 0,10,0,0,0,0,0,-10],
                        [ 0,5,-5,-5,-5,-5,-5,0], ])

QueenTable = np.array([[ -20,-10,-10,-5,0,-10,-10,-20],
                        [ -10,0,0,0,0,5,0,-10],
                        [ -10,0,5,5,5,5,5,-10],
                        [ -5,0,5,5,5,5,0,-5],
                        [ -5,0,5,5,5,5,0,-5],
                        [ -10,0,5,5,5,5,0,-10],
                        [ -10,0,0,0,0,0,0,-10],
                        [ -20,-10,-10,-5,-5,-10,-10,-20],] )

KingTable = np.array([[ -30,-30,-30,-30,-20,-10,20,20],
                        [ -40,-40,-40,-40,-30,-20,20,30],
                        [ -40,-40,-40,-40,-30,-20,0,10],
                        [ -50,-50,-50,-50,-40,-20,0,0],
                        [ -50,-50,-50,-50,-40,-20,0,0],
                        [ -40,-40,-40,-40,-30,-20,0,10],
                        [ -40,-40,-40,-40,-30,-20,20,30],
                        [ -30,-30,-30,-30,-20,-10,20,20],])

KingEndGameTable = np.array([[ -50,-30,-30,-30,-30,-30,-30,-50],
                            [ -40,-20,-10,-10,-10,-10,-30,-30],
                            [ -30,-10,20,30,30,20,0,-30],
                            [ -20,0,30,40,40,30,0,-30],
                            [ -20,0,30,40,40,30,0,-30],
                            [ -30,-10,20,30,30,20,0,-30],
                            [ -40,-20,-10,-10,-10,-10,-30,-30],
                            [ -50,-30,-30,-30,-30,-30,-30,-50],])