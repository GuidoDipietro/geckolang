# Gecko

![REPL intro image](img/intro.PNG)

An interactive REPL devised for quickly getting calculations done.

# Features

<!-- Clean expr syntax -->
### Clean expression syntax
![Clean Syntax example 1](img/clean_syntax_1.PNG)  

<!-- Straightforward piping for verbose expressions -->
### Straightforward piping for intricate expressions
![Piping example 1](img/piping_1.PNG)  
![Piping example 2](img/piping_2.PNG)  
![Piping example 3](img/piping_3.PNG)  

<!-- Built-in math functions -->
### Built-in math functions and constants
![Builtin math example 1](img/builtin_math_1.PNG)  

<!-- Complex numbers -->
### Complex numbers support
![Complex numbers example 1](img/complex_1.PNG)  

<!-- ans -->
### Ans feature
![Ans example 1](img/ans_1.PNG)  

<!-- Calc command -->
### Calc command
![Calc example 1](img/calc_1.PNG)  
![Calc example 2](img/calc_2.PNG)  

<!-- Var dump -->
### Var dump
![Var dump example 1](img/vars_1.PNG)  

### Expression reducer operator
![Haskell-like $ operator](img/crocante.PNG)

<!-- One-line function definitions -->
### Functions
![Fuctions 1](img/funcs_1.PNG)  
![Fuctions 2](img/funcs_2.PNG)  
![Fuctions 3](img/funcs_3.PNG)  
![Fuctions 4](img/funcs_4.PNG)  

<!-- ONE LINE INTEGRATION -->
### Integrals
![Integrals 1](img/integral_1.PNG)  
![Integrals 2](img/integral_2.PNG)  
![Integrals 3](img/integral_3.PNG)  
![Integrals 4](img/integral_4.PNG)  

<!-- PLOTTING -->
![Plots 1](img/plot_1.PNG)  
![Plots 2](img/plot_2.PNG)  

# Gecko REPL feature description

*"Let's break Gecko"*, they said.

---

Sentences are the big 'blocks' that make up _Gecko_.  
They are like commands that you enter to the REPL for _Gecko_ to eat.  
Multiple sentences are separated by comma or by newline.  

Everything _Gecko_ understands is the following:

## Sentences
- Any valid *expression* **(see next section)**
- *Variable assignments*
    - `a=5` -> **a=5**
    - `n1=n2=n3=15` -> **n1=15, n2=15, n3=15**
    - `value = 2*3 + 1` -> **value = 7**
- *Function definition*
    - `f(x,y) = x+y`
    - `g(x,y) = 2f(x,y)`
- *`calc` command*
    - `a=2, d=10a, a=5, calc d` -> **d = 50**
- *`polar` command*
    - `d=5+3j, polar d`, or
    - `d=5+3j, d polar`
    - Output: `5.831 @ 0.5404 rad (30.9638 deg)`
- *`vars` command* shows all assigned global variables and its values
- *`new` command* resets all variables and functions

## Expressions

Valid expressions plus some examples of 'real-life' usage:

- *Numbers*
    - Regular numbers: `-3`, `14.27`, `0.2`, `.001`
    - Scientific notation: `3e4`, `-2e-10`, `.02e3`
    - Complex numbers: `4+2j`, `-0.3j + 3`, `rt(-16)+1`
- *IDs*
    - Made from any combination of letters, numbers, and `_`, starting with a non-number. They can store a value, just like variables do in most programming languages (or any?)
    - `value, var1, total_result, n1, _1st_attempt`, etc.
- *Common binary operations:*
    - `+ - * / ^`, as in `5+3`, `0.2^3`
- *Unary minus*: `a=2, result = -a` -> **result = -2**
- *Built-in math functions and constants*
    - `sin, cos, tan`
        - inverse function by prepending `a-` (as in `asin`)
        - use degrees by appending `-d` (as in `tand`, `acosd`, etc.)
    - `ln rt angle abs deg rad` + `pi e tau` reassignable constants
        - **Bonus:** shorthand for `abs(x)` is `|x|`
- *Constant with implicit multiplication*
    - `2x`, `5sin(4)`, `0.5(2+3)`, `6x^3`, etc.
