# Optimal Pokedle Strategy

[Pokedle](https://pokedle.com/) is a Wordle-style Pokemon guessing game. There is a hidden pokemon and you make a series of guesses to try and uncover it. For each guess you're given information on which attributes of the pokemon you guessed match the hidden pokemon, allowing you to narrow down the set of possible solutions.

One night I was playing Pokedle and came across a game state where it would be more informative to make a guess that I knew was wrong! 
I knew from previous guesses that the target pokemon was from generation 8 and that it had one of 3 possible types: fire, grass, water.
(No gen 8 pokemon has a combination of these three types so it had to be a mono-type)
I could have guessed sobble (water), scorbunny (fire), grookey (grass) to determine the type of the pokemon but in the worst case, this would take two guesses to determine the type (plus remaining guesses to find the right pokemon of that type).
Instead, I could guess Volcanion (fire/water), ludicolo (water/grass), or scovillain (grass/fire) -- Pokemon that aren't from gen 8 and thus must not be the right answer, but that would allow me to determine the correct type in a single guess!

This prompted the following question: given a Pokedle game state, how does one determine the best guess to make? 
In an optimal play strategy would you ever find yourself making a guess known to be wrong or was that situation just a result of poor guesses early on?

This repository is an implementation of an optimal Pokedle strategy engine.
Given a game state, it determines a set of the best possible guesses to make at each step in order to minimize the time taking to win.
