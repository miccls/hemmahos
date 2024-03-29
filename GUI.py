import curses
from curses.textpad import Textbox, rectangle
import os.path
from pprint import pprint
import time


def read_screens(path: str) -> dict:
    '''Reads the available screens from textfile
    '''
    screens = {}
    with open(path, 'r') as file:
        lines = file.readlines()
    for i, line in enumerate(lines):
        # Determine which types of lines we have
        if '=' in line:
            # This means we have a screen declaration
            screen = line.split('=')[0]
            # The input dictionary will be with what is before the colon as key
            screens[screen] = {"lines" : [], "inputs" : {}}
            screen_index = (i + 1)
        else:
            if screen:
                if ':' in line:
                    # As of now, there should only be one input per line so 
                    # splitting in : should yield a list of length 2
                    name = line.split(':')[0]
                    print([s for s in line])
                    x, y = line.index(':') + 1, i - screen_index
                    # Store the coordinates of the input in the input dict.
                    screens[screen]['inputs'][name.strip()] = (y, x)
                    # Then add line as we want it printed as well.
                    screens[screen]['lines'].append(line)
                else:
                    screens[screen]['lines'].append(line)
    return screens

def check_answers(answers: dict) -> bool:
    '''Returns either true or false if the 
    retrieved answers are fit for the ckl class
    '''
    # Checks that we require from the answers.
    reqs = {
        'Filnamn' : lambda x: os.path.exists(x),
        'Regel/Slump (1/2)' : lambda x: x in ('1', '2'),
        'Samples' : lambda x: int(x) > 100,
        'Stopp' : lambda x: int(x) > 2
    }

    checks = [func(answers[input]) for input, func, in reqs.items()]
    return all(checks)

def draw_screen(stdscr, lines):
    stdscr.move(0, 0)
    stdscr.clrtobot()
    '''Draws screen contained in lines
    '''
    for i, line in enumerate(lines):
        stdscr.addstr(i, 0, line)

# Using cureses to modify the command window.
stdscr = curses.initscr()
# So that it does not display what you type in
curses.noecho()
curses.cbreak()
stdscr.keypad(True)
curses.start_color()
curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
screen_dict = read_screens("main.txt")
draw_screen(stdscr, screen_dict['main']['lines'])
LEFT_ARROW = 260
UP_ARROW = 259
RIGHT_ARROW = 261
DOWN_ARROW = 258
inputs = list(screen_dict['main']['inputs'].keys())
input_index = 0
curr_input = inputs[input_index]
stdscr.move(*(screen_dict['main']['inputs'][curr_input]))
# Make text boxes
text_boxes = {}
for input in inputs:
    y, x = (screen_dict['main']['inputs'][input])
    win = curses.newwin(1, 18, y, x+1)
    box = Textbox(win)
    rectangle(stdscr, y-1, x, y+1, x + 20)
    text_boxes[input] = box

approved = False
# Run until proper answers are put in.
while not approved:
    answers = {}
    for input, box in text_boxes.items():
        stdscr.refresh()
        box.edit()
        answers[input] = box.gather().strip()
    approved = check_answers(answers)

# Now good answers are guaranteed.
draw_screen(stdscr, screen_dict['loading']['lines'])
# Now draw screen with stats.
pprint(answers)

path = answers['Filnamn']
rule = answers['Regel/Slump (1/2)'] == 1
samples = answers['Samples']
stops = answers['Stopp']

# Now samples have been gathered, generate a schedule


# This will probably not be used.
while True:
    # Here starts the program
    key = stdscr.getch()
    # To quit
    if key == 27:
        break
    elif key == UP_ARROW:
        input_index -= 1
        input_index = input_index % len(inputs)
        curr_input = inputs[input_index]
        text_boxes[curr_input].edit()
    elif key == DOWN_ARROW:
        input_index += 1
        input_index = input_index % len(inputs)
        curr_input = inputs[input_index]
        text_boxes[curr_input].edit()
    else:
        # Not a special key.
        pass
