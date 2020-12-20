# Cykelfest python - edition.

import random
import math
import json
import numpy as np


def print_array(array):
    for list in array:
        print(list)

def make_schedule():

    array = []
    for i in range(len(participants_dict)):
        array.append([])
        for j in range(stops + 1): 
            if j == 0: 
                array[i].append(list(participants_dict.keys())[i])
            else:
                array[i].append("")

    participants_list = list(participants_dict.keys())
    # Blanda listan 
    random.shuffle(participants_list)

    for i in range(1, stops + 1):
        for j in range(0, stops):
            # Placerar ut de som ska hosta hos dem själva först.
            host = participants_list[j + (i * stops)]
            for k in range(len(array)):
                if array[k][0] == host:
                    array[k][i] = host
            # Placera sedan ut resten.
        for j in range(stops):
            host = participants_list[j + (i * stops)]
            for k in range(group_size-1):
                random_place = random.randint(0, len(participants_list)-1)
                while array[random_place][i] != "":
                    random_place = random.randint(0, len(participants_list)-1)
                array[random_place][i] = host
    return array
                

def evaluate(schedule):
    points = 100
    # Poängavdrag ifall man lämnar sitt område.
    for i in range(len(participants_dict)):
        previous_stop = participants_dict[schedule[i][0]]
        for j in range(1, stops + 1):
            if previous_stop != participants_dict[schedule[i][j]]:
                points -= 3
            previous_stop = participants_dict[schedule[i][j]]
    # Poängavdrag ifall man träffar samma par flera gånger.
    # Vi tar en rad och kollar dubletter i alla rader under den.
    # På så vis råkar vi aldrig ta samma par flera gånger.
    position = 0
    for participant in schedule[0:]:
        position += 1
        host_stops = participant[1:]
        for row in schedule[position:]:
            unique_set = set(row[1:] + host_stops)
            points -= (len(unique_set) - ((2 * stops) -1))
    return points


participants_dict = {
    "Martin": "Kantorn",
    "Majd": "Flogsta",
    "Linda": "Flogsta",
    "Alex": "Rackis",
    "Tyra": "Kantorn",
    "Melker": "Rackis",
    "Alva": "Rackis",
    "Clas": "Kantorn",
    "Joar": "Flogsta",
    "Tyra 2": "Kantorn",
    "Sofia": "Rackis",
    "Mattias": "Flogsta",
    "Oskar" : "Flogsta",
    "Emil" : "Kantorn",
    "Alice" : "Rackis"
}

stops = 3; 
#Tar fram den nödvändiga gruppstorleken.
group_size = len(participants_dict) // stops

# schedule_array = make_schedule(schedule_array)
# print_array(schedule_array)
# print(evaluate(schedule_array))
schedule_array = []
best_schedule= []
# Loop som evaluerar kvaliten på ett schema.
score = 0
iteration_found = 1
it = 0
best_score = 0
# Tar fram hundra olika slumpade listor och väljer bästa alternativet.
while score < 46:
    old_schedule = schedule_array
    schedule_array = make_schedule()
    score = evaluate(schedule_array)
    if score > best_score:
        iteration_found = it
        best_schedule = schedule_array
        best_score = score
    
    it += 1
    
print_array(best_schedule)
print("Poäng: ", best_score)
print("Hittades i iteration: ", iteration_found)
