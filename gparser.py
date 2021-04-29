from math import sin, cos, tan, asin, acos, atan, degrees, radians, sqrt
from sly import Parser
from glexer import GeckoLexer
from colorama import init
from termcolor import colored

class GeckoParser(Parser):
    debugfile = 'parser.out'

    tokens = GeckoLexer.tokens

    precedence = (
        ('left', THEN),
        ('left', PLUS, MINUS),
        ('left', TIMES, DIV),
        ('right', UMINUS, MATHFUNC),
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


    # Evaluate AST
    def eval_tree(self, tree, prev=None):
        op = tree[0]
        # ('tree', root)
        if op=='tree':
            return self.eval_tree(tree[1],prev=prev)
        # ('number', float)
        elif op=='number':
            return tree[1]
        # ('id-lookup', id)
        elif op=='id-lookup':
            try:
                val = (prev if prev else self.ids[tree[1]][1])

                if (prev is None and not tree[1] in self.printed_ids):
                    print(f"{tree[1]} = {self.pprint_int(val)}")
                    self.printed_ids += [tree[1]]
                return val
            except:
                print(f"Invalid ID {tree[1]}.")
                return 0
        # ('group',expr)
        elif op=='group':
            return self.eval_tree(tree[1],prev=prev)
        # ('mathfunc', funcname, arg)
        elif op=='mathfunc':
            return self.mathfuncs[tree[1]](self.eval_tree(tree[2],prev=prev))
        # ('binop', op, arg1, arg2)
        elif op=='binop':
            return self.binops[tree[1]](self.eval_tree(tree[2],prev=prev), self.eval_tree(tree[3],prev=prev))
        # ('lambda', prev_exp, exp)
        elif op=='lambda':
            return self.eval_tree(tree[2], self.eval_tree(tree[1],prev=prev))
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
    @_('statement')
    def statements(self, p):
        pass

    ### STATEMENT ###

    @_('EXIT')
    def statement(self, p):
        exit()

    @_('expr')
    def statement(self, p):
        self.printed_ids = []
        # print(p.expr)
        print(f"Result: {self.pprint_int(self.eval_tree(('tree',p.expr)))}")

    @_('ID ASSIGN expr')
    def statement(self, p):
        self.printed_ids = []
        self.ids[p.ID] = [p.expr, self.eval_tree(p.expr)]
        self.pprint_final(p.ID, self.ids[p.ID][1])

    @_('CALC ID')
    def statement(self, p):
        self.printed_ids = []
        tree = self.ids[p.ID][0]
        self.ids[p.ID][1] = self.eval_tree(tree)
        self.pprint_final(p.ID, self.ids[p.ID][1])

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

    @_('expr THEN expr')
    def expr(self, p):
        return ('lambda',p.expr0,p.expr1)

if __name__ == '__main__':

    init() # Colorama stuff
    lexer = GeckoLexer()
    parser = GeckoParser()

    while True:
        try:
            print(colored('\ngecko> ', 'yellow',attrs=['bold']), end='')
            text = input()
        except EOFError:
            break
        if text:
            parser.parse(lexer.tokenize(text))