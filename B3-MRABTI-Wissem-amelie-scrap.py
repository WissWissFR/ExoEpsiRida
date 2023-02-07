import requests
from bs4 import BeautifulSoup
import csv
import re

payload = {
    "type": "ps",
    "ps_profession": "34",
    "ps_profession_label": "Médecin généraliste",
    "ps_localisation": "HERAULT (34)",
    "localisation_category": "departements",
}

url = "http://annuairesante.ameli.fr/recherche.html"
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}

req = requests.Session()
page = req.post(url, params=payload, headers=header)

if page.status_code == 200:
    lienrecherche = page.url

soup = BeautifulSoup(page.text, 'html.parser')

professionals = soup.find_all("div", class_="nom_pictos")

data = []

def scrap_all(text):
    for professional in professionals:
        name = professional.find("a").text.strip()
        tel = "".join(re.findall(r"\d+", professional.find_next("div", class_="item left tel").text))
        address = professional.find_next("div", class_="item left adresse").text.strip().replace("\n", " ")
    
        data.append([name, tel, address])
        # print(name + " ; " + tel + " ; " + address)

    with open("professionals.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Name", "Phone Number", "Address"])
        writer.writerows(data)
        
for i in range(20):
   page = req.get('http://annuairesante.ameli.fr/professionnels-de-sante/recherche/liste-resultats-page-'+str(i+1)+'-par_page-20-tri-aleatoire.html')
   print(page.url)
   print(data)
   scrap_all(page.text)
   
