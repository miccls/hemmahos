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
 Det är inlagt så att det ska fungera att bara välja 3 men just nu så går det inte hehe, programmet ger fel.
 Lägg allt i en klass. Ta json eller csv med deltagare som inparameter tillsammans
 med antalet stopp som ska finnas på rundan.
 Dela upp funktionen make_schedule till flera funktioner, exempelvis
 assign_host och assign_to_host.


För övrigt. Kör på multiprocessing här. Dela upp antalet önskade försök och kör det på alla kärnor
Denna datorn som jag skriver detta på, Dell XPS 15, har 6 kärnor vilket är rätt gott. 12 hade vart optimalt.
Kan man komma in på universitetets linuxmaskiner kan man köra över natten, tiotals
om inte hundratals miljoner scheman gissningsvis. 

Lite cursed nu att köra multicore men lagra en variabel self.array som programmet ska mecka med 


Fram över -> för att verkligen krydda effektiviteten,
gör lista med alla index när man ska slumpa ut folk, shuffla och poppa värden. Det är mad value jämfört med nu.
Har lagt in det nu lite lowkey så, men kan säkert bli bättre! Rad 126, den logiska satsen kan nog optimeras lite.

'''

import random
import math
import json
import numpy as np
import time
import csv
# För multiprocessing
import concurrent.futures as future
import os

class FHR:
    '''
    Klass som innehåller allt godis som hanterar Femma-hos-rundan.
    '''
    def __init__(self, participants_dict, stops):

        if type(participants_dict) is str:
            # We have been given file_path, read from form
            self.addresses, self.participants_dict = self.read_form(participants_dict)
        else:
            self.participants_dict = participants_dict
        print(self.participants_dict)
        self.stops = stops; 
        # Gruppstorleken är i det optimala fallet optimalt antal stopp
        self.group_size =  stops
        # Antal hosts per stopp blir följande: 
        self.num_hosts = len(self.participants_dict) // stops
        self.participants_list = list(self.participants_dict.keys())
        # Börja med tomt schema
        self.best_schedule = {'schedule': [], 'iteration' : 0, 'score': 0}
        # schedule_array = make_schedule(schedule_array)
        # print_array(schedule_array)
        # print(evaluate(schedule_array))

    def __str__(self):
        '''Gör så att man kan kalla print med en instans
        av denna klass som parameter.
        '''
        string = self.array_to_str(self.best_schedule['schedule'])
        string += "\nPoäng: " + str(best_result['score'])
        string += "\nHittades i iteration: " + str(best_result['iteration'])
        return string

    def array_to_str(self,array):
        '''Skapar en sträng representation av ett schema
        '''
        string = ''
        for list in array:
            string += str(list) + '\n'
        return string

    def read_form(self, file_path):
        '''Läser in deltagare från svarsfil från google forms.
        '''
        participants_dict = {}
        addresses = {}
        with open(file_path, 'r') as file:
            reader = csv.reader(file)
            # Första raden är titlar på frågorna.
            for row in reader:
                # Första kolonnen är tidsstämpel, man ska ha plats, adress och namn.
                if not row[-1].isdigit():
                    continue
                assert len(row[1:]) == 3
                participants_dict[row[1] + ", " + row[-1]] = row[-1]
                addresses[row[1]] = row[2] 

        return addresses, participants_dict 
            

    def assign_host(self, host, i):
        '''Placerar ut en host under ett stopp på
        dennes egna adress så att hen är garanterat
        hemma då folk har dennes hem som stopp.
        array är schemat, i är kolonnen eller stoppet i schemat
        '''
        for k in range(len(self.array)):
            if self.array[k][0] == host:
                self.array[k][i] = host
        return self.array

    def assign_to_host(self, host, i, random_places):
        '''Placerar ut slumpmässiga deltagare (participants_list) till angiven
        host (host) vid angivet stopp (i) i angivet schema (array)
        '''
        for k in range(self.group_size - 1):
            random_place = random_places.pop()
            self.array[random_place][i] = host
        return self.array

    def make_empty_schedule(self,):
        '''Gör ett tomt schema med bara namnkolonnen ifylld.
        '''
        array = []
        for i in range(len(self.participants_dict)):
            array.append([])
            for j in range(self.stops + 1): 
                if j == 0: 
                    array[i].append(list(self.participants_dict.keys())[i])
                else:
                    array[i].append("")
        return array

    def make_schedule(self):
        '''Slumpar fram ett schema
        '''
        self.array = self.make_empty_schedule()

        # Blanda listan 
        random.shuffle(self.participants_list)
       
        for i in range(1, self.stops + 1):
            for j in range(0, self.num_hosts):
                # Placerar ut de som ska hosta hos dem själva först.
                host = self.participants_list[j + ((i-1)*self.num_hosts)]
                self.array = self.assign_host(host, i)
                # Placera sedan ut resten.
                
            col = [row[i] for row in self.array]
            # Tar fram de platser som är kvar att dela ut
            random_nums = [ind for ind, name in enumerate(col) if name == '']
            random.shuffle(random_nums)

            for j in range(0, self.num_hosts):
                host = self.participants_list[j + ((i-1)*self.num_hosts)]
                self.array = self.assign_to_host(host, i, random_nums[j*(self.group_size - 1): (j+1)*(self.group_size - 1)])
        return self.array
                    

    def evaluate(self, schedule):
        '''Denna metod evaluerar hur bra ett schema faktiskt är.
        Det är i denna metod man styr vad som är viktigt för ett bra schema.
        Ändrar man hur mycket poängavdrag en viss egenskap ger kommer 
        karaktären hos scheman ändras.
        '''
        points = 100
        # Poängavdrag ifall man lämnar sitt område.
        for i in range(len(self.participants_dict)):
            previous_stop = self.participants_dict[schedule[i][0]]
            for j in range(1, self.stops + 1):
                if previous_stop != self.participants_dict[schedule[i][j]]:
                    points -= 1
                previous_stop = self.participants_dict[schedule[i][j]]
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

    def get_best_schedule(self):
        '''Metod som returnerar det bästa funna schemat
        '''
        # Detta är ifall sample inte redan körts.
        if not self.best_schedule['schedule']:
            print("Inget schema genererat!")
            num_of_its = input("Vill du generera? Ange antar iterationer om ja annars 0.")
            return self.sample(num_of_its)
        else:
            return self.best_schedule

    def find_schedule(self, number):
        '''Metod som tar fram number antal scheman och 
        väljer ut det bästa. Den returnerar schemat, i vilken iteration
        det hittades och vilken poäng det fick. find_schedule agerar 
        samordnings 
        '''
        schedule = []
        best_schedule = []
        # Loop som evaluerar kvaliten på ett schema.
        score = 0
        iteration_found = 1
        it = 0
        best_score = 0
        while it < number:
            # Gör ett schema
            schedule = self.make_schedule()
            # Ge poäng
            score = self.evaluate(schedule)
            # Om det bästa, kom ihåg det!
            if score > best_score:
                iteration_found = it
                best_schedule = schedule
                best_score = score
    
            it += 1
        return {'schedule': best_schedule, 'iteration': iteration_found, 'score': best_score}


    def sample(self, number):
        # Hämtar antal kärnor på datorn för att veta hur många processer
        # man ska dela upp programmet på.
        cores = os.cpu_count()
        # Använder modulen concurrent.futures för att hantera MP.
        with future.ProcessPoolExecutor() as ex:
            # Antal iterationer av schema funktionen per process
            sub_num = number // cores
            # Lägger dessa i en lista för att använda map-funktionen
            sub_nums = [sub_num for _ in range(cores)]
            # Lägger till eventuell rest i ettan för att det ändå ska vara exakt
            sub_nums[0] += number % cores
            # Vi kör över alla kärnor. Detta tar upp 100% av CPU:n
            results = ex.map(self.find_schedule, sub_nums)
            # Loopar över alla resultat och hämtar det bästa.
            for index, result in enumerate(results):
                if result['score'] > self.best_schedule['score']:
                    self.best_schedule = result
                    self.best_schedule['iteration'] += sum(sub_nums[0:index + 1])
        
            return self.best_schedule


if __name__ == '__main__':

    start_time = time.time()
    '''
    participants_dict = {
        "Martin": "Kantorn",
        "Majd": "Flogsta",
        "Linda": "Flogsta",
        "Alex": "Rackis",
        "Tyra A": "Kantorn",
        "Melker": "Rackis",
        "Alva": "Rackis",
        "Clas": "Kantorn",
        "Joar": "Flogsta",
        "Tyra S": "Kantorn",
        "Sofia": "Rackis",
        "Mattias": "Flogsta",
        "Oskar" : "Flogsta",
        "Emil" : "Kantorn",
        "Alice" : "Rackis",
        "Johan" : "Kantorn"
    }
    '''
    # Tar fram hundra olika slumpade listor och väljer bästa alternativet.
    # Fungerar just nu bara för 3.
    participants_dict = "C:/Users/marti/Downloads/Femma fucking rundan.csv/Femma fucking rundan.csv"
    femma = FHR(participants_dict, stops = 3)
    best_result = femma.sample(1000)
    print(femma)
    print(f"Det tog {time.time() - start_time} sekunder")