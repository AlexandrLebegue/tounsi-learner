import streamlit as st
import json

def charger_dictionnaire(chemin_fichier):
    """
    Charge le dictionnaire depuis un fichier JSON
    """
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

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

# Configuration de la page Streamlit
st.set_page_config(page_title="Dictionnaire Français-Tunisien")
st.title("🔍 Dictionnaire Français-Tunisien")

# Chargement du dictionnaire
dictionnaire = charger_dictionnaire('ressource/dico.json')

# Création des onglets
tab1, tab2 = st.tabs(["Rechercher en tunisien", "Rechercher en français"])

with tab1:
    # Interface de recherche en arabe
    recherche_arabe = st.text_input("Rechercher un mot en tunisien:", key="recherche_arabe")
    if recherche_arabe:
        resultats = rechercher_mot(dictionnaire, recherche_arabe, mode='arabe')
        if resultats:
            for mot, details in resultats.items():
                with st.expander(f"{mot} - {details['traduction']}"):
                    st.write(f"**Type:** {details['type']}")
                    st.write(f"**Genre:** {details['genre']}")
        else:
            st.warning("Aucun résultat trouvé")

with tab2:
    # Interface de recherche en français
    recherche_francais = st.text_input("Rechercher un mot en français:", key="recherche_francais")
    if recherche_francais:
        resultats = rechercher_mot(dictionnaire, recherche_francais, mode='francais')
        if resultats:
            for mot, details in resultats.items():
                with st.expander(f"{details['traduction']} - {mot}"):
                    st.write(f"**Type:** {details['type']}")
                    st.write(f"**Genre:** {details['genre']}")
        else:
            st.warning("Aucun résultat trouvé")

# Ajout d'informations sur l'utilisation
with st.sidebar:
    st.markdown("""
    ### Comment utiliser le dictionnaire
    1. Choisissez l'onglet selon la langue de recherche
    2. Tapez le mot ou une partie du mot
    3. Les résultats s'afficheront automatiquement
    
    ### À propos
    Ce dictionnaire permet de chercher des mots en français et en tunisien. 
    Les résultats incluent :
    - La traduction
    - Le type de mot
    - Le genre grammatical
    """)