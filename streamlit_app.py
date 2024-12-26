import streamlit as st

st.set_page_config(
        page_title="🏚️ - Accueil",
)

st.markdown("<h1 style='text-align: center; color: white;'>🇹🇳 Tounsi-Learner</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: grey;'>Avec tounsi-learner, deviens un pro du tunisien 😁</h2>", unsafe_allow_html=True)
st.divider()
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

    
