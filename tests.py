from gparser import GeckoParser
from glexer import GeckoLexer
from colorama import init
from termcolor import colored
import sys
import os

if __name__ == "__main__":

    print("\n---------- RUNNING TESTS -----------\n\n")

    failed = 0

    init() # Colorama stuff
    lexer = GeckoLexer()
    parser = GeckoParser()

    tests = [
        # Last expression is called twice, keep in mind if you're testing 'ans' stuff
        ("4+5", 9),
        ("a=b=2, d=-2a^2+5b, ans", 0),
        ("a=b=2, d=-2a^2+5b, d, 10ans, ans", 10*(-2*4+10)),
        ("x=10, d=a+x with a=6;, d", 16),
        ("3+a with a=12; then 1/x", 1/15),
        ("f(x,y)=x+y, f(2,3)", 5),
        ("""   sum(x,y)=x+y
            sub(x,y) = x - y
            diff(x,y)=sum(x,y) * sub ( x ,y)
            diff(14,27)""", 14**2 - 27**2),
        ("d=1+a, a=14, calc d, d", 15),
        ("""   n1 = 5+4j
            n2 = rt(-16)
            final = n1 * n2 then x^2
            final""", ((5+4j)*(4j))**2),
        ("a=2, result = 10a+b with b=3; then rt(x), result", 23**0.5),
        ("a", 0),
        ("f(x,y) = x + 2^x, f(2, -135)", 2+2**2),
        ("""   f(x,y)=x+y
            f(1+s with s=22; then rt(x),   5)""", 23**0.5+5),
        ("sum(x,y)=x+y, sum=15, sum(sum,sum(sum,sum))", 15+(15+15)), # what??
    ]

    for (expr, val) in tests:
        # Parsing wrapped with a stdout redirect to prevent prints unless --echo flag
        if (len(sys.argv)>1 and sys.argv[1]=='--echo'):
            tree = parser.parse(lexer.tokenize("new,"+expr))
            comp = parser.eval_tree(tree)
            print(tree)
        else:
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, "w")
            tree = parser.parse(lexer.tokenize("new,"+expr))
            comp = parser.eval_tree(tree)
            sys.stdout = old_stdout

        if comp == val:
            print(f"{colored('PASSED','green')} [ {expr} ] == {colored(f'({val})','cyan')}\n")
        else:
            print(  f"{colored('FAILED','red')} [ {expr} ], {colored(f'EXPECTED ({val})','yellow')}"+
                    f", {colored(f'GOT ({comp})','red')}\n")
            failed += 1

    print("------------------------------------")
    if failed>0:
        print(f"{colored(f'FAILED: {failed}','red')} (out of {len(tests)})\n")
    else:
        print(colored("All tests were successful.\n",'green'))