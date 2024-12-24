import streamlit as st
import uuid
from urllib.parse import urlencode, quote_plus
from streamlit_javascript import st_javascript
import time
from coolname import generate_slug
import random

# Configuration de la page
st.set_page_config(
    page_title="Klemi - Battle des mots tunisiens",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialisation du jeu
def initialize_game(mode='pvp'):
    player_x = str(uuid.uuid4())
    return {
        'player_x': player_x,
        'player_o': None,
        'words_x': set(),
        'words_o': set(),
        'current_player': 1,
        'timer': 60,  # 60 secondes par partie
        'game_over': False,
        'mode': mode,
        'start_time': None
    }

# Gestion des sessions de jeu
def get_game_sessions():
    if 'game_sessions' not in st.session_state:
        st.session_state.game_sessions = {}
    return st.session_state.game_sessions

def join_game(session_id):
    game_sessions = get_game_sessions()
    if session_id in game_sessions:
        session = game_sessions[session_id]
        if session['player_o'] is None:
            session['player_o'] = str(uuid.uuid4())
            st.session_state.session_id = session_id
            st.session_state.player_id = session['player_o']
            game_sessions[session_id] = session
            return True
    return False

# Interface du jeu
def game_board(session):
    if session['start_time'] is None and not session['game_over']:
        session['start_time'] = time.time()

    current_time = time.time()
    elapsed_time = int(current_time - session['start_time']) if session['start_time'] else 0
    remaining_time = max(0, session['timer'] - elapsed_time)

    # Affichage du temps restant
    st.progress(remaining_time / session['timer'])
    st.markdown(f"### ⏱️ Temps restant: {remaining_time} secondes")

    # Déterminer le joueur actuel
    player_symbol = 'X' if st.session_state.player_id == session['player_x'] else 'O'
    is_current_player = (player_symbol == 'X' and session['current_player'] == 1) or \
                       (player_symbol == 'O' and session['current_player'] == 2)

    # Interface de saisie des mots
    if not session['game_over'] and is_current_player and remaining_time > 0:
        word = st.text_input("Ajoute un mot en dialecte tunisien:", key="word_input")
        if st.button("Valider", type="primary"):
            if word:
                if player_symbol == 'X':
                    session['words_x'].add(word.lower())
                else:
                    session['words_o'].add(word.lower())
                session['current_player'] = 2 if session['current_player'] == 1 else 1

    # Affichage des scores
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 🎮 Joueur X")
        st.markdown(f"**Score:** {len(session['words_x'])}")
        st.markdown("**Mots:**")
        st.write(", ".join(session['words_x']))

    with col2:
        st.markdown("### 🎮 Joueur O")
        st.markdown(f"**Score:** {len(session['words_o'])}")
        st.markdown("**Mots:**")
        st.write(", ".join(session['words_o']))

    # Vérification de fin de partie
    if remaining_time <= 0 and not session['game_over']:
        session['game_over'] = True
        winner = None
        if len(session['words_x']) > len(session['words_o']):
            winner = 'X'
        elif len(session['words_o']) > len(session['words_x']):
            winner = 'O'
        
        if winner:
            st.balloons()
            st.success(f"🏆 Le joueur {winner} gagne avec {len(session['words_' + winner.lower()])} mots!")
        else:
            st.info("🤝 Match nul!")

# Fonction de partage
def share_match(session_id):
    base_url = str(st_javascript("window.location.href")).split("?")[0]
    join_url = f"{base_url}?{urlencode({'session_id': session_id})}"
    st.code(join_url, language="text")
    
    whatsapp_message = f"Yezi na3mlou battle des mots tunisiens! 🎯 {join_url}"
    whatsapp_url = f"https://wa.me/?text={quote_plus(whatsapp_message)}"
    
    st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; 
                         padding:10px 20px; border-radius:5px; cursor:pointer;">
                Partager sur WhatsApp 📱
            </button>
        </a>
    """, unsafe_allow_html=True)

# Interface principale
st.title("🎯 Klemi")
st.markdown("*Battle des mots en dialecte tunisien*")

# Création ou rejoindre une partie
if 'session_id' not in st.session_state:
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Nouvelle partie", use_container_width=True):
            session_id = generate_slug(2)
            game_sessions = get_game_sessions()
            game_sessions[session_id] = initialize_game()
            st.session_state.session_id = session_id
            st.session_state.player_id = game_sessions[session_id]['player_x']
            st.rerun()

    with col2:
        session_id = st.text_input("Code de la partie:")
        if st.button("Rejoindre", use_container_width=True):
            if join_game(session_id):
                st.success("Partie rejointe avec succès!")
                st.rerun()
            else:
                st.error("Partie non trouvée!")

# Affichage du jeu si une session est active
if 'session_id' in st.session_state:
    session_id = st.session_state.session_id
    game_sessions = get_game_sessions()
    session = game_sessions[session_id]
    
    if st.button("Partager la partie"):
        share_match(session_id)
    
    game_board(session)

# Styles CSS personnalisés
st.markdown("""
<style>
    .stButton button {
        width: 100%;
        background-color: #FF4B4B;
        color: white;
        font-weight: bold;
    }
    .stTextInput input {
        font-size: 1.2rem;
        padding: 1rem;
    }
    .stProgress .st-bo {
        background-color: #FF4B4B;
    }
</style>
""", unsafe_allow_html=True)