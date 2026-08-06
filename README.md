# Pokedle Solver

This repository contains some algorithms for solving Pokedle (and similar, wordle-style games) and a few experiments to
compare the algorithms. 

- [What is Pokedle](#what-is-pokedle)
- [Motivation](#motivation)
- [Algorithm Explanations](#algorithm-explanations)
  - [Experimental Comparisons](#experimental-comparisons)
- [Code Details](#code-details)


# What is Pokedle

[Pokedle](https://pokedle.com/) is a Wordle-style Pokemon guessing game. There is a hidden pokemon and you make a series of guesses to try and uncover it. For each guess you're given information on which attributes of the pokemon you guessed match the hidden pokemon, allowing you to narrow down the set of possible solutions.

![Image of Pokedle Interface. On top is a search bar where the user may guess a pokemon. Below is a users guess, Scorbunny, showing which of Scorbunny's attributes match the hidden answer](Images/pokedle-sample.png)

Above, I've guessed Scorbunny. The game records the guess and tells me how Scorbunny's attributes compare to the hidden Pokemon's attributes.
- Red in the 'Type 1' column, Fire, indicates neither of the hidden Pokemon's types is Fire.
- Likewise, we know the Pokemon must be a dual type since 'Type 2' is red for None.
- We know the Pokemon must be a first stage evolution.
- It must be fully evolved.
- It is not classified as having either white or orange coloration.
- It is not in the grasslands habitat.
- It was introduced earlier than generation 8.

Using this information, the player continues to make guesses, narrowing down the possibilities to help identify the hidden Pokemon.
The answer here happened to be Mega Sableye.

# Motivation
One night I was playing Pokedle and came across a game state where it would be more informative to make a guess that I knew was wrong! 
I forget the exact details, so let's consider a simple, hypothetical.

Let's say you knew from previous guesses that the target Pokemon is from generation 8 and that it has one of 3 possible types: fire, grass, water.
(No gen 8 Pokemon has a combination of these three types so it must be a mono-type)
You could guess Sobble (water), Scorbunny (fire), and Grookey (grass) to determine the type of the Pokemon but in the worst case, this would take two guesses to determine the type (plus remaining guesses to find the right Pokemon of that type).
Instead, you could guess Volcanion (fire/water), ludicolo (water/grass), or scovillain (grass/fire) -- Pokemon that aren't from gen 8 and thus must not be the right answer, but that would allow you to determine the correct type in a single guess!

This prompted the following question: given a Pokedle game state, how does one determine the best guess to make? 
In an optimal play strategy would you ever find yourself making a guess known to be wrong or is a situation as described above just a result of poor guesses early on?

This repository is a result of researching that question and contains implementations for different 'optimal' Pokedle strategies.
Given a game state, any of the guessing strategies implemented allow you to determine (one of) the 'best' guesses to make at each step.

# Algorithm Explanations

## Experimental Comparisons

# Code Details