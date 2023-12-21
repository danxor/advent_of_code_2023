# Solutions to Advent of Code 2023

These are my solutions for Advent of Code 2023. They may be naïve and troublesome in many ways but that's part of the fun and part of the challenge.

My goal this year is to reach the global leaderboard; which I have yet to complete, my best day currently is day 21 and star 2 which gave me position 139.

If you'd like to try these challenges yourself you can do it by following [this](https://adventofcode.com/2023) link.

## Struture

I rely heavily on the main script: runner.py; which does all of the heavylifting for me. It downloads the puzzle inputs it solves the test examples as given by the daily instructions and validates that they give the correct answer.

The src-folder contains a class for each day that is used to implement the solutions.

The common-folder contains code to generate a python-file for each day and also the code for downloading the puzzle-inputs.

The data-folder contains all the puzzle-inputs.

## Usage

$ pip3 install -r requirements.txt\
Requirement already satisfied: requests>=2.31.0 ...\
...

$ ./runner.py --test 1\
Day #1 - Part #1: XXX - Ok\
Day #1 - Part #2: XXX - Ok

$ ./runner.py 1\
Day #1 - Part #1: XXX\
Day #1 - Part #2: XXX
