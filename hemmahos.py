# Cykelfest python - edition.

'''
Här ska en liten förklaring av koden ligga.

I schemat som skrivs ut så är första kolonnen 
namn på alla deltagande och på den raden i de övriga
kolonnerna står det vilka stopp de har. Indata till 
detta program är namn och område. Programmet kommer
i framtiden läsa in och bilda en lista av dessa områden.
För enkelhetens skull (i början) så kommer alla områdes-byten
vara lika "dåliga" men framöver kommer man förhoppningsvis kunna skriva
in address och så beräknas avståndet mellan platserna med koordinater.
Google har förhoppningsvis någon API heh.

To do:
 Ändra programmet så att det inte är hårdkodat för 3 stopp.
 Lägg allt i en klass. Ta json eller csv med deltagare som inparameter tillsammans
 med antalet stopp som ska finnas på rundan.
 Dela upp funktionen make_schedule till flera funktioner, exempelvis
 assign_host och assign_to_host.


För övrigt. Kör på multiprocessing här. Dela upp antalet önskade försök och kör det på alla kärnor
Denna datorn som jag skriver detta på, Dell XPS 15, har 6 kärnor vilket är rätt gott. 12 hade vart optimalt.
Kan man komma in på universitetets linuxmaskiner kan man köra över natten, tiotals
om inte hundratals miljoner scheman gissningsvis. 


'''

import random
import math
import json
import numpy as np
import time

class FHR:
    '''
    Klass som innehåller allt godis som hanterar Femma-hos-rundan.
    '''
    def __init__(self, participants_dict, stops):


        self.participants_dict = participants_dict
        self.stops = stops; 
        #Tar fram den nödvändiga gruppstorleken.
        self.group_size = len(participants_dict) // stops
        self.participants_list = list(participants_dict.keys())

        # schedule_array = make_schedule(schedule_array)
        # print_array(schedule_array)
        # print(evaluate(schedule_array))

    def print_array(self,array):
        for list in array:
            print(list)

    def assign_host(self, host, i):
        '''
        Placerar ut en host under ett stopp på
        dennes egna adress så att hen är garanterat
        hemma då folk har dennes hem som stopp.
        array är schemat, i är kolonnen eller stoppet i schemat
        '''
        for k in range(len(self.array)):
            if self.array[k][0] == host:
                self.array[k][i] = host
        return self.array

    def assign_to_host(self, host, i):
        '''
        Placerar ut slumpmässiga deltagare (participants_list) till angiven
        host (host) vid angivet stopp (i) i angivet schema (array)
        '''
        for k in range(self.group_size-2):
            random_place = random.randint(0, len(self.participants_list)-1)
            while self.array[random_place][i] != "":
                random_place = random.randint(0, len(self.participants_list)-1)
            self.array[random_place][i] = host
        return self.array

    def make_empty_schedule(self,):
        '''
        Gör ett tomt schema med bara namnkolonnen ifylld.
        '''
        array = []
        for i in range(len(participants_dict)):
            array.append([])
            for j in range(self.stops + 1): 
                if j == 0: 
                    array[i].append(list(participants_dict.keys())[i])
                else:
                    array[i].append("")
        return array

    def make_schedule(self,):
        self.array = self.make_empty_schedule()

        # Blanda listan 
        random.shuffle(self.participants_list)

        for i in range(1, self.stops + 1):
            for j in range(0,1 + len(self.participants_list)//self.group_size):
                # Placerar ut de som ska hosta hos dem själva först.
                host = self.participants_list[j + (i * (1 + len(self.participants_list)//self.group_size))]
                self.array = self.assign_host(host, i)
                # Placera sedan ut resten.
                
            for j in range(0,1 + len(self.participants_list)//self.group_size):
                host = self.participants_list[j + (i * (1 + len(self.participants_list)//self.group_size))]
                self.array = self.assign_to_host(host, i)
        return self.array
                    

    def evaluate(self,schedule):
        points = 100
        # Poängavdrag ifall man lämnar sitt område.
        for i in range(len(participants_dict)):
            previous_stop = participants_dict[schedule[i][0]]
            for j in range(1, self.stops + 1):
                if previous_stop != participants_dict[schedule[i][j]]:
                    points -= 1
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
                if (2 * self.stops) - 1 > len(unique_set):
                    points += len(unique_set) - ((2 * self.stops) -1)
        return points



    def sample(self, number):
        schedule = []
        best_schedule = []
        # Loop som evaluerar kvaliten på ett schema.
        score = 0
        iteration_found = 1
        it = 0
        best_score = 0
        while it < number:
            schedule = self.make_schedule()
            score = self.evaluate(schedule)
            if score > best_score:
                iteration_found = it
                best_schedule = schedule
                best_score = score
    
            it += 1
        return best_schedule, iteration_found, best_score

# Lägg detta i en run-funktion och en init-metod!

start_time = time.time()

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
    "Alice" : "Rackis",
    "Johan" : "Kantorn"
}

 
# Tar fram hundra olika slumpade listor och väljer bästa alternativet.
# Fungerar just nu bara för 3.
femma = FHR(participants_dict, stops = 3)
best_schedule, iteration_found, best_score = femma.sample(100000)

femma.print_array(best_schedule)
print("Poäng: ", best_score)
print("Hittades i iteration: ", iteration_found)
print(f"Det tog {time.time() - start_time} sekunder")