import streamlit as st
from streamlit_navigation_bar import st_navbar
import streamlit_antd_components as sac
import random

st.session_state["current_page"] = "Accueil"
with open( ".streamlit/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.session_state["current_page"] = "Home"

st.markdown("<div class='Main_Title'><h1 style='text-align: center; color: white;'><font size='30'><big><big><big>🇹🇳 Tounsi Learner</big></big></big></font></h1></div>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Avec tounsi-learner, deviens un pro du tunisien 😁</h2>", unsafe_allow_html=True)
st.divider()


# Dictionnaire des faits
faits = [
    {'label': 'Fact', 'description': '🐟 Les meilleurs couscous sont tunisiens 🐟'},
    {'label': 'Fact', 'description': '🏖️ La Tunisie abrite certaines des plus belles plages de la Méditerranée 🏖️'},
    {'label': 'Fact', 'description': '🏺 Carthage, l’une des civilisations les plus puissantes de l’histoire, est en Tunisie 🏺'},
    {'label': 'Fact', 'description': '🐪 Le désert tunisien est un lieu emblématique où plusieurs scènes de Star Wars ont été tournées 🐪'},
    {'label': 'Fact', 'description': '🌍 La Tunisie est le pays le plus au nord de tout le continent africain 🌍'},
    {'label': 'Fact', 'description': '🎶 Le malouf tunisien est un style musical unique, hérité d’Andalousie 🎶'}
]

# Sélection d'un fait aléatoirer
fait_aleatoire = random.choice(faits)

# Affichage du fait avec sac.alert
sac.alert(label=fait_aleatoire['label'],description=fait_aleatoire['description'],banner=True,icon=False,closable=False)

st.write("## Activités\n")
st.caption("Selectionne une activité et lance toi dans l'aventure !")
left, middle, right = st.columns(3, border=True)
with left:
    st.markdown("<b style='text-align: center; color: white;'>😴 Leçons ennuyeuse 😴</b>", unsafe_allow_html=True)
    st.caption("Ici des leçons à dormir debout...")
    if st.button("Commencer", type="primary", key="lecons_button"):
       st.balloons() 
       st.switch_page("pages/page_lecons.py")

with middle:
    st.markdown("<b style='text-align: center; color: white;'>🤓 Dico pour les pros 🤓</b>", unsafe_allow_html=True)
    st.caption("kestceke ça veut dire")
    if st.button("Commencer", type="primary", key="dico_button"):
       st.balloons() 
       st.switch_page("pages/page_dico.py")

with right:
    st.markdown("<b style='text-align: center; color: white;'>🤓 Quizz of champions 🤓</b>", unsafe_allow_html=True)
    st.caption("Toi contre le monde 🌍")
    if st.button("Commencer", type="primary", key="quizz_button"):
        st.balloons() 
        st.switch_page("pages/page_quizz.py")
st.write("## A propos du site")
with st.columns(1, border=True)[0]:
    st.markdown(
        """
        **Tounsi-Learner**, c'est ton compagnon idéal pour apprendre le tunisien en t'amusant ! 
        Que tu sois débutant ou que tu souhaites perfectionner ton accent, notre plateforme te propose des leçons interactives, un dictionnaire complet et des quiz stimulants. 
        Le tout gratuitement et accessible depuis n'importe où ! 
        """
    )
st.write("## Comment devenir un pro du tunisien ? \n")
st.caption("C'est simple ! Il suffit de suivre les étapes suivantes \n")
sac.steps(
    items=[
        sac.StepsItem(title='Apprendre les bases 🤓', description='Ne pas avoir peur de lire les cours !'),
        sac.StepsItem(title='Connaître les mots du dico 📖'),
        sac.StepsItem(title='Mesurer ses connaissances dans le quizz 📝'),
        sac.StepsItem(title="Partir en Tunisie s'entrainer sur le terrain ! "),
    ], direction = "vertical"
)  
