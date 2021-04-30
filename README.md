# Gecko

![REPL intro image](img/intro.PNG)

An interactive REPL devised for quickly getting calculations done.

## Features

<!-- Clean expr syntax -->

<!-- Straightforward piping for verbose expressions -->

<!-- Built-in math functions -->

<!-- Calc command -->

<!-- Var dump -->

<!-- One-line function definitions -->

## Motivation

As an engineering student, I've faced the task of repeating similar or identical calculations for problem solving way too often. Or just, a random piece of math I wanted to quickly solve and carry on doing something else.  

Using a scientific calculator was ok, but I wanted something I could type on. It was too slow to use.  

The *Python* interpreter was alright, but I didn't like typing `**` for powers, typing `2*x` every time, having to import the `math` module whenever I opened it...  

Also, I couldn't use the `ANS` featured on the scientific calculator. Often, I found myself typing out formulas on-the-spot, having to go back and forth on the command line adding symbols.  

Say I had to solve for `x` in `x² = a+b*c^15/9e9`.  
I would first type `a+b*c**15/9e9`. Then realise it.  
Oh.  
I have to take the root of this.  
Go back. Add the `sqrt(` at the start. Ok. Then the `)` at the end. (Thankfully I had imported the `math` module already).  

*S L O W.*

My dream was something like:

```python
stuff_i_want = a+b*c**15/9e9 then sqrt(ans) # nothing like this
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

Gorgeous. A bit strange to fast-type (`|> x->` would get my fingers entangled somewhat often), but it was pretty neat.

*Julia* also has built-in math functions, which I simply loved. No more `from math import *` at the start, or no more ugly `cos(radians(thing))`!!!!

Still no solution for the 're-calc' issue...  

And no way of finding roots for quadratic formulas quickly...  
Or just zeros of a function...  
Too many parentheses...

I had to take action.

This is when *Gecko* came to be. :lizard:

I decided to take all the features of the *Julia* REPL that I absolutely loved, and add to those my own needs.  
And the nice looking Gecko ASCII art at the start. Credit to [Andreas Freise](http://www.ascii-art.de/) for it, it's super cute. (I don't know who you are).

## Thanks to

[David Beazley](https://www.dabeaz.com/) for the [Sly Lex Yacc](https://github.com/dabeaz/sly) tool. It is wonderful and really easy to use. Definitely couldn't (or wouldn't) have done this without it.

[Andreas Freise](http://www.ascii-art.de/) for the Gecko ASCII art.

[Julia](https://julialang.org/) creators for making that wonder. Many features of my REPL have been inspired in yours.

*You* for reading. Thanks.