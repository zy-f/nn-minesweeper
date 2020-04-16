"""
@author: trevnels
"""

import colorama

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

def init():
    colorama.init()

def create_unknown_glyph(tag):
    return colorama.Back.WHITE + colorama.Fore.LIGHTBLACK_EX + " " + tag + " "

def render(board):

    for r in range(6):
        buf = ""
        for c in range(6):
            buf += create_unknown_glyph(TAGS[c + r * 6]) + colorama.Style.RESET_ALL
        print(buf)

    print(MINE_GLYPH + colorama.Style.RESET_ALL)
    print(FLAG_GLYPH + colorama.Style.RESET_ALL)

    print(ADJACENT_0_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_1_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_2_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_3_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_4_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_5_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_6_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_7_GLYPH + colorama.Style.RESET_ALL)
    print(ADJACENT_8_GLYPH + colorama.Style.RESET_ALL)

if __name__ == "__main__":
    init()
    render(None)