# Cykelfest python - edition.

'''
Här ska en liten förklaring av koden ligga.

I schemat som skrivs ut så är första kolonnen 
namn på alla deltagande och på den raden i de övriga
kolonnerna står det vilka stopp de har. Indata till 
detta program är ett exceldokument. Koden slumpar sedan 
en massa scheman av vilka den sedan väljer den som är
bäst ur ett antal aspekter. Sedan så skapar den en massa
personliga mail som den till sist skickar ut till de 
anmälda. För detta används klassen MailSender.

Konfigurationsparametrar ligger i klassen Settings. 
Den kan användas för att lätt ändra grejor utan att
behöva gå in på massa ställen i CKL-klassen.


Att göra: Så att find_schedule också ta ett godtyckligt dictionary som input 
så att man ka ge make_groups-grupper till den.

'''
from re import S
import time
import random
import os
import pandas as pd
import concurrent.futures as future
from mailsender import MailSender
from settings import Settings
import keyboard
from pprint import pprint


class CKL:
    '''
    Klass som innehåller allt godis som hanterar Femma-hos-rundan.
    '''
    def __init__(self, participants_dict: dict, stops: int):

        self.settings = Settings()
        if type(participants_dict) is str:
            # We have been given file_path, read from form
            self.participants_dict = self.read_form(participants_dict)
        else:
            self.participants_dict = participants_dict
        self.stops = stops; 
        # Gruppstorleken är i det optimala fallet optimalt antal stopp
        self.group_size =  stops
        # Antal hosts per stopp blir följande: 
        self.num_hosts = len(self.participants_dict) // stops
        self.participants_list = list(self.participants_dict.keys())
        # Börja med tomt schema
        self.best_schedule = {'schedule': [], 'iteration' : 0, 'score': -999}
        # Områden med best byten



    def __str__(self) -> str:
        '''Gör så att man kan kalla print med en instans
        av denna klass som parameter.
        '''
        string = self.array_to_str(self.best_schedule['schedule'])
        string += "\nPoäng: " + str(self.best_schedule['score'])
        string += "\nHittades i iteration: " + str(self.best_schedule['iteration'])
        return string

    def array_to_str(self, array: list) -> str:
        '''Skapar en sträng representation av ett schema
        '''
        string = ''
        for list in array:
            string += str(list) + str(self.give_row_points(list)) + '\n'
        return string

    def read_form(self, file_path: str) -> dict:
        '''Läser in deltagare från svarsfil från google forms.
        '''
        participants_dict = {}
        data = pd.read_excel(file_path, dtype = {self.settings.phone_column: str}, engine = 'openpyxl')
        # Första raden är titlar på frågorna.
        for _, row in data.iterrows():
            # Första kolonnen är tidsstämpel, man ska ha plats, adress och namn.
            # Number of data entries
            try:
                assert len(row[1:]) == self.settings.data_points
            except:
                print("Form doesn't match setting, the length is:", len(row[1:]))
                quit()
            participants_dict[row[self.settings.name_index]] = self.settings.get_data(row)
            #print(row)

        return participants_dict 
    

    def make_empty_schedule(self, participants_dict) -> list:
        '''Gör ett tomt schema med bara namnkolonnen ifylld.
        '''
        array = []
        for i in range(len(participants_dict)):
            array.append([])
            for j in range(self.stops + 1): 
                if j == 0: 
                    # Här hamnar namnen på deltagande
                    array[i].append(list(participants_dict.keys())[i])
                else:
                    array[i].append("")
        return array

    def make_schedule(self, participants_dict) -> list: 
        '''Slumpar fram ett schema
        '''
        self.array = self.make_empty_schedule(participants_dict)
        participants_list = [row[0] for row in self.array]
        num_hosts = len(participants_dict) // self.stops
        # Ta fram de som tackat ja till sista stoppet
        last_stoppers = [part for part in participants_list if self.participants_dict[part]["last_stop"] == 'Ja']
        nbr = len(last_stoppers)
        # Ta fram resten
        the_rest = list(set(participants_list)-set(last_stoppers))
        # Blanda upp
        random.shuffle(the_rest)
        random.shuffle(last_stoppers)

        if num_hosts - nbr > 0:
            # Fyll på med self.num_hosts-nbr antal personer
            for _ in range(num_hosts - nbr):
                last_stoppers.append(the_rest.pop())
        else:
            for _ in range(nbr - num_hosts):
                the_rest.append(last_stoppers.pop())

        first_col = [row[0] for row in self.array]

        # Placera ut alla på sista stoppet
        for i, part in enumerate(first_col):
            if part in last_stoppers:
                self.array[i][-1] = part

        # Placera ut resten av alla hosts.
        for i in range(1, self.stops):
            for _ in range(num_hosts):
                host = the_rest.pop()
                self.array[first_col.index(host)][i] = host

        for i in range(1, self.stops + 1):

            col = [row[i] for row in self.array]
            # Tar fram de platser som är kvar att dela ut
            random_nums = [ind for ind, name in enumerate(col) if name == '']
            hosts = [name for ind, name in enumerate(col) if name != ''] 
            random.shuffle(random_nums)
            hosts_w_index = {host : random_nums[(self.stops - 1)*i:(self.stops - 1)*(i + 1)] for i, host in enumerate(hosts)}

            for host, indices in hosts_w_index.items():
                for index in indices:
                    self.array[index][i] = host

        return self.array
                    

    def evaluate(self, schedule: list) -> int:
        '''Denna metod evaluerar hur bra ett schema faktiskt är.
        Det är i denna metod man styr vad som är viktigt för ett bra schema.
        Ändrar man hur mycket poängavdrag en viss egenskap ger kommer 
        karaktären hos scheman ändras.
        '''
        points = 100
        # Poängavdrag ifall man lämnar sitt område.
        for i in range(len(schedule)):
            previous_stop = schedule[i][0]
            for j in range(1, self.stops + 1):
                # Här hämtar man straffet från ett evenutellt områdesbyte
                points -= \
                    self.settings.areas\
                        [self.participants_dict[previous_stop]['area']]\
                        [self.participants_dict[schedule[i][j]]['area']]

                # Här delar man ut pluspoäng ifall hosten sagt att de gärna har sista stoppet
                if j == self.stops and\
                    self.participants_dict[schedule[i][j]]['last_stop'] == 'Ja':
                    points += self.settings.last_stop_points
                
                    
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

    def get_best_schedule(self) -> list:
        '''Metod som returnerar det bästa funna schemat
        '''
        # Detta är ifall sample inte redan körts.
        if not self.best_schedule['schedule']:
            print("Inget schema genererat!")
            num_of_its = input("Vill du generera? Ange antal iterationer om ja annars 0.")
            return self.sample(num_of_its)
        else:
            return self.best_schedule

    def schedule_w_groups(self):
        '''Metod som tvingar ut folk på deras
        valda områden.
        '''
        get_dict = lambda group: {name: self.participants_dict[name] for name in group}
        rest_approved = 'n'
        its = 10000
        best_rest_score = 0
        best_rest = {}
        while rest_approved not in ['y', 'c']:
            groups, rest = self.make_groups()
            # Ger möjligheten att utvärdera rest-schemat.
            rest_dict = get_dict(rest)
            rest_sch = self.find_schedule(its, rest_dict)['schedule']
            score = self.evaluate(rest_sch)
            print(self.array_to_str(rest_sch), f"\nScore: {score}")
            if score > best_rest_score:
                best_rest = rest_sch
            rest_approved = input('Är resten ok? Ge c för att använda bästa hittils. (y/c/n)\n\t::: ')
            if rest_approved == 'y':
                # Sätt senaste till bästa
                best_rest = rest_sch
            # Schedule to which all groups will be appended.
        sch = []
        for group in (list(groups.values())):
            group_dict = get_dict(group)
            sch += self.find_schedule(its, group_dict)['schedule']
        # Lägger på resten.
        sch += best_rest
        return {'schedule' : sch, 'score' : self.evaluate(sch)}
        

    def find_schedule(self, number: int, participants_dict = None) -> dict:
        '''Metod som tar fram number antal scheman och 
        väljer ut det bästa. Den returnerar schemat, i vilken iteration
        det hittades och vilken poäng det fick. find_schedule agerar 
        samordnings 
        '''
        if participants_dict is None:
            participants_dict = self.participants_dict
        schedule = []
        # Loop som evaluerar kvaliten på ett schema.
        score = 0
        iteration_found = 1
        it = 0
        best_score = -999
        while it < number: #and best_score < 400:
            # Gör ett schema
            schedule = self.make_schedule(participants_dict)
            # Ge poäng
            score = self.evaluate(schedule)
            # Om det bästa, kom ihåg det!
            if score > best_score:
                iteration_found = it
                best_schedule = schedule
                best_score = score
    
            it += 1
            

        return {'schedule': best_schedule, 'iteration': iteration_found, 'score': best_score}

    def give_row_points(self, row: list) -> int:
        '''För att ge en enskild rad poäng.
        '''
        temp_points = 0
        previous_stop = row[1]
        for j in range(1, self.stops + 1):
            # Här hämtar man straffet från ett evenutellt områdesbyte
            temp_points -= \
                self.settings.areas\
                    [self.participants_dict[previous_stop]['area']]\
                    [self.participants_dict[row[j]]['area']]
            previous_stop = row[j]
            ############# TEST
            # Här delar man ut pluspoäng ifall hosten sagt att de gärna har sista stoppet
            if j == self.stops and\
                self.participants_dict[row[j]]['last_stop'] == 'Ja':
                ######## TEST
                temp_points += self.settings.last_stop_points
        return temp_points

    def get_pref(self, schedule, row: list, pref: str) -> str:
        '''Hämtar preferenser som gäster har på visst stopp.
        '''
        host = row[0]
        index = row[1:].index(host) + 1
        # Fixa mat/alk med listcomp.
        prefs = [self.participants_dict[part[0]][pref] for part in schedule if (part[index] == host)]
        # print(prefs)
        # För att bli av med [ & ]
        return str(prefs)[1:-1].replace('nan', '')

    def make_groups(self) -> tuple:
        '''Groups people by area
        '''
        groups = {}
        for area in self.settings.areas.keys():
            groups[area] = [person for person in \
                self.participants_dict.keys() if self.participants_dict[person]['area'] == area]
        # Get rest
        rest = []
        for group, participants in groups.items():
            if len(participants) % self.stops != 0:
                random.shuffle(participants)
                for _ in range(len(participants) % self.stops):
                    rest.append(groups[group].pop())
        return groups, rest
        

    def send_route_mail(self, sch: dict) -> bool:
        '''Skapar och skickar mail som passar schemat schedule
        '''
        # Hämtar schema-arrayn
        schedule = sch['schedule']
        # Detta dictionary innehåller textstycken som ska ersättas och en funktion som 
        # hämtar texten de ska ersättas med.
        # tele1, tele2, tele3 osv hade man kunnat göra mer generellt.
        fill_ins = {'[stopp1]': lambda x: self.participants_dict[x[1]]['adress'],
        '[stopp2]' :  lambda x: self.participants_dict[x[2]]['adress'],
        '[stopp3]' :  lambda x: self.participants_dict[x[3]]['adress'],
        '[foodpreference]' : lambda x: self.get_pref(schedule, x, 'food')[1:-1].replace("'", ''),
        '[alcoholpreference]' : lambda x: self.get_pref(schedule, x, 'alcohol')[1:-1].replace("'", ''),
        '[tele1]' : lambda x: self.participants_dict[x[1]]['phone'],
        '[tele2]' : lambda x: self.participants_dict[x[2]]['phone'],
        '[tele3]' : lambda x: self.participants_dict[x[3]]['phone']}
        
        mails = {self.participants_dict[row[0]]['mail'] : '' for row in schedule}

        for row in schedule:
            current_mail = self.settings.mail_template
            for key, func in fill_ins.items():
                current_mail = current_mail.replace(key, str(func(row)))
            mails[self.participants_dict[row[0]]['mail']] = current_mail
        # This is the dangerous one...
        return self.send_mails(mails)
    
    def save_as_txt(self, schedule: list) -> None:
        '''Saves a text copy of the schedule
        '''
        with open(self.settings.textfilename, 'w') as f:
            for row in schedule:
                f.write(str(row) + str(self.give_row_points(row)) + '\n')


    def send_confirmation_mail(self) -> bool:
        '''Skickar bekräftelsemail till alla deltagare
        '''        
        mails = {data['mail']: self.settings.confirmation_mail\
            for data in self.participants_dict.values()}
        #return self.send_mails(mails)
            
    def send_mails(self, mails: dict, subject = None) -> bool:
        '''Implementerar MailSenderklassen för att skicka mailen
        i mails-variabeln
        '''
        if subject is None:
            subject = self.settings.mail_subject
        s = MailSender(self.settings.password, self.settings.sender_email)
        return s.bulk_send(mails, subject = subject)



    def sample(self, number: int) -> dict:
        '''sample är den funktion man kallar på för att få ett schema.
        Man anger antal "samples" väjla det bästa ifrån så skapar datorn
        number antal scheman och returnerar det bästa.
        '''

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

    #-------------------- Filsökväg ------------------------

    path = os.path.dirname(os.path.abspath(__file__)) + '/' + input('Filnamn: ')

    #-------------- With or without groups -----------------

    groups = (input("Områdesgruppering? (y/n)") == 'y')

    #----------------Number of iterations-------------------

    stops = int(input("Antal stopp: "))

    #----------------Number of iterations-------------------

    num = int(input("Antal samples? "))
    
    #-------------------------------------------------------

    ckl = CKL(path, stops)
    ok = ''
    if groups:
        best_result = ckl.schedule_w_groups()
    else:
        best_result = ckl.sample(num)
        # Tvingar ut grupper i deras områden
        #best_result, score = ckl.schedule_w_groups()
        #print(time.time() - start)
    while ok not in ['y', 'n']:
        print(ckl.array_to_str(best_result['schedule']))
        print(f"\nBetyg: {best_result['score']}")
        ok = input("Vill du söka efter namn, skriv s. Annars bekräftar du schema med (y/n)\n\t::: ")
        while ok == 's':
            name = input('Vems rutt vill du se? ')
            participating = [row[0] == name for row in best_result['schedule']]
            if name == 'q':
                ok = input("OK? (y/n)")
            elif any(participating):
                for index, boolean in enumerate(participating):
                    if boolean:
                        print(f"Rutt: {best_result['schedule'][index]}")
            elif not any(participating):
                print("Ingen med det namnet i schemat")
                

    #print(len(ckl.participants_list))
    #print(ckl.participants_dict.values())
    #ckl.send_confirmation_mail()
    #ckl.make_groups()
    #start = time.time()

    if ok.lower() == 'y':
        result = ckl.send_route_mail(best_result)
        if result:
            print("Alla mail skickade.")
            ckl.save_as_txt(ckl.best_schedule['schedule'])
        else:
            print("Mailutskick misslyckades.")  