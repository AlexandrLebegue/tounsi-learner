import streamlit as st
import uuid
from urllib.parse import urlencode, quote_plus
from streamlit_javascript import st_javascript
import time
from coolname import generate_slug
import random
import json
from streamlit.components.v1 import html


# Configuration de la page
st.set_page_config(
    page_title="Klemi - Battle des mots tunisiens",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ajout d'informations sur l'utilisation
with st.sidebar:
    if st.button("Retour à l'accueil 🏚️", type="secondary", key="lecons_button"):
       st.switch_page("streamlit_app.py")
    option = st.selectbox(
    "**Mode de jeu** 🕹️",
    ("Solo", "Multijoueur"),
    placeholder="Select contact method...",
    )

def charger_dictionnaire(chemin_fichier):
    """
    Charge le dictionnaire depuis un fichier JSON
    """
    try:
        with open(chemin_fichier, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    
#### Solo

def create_countdown_timer():
    timer_html = """
        <div style="display: inline-block; color: white; font-size: 24px; font-weight: bold;" id="timer">60</div>
        <script>
            function startTimer() {
                var timeLeft = 60;
                var timerElement = document.getElementById('timer');
                
                var countdown = setInterval(function() {
                    timeLeft--;
                    timerElement.textContent = timeLeft + ' secondes';
                    
                    if (timeLeft <= 0) {
                        clearInterval(countdown);
                        window.parent.postMessage({type: 'streamlit:timer_finished'}, '*');
                    }
                }, 1000);
            }
            
            startTimer();
        </script>
    """
    return html(timer_html, height=50)

# Fonction pour initialiser le jeu solo
def initialize_solo_game():
    return {
        'start_time': time.time(),  # Utiliser time.time() au lieu de datetime
        'game_over': False,
        'current_word': None,
        'score': 0
    }

# Fonction pour obtenir un mot aléatoire
def get_random_word(dico):
    if dico:  # Vérification si le dictionnaire est valide et non vide
        return random.choice(list(dico.keys()))
    else:
        st.error("Le dictionnaire est vide ou invalide.")
        return print(dico.keys())
    
def solo_game_board(session, dico):
    # Affichage du mot arabe
    arabic_word = session['current_word']
    st.markdown(f"### Mot en arabe: {arabic_word}")
    
    # Saisie de la traduction
    translation = st.text_input("Traduisez ce mot en français:", key=f"word_input_{arabic_word}")
    
    # Créer deux colonnes pour les boutons et les messages
    col1, col2 = st.columns([3, 7])
    
    # Ajout d'un état pour vérifier quel bouton a été cliqué
    if 'button_clicked' not in session:
        session['button_clicked'] = None
    
    # Vérification de la traduction
    with col1:
        if st.button("Valider", type="primary"):
            correct_translation = dico[arabic_word]["traduction"]
            if translation.lower() == correct_translation.lower():
                session['score'] += 1
                with col2:
                    st.success("Bonne traduction ! ")
            else:
                session['score'] -= 2  # Réduire le score de 2 points en cas de mauvaise réponse
                with col2:
                    st.error(f"Mauvaise réponse ! La bonne traduction était: {correct_translation}")
            session['current_word'] = get_random_word(dico)
            session['button_clicked'] = "valider"
    
    # Créer deux nouvelles colonnes pour le bouton passer et son message
    col3, col4 = st.columns([3, 7])
    
    # Bouton pour passer
    with col3:
        if st.button("Passer", type="secondary"):
            with col4:
                st.info(f"Le mot '{arabic_word}' signifiait: {dico[arabic_word]['traduction']}")
            session['current_word'] = get_random_word(dico)
            session['button_clicked'] = "passer"
    
    # Enlever le message de validation si le bouton "Passer" est cliqué
    if session['button_clicked'] == "valider":
        col4.empty()
    
    # Enlever le message de passer si le bouton "Valider" est cliqué
    if session['button_clicked'] == "passer":
        col2.empty()


##### Multijoueur

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

# Charger le dictionnaire à partir du fichier JSON
dico = charger_dictionnaire('ressource/dico.json')

# Mode solo
if option == "Solo":
    if 'game_data' not in st.session_state:
        st.session_state.game_data = None
        st.session_state.game_start_time = None
    
    # Si le jeu n'est pas commencé
    if st.session_state.game_data is None:
        if st.button("Démarrer le jeu"):
            st.session_state.game_data = initialize_solo_game()
            st.session_state.game_data['current_word'] = get_random_word(dico)
            st.session_state.game_start_time = time.time()
            st.rerun()
    
    # Si le jeu est actif
    elif not st.session_state.game_data['game_over']:
        # Header avec temps et score
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.write("### Temps restant: ", end='')
            create_countdown_timer()
        with col3:
            st.markdown(f"### Score: {st.session_state.game_data['score']}")
            
        # Vérifier si le temps est écoulé (côté serveur)
        elapsed_time = time.time() - st.session_state.game_start_time
        if elapsed_time >= 60:
            st.session_state.game_data['game_over'] = True
            st.rerun()
        else:
            solo_game_board(st.session_state.game_data, dico)
            time.sleep(0.1)
            st.rerun()
    
    # Si le jeu est terminé
    else:
        st.write("Temps écoulé! 🏁")
        st.write(f"Score final: {st.session_state.game_data['score']} points")
        if st.button("Rejouer"):
            st.session_state.game_data = None
            st.session_state.game_start_time = None
            st.rerun()

# Mode multijoueur : initialisation de la partie
if option == "Multijoueur":
    # Création ou rejoindre une partie
    if 'session_id' not in st.session_state:
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Nouvelle partie", use_container_width=True):
                session_id = str(uuid.uuid4())  # Génère un nouvel ID pour la session
                game_sessions = get_game_sessions()
                game_sessions[session_id] = initialize_game('pvp')  # Initialisation en mode 'pvp'
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