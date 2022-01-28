

class Settings:

    def __init__(self) -> None:

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
        areas = {'Flogsta' : [0, 5, 2, 1, 3, 2, 2],
            'Kantorn - Väktargatan - Djäknegatan' : [5, 0, 5, 1, 1, 2, 1],
            'Rosendal' : [2, 5, 0, 2, 5, 2, 2],
            'Rackarberget - Studentvägen' : [1, 1, 2, 0, 2, 2, 0],
            'Sala Backe - Gränby' : [5, 1, 5, 2, 0, 1, 2],
            'Fålhagen - Industristaden' : [2, 2, 2, 2, 1, 0, 1],
            'Luthagen' : [2, 1, 2, 0, 2, 1, 0]}
        # Makes a dict with form -> [from][to] = penalty
        self.areas = {area1: {area2 : grade2 for area2, grade2 in zip(areas.keys(), grade1)}\
            for area1, grade1 in areas.items()}

        #----------------- Mailrealterade inställningar ----------------------


        self.mail_template = '\
            <html>\
            <body>\
                <meta charset="utf-8">\
                <h1><span style="color:#0713f0";>Håll </span><span style="color:#006600";>Käften</span> & <span style="color:#f1b434";>Försvinn</span></h1>\
                <p>Här kommer din rutt för kvällen!!<br>\
                Du kommer vara på följande stopp:<br>\
                <br> <strong>18:30 [stopp1]</strong> Tel: [tele1]<br>\
                <strong>19:30 [stopp2]</strong> Tel: [tele2]<br>\
                <strong>20:30 [stopp3]</strong> Tel: [tele3]<br>\
                <br>\
                Då ni serverar har ni följande matpreferenser: <br>\
                [foodpreference] <br>\
                och följande alkoholprefrerenser: <br>\
                [alcoholpreference]\
                </p>\
            </body>\
            </html>\
            '
        self.mail_subject = 'Cykelsittning'
        self.password = 'futftuppen1'
        self.sender_email = 'schemacykelsittning@gmail.com'


        self.textfilename = 'schema.txt'



if __name__ == '__main__':
    s = Settings()