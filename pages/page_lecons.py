import streamlit as st
import pandas as pd

import streamlit as st

# Titre de l'application
st.title("👩‍🏫 - La leçon ennuyeuse !")
# Ajout d'informations sur l'utilisation
with st.sidebar:
    if st.button("Retour à l'accueil 🏚️", type="secondary", key="lecons_button"):
       st.switch_page("streamlit_app.py")
    with st.expander("**Liste des cours ** ", True):
        st.markdown("""
        1. Choisissez l'onglet selon la langue de recherche
        2. Tapez le mot ou une partie du mot
        3. Les résultats s'afficheront automatiquement
        """)

# Introduction
st.write("""
    Place au cour de Tunisien 🤓, ne t'endors pas trop vite! On a mis des quizzs! """)

# Section Conjugaison
st.write("### 1. Conjugaison")
with st.expander("1. 📖 - Conjugaison ", True):
    st.write("""
        En tunisien, la conjugaison est souvent simplifiée par rapport à l'arabe classique! 
    """)

    verbs_data = {
    'Pronom': ['Ana (Je)', 'Inti (Tu)', 'Huwa (Il)', 'Hiya (Elle)', 
              'Ahna (Nous)', 'Intouma (Vous)', 'Houma (Ils/Elles)'],
    'Manger (Yekol)': ['Nekol', 'Tekol', 'Yekol', 'Tekol', 
                      'Neklo', 'Teklo', 'Yeklo'],
    'Parler (Yahki)': ['Nahki', 'Tahki', 'Yahki', 'Tahki', 
                      'Nahkio', 'Tahkio', 'Yahkio'],
    'Faire (Y3mel)': ['N3mel', 'T3mel', 'Y3mel', 'T3mel', 
                      'N3amlo', 'T3amlo', 'Y3amlo']
    }

    
    st.dataframe(pd.DataFrame(verbs_data))
    st.write(" **Quiz Time** ")
    # Quiz conjugaison
    verbe = st.radio( 
        "Comment on écrit 'nous mangeons' ?",
        ('Neklo', 'Tekol', 'N3mel'), index = None
    )
    
    if verbe is not None:
        if verbe == 'y3ml':
            st.success("Bonne réponse ! 🎉 'y3ml' est le verbe tunisien pour 'faire'.")
        else:
            st.error("Oups, essaye encore ! 😅")


# Section Nombres
st.header("2. Les Nombres")
with st.expander("2. 🔢 - Les nombres ", True):

    numbers_data = {
        'Nombre': list(range(0, 11)),
        'En tunisien': ['Sfar', 'Wahed', 'Zouz', 'Tleta', 'Arba', 'Khamsa', 
                       'Setta', 'Seba', 'Tmenja', 'Tesaa', 'Achra']
    }
    
    st.dataframe(pd.DataFrame(numbers_data))
    
    st.write("**Règles spéciales ⚠️**")
    st.write("""
    - Pour 11-19: Ajoutez '-ach' au nombre de base
    - Pour les dizaines: 20 (Aachrin), 30 (Tlethin), 40 (Arbain)
    - Pour composer: 21 = Wahed w aachrin
    """)

# Afficher un exemple de nombre
number = st.selectbox(
    "Choisissez un nombre en tunisien :",
    ['1', '5', '10', '100']
)

if number == '1':
    st.write("Le nombre 1 en tunisien est 'wa7ed'.")
elif number == '5':
    st.write("Le nombre 5 en tunisien est 'khamsa'.")
elif number == '10':
    st.write("Le nombre 10 en tunisien est '3ashra'.")
else:
    st.write("Le nombre 100 en tunisien est 'miya'.")

# Section Grammaire de base
st.header("3. Grammaire de base")
st.write("""
    En tunisien, la grammaire est plus simple qu'en arabe classique. Voici quelques éléments de base :
    
    - **Pronoms personnels :**
      - Ana : Je
      - Enta : Tu (masculin)
      - Enti : Tu (féminin)
      - Houwa : Il
      - Heya : Elle
      - Ahna : Nous
      - Intu : Vous
      - Houm : Ils
    
    - **Les négations :**
      - La : Non
      - Ma- : Préfixe de négation, par exemple : "ma-n3mlch" (Je ne fais pas).
    
    - **Les questions :**
      - Chnowa ? (Quoi ?)
      - Wain ? (Où ?)
      - 3lech ? (Pourquoi ?)
    
    Ça a l'air facile, non ?
""")

# Test de grammaire
question = st.radio(
    "Comment diriez-vous 'Où est-ce que tu vas ?' en tunisien ?",
    ('Wain inti ray7a ?', 'Chnowa enti ray7a ?', 'Wain enta ray7 ?')
)

if question == 'Wain inti ray7a ?':
    st.success("Bravo ! 🎉 C'est bien ça. 'Wain inti ray7a ?' signifie 'Où vas-tu ?' (pour une fille).")
else:
    st.error("Pas tout à fait ! Essaie encore. 😅")




