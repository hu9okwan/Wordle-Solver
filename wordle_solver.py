
####################################################################### Imports

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException

import time, random
import collections 
import os, sys



##################################################################### Variables

first_word = "audio"
filename = "words.txt"
url = "https://www.nytimes.com/games/wordle/index.html"

# Set to True to open in default chrome profile (requires closing all chrome instances)
open_with_chrome_profile = False


# keeps track of letters; DONT CHANGE THESE!!
all_correct_letters_set = set()
all_present_letters_set = set()
all_absent_letters_set = set()



############################################# Initialize Selenium Chrome Driver

options = webdriver.ChromeOptions()

if open_with_chrome_profile:
    username = os.environ['USERPROFILE']
    user_data_dir = "--user-data-dir=" + username + "\\AppData\\Local\\Google\\Chrome\\User Data"
    options.add_argument(user_data_dir)

options.add_experimental_option('excludeSwitches', ['enable-logging'])
driver = webdriver.Chrome(options=options, executable_path = './selenium/chromedriver.exe')



##################################################################### Functions

def get_words(filename):
    # Returns list of words to use from text file
    with open(filename) as f:
        data = f.readlines()

        words_list = [] 
        for line in data:
            words_list.append(line.strip("\n"))

    return words_list


def map_str_to_dict(word):
    # Maps string to dictionary with index as key and letter as value
    dict = {}
    for index, value in enumerate(word):
        dict[index] = value
    
    return dict


def type_word(word_dict):
    # Sends the key presses to webdriver on body element of document
    word = ''.join(word_dict.values())
    print(f"Entering '{word}'...")
    print()
    driver.find_element_by_tag_name('body').send_keys(word)
    driver.find_element_by_tag_name('body').send_keys("\ue007")


def format_correct_letters(correct_letters_dict):
    letter_map = {
        0: "", 
        1: "", 
        2: "", 
        3: "",
        4: ""
    }
    word = ""
    for i in letter_map:
        try:
            if letter_map[i] != correct_letters_dict[i]:
                word += correct_letters_dict[i]
        except KeyError:
            word += "?"
            
    return word


def get_tile_status(attempt):
    # Gets the evaluation status of attempted word

    # create dicts to keep track of positions of letters 
    correct_letters_dict = {}
    present_letters_dict = {}
    
    # Get element of last attempted row 
    row_elements = driver.execute_script(f" return document.querySelector('game-app').shadowRoot.querySelector('game-row:nth-child({attempt})').shadowRoot.querySelectorAll('game-tile[letter]') ")
    
    
    for index, tile in enumerate(row_elements):
        
        letter = tile.get_attribute("letter")
        evaluation = tile.get_attribute("evaluation")

        if evaluation == "correct":
            correct_letters_dict[index] = letter
            all_correct_letters_set.add(letter)
            try:
                all_absent_letters_set.remove(letter) # in case a word with dupe letters is entered and first is absent but second is correct
            except KeyError:
                pass # ignore error of letter not in all_absent_letters_set
        elif evaluation == "present":
            present_letters_dict[index] = letter
            all_present_letters_set.add(letter)
        elif evaluation == "absent" and not (letter in all_correct_letters_set or letter in all_present_letters_set):
            all_absent_letters_set.add(letter)


    print("correct letters:", " ".join(format_correct_letters(correct_letters_dict)))
    print("present letters:", *all_present_letters_set)
    print("absent  letters:", *all_absent_letters_set)
    print()

    return correct_letters_dict, present_letters_dict, all_absent_letters_set


def remove_garbage_words(words_list, correct_letters_dict, present_letters_dict, all_absent_letters_set):
    # Removes words that contains absent letters or does not contain present/correct letters
    
    # removes all words that contains the absent letters
    words_list = [word for word in words_list if all(letter not in word for letter in all_absent_letters_set)]

    # removes all words that does not contain correct letters
    words_list = [word for word in words_list if all(correct_letters_dict[index] in word for index in correct_letters_dict)]

    # removes all words that does not contain present letters
    words_list = [word for word in words_list if all(present_letters_dict[index] in word for index in present_letters_dict)]

    # removes all words that contains present letter in the tested spot that didnt work
    words_list = [word for word in words_list if all(present_letters_dict[index] != word[index] for index in present_letters_dict)]

    # print(f"word list after garbage removal {len(words_list)}:", words_list)
    return words_list


def filter_correct_position(filtered_words_list, correct_letters_dict, word_dict):
    # Returns only words that has the correct letters in right positions

    potential_words_set = set()
    for word_dict in filtered_words_list:
        
        for index in correct_letters_dict:

            if word_dict[index] == correct_letters_dict[index]:
                potential_words_set.add(word_dict)

    # case where didnt have any correctly picked letters, return original 
    if len(correct_letters_dict) == 0:
        return filtered_words_list

    return potential_words_set


