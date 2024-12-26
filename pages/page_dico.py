import streamlit as st
import json
from difflib import SequenceMatcher
from pages import menu_sidebar

st.session_state["current_page"] = "Dictionnaire"
menu_sidebar.show_menu()

# Ajout d'informations sur l'utilisation
with st.sidebar:
    st.divider()
    with st.expander("**Utilisation** ⚙️", True):
        st.markdown("""
        1. Choisissez l'onglet selon la langue de recherche
        2. Tapez le mot ou une partie du mot
        3. Les résultats s'afficheront automatiquement
        """)


def charger_dictionnaire(chemin_fichier):
    """
    Charge le dictionnaire depuis un fichier JSON
    """
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def calculer_similarite_phrase(phrase1, phrase2):
    """
    Calcule la similarité entre deux phrases en comparant les mots individuels.
    Retourne une moyenne des similarités entre les mots.
    """
    mots1 = phrase1.split()
    mots2 = phrase2.split()
    total_similarite = 0
    nb_comparaisons = 0
    
    for mot1 in mots1:
        for mot2 in mots2:
            total_similarite += SequenceMatcher(None, mot1, mot2).ratio()
            nb_comparaisons += 1

    # Éviter la division par zéro
    return total_similarite / nb_comparaisons if nb_comparaisons > 0 else 0

def trier_par_correspondance(resultats, recherche):
    """
    Trie les résultats en fonction de la correspondance avec le mot ou la phrase recherchée.
    """
    return sorted(
        resultats.items(),
        key=lambda item: calculer_similarite_phrase(recherche, item[0]),
        reverse=True
    )
def rechercher_mot(dictionnaire, recherche, mode='arabe'):
    """
    Recherche un mot dans le dictionnaire
    mode: 'arabe' pour chercher dans les mots arabes
          'francais' pour chercher dans les traductions
    """   

    resultats = {}
    recherche = recherche.lower().strip()
    
    if mode == 'arabe':
        # Recherche dans les mots arabes
        for mot, details in dictionnaire.items():
            if recherche in mot.lower():
                resultats[mot] = details
    else:
        # Recherche dans les traductions françaises
        for mot, details in dictionnaire.items():
            if recherche in details['traduction'].lower():
                resultats[mot] = details
    
    return resultats

st.title("🔍 Dictionnaire Français-Tunisien")

# Chargement du dictionnaire
dictionnaire = charger_dictionnaire('ressource/dico.json')

# Création des onglets
tab1, tab2 = st.tabs(["Rechercher en français",  "Rechercher en tunisien"])

with tab2:
    # Interface de recherche en arabe
    recherche_arabe = st.text_input("Rechercher un mot en tunisien:", key="recherche_arabe")
    if recherche_arabe:
        resultats = rechercher_mot(dictionnaire, recherche_arabe, mode='arabe')
        if resultats:
            # Trier les résultats par correspondance avec le mot ou la phrase recherchée
            resultats_tries = trier_par_correspondance(resultats, recherche_arabe)
            for mot, details in resultats_tries:
                with st.expander(f"{details['traduction']} - {mot}"):
                    st.write(f"**Type:** {details['type']}")
                    st.write(f"**Genre:** {details['genre']}")
        else:
            st.warning("Aucun résultat trouvé")
with tab1:
    # Interface de recherche en français
    recherche_francais = st.text_input("Rechercher un mot en français:", key="recherche_francais")
    if recherche_francais:
        resultats = rechercher_mot(dictionnaire, recherche_francais, mode='francais')
        if resultats:
            # Trier les résultats par correspondance avec le mot ou la phrase recherchée
            resultats_tries = trier_par_correspondance(resultats, recherche_francais)
            for mot, details in resultats_tries:
                with st.expander(f"{details['traduction']} - {mot}"):
                    st.write(f"**Type:** {details['type']}")
                    st.write(f"**Genre:** {details['genre']}")
        else:
            st.warning("Aucun résultat trouvé")

