#!/usr/bin/python3

from skimage.io import imshow, show, imread, imsave
import numpy as np
from PIL import Image
from toolz import pipe
from skimage.color import rgb2gray
import io
import pyautogui
import time
from os import system
import numpy as np
import z3
import random
from sys import exit
from logzero import logger, logfile
import re
from copied_code import load_dictionary, remove_plurals, remove_words_with_invalid_chars, pretty_print_solution
from copied_code import define_letter_variables, add_legal_words_constraints, add_alphabet_modeling_constraints
from copied_code import add_doesnt_contain_letter_constraint, add_contains_letter_constraint, add_invalid_position_constraint
from copied_code import add_exact_letter_position_constraint, add_letter_appears_once_constraint
from copied_code import letter_to_index_map, index_to_letter_map

def get_dominant_color(letter_square):

  img = Image.fromarray(letter_square)
  dom_color = sorted(img.getcolors(2 ** 24), reverse = True)[0][1]

  return(dom_color)

def euclidean_distance(p1, p2):

  temp = np.array(p1) - np.array(p2) 
  sum_sq = np.dot(temp.T, temp)
  result = np.sqrt(sum_sq)

  return(result)

def get_color(letter_square):

  color = get_dominant_color(letter_square)
  dists = [euclidean_distance(color, x[1]) for x in wordle_colors]
  closest_color_index = dists.index(min(dists))
  closest_color = wordle_colors[closest_color_index][0]

  return(closest_color)

def show_letter(word, col):

  letter_square = word[:, col*55:(col+1)*55]
  closest_color = get_color(letter_square)

  return(closest_color)

def show_word(im, row):

  word = im[row*55:(row+1)*55, :]
  colors = list(map(lambda x: show_letter(word, x), range(5)))
  word_info = [(letter, colors[i], i) for i, letter in enumerate(guess)]
  _ = update_solver(word_info)
  if set(colors) == set(["green"]): exit(0)

  return(True)

def update_solver(word_info):

  global solver
  
  for letter_info in word_info:
    print(letter_info)
    if letter_info[1] == "green":
      solver = add_contains_letter_constraint(solver, letter_vars, letter_info[0])
      solver = add_exact_letter_position_constraint(solver, letter_vars, letter_info[0], letter_info[2])
      constraints = solver.assertions() 
      check_if_grey_before = f"letter_{str(letter_info[2])} != {letter_to_index_map[letter_info[0]]}"
      new_constraints = [constraint for constraint in constraints if constraint.__repr__() != check_if_grey_before]
      if len(constraints) != len(new_constraints): 
        solver.reset()
        solver.add(new_constraints)
    elif letter_info[1] == "yellow":
      solver = add_contains_letter_constraint(solver, letter_vars, letter_info[0])
      solver = add_invalid_position_constraint(solver, letter_vars, letter_info[0], letter_info[2])
      constraints = solver.assertions() 
      check_if_grey_before = f"letter_{str(letter_info[2])} != {letter_to_index_map[letter_info[0]]}"
      new_constraints = [constraint for constraint in constraints if constraint.__repr__() != check_if_grey_before]
      if len(constraints) != len(new_constraints): 
        solver.reset()
        solver.add(new_constraints)
    elif letter_info[1] == "gray": 
      constraints = solver.assertions() 
      check_if_added = f"letter_{str(letter_info[2])} == {letter_to_index_map[letter_info[0]]}"
      new_constraints = [constraint for constraint in constraints if constraint.__repr__() != check_if_added]
      if len(constraints) == len(new_constraints): 
        solver = add_doesnt_contain_letter_constraint(solver, letter_vars, letter_info[0])

  return(True)
  
wordle_colors = [("yellow", (228, 218, 0)), ("gray", (162, 162, 162)), ("green", (63, 186, 119))]
logfile('log.log')
system("> log.log")

words = load_dictionary("/usr/share/dict/words")
letter_vars = define_letter_variables()
solver = z3.Solver()
solver = add_alphabet_modeling_constraints(solver, letter_vars)
solver = add_legal_words_constraints(solver, words, letter_vars)

system('google-chrome https://hellowordl.net/')
time.sleep(2)
pyautogui.click(500, 500)

for i in range(6):

  result = solver.check()
  model = solver.model()
  guess = pretty_print_solution(model, letter_vars)
  
  for con in solver.assertions()[11:]: 
    info = con.__repr__()
    match = re.search(" [0-9]{1,2}", info).group().strip()
    info = re.sub(match, index_to_letter_map[int(match)], info)
    logger.info("word_{}: {}".format(i, info))
  
  pyautogui.write(guess) 
  pyautogui.press('enter')
  im = pyautogui.screenshot()
  im = np.asanyarray(im)[260:600, 690:990]
  #imsave(f"wordle_{i}.jpg", im)
  _ = show_word(im, i)
