import concurrent.futures
import os
import requests
from bs4 import BeautifulSoup

#pobieranie wszystkich zdjec z głównej strony www.wykop.pl używając wielowątkowości,
#które znacznie skraca czas pobierania wielu zdjęć


def zdjecie(image):
    #jeśli folder nie istnieje stwórz go:
    if not os.path.isdir("wykop"):
        os.mkdir("wykop")
    #zdjęcia na stronie mają 2 różne tagi HTML "src" lub "data-original"
    try:
        with open(f"wykop/{image['src']}", 'wb') as f:
            f.write(requests.get(image["src"].replace('/', '').replace(':', '')).content)
    except Exception:
        try:
            with open(f"wykop/{image['data-original'].replace('/', '').replace(':', '')}", 'wb') as f:
                f.write(requests.get(image["data-original"]).content)
        except Exception:
            pass


#start = time.perf_counter()
try:
    source = requests.get("https://www.wykop.pl/mikroblog/hot/ostatnie/6/").text
except Exception:
        print("Błąd w pobieraniu kodu strony")
else:
    soup = BeautifulSoup(source, "lxml")
    images = soup.find_all("img")

    with concurrent.futures.ThreadPoolExecutor() as ex:
        ex.map(zdjecie, images)

#stop = time.perf_counter()
#print(stop - start)

#usuwanie pobranych plików
# for x in os.listdir("wykop"):
#     os.remove(f"wykop/{x}")
