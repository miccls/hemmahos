# Cykelschema-program   
## Vad måste man göra?
### 0
Klona detta repo på valfri plats.
Fixa email och lösenord som du skriver in i $\texttt{settings.py}$ på rader 92, 93.
### 1
Fixa Google-forms-formulär med följande information:
* Värdens namn
* Värdens adress
* Värdens telefonnummer
* Matpreferenser för de som anmäler sig
* Alkoholpreferenser -||-
* Område man bor i. De som ska vara med finns som nycklar i dictionary:t som heter $\texttt{areas}$ i $\texttt{settings.py}$ filen. De måste vara stavade på samma sätt.
* Om man kan tänka sig ha sista stoppet (valfritt)
### 2
Ladda ner formulärsvaren som excel-fil. Se till att antalet deltagare är delbart med 3.
### 3
Anpassa $\texttt{settings.py}$ efter formuläret ni gjort och uppdatera $\texttt{self.mailtemplate}$.
Se också till att alla mailadresser i formuläret är korrekta, om inte kommer de inte få ett mail och några kommer bli utan rutt (man kan ju såklart gå in och kolla i skickade mail och kopiera mailet och skicka till rätt adress men jobbigt ju).

### 4
Kör filen $\texttt{ckl.py}$ och följ instruktionerna i terminalen. __VAR FÖRSIKTIG MED ATT TRYCKA IGENOM ALLT SNABBT FÖR DÅ SKICKAR MAIL MED RUTTER UT__. 
När du fått en rutt du är nöjd med kan man gå vidare.
### 5
Programmet skickar nu ut alla mail och du är färdig, ha så kul!
