from datetime import datetime
import os
import time
import requests
from bs4 import BeautifulSoup

'''cykliczne, zależnie od ustawionego czasu, zapisywanie prac związanych z pythonem, brane pod uwage są tylko prace
z lokalzacją "Wrocław", nie "dolnośląskie" lub "Krzyki". W pliku są informacje o poszczególnych ofertach i godzina z datą
o której został zapisany plik
przykład:

Job: Trener Programowania dla dzieci i m�odzie�y
Company: Giganci Programowania sp. z o.o.
link: https://www.pracuj.pl/praca/trener-programowania-dla-dzieci-i-mlodziezy-wroclaw,oferta,1002258557
------------------------
Job: Linux Scripting DevOps Working Student with Bash/Python
Company: Nokia
link: https://www.pracuj.pl/praca/linux-scripting-devops-working-student-with-bash-python-wroclaw,oferta,1002258493
------------------------
21/12/2022 14:10:34
'''

def pracuj_oferty():
    #jeśli folder "oferty" nie istnieje, stwórz go:
    if not os.path.isdir("oferty"):
        os.mkdir("oferty")

    check1 = None
    check2 = None
    #by skrypt zadziałał spełnione musi zostac check1 i check2 / beautifulsoup nie zawsze widzi potrzebne tagi HTML
    while None in [check1,check2]:
        print("Loading...")
        time.sleep(1)
        try:
            url = requests.get("https://www.pracuj.pl/praca/python;kw/wroclaw;wp?rd=30").text
            soup = BeautifulSoup(url, "lxml")
            table = soup.find("ul",class_="results__list-container")
            check1 = table
            job_offers = table.find_all("li",class_="results__list-container-item offer-container")
            check2 = job_offers
        except:
            pass
    now = datetime.now()
    #nazwą pliku będzie odpowiednio zformatowana data i czas
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    with open(f"oferty/{dt_string.replace(' ','').replace('/','').replace(':','')}.txt", "w") as f:
        for job_offer in job_offers:
                try:
                    if "Wrocław" in  job_offer.find("li",class_="offer-labels__item offer-labels__item--location").text:
                        job_title = job_offer.find("h2",class_="offer-details__title").text.strip()
                        employer = job_offer.find("p",class_="offer-company").a.text
                        more_info = job_offer.find("h2",class_="offer-details__title").a["href"]

                        f.write(f"Job: {job_title}\n")
                        f.write(f"Company: {employer}\n")
                        f.write(f"link: {more_info}\n")
                        f.write("------------------------\n")

                except ValueError:
                    f.write("Błąd w ofercie")
        f.write(f"{dt_string}\n")
    print("finished")


#skrypt zostanie uruchamiony "limit" razy w odstępie "minutes" minut między każdym uruchomieniem
limit = 2
current = 0
while True:
    pracuj_oferty()
    minutes = 60
    time.sleep(minutes*60)
    current+=1
    if current == limit:
        break
