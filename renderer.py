"""
@author: trevnels
"""

import colorama

from board import Board

TAGS = "abcdefghijklmnopqrstuvwxyz0123456789"




MINE_GLYPH = colorama.Fore.LIGHTBLACK_EX + " * "
FLAG_GLYPH = colorama.Back.LIGHTRED_EX + colorama.Fore.LIGHTWHITE_EX + " ! "

ADJACENT_0_GLYPH = "   "
ADJACENT_1_GLYPH = colorama.Fore.LIGHTBLUE_EX + " 1 "
ADJACENT_2_GLYPH = colorama.Fore.LIGHTGREEN_EX + " 2 "
ADJACENT_3_GLYPH = colorama.Fore.LIGHTRED_EX + " 3 "
ADJACENT_4_GLYPH = colorama.Fore.BLUE + " 4 "
ADJACENT_5_GLYPH = colorama.Fore.RED + " 5 "
ADJACENT_6_GLYPH = colorama.Fore.CYAN + " 6 "
ADJACENT_7_GLYPH = colorama.Fore.LIGHTBLACK_EX + " 7 "
ADJACENT_8_GLYPH = colorama.Fore.WHITE + " 8 "

NUMERIC_GLYPHS = [
    ADJACENT_0_GLYPH,
    ADJACENT_1_GLYPH,
    ADJACENT_2_GLYPH,
    ADJACENT_3_GLYPH,
    ADJACENT_4_GLYPH,
    ADJACENT_5_GLYPH,
    ADJACENT_6_GLYPH,
    ADJACENT_7_GLYPH,
    ADJACENT_8_GLYPH
]

def init():
    colorama.init()

def create_unknown_glyph(r,c,w):
    return colorama.Back.WHITE + colorama.Fore.LIGHTBLACK_EX + str(r*w+c) + " " * (3-len(str(r*w+c)))

def render(board):
    TOP_GLYPH = "┌" + "─" * (board.width*3) + "┐"
    SIDE_GLYPH = "│"
    BOTTOM_GLYPH = "└" + "─" * (board.width*3) + "┘"

    play_board = board.play_board
    print(TOP_GLYPH)

    for r in range(board.height):
        buf = SIDE_GLYPH
        for c in range(board.width):

            if play_board[r][c] == -2:
                # not uncovered yet
                buf += create_unknown_glyph(r,c,board.width)
            elif play_board[r][c] == -3:
                # you ded
                buf += MINE_GLYPH
            elif play_board[r][c] == -1:
                # flagged
                buf += FLAG_GLYPH
            else:
                # draw adjacencies
                buf += NUMERIC_GLYPHS[play_board[r][c]]

            buf += colorama.Style.RESET_ALL

        buf += SIDE_GLYPH
        print(buf)

    print(BOTTOM_GLYPH)

if __name__ == '__main__':
    board = Board(6,6,4)
    init()
    while True:
        render(board)
        move = input("> ").split(",")

        idx = int(move[0])

        r = idx // board.width
        c = idx % board.width

        dead = board.make_move(c, r,int(move[1]))
        if dead:
            break
    render(board)
