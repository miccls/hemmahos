

class Settings:

    def __init__(self) -> None:
        #------------------------- Kategorilösa inställningar ---------------------
        # FUTF:s swish
        self.swish_number = "123 158 89 46"
        # Pris som visas i bekräftelse mail
        self.price = "40"
        #---------------------- Index för data från formulär ---------------------
        self.name_index = 2
        self.phone_index = 3
        self.mail_index = 4
        self.adress_index = 5
        self.area_index = 6
        self.last_stop_index = 7
        self.food_index = 8
        self.alcohol_index = 9
        self.phone_column = 'Värdens telefonnummer'

        #---------------------- Poäng för evaluering ---------------------
        self.last_stop_points = 5
        areas = {'Flogsta' : [0, 10, 2, 1, 3, 2, 2],
            'Kantorn - Väktargatan - Djäknegatan' : [10, 0, 10, 1, 1, 2, 1],
            'Rosendal' : [2, 10, 0, 2, 10, 2, 2],
            'Rackarberget - Studentvägen' : [1, 1, 2, 0, 2, 2, 0],
            'Sala Backe - Gränby' : [10, 1, 10, 2, 0, 1, 2],
            'Fålhagen - Industristaden' : [2, 2, 2, 2, 1, 0, 1],
            'Luthagen' : [2, 1, 2, 0, 2, 1, 0]}
        # Makes a dict with form -> [from][to] = penalty
        self.areas = {area1: {area2 : grade2 for area2, grade2 in zip(areas.keys(), grade1)}\
            for area1, grade1 in areas.items()}

        #----------------- Mailrealterade inställningar ----------------------

        # Dessa mail kan man ha i textfiler så folk slipper gå in och mecka med koden. 

        self.mail_template = '\
            <html>\
            <body>\
                <meta charset="utf-8">\
                <h1><span style="color:#00A4FF";>Wave</span></h1>\
                <p>Cykelmiddag på fredag!<br>\
                Du kommer vara på följande stopp:<br>\
                <br> <strong>18:30 Förrätt på adress: [stopp1]</strong> Tel: [tele1]<br>\
                <strong>20:00 Varmrätt på adress: [stopp2]</strong> Tel: [tele2]<br>\
                <strong>21:30 Efterrätt på adress: [stopp3]</strong> Tel: [tele3]<br>\
                <br>\
                Då ni serverar har ni följande matpreferenser: <br>\
                [foodpreference] <br>\
                och följande alkoholprefrerenser: <br>\
                [alcoholpreference] <br> <br>\
                Betalning sker till WAVE på 1234264180 och kalaset kostar 40kr per par<br>\
                Märk betalningen med "Det står skrivet i stjärnorna."<br><br>\
                Hoppas ni får en oförglum kväll! <br><br>\
                Puss och kram / KlubbWerket\
                </p>\
            </body>\
            </html>\
            '

        self.confirmation_mail = f'\
            <html>\
            <body>\
                <meta charset="utf-8">\
                <h1><font face="Bauhaus 93" size="20px" color="#07fff0">Way</font><span style="color:#0713f0";>Håll </span><span style="color:#006600";>Käften</span> & <span style="color:#f1b434";>Försvinn</span></h1>\
                <p>Kul att ni har anmält er till cykelsittningen!!<br>\
                För att behålla eran plats och vara med på evenemanget behöver ni bara\
                swisha {self.price}kr ({int(self.price)/2} kr var) till {self.swish_number} med värdens telefon. (Dvs det telefonnummer ni anmälde så vi kan se vem betalningen kommer ifrån)<br>\
                <strong>Betala senast tisdag 1:a februari, betalningar efter det datumet tas inte emot och du förlorar din plats!</strong>\
                </p>\
            </body>\
            </html>\
        '

        self.mysk_mail ='<html>\
            <body>\
                <meta charset="utf-8">\
                <h1><font  color="#00A4FF">WAVE</font> <span style="color:#808080";><br>\
                <p>Grattis, du har fått plats till <span style="color:#07fff0";>W</span>ay out <span style="color:#F1b434";>F</span>eSTS!!<br>\
                Det är sittning på bridgens och temat är <strong>FESTIVAL</strong>!\
                För att behålla din plats och vara med på evenemanget behöver du bara\
                swisha 110 kr till 123 158 89 46 (FUTF). <br>\
                <strong>Betala snarast!!</strong>\
                </p>\
            </body>\
            </html>'
        # Ganska self-explanatory
        self.mail_subject = 'Cykelsittning'
        self.password = 'futftuppen1'
        self.sender_email = 'schemacykelsittning@gmail.com'

        # Namnet på textfilen som innehåller det färdiga schemat.
        self.textfilename = 'schema.txt'

    def get_data(self, row: list) -> dict:
        '''Återger formulärets data som ett dictionary
        '''
        # Har lagt denna metod här då jag tycker att 
        # namnen på alla svar (food, area osv) är lite av en inställning.
        return {'area' : row[self.area_index], 
            'adress' : row[self.adress_index], 
            'mail' : row[self.mail_index], 
            'phone' : row[self.phone_index], 
            'name' : row[self.name_index],
            'food' : row[self.food_index],
            'alcohol' : row[self.alcohol_index],
            'last_stop' : row[self.last_stop_index]}

if __name__ == '__main__':
    s = Settings()