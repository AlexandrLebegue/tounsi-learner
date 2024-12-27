import streamlit as st
import json
from difflib import SequenceMatcher
from pages import menu_sidebar
import pandas as pd
from datetime import datetime, timedelta
import random
import streamlit_antd_components as sac

def get_filtered_scores(scores, period="all"):
    """Filtre les scores selon la période choisie"""
    if not scores:
        return []
    
    df = pd.DataFrame(scores)
    df['date_du_score'] = pd.to_datetime(df['date_du_score'])
    
    if period == "week":
        one_week_ago = datetime.now() - timedelta(days=7)
        df = df[df['date_du_score'] >= one_week_ago]
    
    return df.sort_values('point', ascending=False).head(10).to_dict('records')

def view():
    
    # Titre avec animation CSS
    st.markdown("""
        <style>
        .title {
            text-align: center;
            color: #FF4B4B;
            font-size: 3em;
            font-weight: bold;
            text-shadow: 2px 2px 4px #000000;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(1); }
            50% { transform: scale(1.05); }
            100% { transform: scale(1); }
        }
        .score-card {
            padding: 20px;
            border-radius: 10px;
            background: linear-gradient(45deg, #FF4B4B, #FF9B4B);
            color: white;
            text-align: center;
            margin: 10px 0;
        }
        </style>
        <h1 class='title'>🎮 Hall of Fame 🏆</h1>
    """, unsafe_allow_html=True)
    st.markdown(""" <center style="color: #808080 ;">J'espère que ton score se trouve ici, sinon bon courage 💪 </center> """ , unsafe_allow_html=True)
    st.caption("")
    st.divider()

    # Sélecteur de période
    #period = st.select_slider(
    #    "Sélectionner la période :",
    #    options=["week", "all"],
    #    format_func=lambda x: "Cette semaine" if x == "week" else "Tout les temps"
    #)   
    result = sac.buttons(['Cette semaine', 'Tout les temps'], align='center')
    if result ==  'Cette semaine'  :  
        period = "week"
    else:
        period = "De Tout les temps"
    # Récupération et filtrage des scores
    scores = st.session_state.get("classement", [])
    filtered_scores = get_filtered_scores(scores, period)

    if not filtered_scores:
        st.info("Aucun score enregistré pour le moment ! 🎮")
        return

    
    
    
    # Top 3 avec des médailles
    for i, score in enumerate(filtered_scores[:3]):
        medals = ["🥇", "🥈", "🥉"]
        st.markdown(f"""
            <div class='score-card'>
                <h2>{medals[i]} {score['nom_du_joueur']}</h2>
                <h3>{score['point']} points</h3>
                <p>{score['date_du_score'].strftime('%d/%m/%Y')}</p>
            </div>
        """, unsafe_allow_html=True)


    # Reste du classement dans un tableau
    if len(filtered_scores) > 3:
        st.subheader("Autres joueurs dans le top 10 🎮")
        
        
        df_other = pd.DataFrame(filtered_scores[3:])
        df_other['Rang'] = range(4, len(filtered_scores) + 1)
        df_other['Date'] = df_other['date_du_score'].dt.strftime('%d/%m/%Y')
        st.dataframe(
            df_other[['Rang', 'nom_du_joueur', 'point', 'Date']],
            hide_index=True,
            column_config={
                'nom_du_joueur': 'Joueur',
                'point': 'Score'
            },
            use_container_width=True
            
        )

    # Statistiques
    st.markdown("---")
    stats_cols = st.columns(3)
    with stats_cols[0]:
        st.metric("Meilleur score", f"{filtered_scores[0]['point']} pts")
    with stats_cols[1]:
        avg_score = sum(s['point'] for s in filtered_scores) / len(filtered_scores)
        st.metric("Score moyen", f"{avg_score:.1f} pts")
    with stats_cols[2]:
        total_players = len(filtered_scores)
        st.metric("Nombre de joueurs", total_players)



st.session_state["current_page"] = "Classement"
menu_sidebar.show_menu()
# Création de données d'exemple si elles n'existent pas déjà

# Liste de noms pour générer des données aléatoires
noms = ["Alice", "Bob", "Charlie", "David", "Emma", "Frank", "Grace", 
        "Henry", "Iris", "Jack", "Kelly", "Liam", "Maria", "Noah", "Olivia"]

# Génération de dates sur les 2 dernières semaines
aujourdhui = datetime.now()
dates = [(aujourdhui - timedelta(days=x)).strftime("%Y-%m-%d") for x in range(14)]

# Création des scores
st.session_state["classement"] = []

for _ in range(20):  # Génération de 20 scores
    score = {
        "nom_du_joueur": random.choice(noms),
        "point": random.randint(50, 1000),
        "date_du_score": random.choice(dates)
    }
    st.session_state["classement"].append(score)
view()

