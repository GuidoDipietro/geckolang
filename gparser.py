from math import sin, cos, tan, asin, acos, atan, degrees, radians, sqrt
from pprint import pprint
from sly import Parser
from glexer import GeckoLexer
from colorama import init
from termcolor import colored

class GeckoParser(Parser):
    # debugfile = 'parser.out'

    tokens = GeckoLexer.tokens

    precedence = (
        ('right', ASSIGN),
        ('left', THEN),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIV),
        ('right', MATHFUNC, UMINUS, CONSTANT),
        ('right', POW)
    )

    mathfuncs = {
        "sin": sin,
        "cos": cos,
        "tan": tan,
        "asin": asin,
        "acos": acos,
        "atan": atan,
        "sind": lambda x: sin(radians(x)),
        "cosd": lambda x: cos(radians(x)),
        "tand": lambda x: tan(radians(x)),
        "asind": lambda x: degrees(asin(x)),
        "acosd": lambda x: degrees(acos(x)),
        "atand": lambda x: degrees(atan(x)),
        "rt": lambda x: sqrt(x),
        "ln": lambda x: log(x)
    }

    binops = {
        '+': lambda x,y: x+y,
        '-': lambda x,y: x-y,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x/y,
        '^': lambda x,y: x**y
    }

    def __init__(self):
        self.ids = {}
        self.printed_ids = []

    ## utils ##

    # Print number in scientific notation if you shall
    def bigint(self, val):
        if len(str(val))>6:
            return f'{val:.2e}'
        return val
    # Round dem floats
    def pprint_int(self, val):
        return self.bigint(int(val) if val%1==0 else round(val,3))
    # Print final in cyan n stuff
    def pprint_final(self, _id, val):
        print(f"{colored('Final ','cyan')} {_id} = {self.pprint_int(val)}")
    # Print using in ???
    def pprint_using(self, _id, val):
        print(f"{colored('using ','magenta')} {_id} = {self.pprint_int(val)}")

    # Evaluate AST
    def eval_tree(self, tree, ctx=None):
        # print(f"Printed ids: {self.printed_ids}")
        op = tree[0]
        # ('tree', root)
        if op=='tree':
            return self.eval_tree(tree[1],ctx=ctx)
        # ('number', float)
        elif op=='number':
            return tree[1]
        # ('id-lookup', id)
        elif op=='id-lookup':
            try:
                # Si hay ctx son variables de scope
                # ej: 5+4 then x'rt(x)' -> la x guarda el valor de 5+4
                if ctx and tree[1] in ctx.keys():
                    val = ctx[tree[1]]
                else:
                    val = self.ids[tree[1]][1]

                if (ctx is None or len(ctx)==0):
                    if not tree[1] in self.printed_ids:
                        self.pprint_using(tree[1], val)
                        self.printed_ids += [tree[1]]
                else:
                    if tree[1] not in ctx.keys() and not tree[1] in self.printed_ids:
                        self.pprint_using(tree[1], val)
                        self.printed_ids += [tree[1]]
                return val
            except:
                print(f"Invalid ID {tree[1]}. Computed as 0.")
                return 0
        # ('group',expr)
        elif op=='group':
            return self.eval_tree(tree[1],ctx=ctx)
        # ('mathfunc', funcname, arg)
        elif op=='mathfunc':
            return self.mathfuncs[tree[1]](self.eval_tree(tree[2],ctx=ctx))
        # ('binop', op, arg1, arg2)
        elif op=='binop':
            return self.binops[tree[1]](self.eval_tree(tree[2],ctx=ctx), self.eval_tree(tree[3],ctx=ctx))
        # ('lambda', prev_exp, exp)
        elif op=='lambda':
            return self.eval_tree(tree[2], ctx = {'x': self.eval_tree(tree[1],ctx=ctx)})
        # ('lambda-x', temp_var, prev_exp, exp)
        elif op=='lambda-x':
            return self.eval_tree(tree[3], ctx = {tree[1]: self.eval_tree(tree[2],ctx=ctx)})
        else:
            print("Error.")
            return None

    ####### Grammar #######

    # yadda yadda root and recursion
    @_('statements','')
    def root(self, p):
        ...
    @_('statements NEWLINE statement')
    def statements(self, p):
        pass
    @_('statements SEMI statement')
    def statements(self, p):
        pass
    @_('statement')
    def statements(self, p):
        self.printed_ids = []

    ### STATEMENT ###

    @_('EXIT')
    def statement(self, p):
        exit()

    @_('expr')
    def statement(self, p):
        # print(p.expr) # cheap debug xd
        print(f"Result: {self.pprint_int(self.eval_tree(('tree',p.expr)))}")

    @_('CALC ID')
    def statement(self, p):
        tree = self.ids[p.ID][0]
        self.ids[p.ID][1] = self.eval_tree(tree)
        self.pprint_final(p.ID, self.ids[p.ID][1])

    @_('VARS')
    def statement(self, p):
        print(colored('Vars:','white',attrs=['bold']))
        for var in self.ids.keys():
            print(f"{var} = {self.pprint_int(self.ids[var][1])}")

    ### EXPR ###

    @_( 'expr PLUS expr',
        'expr MINUS expr',
        'expr TIMES expr',
        'expr DIV expr',
        'expr POW expr')
    def expr(self, p):
        return ('binop',p[1],p.expr0,p.expr1)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return ('binop','-',('number',0),p.expr)

    @_('NUMBER ID %prec CONSTANT')
    def expr(self, p):
        return ('binop','*',('number',float(p.NUMBER)),('id-lookup',p.ID))

    @_('MATHFUNC expr')
    def expr(self, p):
        return ('mathfunc',p.MATHFUNC,p.expr)

    @_('LPAREN expr RPAREN')
    def expr(self, p):
        return ('group',p.expr)

    @_('NUMBER')
    def expr(self, p):
        return ('number',float(p.NUMBER))

    @_('ID')
    def expr(self, p):
        return ('id-lookup',p.ID)

    @_('ID ASSIGN expr')
    def expr(self, p):
        self.printed_ids = []
        self.ids[p.ID] = [p.expr, self.eval_tree(p.expr)]
        self.pprint_final(p.ID, self.ids[p.ID][1])
        return p.expr

    @_('expr THEN TICK ID expr TICK')
    def expr(self, p):
        # I want to actually use x as my var
        return ('lambda-x',p.ID,p.expr0,p.expr1)

    @_('expr THEN expr')
    def expr(self, p):
        return ('lambda',p.expr0,p.expr1)

# Utils for INIT #

g = lambda x: colored(x, 'green')
def REPL():
    gecko ="\n"+\
g(r"                       )/_         ")+"""|\n"""+\
g(r'             _.--..---"-,--c_      ')+"""|   Gecko REPL\n"""+\
g(r"        \L..'           ._O__)_    ")+"""|\n"""+\
g(r",-.     _.+  _  \..--( /           ")+"""|   Version 0.0.1 (2021-04)\n"""+\
g(r"  `\.-''__.-' \ (     \_           ")+"""|\n"""+\
g(r"    `'''       `\__   /\           ")+"""|   Made by Guido Dipietro\n"""+\
g(r"                ')                 ")+"""|\n"""

    print(gecko)

    while True:
        try:
            print(colored('\ngecko> ', 'yellow',attrs=['bold']), end='')
            text = input()
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))

##########################
########## MAIN ##########
##########################

if __name__ == '__main__':

    init() # Colorama stuff
    lexer = GeckoLexer()
    parser = GeckoParser()

    REPL()