- *`with` expression* **(assignments end in `;`)**
    - `2+a with a = 0.1;` -> **2.1**
    - `2alpha+gamma with alpha=6; gamma=2;` -> **14**
    - **Temporary variables assigned in `with` statements are not stored!**
- *`then` expression*
    - `3^2+4^2 then rt(x)` -> **5**
    - `x = 10, result = 14-2^2 then 'var x/var'` -> **result = 1** (`var` could be replaced by any other valid ID)
- *Function calls*
    - `sum(x,y)=x+y, sum(5,6)` -> **11**
    - `mult(x,y)=x*y, square(x) = mult(x,x), square(10)` -> **100**
    - `double(x)=2x, double(double(3))` -> **12**
    - The **variables** and **functions** namespace is disjoint, meaning you can have a variable called `sum` with a value of `69`, and also a function called `sum` doing something else, with **no problems at all.**
- *Special `ans` ID*, stores last printed value or 0
    - `a=10` -> **ans = 0**
    - `a=10, 15a` -> **ans = 150**
    - `sin(4^2), result = 10ans` -> **result = 10sin(4^2)**

# Motivation

As an engineering student, I've faced the task of repeating similar or identical calculations for problem solving way too often. Or just, a random piece of math I wanted to quickly solve and carry on doing something else.  

*Quickly* is the key here. I wanted to know the result as fast as possible, typing as little as I could.  

Using a scientific calculator was not ideal. It was too slow to use, and I had to find it in the first place.  

The *Python* interpreter was alright, but I didn't like typing `**` for powers, `2*x` stuff, having to import the `math` module whenever I opened the terminal...  

Also, I couldn't use the `ANS` button that my scicalc had.  
Often, I found myself typing out formulas on-the-spot, having to go back and forth on the command line adding symbols.  

#### I mean, just look at this situation

Say I had to solve for `x` in `x² = a+b*c^15/9e9`.  
I would first type `a+b*c**15/9e9`. Then realise. Oh.  

I have to take the square root of this.  
Go back.  
Hit the left-arrow key so many times.  
Add the `sqrt(` at the start. Ok.  
Then the `)` at the end.  
_(Thankfully I had imported the `math` module already)._   

*S L O W.*

My dream was something like:

```python
stuff_i_want = a+b*c**15/9e9 then sqrt(ans) # nothing like this available
```

Also, if I wanted to perhaps tweak the value of, say, `a`, I'd have to re-type all the equation, or find out where in the command history it was left.

Switching to the *Julia* <3 interpreter solved several of these issues, with its beautifully clean syntax, also adding new features such as:

```julia
f(x) = 2x^2+x-14 # Lovely, I just defined a function!
```

And I could use the pipe operator to imitate what I wanted to achieve - writing down the formula in the order that it came to my mind:

```julia
result = a+b*c^15/9e9 |> x->sqrt(x)
```

Gorgeous. A bit strange to type rapidly (`|> x->` would get my fingers entangled somewhat often), but it was pretty neat.

*Julia* also has built-in math functions, which I simply loved. No more `from math import *` at the start, or no more ugly `cos(radians(thing))`!!!! *AND* the `ANS` feature!!! What a beast.  

Still, no solution for the 're-calc' issue...  

And no way of finding roots for quadratic formulas quickly...  
Or just zeros of a function...  
Too many parentheses...  
No easy command to find the polar representation of a complex number...

#### I had to take action.

This is when *Gecko* came to be. :lizard:

I decided to take all the features of the *Julia* REPL that I absolutely loved, and add to those my own needs.  
Aaand the nice looking Gecko ASCII art at the start. Credit to [Andreas Freise](http://www.ascii-art.de/) for it, it's super cute.  

# Thanks to

[David Beazley](https://www.dabeaz.com/) for the [Sly Lex Yacc](https://github.com/dabeaz/sly) tool. It is wonderful and really easy to use. Definitely couldn't (or wouldn't) have done this without it.

[Andreas Freise](http://www.ascii-art.de/) for the Gecko ASCII art.

[Julia](https://julialang.org/) creators for making that wonder. Many features of my REPL have been inspired in yours.

People in `ggg` for testing.

*You* for reading. Thanks.