def get_most_freq_letter(potential_words_set, present_letters_dict, most_common_letters_set):
    # Returns most frequent letter out of all potential words that has not been seen before

    most_common_letter = ""

    # string that contains all letters + dupes for counting total most occurrences
    all_letters_string = ""
    
    for word in potential_words_set:
        for letter in word:
            # dont count present letters occurrences (b/c they will have a 100% occurrence or more)
            if not (letter in list(present_letters_dict.values()) or letter in most_common_letters_set):
                all_letters_string += letter
    
    # Get list of tuples of most common letters and its count. ex: [('r', 44), ('e', 32), ('t', 16),...]
    letters_counter_tuple_list = collections.Counter(all_letters_string).most_common() 

    try:
        if letters_counter_tuple_list[0][1] == 1:
            return most_common_letter

        most_common_letter = letters_counter_tuple_list[0][0]

        # for debugging
        # print(letters_counter_tuple_list)
        # print(f"most_common_letters_set: {most_common_letters_set}")
        # print(f"most_common_letter: {most_common_letter}")

    except IndexError:
        # list has been reduced and they all share the same letters with no most common
        pass

    return most_common_letter


def narrow_potential_words(potential_words_set, present_letters_dict, most_common_letters_set=set()):
    # Reduces potential words by picking words that have very common letters
    # this helps eliminate the a larger set of words if they do not contain that common letter

    most_common_letter = get_most_freq_letter(potential_words_set, present_letters_dict, most_common_letters_set)
    most_common_letters_set.add(most_common_letter)

    if most_common_letter == "":
        print("reduced_potential_words_set:", potential_words_set)
        return potential_words_set

    # Remove all words that don't have the most common letter
    reduced_potential_words_set = [word for word in potential_words_set if most_common_letter in word]


    # case where there are no present letters selected or no further reduction on potential words can be done
    if len(reduced_potential_words_set) == 0 or len(reduced_potential_words_set) == len(potential_words_set):
        print("reduced_potential_words_set:", reduced_potential_words_set)
        return potential_words_set


        
    return narrow_potential_words(reduced_potential_words_set, present_letters_dict, most_common_letters_set)


def pick_word(narrowed_words_set):
    # picks a random word from list
    return random.choice(list(narrowed_words_set))



def main():

    driver.get(url)
    words_list = get_words(filename)
    status = False
    attempt = 1

    word_dict = map_str_to_dict(first_word)

    # Wait until game board is loaded
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "body > game-app"))
        )
    except TimeoutException:
        print("Timed out. Page took too long to load")
        sys.exit()

    time.sleep(1.5)


    # Check for game stats modal pop up and exit if game was already played
    game_stats_elem = driver.execute_script('return document.querySelector("body > game-app").shadowRoot.querySelector("#game > game-modal > game-stats")')
    if game_stats_elem:
        print("Game has already been played for today")
        sys.exit()

    # close instructions modal on initial load
    driver.execute_script(" document.querySelector('game-app').shadowRoot.querySelector('div#game > game-modal').shadowRoot.querySelector('div.content > div.close-icon').click() ")

    while attempt != 6:

        print(f"========================= Attempt {attempt} =========================")

        time.sleep(1.5)

        type_word(word_dict)

        time.sleep(1)

        # Get tile status evaluation for current row attempt
        correct_letters_dict, present_letters_dict, all_absent_letters_set = get_tile_status(attempt)

        # Terminate loop if answer has been found
        if len(correct_letters_dict) == 5:
            status = True
            break

        filtered_words_list = remove_garbage_words(words_list, correct_letters_dict, present_letters_dict, all_absent_letters_set)

        potential_words_set = filter_correct_position(filtered_words_list, correct_letters_dict, word_dict)
        print(f"remaining potential words ({len(potential_words_set)}):", potential_words_set)
        print()

        print(f"Calculating next best word to guess...")
        narrowed_words_set = narrow_potential_words(potential_words_set, present_letters_dict)
        print()

        suggested_word = pick_word(narrowed_words_set)
        suggested_word = map_str_to_dict(suggested_word)

        
        words_list = potential_words_set
        word_dict = suggested_word
        attempt += 1 

    
    print("=============================================================")
    if status:
        print(f"SOLVED!!! The correct word is '{format_correct_letters(word_dict)}'" )
    else:
        print("fuck this shits too hard bro better luck next life")
    print("=============================================================")

main()
