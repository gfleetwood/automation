from robocorp import browser
from robocorp.tasks import task
from RPA.Excel.Files import Files as Excel
from RPA.HTTP import HTTP
import time
from os import system
import io
import random
from sys import exit
import re
from skimage.io import imshow, show, imread, imsave
from skimage.color import rgb2gray
import numpy as np
from PIL import Image
from toolz import pipe
import z3
from sat_solver import *
from helper_functions import *
import pyautogui

browser.configure(
browser_engine = "chromium",
screenshot = "only-on-failure",
headless = False
)

wordle_colors = [("yellow", (228, 218, 0)), ("gray", (162, 162, 162)), ("green", (63, 186, 119))]
words = load_dictionary("/usr/share/dict/words")

@task
def wordle():

    letter_vars = define_letter_variables()
    solver = z3.Solver()
    solver = add_alphabet_modeling_constraints(solver, letter_vars)
    solver = add_legal_words_constraints(solver, words, letter_vars)
    
    page = browser.goto("https://hellowordl.net/")
    pyautogui.click(500, 500)
    
    for i in range(6):
    
        result = solver.check()
        model = solver.model()
        guess = pretty_print_solution(model, letter_vars)
    
        for con in solver.assertions()[11:]: 
            info = con.__repr__()
            match_ = re.search(" [0-9]{1,2}", info).group().strip()
            info = re.sub(match_, index_to_letter_map[int(match_)], info)
        
        # \n simulates the enter key
        #page.fill('#root', "hello\n")
        pyautogui.write(guess) 
        pyautogui.press('enter')
        time.sleep(1)
        page.screenshot(path = "./output/pic_{}.png".format(i + 1))
