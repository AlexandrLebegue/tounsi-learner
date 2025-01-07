import streamlit as st
import uuid
from urllib.parse import urlencode, quote_plus
from streamlit_javascript import st_javascript
import time
from coolname import generate_slug
import random
import json
from streamlit.components.v1 import html
from collections import defaultdict

# Global shared state (persist across all sessions)
if 'shared_games' not in st.session_state:
    st.session_state.shared_games = defaultdict(dict)


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


# Gestion des sessions de jeu
def get_game(game_id):
    return st.session_state.shared_games.get(game_id)

def get_game_sessions():
    if 'shared_games' not in st.session_state:
        st.session_state.shared_games = {}
    return st.session_state.shared_games

def initialize_game(mode="multiplayer"):
    """Initialize a new game session"""
    game_id = generate_slug(2)  # Crée un code de partie court et mémorisable
    return {
        'game_id': game_id,
        'status': 'waiting',
        'player_host': str(uuid.uuid4()),  # Créateur de la partie
        'player_guest': None,  # Joueur qui rejoint
        'players': {},
        'game_start_time': None,
        'words_list': [],
        'game_duration': 60
    }

def join_game(game_id, player_name):
    game_sessions = get_game_sessions()
    if game_id in game_sessions:
        session = game_sessions[game_id]
        if session['player_guest'] is None:
            player_id = str(uuid.uuid4())
            session['player_guest'] = player_id
            session['players'][player_id] = {
                'name': player_name,
                'score': 0,
                'current_word_index': 0
            }
            st.session_state.player_session = {
                'game_id': game_id,
                'player_id': player_id
            }
            return True
    return False

def create_new_game(player_name):
    game_sessions = get_game_sessions()
    game = initialize_game()
    game_id = game['game_id']
    player_id = game['player_host']
    
    # Ajouter le joueur créateur
    game['players'][player_id] = {
        'name': player_name,
        'score': 0,
        'current_word_index': 0
    }
    
    game_sessions[game_id] = game
    st.session_state.player_session = {
        'game_id': game_id,
        'player_id': player_id
    }
    return game_id

def share_match(game_id):
    base_url = str(st_javascript("window.location.href")).split("?")[0]
    join_url = f"{base_url}?{urlencode({'game_id': game_id})}"
    st.code(join_url, language="text")
    
    whatsapp_message = f"Yezi na3mlou battle des mots tunisiens! 🎯 Code de partie: {game_id}"
    whatsapp_url = f"https://wa.me/?text={quote_plus(whatsapp_message)}"
    
    st.markdown(f"""
        <a href="{whatsapp_url}" target="_blank">
            <button style="background-color:#25D366; color:white; border:none; 
                         padding:10px 20px; border-radius:5px; cursor:pointer;">
                Partager sur WhatsApp 📱
            </button>
        </a>
    """, unsafe_allow_html=True)

def display_game_interface(game, player_id, dico):
    player = game['players'][player_id]
    st.markdown(f"### Score: {player['score']}")
    
    if game['status'] == 'playing':
        current_word = game['words_list'][player['current_word_index']]
        st.markdown(f"### Mot en arabe: {current_word}")
        
        translation = st.text_input("Traduisez ce mot en français:", 
                                  key=f"mp_word_input_{current_word}")
        
        col1, col2 = st.columns([3, 7])
        with col1:
            if st.button("Valider", type="primary"):
                correct_translation = dico[current_word]["traduction"]
                if translation.lower() == correct_translation.lower():
                    player['score'] += 1
                    with col2:
                        st.success("Bonne traduction!")
                else:
                    player['score'] -= 2
                    with col2:
                        st.error(f"Mauvaise réponse! La bonne traduction était: {correct_translation}")
                player['current_word_index'] += 1
                if player['current_word_index'] >= len(game['words_list']):
                    player['current_word_index'] = 0

# Interface principale pour le mode multijoueur
def multiplayer_interface():
    dico = charger_dictionnaire('ressource/dico.json')
    
    if 'game_id' in st.query_params and 'player_session' not in st.session_state:
        game_id = st.query_params['game_id']
        st.info(f"Rejoindre la partie: {game_id}")
        player_name = st.text_input("Votre pseudo:")
        if st.button("Rejoindre", type="primary") and player_name:
            if join_game(game_id, player_name):
                st.success("Vous avez rejoint la partie!")
                st.rerun()
            else:
                st.error("Partie non trouvée ou complète!")
                
    elif 'player_session' not in st.session_state:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Créer une partie")
            player_name = st.text_input("Votre pseudo (créateur):")
            if st.button("Nouvelle partie", type="primary") and player_name:
                game_id = create_new_game(player_name)
                st.success(f"Partie créée! Code: {game_id}")
                share_match(game_id)
                st.rerun()
        
        with col2:
            st.markdown("### Rejoindre une partie")
            game_id = st.text_input("Code de la partie:")
            player_name = st.text_input("Votre pseudo:", key="join_name")
            if st.button("Rejoindre", type="primary") and game_id and player_name:
                if join_game(game_id, player_name):
                    st.success("Vous avez rejoint la partie!")
                    st.rerun()
                else:
                    st.error("Partie non trouvée ou complète!")
    
    else:
        game_sessions = get_game_sessions()
        game = game_sessions[st.session_state.player_session['game_id']]
        player_id = st.session_state.player_session['player_id']
        
        # Afficher le code de la partie
        st.code(game['game_id'], language="text")
        
        # Afficher les joueurs
        st.subheader("👥 Joueurs connectés:")
        for pid, player_info in game['players'].items():
            st.write(f"• {player_info['name']}")
        
        # Démarrer la partie si deux joueurs sont présents
        if len(game['players']) >= 2 and game['status'] == 'waiting':
            if st.button("Démarrer la partie"):
                game['status'] = 'playing'
                game['game_start_time'] = time.time()
                game['words_list'] = list(random.sample(list(dico.keys()), 20))
                st.rerun()
        
        # Afficher l'interface de jeu
        if game['status'] == 'playing':
            display_game_interface(game, player_id, dico)

