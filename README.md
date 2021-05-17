# Gecko

![REPL intro image](img/intro.PNG)

An interactive REPL devised for quickly getting calculations done.

## Features

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

<!-- One-line function definitions TODO -->

## Motivation

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

## Thanks to

[David Beazley](https://www.dabeaz.com/) for the [Sly Lex Yacc](https://github.com/dabeaz/sly) tool. It is wonderful and really easy to use. Definitely couldn't (or wouldn't) have done this without it.

[Andreas Freise](http://www.ascii-art.de/) for the Gecko ASCII art.

[Julia](https://julialang.org/) creators for making that wonder. Many features of my REPL have been inspired in yours.

*You* for reading. Thanks.