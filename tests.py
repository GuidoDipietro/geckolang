from gparser import GeckoParser
from glexer import GeckoLexer
from colorama import init
from termcolor import colored
import math
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
        ("-4+5^2*10/2-2* 2+2", -4+5**2*10/2-2* 2+2),
        ("x=10, -2x^3", -2000),
        ("x=10, (-2x)^3", (-20)**3),
        ("4+5", 9),
        ("a=b=c=d=e=f=g=1, a+b+c then x*(d+BEN) with BEN=(e+f)*(g+1);", 3*(1+4)),
        ("""   a=b=c=d=e=f=g=h=i=j=k=l=m=n=o=p=q=r=s=t=u=v=w=x=y=z=1
            a+b+c+d+e+f+g+h+i then x*(j+k+l+m+n+o+p+q+BEN) with BEN=(r+s)*(t+u)*(v+w)*(x+y)*z;""", 9*(8+2**3*(9+1))),
        ("""   a=b=c=d=e=f=g=h=i=j=k=l=m=n=o=p=q=r=s=t=u=v=w=x=y=z=1
            a+b+c+d+e+f+g+h+i then x*(j+k+l+m+n+o+p+q+BEN) with BEN=(r+s)*(t+u)*(v+w)*(1+y)*z;""", 9*(8+16)),
        ("_=__=___=____=_____=a, __/___+____/_____+(_+1)/(_+1), d = 14ans, d", 14),
        ("a=10, ----------a", 10),
        ("a=10, -(-a) then --x^2 then --rt(x)", 10),
        ("a=10, --a^2 then (--x^2) then (--x)^2 then --(-x^2)", -10**16),
        ("x=10, f(x,y)=x+y, f(2,3)", 5),
        ("x=10, f(x,y)=y then 's x+s', f(2,3)", 5),
        ("x=10, f(x,y)=y+c with c=0 then 's s+x';, f(2,3)", 5),
        ("x=10, f(x,y)=y+c with c=x;, f(2,3)", 5),
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
        ("x=10, d = a+b+x with a=2; b=3a; then x^2 then 's s+x', d", (2+6+10)**2+10),
        ("f(x,y)=x+y, f(15)", 0),
        ("f(x,y^2)=x+y", None),
        ("polar 3+2j", 3+2j),
        ("f(x) = -3j+rt(x), n1 = rt(-16) + 1j(rt(-9)), n2 = f(-4), n1*n2 then x^0.5", ((-3+4j)*(-1j))**0.5),
        ("r_p(a,b,c) = -b+rt(disc) then x/2a with disc=b^2-4a*c;, r_p(2,3,-5)",1),
        ("r_p(a,b,c) = -b+rt(disc) then x/2a with disc=b^2-4a*c;, r_p(1,0,1)",1j),
        ("f(x)=2x^2+1, g(x)=f(x) then 1/x^2+a with a=6;, int g(x) from 0 to 1;", 6.504422096094687),
        ("f(x) = sin(x)+1, int f(x) from -2pi to 0.5pi;", 1+(5*math.pi)/2),
        ("f(x)=2x, int f(x) from f(1) to f(f(f(2)));", 16*16 - 2*2),
        ("""   x=10, f(x)=x
            int f(x) from x-9 to (a with a=x;); + int f(x) from 0 to x/x;""", 50),
        ("""   x=10, f(x)=x
            int f(x) from x-9 to a with a=x;; + int f(x) from 0 to x/x;""", 50),
        ("f(x) = |x|, int f(x) from -10 to 10;", 100),
        ("f(x) = x, int f(x) from -10 to 10;", 0),
        ("wtf(x,y) = 2y + int e^x from x to 3;, wtf(1,2)", 21.367255094728623),
        ("x=10, int 1/x then 1/x from x with x=1; to x then x-8;", 3/2),
        ("x=10, int 0 then 's s+x' from 5 to 10;", 37.50000000000001), # my face
        ("a=10, int 0 then 's s+a' from 5 to 10;", 50),
    ]

    for (expr, val) in tests:
        # Parsing wrapped with a stdout redirect to prevent prints unless --echo flag
        if (len(sys.argv)>1 and sys.argv[1]=='--echo'):
            tree = parser.parse(lexer.tokenize("new,"+expr))
            comp = parser.eval_tree(tree) if tree else None
            # print(tree)
        else:
            old_stdout = sys.stdout
            sys.stdout = open(os.devnull, "w")
            tree = parser.parse(lexer.tokenize("new,"+expr))
            comp = parser.eval_tree(tree) if tree else None
            sys.stdout = old_stdout

        if comp == val:
            print(  f"{colored('PASSED','green')} [ {expr} ] == {colored(f'({val})','cyan')}\n")
        else:
            print(  f"{colored('FAILED','red')} [ {expr} ], {colored(f'EXPECTED ({val})','yellow')}"+
                    f", {colored(f'GOT ({comp})','red')}\n")
            failed += 1

    print("------------------------------------")
    if failed>0:
        print(f"{colored(f'FAILED: {failed}','red')} (out of {len(tests)})\n")
    else:
        print(colored(f"All {len(tests)} tests were successful.\n",'green'))