def prepare_words_list(dico, num_words=20):
    """Prépare une liste aléatoire de mots pour la partie"""
    words = list(dico.keys())
    return random.sample(words, min(num_words, len(words)))

def display_waiting_room(game, player_id):
    st.subheader("🎮 Salle d'attente")
    
    # Afficher le code de la partie
    st.code(game['game_id'], language="text")
    st.markdown("Partagez ce code avec vos amis pour qu'ils puissent rejoindre la partie!")
    
    # Afficher la liste des joueurs
    st.subheader("👥 Joueurs connectés:")
    for pid, player_info in game['players'].items():
        st.write(f"• {player_info['name']}")
    
    # Si compte à rebours en cours
    if game['status'] == 'countdown' and game['start_countdown']:
        remaining = max(0, game['countdown_duration'] - 
                       (time.time() - game['start_countdown']))
        st.progress(remaining / game['countdown_duration'])
        st.write(f"La partie commence dans {int(remaining)} secondes")
    
    # Bouton pour démarrer directement (visible uniquement pour le créateur)
    if (game['status'] == 'waiting' and 
        len(game['players']) >= 2 and 
        list(game['players'].keys())[0] == player_id):
        if st.button("Démarrer la partie maintenant"):
            game['status'] = 'playing'
            game['game_start_time'] = time.time()
            game['words_list'] = prepare_words_list(dico)
            for player in game['players'].values():
                player['current_word_index'] = 0
            st.rerun()

def display_game_interface(game, player_id, dico):
    player = game['players'][player_id]
    current_word = game['words_list'][player['current_word_index']]
    
    # Afficher le temps restant
    elapsed_time = time.time() - game['game_start_time']
    remaining_time = max(0, game['game_duration'] - elapsed_time)
    st.progress(remaining_time / game['game_duration'])
    st.markdown(f"### ⏱️ Temps restant: {int(remaining_time)} secondes")
    
    # Interface similaire au mode solo
    st.markdown(f"### Mot en arabe: {current_word}")
    translation = st.text_input("Traduisez ce mot en français:", 
                              key=f"mp_word_input_{current_word}")
    
    col1, col2 = st.columns([3, 7])
    with col1:
        if st.button("Valider", type="primary"):
            correct_translation = dico[current_word]["traduction"]
            if translation.lower() == correct_translation.lower():
                player['score'] += 1
                with col2:
                    st.success("Bonne traduction!")
            else:
                player['score'] -= 2
                with col2:
                    st.error(f"Mauvaise réponse! La bonne traduction était: {correct_translation}")
            player['current_word_index'] += 1
            if player['current_word_index'] >= len(game['words_list']):
                player['current_word_index'] = 0

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


if st.button("ajouter un mot a session_state"):
    if st.session_state.get("Player") is None:
        st.session_state["Player"] = []
    st.session_state["Player"].append(random.choice(["player","player_2", "player_3"]))

st.write("Sessiosn_state = " + str(st.session_state.get("Player")))
# Charger le dictionnaire à partir du fichier JSON
dico = charger_dictionnaire('ressource/dico.json')

# Mode solo
if option == "Solo":
    if 'game_data' not in st.session_state:
        st.session_state.game_data = None
        st.session_state.game_start_time = None
        st.session_state.score_saved = False  # Nouveau flag pour suivre si le score a été sauvegardé

    # Si le jeu n'est pas commencé
    if st.session_state.game_data is None:
        if st.button("Démarrer le jeu"):
            st.session_state.game_data = initialize_solo_game()
            st.session_state.game_data['current_word'] = get_random_word(dico)
            st.session_state.game_start_time = time.time()
            st.session_state.score_saved = False  # Réinitialiser le flag
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

        # Formulaire pour sauvegarder le score
        if not st.session_state.score_saved:
            with st.form(key='save_score'):
                pseudo = st.text_input("Entrez votre pseudo pour sauvegarder votre score:")
                submit_button = st.form_submit_button(label='Sauvegarder le score')
                
                if submit_button and pseudo:
                    # Créer un dictionnaire avec les données du score
                    score_data = {
                        'pseudo': pseudo,
                        'score': st.session_state.game_data['score'],
                        'timestamp': time.strftime("%H:%M:%S", time.localtime())
                    }
                    
                    # Vous pouvez maintenant utiliser score_data comme vous le souhaitez
                    # Par exemple, l'ajouter à une liste de scores dans session_state
                    if 'high_scores' not in st.session_state:
                        st.session_state.high_scores = []
                    st.session_state.high_scores.append(score_data)
                    
                    st.session_state.score_saved = True
                    st.success(f"Score sauvegardé pour {pseudo}!")

        # Bouton pour rejouer
        if st.button("Rejouer"):
            st.session_state.game_data = None
            st.session_state.game_start_time = None
            st.session_state.score_saved = False
            st.rerun()

# Mode multijoueur : initialisation de la partie
elif option == "Multijoueur":
    multiplayer_interface()
    

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