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
