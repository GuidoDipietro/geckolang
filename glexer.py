from sly import Lexer

class GeckoLexer(Lexer):
    tokens = {  ID, PLUS, MINUS, TIMES,
                DIV, POW, MATHFUNC, NUMBER,
                LPAREN, RPAREN, ASSIGN, THEN, POLAR,
                CALC, EXIT, NEWLINE, TICK,
                SEMI, VARS, NEW }

    ignore = ' \t'

    ID          = r'[a-zA-Z_][0-9a-zA-Z_]*'
    ID['sin']   = MATHFUNC
    ID['cos']   = MATHFUNC
    ID['tan']   = MATHFUNC
    ID['asin']  = MATHFUNC
    ID['acos']  = MATHFUNC
    ID['atan']  = MATHFUNC
    ID['sind']  = MATHFUNC
    ID['cosd']  = MATHFUNC
    ID['tand']  = MATHFUNC
    ID['asind'] = MATHFUNC
    ID['acosd'] = MATHFUNC
    ID['atand'] = MATHFUNC
    ID['rt']    = MATHFUNC
    ID['ln']    = MATHFUNC
    ID['angle'] = MATHFUNC
    ID['abs']   = MATHFUNC
    ID['polar'] = POLAR
    ID['then']  = THEN
    ID['calc']  = CALC
    ID['gg']    = EXIT
    ID['vars']  = VARS
    ID['new']   = NEW

    NUMBER      = r'([0-9]*[.])?[0-9]+(e\-?[0-9]+)?'

    PLUS        = r'\+'
    MINUS       = r'-'
    TIMES       = r'\*'
    DIV         = r'/'
    POW         = r'\^'
    LPAREN      = r'\('
    RPAREN      = r'\)'
    ASSIGN      = r'='
    NEWLINE     = r'\n'
    TICK        = r"'"
    SEMI        = r';'

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1