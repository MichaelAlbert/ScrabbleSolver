Author: Michael Albert

Credit to Appel and Jacobson for the core algorithm (https://www.cs.cmu.edu/afs/cs/academic/class/15451-s06/www/lectures/scrabble.pdf)

Word list used: ENABLE (https://norvig.com/ngrams/enable1.txt)

This is a personal project of mine. I play Scrabble a lot, and thought it would be fun to write something that could give me the top 10 scoring plays when I'm stuck. This is not intended for use in any competitive play, and is intended only as a fun challenge to myself.

# ScrabbleSolver

A Scrabble move generation and scoring engine that analyzes a board state and a tile rack to compute the highest-scoring legal moves using a trie-based dictionary and crossword validation. No strategy is taken into account.

The solver:
- Generates all valid word placements from anchor squares
- Validates words using a trie dictionary
- Checks crossword constraints for perpendicular words
- Scores moves using Scrabble letter values and board multipliers
- Returns the top N best moves

---

## Features

- Trie-based dictionary lookup for fast word validation
- Anchor-based move generation (only considers legal play locations)
- Crossword validation for intersecting words
- Rack-aware recursive word construction
- Move scoring with letter + board multipliers
- Duplicate move filtering

---

## Requirements

- Python 3.10+

No external libraries are required.

---

## Setup

Ensure python is installed locally.

Clone the repository.

In main.py (under src folder):
- set either "classic" or "crossplay" for the version where Board() is called
- change board_state to match your current board; each placed letter should be (char, is_blank) where char is the letter and is_blank is either True or False
- in rack.fill_rack() enter all letters in your rack. Blanks are represented as a period.



In CLI:
- run python main.py from within src



