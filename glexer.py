from sly import Lexer

class GeckoLexer(Lexer):
    tokens = {  ID, PLUS, MINUS, TIMES,
                DIV, POW, MOD, MATHFUNC, NUMBER,
                LPAREN, RPAREN, ASSIGN, THEN, WITH, POLAR, AT, DEGSYM,
                CALC, EXIT, NEWLINE, TICK, COMMA, PIPE,
                SEMI, VARS, NEW,
                INT, FROM, TO, CROCANTE, PLOT, AS, STRING, TITLE }

    ignore = ' \t'
    ignore_comment = r'/\*.*\*/'

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
    ID['with']  = WITH
    ID['calc']  = CALC
    ID['gg']    = EXIT
    ID['vars']  = VARS
    ID['new']   = NEW
    ID['int']   = INT
    ID['from']  = FROM
    ID['to']    = TO
    ID['plot']  = PLOT
    ID['as']    = AS

    NUMBER      = r'([0-9]*[.])?[0-9]+(e\-?[1-9][0-9]*)?'
    STRING      = r'("[^\"]*")'
    TITLE       = r'\#.*'

    PLUS        = r'\+'
    MINUS       = r'-'
    TIMES       = r'\*'
    DIV         = r'/'
    POW         = r'\^'
    MOD         = r'%'
    LPAREN      = r'\('
    RPAREN      = r'\)'
    ASSIGN      = r'='
    NEWLINE     = r'\n'
    TICK        = r"'"
    SEMI        = r';'
    COMMA       = r','
    PIPE        = r'\|'
    CROCANTE    = r'\$'
    AT          = r'@'
    DEGSYM      = r'<'

    def error(self, t):
        print("Illegal character '%s'" % t.value[0])
        self.index += 1