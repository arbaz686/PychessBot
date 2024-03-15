import random

import pygame
import os
import numpy as np
from pygame.constants import MOUSEBUTTONDOWN
#import Games
import ChessEngine
import ChessPiece
import settings
from settings import *
from ChessPiece import typepiece, possible_move,playbutton
#import PGNfile



def pieceval(piece):
    if piece.isupper():
        if piece == 'P':
            return 100
        elif piece == 'N':
            return 302
        elif piece == 'B':
            return 300
        elif piece ==  'R':
            return 501
        elif piece == 'Q':
            return 900
        elif piece == 'K':
            return 1001
    else:
        if piece == 'p':
            return -100
        elif piece == 'n' :
            return -302
        elif piece == 'b' :
            return -300
        elif piece == 'r':
            return -501
        elif piece == 'q':
            return -900
        elif piece == 'k':
            return -1001

Timer_time = np.array([6000,6000])


FPS = 15
drk_sq = (118, 150, 86)
light_sq = (238, 238, 210)
flag = 0

pygame.init()

move_sound = pygame.mixer.Sound(os.path.join('Sound', 'strt.wav'))
piece_selected = None


font = pygame.font.Font('freesansbold.ttf', 32)
pygame.display.set_caption("Lets Play Chess")
play_button = pygame.image.load(os.path.join('Images', 'Chess_Play.png'))

pygame.display.set_icon(play_button)


def DrawNoOfMoves():
    move_text = font.render("Move: " + str(settings.moves), True, (255, 255, 0))
    move_text_rect = move_text.get_rect()
    move_text_rect.center = (LEFTGAP / 2, HEIGHT / 2)
    screen.blit(move_text, move_text_rect)

def gameover_message(loss):
    s = pygame.Surface((BOARDL, BOARDL), pygame.SRCALPHA)  # per-pixel alpha
    s.fill((128, 128, 128, 128))  # notice the alpha value in the color
    screen.blit(s, (LEFTGAP,BORDER))
    Loss_Text = font.render("Game Over: " + str(loss), True, (0, 0, 0))
    move_text_rect = Loss_Text.get_rect()
    move_text_rect.center = (WIDTH / 2, HEIGHT / 2)
    screen.blit(Loss_Text, move_text_rect)

def AI_process_Text():
    ai_text = font.render("Processing", True, (255, 255, 0))
    ai_text_rect = ai_text.get_rect()
    ai_text_rect.center = (BOARDL+ 3*LEFTGAP / 2, HEIGHT / 2)
    screen.blit(ai_text, ai_text_rect)

