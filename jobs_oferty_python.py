import requests
from bs4 import BeautifulSoup
import datetime



#pobieranie ze strony www.jobs.pl podstawowych informacji o ogłoszeniach związanych z wyszukiwaniem frazy "python"
'''przykład:
           Tytuł: Mid Python Developer
           Firma: TeamQuest Sp. z o.o.
           Lokacja: Wrocław (dolnośląskie)
           Detale: Specjalista (Mid/Regular), Pełny etat
           Data publikacji: 12.12.2022
           Do końca oferty: 28 dni, 15 godzin 04 minut 02 sekund
           Link: https://www.jobs.pl/-mid-python-developer--oferta-3552776'''

try:
    source_pages = BeautifulSoup(requests.get("https://www.jobs.pl/oferty/python;k").text,"lxml")
    #pobieranie indeksu każdej strony zawierjącej oferty
    pages = source_pages.find("div", class_="pagination").text
    pages_list = []
    for x in pages:
        try:
            pages_list.append(int(x))
        except ValueError:
            pass
    print(pages_list)
except Exception:
    print("Couldn't load page")
else:
    for x in pages_list:
        #oferty podzielone są na kilka stron więc link musi zostać modyfikowany w zależności od indeksu strony
        source = requests.get(f"https://www.jobs.pl/oferty/python;k/p-{x}").text
        soup = BeautifulSoup(source,"lxml")
        all_jobs = soup.find("div",class_="grid-col-75 grid-col-padding-0-10 offers-list-box")
        jobs = all_jobs.find_all("div",{"class":["offer-border offer is-just-refreshed","offer-border offer"]})
        #pobieranie informacji/odpowiednie formatowanie danych
        for job in jobs:
            title = job.find("div",class_="offer-title").a.text.strip()
            employer = job.find("p",class_="offer-employer").text
            offer_location = job.find("p",class_="offer-location").text
            link = "https://www.jobs.pl/"+job.find("div",class_="offer-title").a["href"]
            offer_page = requests.get(link).text
            details = BeautifulSoup(offer_page,"lxml").find("div",class_="offer-view-details offer-border")
            try:
                detail = details.find("div","offer-view-all-details").text
            except Exception:
                detail = "Unknown"

            #odpowiednie formatowanie dat i obliczanie czasu pozostałego do kónca oferty"
            date_description = details.find("div",class_="grid-col-30 offer-view-labels has-icon has-calendar-icon")
            date = date_description.find("span",class_="offer-view-label-value js-counter-clock")
            a = datetime.datetime.today()
            time_str = date["clock_data"]
            tformat = "%Y/%m/%d %H:%M:%S"
            b = datetime.datetime.strptime(time_str, tformat)
            delta = b - a
            delta = str(delta).split(",")
            days = delta[0].strip().replace("days","dni")
            time = delta[1].split(":")
            hours = time[0].strip()
            minutes = time[1]
            seconds = time[2][:2]
            date_description_text = str(date_description.text).strip() + f" {days}, {hours} godzin {minutes} minut {seconds} sekund"
            #wyświetlanie zebranych danych o ofercie
            print(f"Tytuł: {title}")
            print(f"Firma: {employer}")
            print(f"Lokacja: {offer_location}")
            print(f"Detale: {detail}")
            print(date_description_text)
            print(f"Link: {link}")
            print()
