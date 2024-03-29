import os
from ckl import CKL

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