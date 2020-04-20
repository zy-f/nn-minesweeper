"""
@author: trevnels
"""

import colorama

TAGS = "abcdefghijklmnopqrstuvwxyz0123456789"

TOP_GLYPH = "┌" + "─" * 18 + "┐"
SIDE_GLYPH = "│"
BOTTOM_GLYPH = "└" + "─" * 18 + "┘"


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

def create_unknown_glyph(tag):
    return colorama.Back.WHITE + colorama.Fore.LIGHTBLACK_EX + " " + tag + " "

def render(board):

    play_board = board.play_board
    print(TOP_GLYPH)

    for r in range(board.height):
        buf = SIDE_GLYPH
        for c in range(board.width):

            if play_board[r][c] == -2:
                # not uncovered yet
                buf += create_unknown_glyph(TAGS[c + r * 6])
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