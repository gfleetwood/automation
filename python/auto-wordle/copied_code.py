'''
All code that was copied from the blog that inspired this project: 

https://typon.github.io/wordle.html

Some variable declarations in app were copied over as well.
'''

from string import ascii_lowercase
import z3

def load_dictionary(dictionary_path = None):

    with open(dictionary_path, "r") as f: all_legal_words = set(word.strip() for word in f.readlines())
    words = remove_words_with_invalid_chars(all_legal_words)
    words = list(words)
    words = remove_plurals(words)
    
    return(words)
    
def remove_plurals(words):

    five_letter_words = list(filter(lambda word: len(word) == 5, words))
    four_letter_words = set(filter(lambda word: len(word) == 4, words))
    five_letter_words_end_in_s = set(filter(lambda word: word[4] == "s", five_letter_words))
    singular_five_letter_words = list(filter(lambda word: not (word in five_letter_words_end_in_s and word[:4] in four_letter_words), five_letter_words))

    return singular_five_letter_words

def remove_words_with_invalid_chars(words):
    valid_chars_set = set(letter_to_index_map.keys())

    def contains_only_valid_chars(word):
        return set(word).issubset(valid_chars_set)

    return filter(contains_only_valid_chars, words)

def pretty_print_solution(model, letter_vars):

    word = []

    for index, letter_var in enumerate(letter_vars):
        word.append(index_to_letter_map[model[letter_var].as_long()])

    return(word)
    
def define_letter_variables():

  result = [z3.Int(f"letter_{index}") for index in range(5)]

  return(result)

def add_legal_words_constraints(solver, words, letter_vars):

    all_words_disjunction = []

    for word in words:
        word_conjuction = z3.And([letter_vars[index] == letter_to_index_map[letter] for index, letter in enumerate(word)])
        all_words_disjunction.append(word_conjuction)

    solver.add(z3.Or(all_words_disjunction))

    return(solver)

def add_alphabet_modeling_constraints(solver, letter_vars):

    for letter_var in letter_vars: solver.add(letter_var >= 0, letter_var <= 25)

    return(solver)

def add_doesnt_contain_letter_constraint(solver, letter_vars, letter):

    for letter_var in letter_vars: solver.add(letter_var != letter_to_index_map[letter])

    return(solver)

def add_contains_letter_constraint(solver, letter_vars, letter):

    solver.add(z3.Or([letter_var == letter_to_index_map[letter] for letter_var in letter_vars]))

    return(solver)

def add_invalid_position_constraint(solver, letter_vars, letter, position):

    solver.add(letter_vars[position] != letter_to_index_map[letter])

    return(solver)

def add_exact_letter_position_constraint(solver, letter_vars, letter, position):

    solver.add(letter_vars[position] == letter_to_index_map[letter])

    return(solver)

def add_letter_appears_once_constraint(solver, letter_vars, letter):

    unique_letter_disjunction = []

    for letter_var in letter_vars:
        this_letter_conjunction = [letter_var == letter_to_index_map[letter]]
        for other_letter_var in letter_vars:
            if letter_var == other_letter_var:
                continue
            this_letter_conjunction.append(other_letter_var != letter_to_index_map[letter])
        unique_letter_disjunction.append(z3.And(this_letter_conjunction))

    solver.add(z3.Or(unique_letter_disjunction))

    return(solver)
    
letter_to_index_map = {letter: index for index, letter in enumerate(ascii_lowercase)}
index_to_letter_map = {index: letter for letter, index in letter_to_index_map.items()}
