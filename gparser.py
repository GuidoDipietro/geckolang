# import readline # linux stuff. Will fix later
import math
from cmath import rect
import numpy as np
import matplotlib.pyplot as plt
from pprint import pprint
from sly import Parser
from glexer import GeckoLexer
from colorama import init
from termcolor import colored
from settings import *
from scipy.integrate import quad
from sys import exit

class GeckoParser(Parser):
    # debugfile = 'parser.out'

    tokens = GeckoLexer.tokens

    precedence = (
        ('right', CROCANTE),
        ('right', ASSIGN),
        ('left', INTEGRAL),
        ('left', THEN),
        ('left', WITH_EXPR),
        ('left', MONO_WITH_EXPR, COMMA),
        ('right', WITH_ASSIGNS),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIV, MOD),
        ('right', CONSTANT),
        ('right', MATHFUNC, UMINUS),
        ('right', POW),
        ('nonassoc', NUMBER),
        ('nonassoc', AT, DEGSYM),
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
        "angle": np.angle,
        "abs": abs,
        "deg": math.degrees,
        "rad": math.radians,
    }

    binops = {
        '+': lambda x,y: x+y,
        '-': lambda x,y: x-y,
        '*': lambda x,y: x*y,
        '/': lambda x,y: x/y,
        '^': lambda x,y: x**y,
        '%': lambda x,y: x%y,
    }

    def __init__(self):
        self.ids = {
            "pi": [('number',math.pi),math.pi],
            "e": [('number',math.e),math.e],
            "tau": [('number',math.tau),math.tau],
            "j": [('number',1j),1j]
        }
        self.funcs = {
            'j': (['x'], ('binop', '*', ('number', 1j), ('id-lookup', 'x')))
        }
        self.mathconsts = list(self.ids.keys())
        self.printed_ids = []
        self.ans = 0

    ## utils ##

    # Print number in scientific notation if you shall
    def scinum(self, val):
        if val==0: return 0
        if int(val)>999999 or int(val)<-999999 or abs(val)<0.001 or 'e' in str(val):
            return f'{val:.2e}'
        return round(val,4)
    # Round dem floats
    def pprint_num(self, val):
        if 'j' in str(val):
            if val.imag != 0:
                sign = '+' if val.imag>0 else '-'
                return f"{tab}{self.pprint_num(val.real)} {sign} {self.pprint_num(abs(val.imag))}j"
            val = val.real
        return self.scinum(int(val) if val%1==0 else val)
    # Print final in cyan n stuff
    def pprint_final(self, _id, val):
        print(f"{tab}{colored('Final',FINAL_COLOR,attrs=['bold'])} {_id} = {self.pprint_num(val)}")
    # Print using in magenta
    def pprint_using(self, _id, val):
        if (not (_id=="j" and val==1j) ):
            print(f"{tab}{colored('using',USING_COLOR)} {_id} = {self.pprint_num(val)}")

    # Evaluate AST
    def eval_tree(self, tree, ctx=None):
        op = tree[0]
        # ('tree', root)
        if op=='tree':
            return self.eval_tree(tree[1],ctx=ctx)
        # ('number', float)
        elif op=='number':
            return tree[1]
        # ('id-lookup', id)
        elif op=='id-lookup':
            if (tree[1]=='ans'):
                print(tab + colored('ans',ANS_COLOR) + f" = {self.ans}")
                return self.ans
            try:
                # scope variables in 'ctx'
                # ex: 5+4 then 'a rt(a)' -> a stores 5+4
                # ex: 5+4 then rt(x) -> x stores 5+4
                # By default, x is the lambda variable.
                # 'ID expr' defines another one if x is a global variable
                if ctx and tree[1] in ctx.keys():
                    try:
                        # Unevaluated 'with_assign'
                        val = self.eval_tree(ctx[tree[1]], ctx=ctx)
                    except:
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
                print(f"{tab}{colored('Invalid ID',INVALID_COLOR)} {tree[1]}")
                return 0
        # ('group',expr)
        elif op=='group':
            return self.eval_tree(tree[1],ctx=ctx)
        # ('mathfunc', funcname, arg)
        elif op=='mathfunc':
            func, val = tree[1], self.eval_tree(tree[2],ctx=ctx)
            try:
                if func=='rt' and val<0:
                    return math.sqrt(-val)*1j
                return self.mathfuncs[func](val)
            except:
                print(f"{tab}Function {func} domain error (used val = {val})")
                return 0
        # ('binop', op, arg1, arg2)
        elif op=='binop':
            try:
                return self.binops[tree[1]](self.eval_tree(tree[2],ctx=ctx), self.eval_tree(tree[3],ctx=ctx))
            except:
                print(f"{tab}Math error")
                return 0
        # ('lambda', prev_exp, exp)
        elif op=='lambda':
            if ctx:
                return self.eval_tree(tree[2], ctx = {**ctx, 'x': self.eval_tree(tree[1],ctx=ctx)})
            return self.eval_tree(tree[2], ctx = {'x': self.eval_tree(tree[1],ctx=ctx)})
        # ('lambda-x', temp_var, prev_exp, exp)
        elif op=='lambda-x':
            if ctx:
                return self.eval_tree(tree[3], ctx = {**ctx, tree[1]: self.eval_tree(tree[2],ctx=ctx)})
            return self.eval_tree(tree[3], ctx = {tree[1]: self.eval_tree(tree[2],ctx=ctx)})
        # ('with-expr', expr, immediate_context)
        elif op=='with-expr':
            if ctx:
                return self.eval_tree(tree[1], ctx = {**ctx, **tree[2]})
            return self.eval_tree(tree[1], ctx = tree[2])
        # ('func-call', ID, [exprs]), self.funcs = { 'hypot': (['x','y'], expr) }
        elif op=='func-call':
            if tree[1] not in self.funcs.keys():
                print(tab+colored(f"Function \"{tree[1]}\" doesn't exist",INVALID_COLOR))
                return 0
            func_args, func_expr = self.funcs[tree[1]]
            # Wrong call, too many/few args
            if len(func_args) != len(tree[2]):
                print(tab + colored('Wrong function call, for',INVALID_COLOR))
                print(2*tab + colored(f'{tree[1]}({",".join(func_args)})',FUNC_ERR_COLOR))
                return 0
            # Actual work done here
            func_ctx = {}
            for _id,expr in zip(func_args, tree[2]):
                func_ctx[_id] = self.eval_tree(expr, ctx=ctx)
            return self.eval_tree(func_expr, ctx = func_ctx)
        # ('integrate', tree, x0, x1)
        elif op=='integrate':
            func = self.tree_to_scalar_function(tree[1], ctx)
            x0 = self.eval_tree(tree[2], ctx)
            x1 = self.eval_tree(tree[3], ctx)
            return quad(func, x0, x1)[0]
        else:
            print(f"{tab}Error.")
            return 0

    def tree_to_scalar_function(self, tree, ctx=None):
        func = lambda x: self.eval_tree(tree, ctx={**ctx,'x': x} if ctx else {'x': x})
        return func

    ####### Grammar #######

    # yadda yadda root and recursion

    @_( 'statements NEWLINE statement',
        'statements SEMI statement')
    def statements(self, p):
        return p.statement

    @_('statement')
    def statements(self, p):
        self.printed_ids = []
        return p.statement

    ### Structural rules stuff (kinda in-between non-terminals for other non-terminals)

    ## Functions stuff ## for definitions and calls
        # FUNC_NAME ( ARGS ) -> just that
        # args are 'exprs' because this is used both for
        # function definitions and for function calls
    @_('ID LPAREN exprs expr RPAREN')
    def func_shape(self, p):
        return p.ID, [*p.exprs, p.expr]
    @_('ID LPAREN expr RPAREN')
    def func_shape(self, p):
        return p.ID, [p.expr]
    @_('expr COMMA')
    def exprs(self, p):
        return [p.expr]
    @_('exprs expr COMMA')
    def exprs(self, p):
        return [*p.exprs, p.expr]

    ## ID assignment (left hand of assignments: id=, id=id=id=, etc)
    @_('ID ASSIGN')
    def ids_assign(self, p):
        return [p.ID]
    @_('ids_assign ID ASSIGN')
    def ids_assign(self, p):
        if p.ID not in p.ids_assign:
            return [*p.ids_assign, p.ID]
        return p.ids_assign

    ### STATEMENT ###

    @_('EXIT')
    def statement(self, p):
        exit()

    @_('TITLE')
    def statement(self, p):
        # Reserved for future use
        ...

    @_('expr', 'expr TITLE')
    def statement(self, p):
        # print(p.expr) # cheap debug xd
        if p.expr[0] in ['nop']: pass
        else:
            self.ans = self.eval_tree(('tree',p.expr))
            print(f"{tab}{self.pprint_num(self.ans)}")

        # return self.eval_tree(('tree',p.expr))
        return p.expr

    # ben=14, a=b=c=3, no return value, this isnt an expression!
    @_('ids_assign expr')
    def statement(self, p):
        for _id in p.ids_assign:
            if (_id=='ans'):
                print(tab + colored('Invalid ID',INVALID_COLOR)+" ans")
                return ('assign',self.ans)
            if (_id in self.mathconsts):
                self.mathconsts.remove(_id)
            self.printed_ids = []
            self.ids[_id] = [p.expr, self.eval_tree(p.expr)]
            self.pprint_final(_id, self.ids[_id][1])

    # Function declaration/definition
    @_('func_shape ASSIGN expr')
    def statement(self, p):
        # Couldn't find another solution, since IDs are expressions...
        # Conflicts with function calls otherwise
        name, args = p.func_shape
        for arg in args:
            if arg[0]!='id-lookup': # f(a,14) = a+2
                print(tab + colored('Invalid arguments in function definition',INVALID_COLOR))
                return
        if len(set(args)) != len(args): # f(a,a)=2
            print(tab + colored('Invalid arguments in function definition',INVALID_COLOR))
        else:
            self.funcs[name] = ([x[1] for x in args], p.expr)

    @_('CALC ID')
    def statement(self, p):
        if (p.ID not in self.ids.keys()):
            print(tab + colored(f"Can't recalculate non-existing id ", INVALID_COLOR) + p.ID)
        else:
            tree = self.ids[p.ID][0]
            self.ids[p.ID][1] = self.eval_tree(tree)
            self.pprint_final(p.ID, self.ids[p.ID][1])

    @_( 'POLAR expr',
        'expr POLAR')
    def statement(self, p):
        num = self.eval_tree(p.expr)
        self.ans = num
        if num.imag == 0:
            print(self.pprint_num(num))
        else:
            norm = colored(self.pprint_num(abs(num)),'white',attrs=['bold'])
            phase = colored(f'{self.pprint_num(np.angle(num))} rad','white',attrs=['bold'])
            phase_deg = self.pprint_num(math.degrees(np.angle(num)))
            print(f"{tab}{norm} {colored('@','green')} {phase} ({phase_deg} deg)")
        return p.expr

    @_( 'PLOT expr FROM expr TO expr',
        'PLOT expr FROM expr TO expr AS ID',
        'PLOT expr FROM expr TO expr AS STRING')
    def statement(self, p):
        func = self.tree_to_scalar_function(p.expr0)
        start, stop = self.eval_tree(p.expr1), self.eval_tree(p.expr2)
        x_axis = np.linspace(start=start, stop=stop, num=200)

        plt.figure()
        plt.xlabel("x")
        plt.ylabel("y")
        try: #lol
            try:
                plt.title(p.ID)
            except:
                plt.title(p.STRING[1:-1])
        except:
            ...
        plt.plot(x_axis, np.array([func(x) for x in x_axis]))
        plt.grid()
        plt.ion()
        plt.show()

    @_('VARS')
    def statement(self, p):
        if (len(self.ids)>0) and not (len(self.mathconsts)==len(self.ids)):
            print(tab + colored('Vars:','white',attrs=['bold']))
            # Longest ID + escape sequences for color + 1
            padding = len(max(self.ids.keys(), key=len))+8+1
            for var in sorted(self.ids.keys()):
                if var not in self.mathconsts:
                    print(f"{tab*2}{colored(var,VAR_COLOR):{padding}} = {self.pprint_num(self.ids[var][1])}")
        else:
            print(tab + colored('No initialized variables','white',attrs=['bold']))

    # Deletes all variables
    @_('NEW')
    def statement(self, p):
        self.__init__()

    ### EXPR ###
    # Everything that can be evaluated. Upon any error evaluates to 0.

    @_( 'expr PLUS expr',
        'expr MINUS expr',
        'expr TIMES expr',
        'expr DIV expr',
        'expr POW expr',
        'expr MOD expr')
    def expr(self, p):
        return ('binop',p[1],p.expr0,p.expr1)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return ('binop','-',('number',0),p.expr)

    @_('NUMBER')
    def expr(self, p):
        return ('number', float(p.NUMBER))

    @_('NUMBER AT expr')
    def expr(self, p):
        return ('number', rect(float(p.NUMBER), self.eval_tree(p.expr)))

    @_('NUMBER AT DEGSYM expr')
    def expr(self, p):
        return ('number', rect(float(p.NUMBER), math.radians(self.eval_tree(p.expr))))

    @_('mini_term')
    def expr(self, p):
        return p.mini_term

    @_('PIPE expr PIPE')
    def expr(self, p):
        return ('mathfunc', 'abs', p.expr)

    @_('expr THEN expr')
    def expr(self, p):
        return ('lambda',p.expr0,p.expr1)

    @_('expr THEN TICK ID expr TICK')
    def expr(self, p):
        # Here I want to actually use x as a global var
        # x=10, var = rt(4) then 's s+x' -> var = 12
        return ('lambda-x',p.ID,p.expr0,p.expr1)

    @_('INT expr FROM expr TO expr %prec INTEGRAL')
    def expr(self, p):
        return ('integrate', p.expr0, p.expr1, p.expr2)

    # good ol' haskell curry
    # $ CROCANTE operator reduces the expression no matter what it is
    @_('expr CROCANTE')
    def expr(self, p):
        # 1+2 $ * 3 -> 9
        return p.expr

    # expr WITH stuff (5+15a*b^2 with a=sin(4)^2)
    @_('mono_with_expr %prec WITH_EXPR')
    def expr(self, p):
        return p.mono_with_expr

    # expr WITH stuffs (5+15a*b^2 with a=sin(4)^2, b=2pi)
    @_('mono_with_expr with_assigns %prec WITH_EXPR')
    def expr(self, p):
        _, expr0, _dict = p.mono_with_expr
        return ('with-expr', expr0, {**_dict, **p.with_assigns})

    ### WITH expression non-terminals - it gets a bit messy here
    # I really couldn't figure out another way to supress grammar conflicts, even though the parser was working swell with them

    ## mono_with_expr (base WITH expression)
    @_('expr WITH ID ASSIGN expr %prec MONO_WITH_EXPR')
    def mono_with_expr(self, p):
        return ('with-expr', p.expr0, {p.ID: p.expr1})

    ## with_assigns (different from regular assigns)
    # These assignments are temporal and are not stored as vars
    # They look 'identical' to regular assigns, but these belong to WITH expressions
    # only, and they actually begin with a comma (grammar tricks, I guess)
    @_('COMMA ids_assign expr %prec WITH_ASSIGNS')
    def with_assigns(self, p):
        return {_id: p.expr for _id in p.ids_assign}
    @_('with_assigns COMMA ids_assign expr %prec WITH_ASSIGNS')
    def with_assigns(self, p):
        new_dict = {_id: p.expr for _id in p.ids_assign}
        return {**p.with_assigns, **new_dict}

    ### mini_term
    # not a boolean miniterm. This is my own mini_term.
    # These allow constant pre-pending as implicit multiplication (4x^2, 5sin(2))
    # Implicit product with this rule takes precedence over TIMES, DIV, PLUS, MINUS

    @_('ID')
    def mini_term(self, p):
        return ('id-lookup',p.ID)

    @_('NUMBER mini_term %prec CONSTANT')
    def mini_term(self, p):
        # Regular ol' NUMBER mini_term 5x type of thing
        return ('binop','*',('number',float(p.NUMBER)),p.mini_term)

    @_('LPAREN expr RPAREN mini_term %prec CONSTANT')
    def mini_term(self, p):
        return ('binop','*',p.expr,p.mini_term)

    @_('NUMBER mini_term POW expr')
    def mini_term(self, p):
        return ('binop','*',('number',float(p.NUMBER)),('binop','^',p.mini_term,p.expr))

    @_('LPAREN expr RPAREN mini_term POW expr')
    def mini_term(self, p):
        return ('binop','*',p.expr0,('binop','^',p.mini_term,p.expr1))

    @_('MATHFUNC LPAREN expr RPAREN')
    def mini_term(self, p):
        return ('mathfunc',p.MATHFUNC,p.expr)

    @_('func_shape')
    def mini_term(self, p):
        name, args = p.func_shape
        return ('func-call', name, args)

    @_('LPAREN expr RPAREN')
    def mini_term(self, p):
        return ('group',p.expr)

########## END OF PARSER CLASS ##########

# Utils for INIT #

g = lambda x: colored(x, 'green')
b = lambda x: colored(x, 'white', attrs=['bold'])
pipe = colored('|','red')

def REPL(lexer, parser):
    # Credits to ANDREAS FREISE (whoever you are) for the ASCII gecko
    gecko ="\n"+\
g(r"                       )/_         ")+pipe+"""\n"""+\
g(r'             _.--..---"-,--c_      ')+pipe+"""   https://github.com/GuidoDipietro/geckolang\n"""+\
g(r"        \L..'           ._O__)_    ")+pipe+"""\n"""+\
g(r",-.     _.+  _  \..--( /           ")+pipe+"""   """+b('Gecko REPL')+""" - v0.1.0 (2021-08)\n"""+\
g(r"  `\.-''__.-' \ (     \_           ")+pipe+"""\n"""+\
g(r"    `'''       `\__   /\           ")+pipe+"""   Made by Guido Dipietro - Artwork by Andreas Freise\n"""+\
g(r"                ')                 ")+pipe+"""\n"""

    print(gecko)

    while True:
        try:
            print(colored('\ngecko> ', 'yellow',attrs=['bold']), end='')
            text = input()
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))
