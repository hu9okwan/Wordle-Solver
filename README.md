# Wordle-Solver 🎓

 
This script automatically solves [Wordle](https://www.nytimes.com/games/wordle/index.html) puzzles usually within 3 or 4 attempts. 

The method I used attempts to solve the puzzle by recursively reducing down a set of words that possess the most common letter among themselves in that iteration. 
This will eliminate a large number of words from the pool when a letter is evaluated, in which a word is then randomly picked from the narrowed set of words.


## Requirements
- [Python](https://www.python.org/downloads/)
- [Selenium](https://chromedriver.chromium.org/downloads)

## Setup 
1. Create root folder
2. cd to root folder
4. Clone this repo
5. Open terminal and enter ``` cd Wordle-Solver ```

### Variables
At the top of the python file, you can change the following variables:

- ``` first_word = "<enter desired word>" ``` First word that the script guesses with. The default word is set to "audio". 

- ``` open_with_chrome_profile = <True/False> ``` If set to True, it will open the Chrome browser with your default profile. Note that all Chrome instances will have to be closed if set to True.
If False, it will open it in an anonymous webdriver profile.


## Usage
Enter ``` & path/to/python.exe path/to/wordle_solver.py ``` in terminal

