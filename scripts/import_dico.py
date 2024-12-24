import requests
from time import sleep
from bs4 import BeautifulSoup

# Liste des mots à parcourir
mots = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "3", "5", "7", "9"
]

# URL de base
base_url = "https://www.arabetunisien.com/dictionnaire-tunisien-francais/"

# Parcourir chaque mot de la liste
for mot in mots:
    url = f"{base_url}{mot}"
    print(f"Fetching URL: {url}")
    try:
        # Récupérer le code source de la page
        response = requests.get(url)
        response.raise_for_status()
        html_content = response.text

        # Parser le contenu HTML pour extraire les balises <li>
        soup = BeautifulSoup(html_content, 'html.parser')
        li_elements = soup.find_all('li')

        for li in li_elements:
            a_tag = li.find('a')
            if a_tag and 'href' in a_tag.attrs:
                word_url = a_tag['href']
                full_url = f"https://www.arabetunisien.com{word_url}"
                print(f"Fetching linked URL: {full_url}")

                try:
                    # Récupérer le contenu de la page liée
                    word_response = requests.get(full_url)
                    word_response.raise_for_status()
                    word_content = word_response.text

                    # Sauvegarder le contenu dans un fichier
                    file_name = word_url.split('/')[-1] + ".html"
                    with open(file_name, "w", encoding="utf-8") as file:
                        file.write(word_content)

                    print(f"Contenu de {file_name} sauvegardé avec succès.")
                except requests.exceptions.RequestException as e:
                    print(f"Erreur lors de la récupération de la page liée {full_url}: {e}")

        # Sauvegarder la page principale
        with open(f"page_{mot}.html", "w", encoding="utf-8") as file:
            file.write(html_content)

        print(f"Page {mot} sauvegardée avec succès.")
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page {mot}: {e}")

    # Pause entre les requêtes pour éviter de surcharger le serveur
    sleep(2)
