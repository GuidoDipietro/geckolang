import math
from numpy import angle
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
        "sin": math.sin,
        "cos": math.cos,
        "tan": math.tan,
        "asin": math.asin,
        "acos": math.acos,
        "atan": math.atan,
        "sind": lambda x: math.sin(math.radians(x)),
        "cosd": lambda x: math.cos(math.radians(x)),
        "tand": lambda x: math.tan(math.radians(x)),
        "asind": lambda x: math.degrees(math.asin(x)),
        "acosd": lambda x: math.degrees(math.acos(x)),
        "atand": lambda x: math.degrees(math.atan(x)),
        "rt": math.sqrt,
        "ln": math.log,
        "angle": angle,
        "abs": abs,
        "deg": math.degrees,
        "rad": math.radians
    }

    binops = {
        '+': lambda x,y: x+y,
        '-': lambda x,y: x-y,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x/y,
        '^': lambda x,y: x**y
    }

    def __init__(self):
        self.ids = {
            "pi": [('number',math.pi),math.pi],
            "e": [('number',math.e),math.e],
            "tau": [('number',math.tau),math.tau]
        }
        self.mathconsts = ["pi","e","tau"]
        self.printed_ids = []
        self.ans = 0

    ## utils ##

    # Print number in scientific notation if you shall
    def scinum(self, val):
        if int(val)>999999 or int(val)<-999999 or 'e' in str(val):
            return f'{val:.2e}'
        return round(val,3)
    # Round dem floats
    def pprint_num(self, val):
        if 'j' in str(val):
            if val.imag != 0:
                sign = '+' if val.imag>0 else '-'
                return f"{self.pprint_num(val.real)} {sign} {self.pprint_num(abs(val.imag))}j"
            val = val.real
        return self.scinum(int(val) if val%1==0 else val)
    # Print final in cyan n stuff
    def pprint_final(self, _id, val):
        print(f"{colored('Final ','cyan',attrs=['bold'])} {_id} = {self.pprint_num(val)}")
    # Print using in magenta
    def pprint_using(self, _id, val):
        print(f"{colored('using ','magenta')} {_id} = {self.pprint_num(val)}")

    # Evaluate AST
    def eval_tree(self, tree, ctx=None):
        op = tree[0]
        # ('tree', root)
        # ('assign', thing)
        if op=='tree' or op=='assign':
            return self.eval_tree(tree[1],ctx=ctx)
        # ('number', float)
        elif op=='number':
            return tree[1]
        # ('id-lookup', id)
        elif op=='id-lookup':
            if (tree[1]=='ans'):
                print(colored('ans','cyan') + f" = {self.ans}")
                return self.ans
            try:
                # scope variables in 'ctx'
                # ex: 5+4 then 'a rt(a)' -> a stores 5+4
                # ex: 5+4 then rt(x) -> x stores 5+4
                # By default, x is the lambda variable.
                # 'ID expr' defines another one if x is a global variable
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
                print(f"{colored('Invalid ID','red')} {tree[1]}")
                return 0
        # ('group',expr)
        elif op=='group':
            return self.eval_tree(tree[1],ctx=ctx)
        # ('mathfunc', funcname, arg)
        elif op=='mathfunc':
            func, val = tree[1], self.eval_tree(tree[2],ctx=ctx)
            try:
                return self.mathfuncs[func](val)
            except:
                print(f"Function {func} domain error (used val = {val})")
                return 0
        # ('binop', op, arg1, arg2)
        elif op=='binop':
            try:
                return self.binops[tree[1]](self.eval_tree(tree[2],ctx=ctx), self.eval_tree(tree[3],ctx=ctx))
            except:
                print("Error: division by zero")
                return 0
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
        if p.expr[0] in ['assign','nop']: pass
        else:
            self.ans = self.eval_tree(('tree',p.expr))
            print(f"{self.pprint_num(self.ans)}")

    @_('CALC ID')
    def statement(self, p):
        tree = self.ids[p.ID][0]
        self.ids[p.ID][1] = self.eval_tree(tree)
        self.pprint_final(p.ID, self.ids[p.ID][1])

    @_( 'POLAR expr',
        'expr POLAR')
    def statement(self, p):
        num = self.eval_tree(p.expr)
        if num.imag == 0:
            print(self.pprint_num(num))
        else:
            norm = colored(self.pprint_num(abs(num)),'white',attrs=['bold'])
            phase = colored(f'{self.pprint_num(angle(num))} rad','white',attrs=['bold'])
            phase_deg = self.pprint_num(math.degrees(angle(num)))
            print(f"{norm} {colored('@','green')} {phase} ({phase_deg} deg)")

    @_('VARS')
    def statement(self, p):
        if (len(self.ids)>0) and not (len(self.mathconsts)==len(self.ids)):
            print(colored('Vars:','white',attrs=['bold']))
            # Longest ID + escape sequences for color + 1
            padding = len(max(self.ids.keys(), key=len))+8+1
            for var in self.ids.keys():
                if var not in self.mathconsts:
                    print(f"{colored(var,'red'):{padding}} = {self.pprint_num(self.ids[var][1])}")
        else:
            print(colored('No initialized variables','white',attrs=['bold']))

    # Deletes all variables
    @_('NEW')
    def statement(self, p):
        self.__init__()

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
        if p.ID=='j':
            return ('number',complex(p.NUMBER+"j"))
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
        if (p.ID=='ans'):
            print(colored('Invalid ID','red')+" ans")
            return ('assign',self.ans)
        if (p.ID in self.mathconsts):
            self.mathconsts.remove(p.ID)
        self.printed_ids = []
        self.ids[p.ID] = [p.expr, self.eval_tree(p.expr)]
        self.pprint_final(p.ID, self.ids[p.ID][1])
        return ('assign',p.expr)

    @_('expr THEN TICK ID expr TICK')
    def expr(self, p):
        # I want to actually use x as a global var
        return ('lambda-x',p.ID,p.expr0,p.expr1)

    @_('expr THEN expr')
    def expr(self, p):
        return ('lambda',p.expr0,p.expr1)

# Utils for INIT #

g = lambda x: colored(x, 'green')
def REPL():
    # Credits to ANDREAS FREISE (whoever you are) for the ASCII gecko
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