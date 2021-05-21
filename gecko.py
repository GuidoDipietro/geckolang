from gparser import GeckoParser, REPL
from glexer import GeckoLexer
from colorama import init

##########################
########## MAIN ##########
##########################

if __name__ == '__main__':

    init() # Colorama stuff
    lexer = GeckoLexer()
    parser = GeckoParser()

    REPL(lexer, parser)