def DrawTimer(t_old):
    if settings.moves == 0:
        t_old =  pygame.time.get_ticks()
    else:
        Time_Now = pygame.time.get_ticks()
        Timer_time[settings.moves % 2] -= (Time_Now - t_old)/10000
        t_old = Time_Now

    timer_b = font.render("Time: " + str(Timer_time[1]//600) + ":"+str((Timer_time[1]%600)/10) , True, (255, 255, 0))
    timer_b_rect = timer_b.get_rect()
    timer_b_rect.center = (LEFTGAP / 2, BORDER + BOARDSQ/2)
    screen.blit(timer_b, timer_b_rect)

    timer_w = font.render("Time: " + str(Timer_time[0]//600) + ":"+str((Timer_time[0]%600)/10), True, (255, 255, 0))
    timer_w_rect = timer_w.get_rect()
    timer_w_rect.center = (LEFTGAP / 2, BORDER + BOARDL - BOARDSQ / 2)
    screen.blit(timer_w, timer_w_rect)

    return t_old

def initialiseboard():
    file = 7
    rank = 0
    for piece in FEN:
        if piece == '/':
            rank = 0
            file -= 1
        elif piece.isdigit():
            rank += int(piece)
        else:

            location = np.array([rank, file])

            if piece.isupper():
                white_pieces.add(typepiece(piece, location))
            else:
                black_pieces.add(typepiece(piece, location))
            piecearray[tuple(location)] = pieceval(piece)
            rank += 1


def drawboard():
    screen.fill((30, 30, 30))
    for i in range(8):
        for j in range(8):
            if (i + j) % 2 == 1:
                pygame.draw.rect(screen, drk_sq, [LEFTGAP + i * BOARDSQ, BORDER + j * BOARDSQ, BOARDSQ, BOARDSQ])
            else:
                pygame.draw.rect(screen, light_sq, [LEFTGAP + i * BOARDSQ, BORDER + j * BOARDSQ, BOARDSQ, BOARDSQ])

def draw_possible_moves():
    for move in moves_array:
        selectionbrd.add(possible_move(move))

def makemainmenu():
    Background_img = pygame.image.load(os.path.join('Images', 'BackgroundR.png'))
    screen.blit(Background_img,(0,0))
    #screen.blit(Play_img,(WIDTH/10,HEIGHT/2))
    buttongrp.add(playbutton((WIDTH/4,HEIGHT/2)))

def Chess_ai():
    AI_out = ChessEngine.MoveGetterAI()
    print(AI_out)
    if AI_out == -ChessEngine.INfinity:
        settings.GAMEOVER = True
        settings.LOSS = "You Won"
    elif type(AI_out) == str:
        ChessEngine.CastleMove(AI_out)
        ChessPiece.make_png(0, 0, AI_out)

    else:
        locn_old = ((AI_out % 100) // 8, (AI_out % 100) % 8)
        locn_new = ((AI_out // 100) // 8, (AI_out // 100) % 8)
        ChessPiece.make_png(locn_old, locn_new, 0)
        val_old = piecearray[locn_old]
        piecearray[locn_old] = 0
        piecearray[locn_new] = val_old
        if val_old == 100 and locn_new[1] == 7:
            piecearray[tuple(locn_new)] = 900
        elif val_old == -100 and locn_new[1] == 0:
            piecearray[tuple(locn_new)] = -900
    ChessPiece.respriteboard()
    settings.moves += 1
    #move_sound.play()





def main():
    setting_init()
    CHECKMATE = False
    Game_Play = False
    book_move_possible = True
    pgn_file_1 = open("PGNfile1.txt",'r')
    pgn_file_2 = open("PGNfile2.txt",'r')
    
    game_lines = pgn_file_1.readlines() + pgn_file_2.readlines()
    
    settings.moves
    

    
    #moves = 0
    t_old =  pygame.time.get_ticks()

    run = True
    clock = pygame.time.Clock()
    #drawboard()
    initialiseboard()
    makemainmenu()
    # drawpiece()
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == MOUSEBUTTONDOWN and event.button == 1 and Game_Play:
                if settings.moves%2 == 0:
                    for selects in selectionbrd:
                        if selects.rect.collidepoint(event.pos):
                            print(piece_selected.type)
                            ChessPiece.make_png(piece_selected.location,selects.location, selects.castletype)
                            print(settings.PGN)
                            piece_selected.update(selects.location,selects.castletype)
                            
                            settings.moves += 1
                            
                            if Game_Play :
                                drawboard()
                                selectionbrd.draw(screen)

                                white_pieces.draw(screen)
                                black_pieces.draw(screen)

                                DrawNoOfMoves()
                                AI_process_Text()
                                # t_new = DrawTimer(t_old)
                                # t_old = t_new
                                if settings.GAMEOVER == True:
                                    gameover_message(settings.LOSS)
                            pygame.display.update()

                            move_sound.play()

                            t = ChessPiece.isCheckStaleMate()
                            if t:
                                if t == 10:
                                    settings.GAMEOVER = True
                                    settings.LOSS = "You Lost"
                                else:
                                    settings.GAMEOVER = True
                                    settings.LOSS = "Stale Mate"

                            print(piecearray)
                    selectionbrd.empty()
                    for piece in piece_group[settings.moves % 2]:
                        if piece.rect.collidepoint(event.pos):
                            piece_selected = piece
                            moves_array.clear()
                            piece.get_moves(moves_array)

                            draw_possible_moves()
                if settings.moves%2 == 1:
                    print(settings.PGN)
                    if book_move_possible:
                        print("Chess Engine Output : ")
                        str_present = [s for s in game_lines if settings.PGN in s]
                        random.shuffle(str_present)
                        if len(str_present)!=0:
                            for string in str_present:
                                print(string)
                                pgn_copy = settings.PGN.split(" ")
                                print(pgn_copy)
                                string = string.split(" ")
                                print(string)
                                if ChessPiece.makebookmove(string[len(pgn_copy)-1]):
                                    settings.PGN += string[len(pgn_copy) - 1]  + " "
                                    settings.moves+=1
                                    ChessPiece.respriteboard()
                                    move_sound.play()
                                    break
                                print(string[len(pgn_copy)-1]  + " ")
                            else:
                                book_move_possible = False
                                Chess_ai()
                        else:
                            book_move_possible = False
                            Chess_ai()
                    else:
                        print("Chess Engine Output : ")
                        Chess_ai()

            elif event.type == MOUSEBUTTONDOWN and Game_Play == False:
                    for button in buttongrp:
                        print("Hi")
                        if button.rect.collidepoint(event.pos):
                            Game_Play = True
                            strt_sound = pygame.mixer.Sound(os.path.join('Sound','move.wav'))
                            strt_sound.play()

            elif Game_Play == False and event.type == pygame.KEYDOWN:
                Game_Play = True
                strt_sound = pygame.mixer.Sound(os.path.join('Sound','move.wav'))
                strt_sound.play()

        if Game_Play :
            drawboard()
            selectionbrd.draw(screen)

            white_pieces.draw(screen)
            black_pieces.draw(screen)

            DrawNoOfMoves()
            # t_new = DrawTimer(t_old)
            # t_old = t_new
            if settings.GAMEOVER == True:
                gameover_message(settings.LOSS)
        else:

            buttongrp.draw(screen)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    setting_init()
    main()
