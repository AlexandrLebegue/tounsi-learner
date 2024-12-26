import requests
from time import sleep
from bs4 import BeautifulSoup
import time
import json
import random
class Mot_Translated:
    def __init__(self, mot_arabe="", traduction_francais="", genre="", type=""):
        """
        Initialise un mot avec ses attributs (valeurs par défaut : chaînes vides).
        
        :param mot_arabe: Le mot en arabe (str)
        :param traduction_francais: Traduction en français (str)
        :param genre: Genre grammatical (ex: masculin, féminin) (str)
        :param type: Type du mot (ex: nom, verbe, adjectif) (str)
        """
        self.mot_arabe = mot_arabe
        self.traduction_francais = traduction_francais
        self.genre = genre
        self.type = type

    def __repr__(self):
        """
        Retourne une représentation lisible de l'objet.
        """
        return (f"Mot(mot_arabe='{self.mot_arabe}', traduction_francais='{self.traduction_francais}', "
                f"genre='{self.genre}', type='{self.type}')")

    def afficher_details(self):
        """
        Affiche les détails du mot.
        """
        print(f"Mot arabe       : {self.mot_arabe}")
        print(f"Traduction (FR) : {self.traduction_francais}")
        print(f"Genre           : {self.genre}")
        print(f"Type            : {self.type}")

    def to_json(self):
        """
        Exporte l'objet sous forme de dictionnaire JSON dans le format attendu.
        """
        return f""" "{self.mot_arabe}": 
        {{
            "traduction": "{self.traduction_francais}",
            "type": "{self.type}",
            "genre": "{self.genre}"
        }},\n"""
        

# Liste des mots à parcourir
mots = [
    "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "3", "5", "7", "9"
]


# URL de base
base_url = "https://www.arabetunisien.com/dictionnaire-tunisien-francais/"


# Écrire la liste dans un fichier JSON
with open("mots.json", "a+", encoding="utf-8") as fichier:
    fichier.write("{\n")


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
                if str(a_tag['href']).find("/traduction/TN") != -1:
                    word_url = a_tag['href']
                    full_url = f"https://www.arabetunisien.com{word_url}"

                    try:
                        
                        # Récupérer le contenu de la page liée
                        word_response = requests.get(full_url)
                        word_response.raise_for_status()
                        word_content = word_response.text
                        print(full_url)
                        # Parser le contenu HTML pour extraire les balises <li>
                        soup = BeautifulSoup(word_content, 'html.parser')
                        row = soup.find_all('tr',class_='noTopLineSeparation')[0]
                        
                        # Extraire les données
                        mot_arabe = row.find('b').text.strip()
                        try:
                            genre_et_type = row.find('span', class_='abr').text.strip()
                        except:
                            genre_et_type = "none"
                           
                        traduction = row.find_all('a')[1].text.strip()

                        # Mapping pour le genre et le type
                        def extraire_genre_et_type(abr):
                            genre = ""
                            type_mot = ""
                            if "n." in abr:
                                type_mot = "nom commun"
                            elif "adj" in abr:
                                type_mot = "adjectif"
                            else:
                                type_mot = "none"
                            if "masc" in abr:
                                genre = "masculin"
                            elif "fem" in abr:
                                genre = "féminin"
                            else:
                                genre = "none"

                            return genre, type_mot

                        # Appliquer le mapping
                        genre, type_mot = extraire_genre_et_type(genre_et_type)

                        # Créer un objet Mot
                        mot = Mot_Translated(mot_arabe=mot_arabe, traduction_francais=traduction, genre=genre, type=type_mot)
                        
                        # Écrire la liste dans un fichier JSON
                        with open("mots.json", "a+", encoding="utf-8") as fichier:
                            fichier.write(mot.to_json())
                        print(f"AJOUT MOOOT {mot}")
                        time.sleep(random.uniform(0.5, 2))
                    
                    except requests.exceptions.RequestException as e:
                        print(f"Erreur lors de la récupération de la page liée {full_url}: {e}")
                    except:
                        print(f"Echec pour récuperation du mot {word_url}")
                        time.sleep(random.uniform(0.5, 2))
                        continue

        
    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération de la page {mot}: {e}")


    # Pause entre les requêtes pour éviter de surcharger le serveur
    sleep(2)

    with open("mots.json", "a+", encoding="utf-8") as fichier:
        fichier.write("}")
