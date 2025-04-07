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

@st.cache_resource
def get_game_sessions():
    return st.session_state.shared_games

# Global shared state (persist across all sessions)
if 'shared_games' not in st.session_state:
    st.session_state.shared_games = defaultdict(dict)


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

def initialize_game(mode="multiplayer"):
    """Initialize a new game session"""
    game_id = generate_slug(2)
    game = {
        'game_id': game_id,
        'status': 'waiting',
        'player_host': str(uuid.uuid4()),
        'player_guest': None,
        'players': {
            'host': {
                'name': None,
                'score': 0,
                'current_word_index': 0
            },
            'guest': {
                'name': None,
                'score': 0,
                'current_word_index': 0
            }
        },
        'game_start_time': None,
        'words_list': [],
        'game_duration': 60,
        'countdown_duration': 30,
        'countdown_start': None
    }
    return game


def create_new_game(player_name, game_mode="multiplayer"):
    """Crée une nouvelle partie"""
    game_id = generate_slug(2)
    game_sessions = get_game_sessions()
    
    # Initialiser la session de jeu
    game_sessions[game_id] = initialize_game(mode=game_mode)
    game_sessions[game_id]['players']['host']['name'] = player_name
    player_id = game_sessions[game_id]['player_host']
    
    # Mettre à jour les états de session
    st.session_state.game_id = game_id
    st.session_state.player_id = player_id
    st.session_state.wait_to_start = game_mode == 'multiplayer'
    
    # Mettre à jour l'URL avec l'ID de la partie
    st.query_params['game_id'] = game_id
    
    return game_id

def display_waiting_room(game, player_id):
    """Affiche la salle d'attente et gère la synchronisation du début de partie"""
    game_sessions = get_game_sessions()
    
    # Si les deux joueurs sont présents
    if game['players']['guest']['name'] and game['players']['host']['name']:
        # Initialiser le compte à rebours si ce n'est pas déjà fait
        if game['countdown_start'] is None:
            game['countdown_start'] = time.time()
            game['status'] = 'countdown'
            game_sessions[game['game_id']] = game
        
        # Afficher le compte à rebours avec JavaScript
        waiting_container = st.empty()
        with waiting_container.container():
            st.markdown("# Préparation de la partie")
            st.markdown("### 👥 Joueurs de la partie:")
            st.write(f"• {game['players']['host']['name']} (Créateur)")
            st.write(f"• {game['players']['guest']['name']} (Invité)")
            
            countdown_html = """
                <div style="text-align: center;">
                    <div style="font-size: 48px; font-weight: bold;" id="countdown">30</div>
                    <div style="font-size: 18px;">secondes avant le début de la partie</div>
                </div>

                <script>
                    var countdownElement = document.getElementById('countdown');
                    var timeLeft = 30;
                    
                    function updateCountdown() {
                        countdownElement.textContent = timeLeft;
                        if (timeLeft <= 0) {
                            clearInterval(countdownInterval);
                            // Déclencher le début de la partie
                            window.parent.postMessage({type: 'streamlit:start_game'}, '*');
                            window.location.reload();
                            return;
                        }
                        timeLeft -= 1;
                    }
                    
                    var countdownInterval = setInterval(updateCountdown, 1000);
                    updateCountdown();
                </script>
            """
            st.components.v1.html(countdown_html, height=150)
            
            # Ajouter un listener pour le début de la partie
            st.markdown("""
                <script>
                    window.addEventListener('message', function(event) {
                        if (event.data.type === 'streamlit:start_game') {
                            window.location.reload();
                        }
                    });
                </script>
            """, unsafe_allow_html=True)

            
            # Vérifier si c'est l'heure de commencer
            elapsed = time.time() - game['countdown_start']
            if elapsed >= game['countdown_duration']:
                game['status'] = 'playing'
                game['game_start_time'] = time.time()
                if not game['words_list']:
                    game['words_list'] = prepare_words_list(dico, 20)
                game_sessions[game['game_id']] = game
                st.rerun()  # Un seul rerun au début de la partie
    
    else:
        # Salle d'attente standard
        waiting_container = st.empty()
        with waiting_container.container():
            st.subheader("🎮 Salle d'attente")
            st.code(game['game_id'], language="text")
            st.markdown("Partagez ce code avec votre adversaire!")
            
            st.subheader("👥 Joueurs connectés:")
            if game['players']['host']['name']:
                st.write(f"• {game['players']['host']['name']} (Créateur)")
            if game['players']['guest']['name']:
                st.write(f"• {game['players']['guest']['name']} (Invité)")
                
            if not game['players']['guest']['name']:
                st.info("En attente d'un autre joueur...")
            
            # Actualiser la page toutes les 3 secondes en attente d'un autre joueur
            st.markdown("""
                <script>
                    setTimeout(function() {
                        window.location.reload();
                    }, 3000);
                </script>
            """, unsafe_allow_html=True)

def display_game_interface(game, player_id, dico):
    """Affiche l'interface de jeu pour un joueur"""
    game_sessions = get_game_sessions()
    
    # Déterminer si le joueur est l'hôte ou l'invité
    is_host = player_id == game['player_host']
    player_type = 'host' if is_host else 'guest'
    player = game['players'][player_type]
    opponent = game['players']['guest' if is_host else 'host']

    # Calculer le temps restant
    elapsed_time = time.time() - game['game_start_time']
    remaining_time = max(0, game['game_duration'] - elapsed_time)
    
    # Header avec temps et score
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        st.write("### ⏱️ Temps restant:")
        st.progress(remaining_time / game['game_duration'])
        st.write(f"{int(remaining_time)} secondes")
    
    with col3:
        st.markdown(f"### Score: {player['score']}")
    
    # Ajoute le listener dans Streamlit pour gérer la fin du jeu
    st.markdown("""<script>
        window.addEventListener('message', function(event) {
            if (event.data.type === 'streamlit:timer_finished') {
                // Quand le message est reçu, mettre à jour l'état du jeu sans interaction manuelle
                window.location.reload();  // Rafraîchit la page pour appliquer la logique de fin
            }
        });
    </script>""", unsafe_allow_html=True)
    
    # Vérifier si le jeu est terminé
    if remaining_time <= 0:
        st.session_state.game_over = True
        st.session_state.player_final = game['players']['host' if player_id == game['player_host'] else 'guest']
        st.session_state.opponent_final = game['players']['guest' if player_id == game['player_host'] else 'host']
        st.rerun()
        return

    # Afficher le mot actuel
    if game['words_list'] and len(game['words_list']) > player['current_word_index']:
        current_word = game['words_list'][player['current_word_index']]
        st.markdown(f"### Mot en arabe: {current_word}")
        
        # Interface de traduction
        translation = st.text_input(
            "Traduisez ce mot en français:",
            key=f"mp_word_input_{current_word}"
        )
        
        # Colonnes pour les boutons et messages
        col1, col2 = st.columns([3, 7])
        
        # Ajout d'un état pour vérifier quel bouton a été cliqué
        if 'button_clicked' not in st.session_state:
            st.session_state.button_clicked = None
        
        # Vérification de la traduction
        with col1:
            if st.button("Valider", type="primary"):
                correct_translation = dico[current_word]["traduction"]
                if translation.lower() == correct_translation.lower():
                    player['score'] += 1
                    with col2:
                        st.success("Bonne traduction !")
                else:
                    player['score'] -= 2
                    with col2:
                        st.error(f"Mauvaise réponse ! La bonne traduction était: {correct_translation}")
                player['current_word_index'] += 1
                st.session_state.button_clicked = "valider"
                game_sessions[game['game_id']] = game
        
        # Colonnes pour le bouton passer
        col3, col4 = st.columns([3, 7])
        
        # Bouton pour passer
        with col3:
            if st.button("Passer", type="secondary"):
                with col4:
                    st.info(f"Le mot '{current_word}' signifiait: {dico[current_word]['traduction']}")
                player['current_word_index'] += 1
                st.session_state.button_clicked = "passer"
                game_sessions[game['game_id']] = game

        # Enlever les messages en fonction de l'action
        if st.session_state.button_clicked == "valider":
            col4.empty()  # Enlève le message de "Passer"
        
        if st.session_state.button_clicked == "passer":
            col2.empty()  # Enlève le message de validation
        
    time.sleep(0.1)  # Petit délai pour contrôler les rafraîchissements
    st.rerun()

    
def display_game_over(player, opponent):
    """Affiche l'écran de fin de partie"""
    st.empty()  # Nettoyer l'interface précédente
    
    st.markdown("# 🏁 Fin de la partie!")
    
    # Calculer et afficher les scores
    player_score = player['score']
    opponent_score = opponent['score']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Votre score:")
        st.markdown(f"## {player_score} points")
    
    with col2:
        st.markdown("### Score adversaire:")
        st.markdown(f"## {opponent_score} points")
    
    # Déterminer et afficher le résultat
    if player_score > opponent_score:
        st.balloons()
        st.success("### 🏆 Félicitations! Vous avez gagné!")
    elif player_score < opponent_score:
        st.error("### Vous avez perdu... Meilleure chance la prochaine fois!")
    else:
        st.info("### 🤝 Match nul!")
    
    # Bouton pour rejouer
    if st.button("Nouvelle partie"):
        # Nettoyer les états de session
        if 'player_id' in st.session_state:
            del st.session_state.player_id
        if 'game_id' in st.session_state:
            del st.session_state.game_id
        if 'game_over' in st.session_state:  # <- AJOUTER CETTE LIGNE
            del st.session_state.game_over   # <- AJOUTER CETTE LIGNE
        if 'player_final' in st.session_state:  # <- AJOUTER CETTE LIGNE
            del st.session_state.player_final   # <- AJOUTER CETTE LIGNE
        if 'opponent_final' in st.session_state:  # <- AJOUTER CETTE LIGNE
            del st.session_state.opponent_final   # <- AJOUTER CETTE LIGNE
        # Retirer le paramètre game_over de l'URL
        st.query_params.clear()
        st.rerun()

@st.cache_data
def update_final_score(game_id, player_id, final_score):
    """Met à jour le score final d'un joueur"""
    game_sessions = get_game_sessions()
    game = game_sessions[game_id]
    
    if player_id == game['player_host']:
        game['players']['host']['final_score'] = final_score
    else:
        game['players']['guest']['final_score'] = final_score
    
    game_sessions[game_id] = game
    return game
    
def join_existing_game():
    """Interface pour rejoindre une partie existante"""
    game_id = st.text_input("Code de la partie:")
    player_name = st.text_input("Votre pseudo:", key="join_name")
    if st.button("Rejoindre", type="primary") and game_id and player_name:
        if join_game(game_id, player_name):
            st.success("Vous avez rejoint la partie!")
            st.rerun()
        else:
            st.error("Partie non trouvée ou complète!")

# Interface principale pour le mode multijoueur

def multiplayer_interface():
    """Interface principale du mode multijoueur"""
    dico = charger_dictionnaire('ressource/dico.json')
    game_sessions = get_game_sessions()
    
    # Si le joueur n'est pas dans une partie
    if 'player_id' not in st.session_state:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Créer une partie")
            player_name = st.text_input("Votre pseudo (créateur):")
            if st.button("Nouvelle partie", type="primary") and player_name:
                game = initialize_game()
                game_id = game['game_id']
                game['players']['host']['name'] = player_name
                game_sessions[game_id] = game
                st.session_state.game_id = game_id
                st.session_state.player_id = game['player_host']
                st.success(f"Partie créée! Code: {game_id}")
                share_match()
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
    
    # Si le joueur est dans une partie
    else:
        game_id = st.session_state.game_id
        game = game_sessions.get(game_id)
        
        if game:
            if game['status'] in ['waiting', 'countdown']:
                display_waiting_room(game, st.session_state.player_id)
            elif game['status'] == 'playing':
                display_game_interface(game, st.session_state.player_id, dico)
        else:
            st.error("Partie non trouvée!")
            del st.session_state.player_id
            del st.session_state.game_id
            st.rerun()

def join_game(game_id, player_name):
    """Permet à un joueur de rejoindre une partie existante"""
    game_sessions = get_game_sessions()
    if game_id in game_sessions:
        game = game_sessions[game_id]
        if game['player_guest'] is None:
            player_id = str(uuid.uuid4())
            game['player_guest'] = player_id
            game['players']['guest']['name'] = player_name
            st.session_state.game_id = game_id
            st.session_state.player_id = player_id
            game_sessions[game_id] = game
            return True
    return False

def prepare_words_list(dico, num_words=20):
    """Prépare une liste aléatoire de mots pour la partie"""
    words = list(dico.keys())
    return random.sample(words, min(num_words, len(words)))

def display_waiting_room(game, player_id):
    """Affiche la salle d'attente"""
    game_sessions = get_game_sessions()
    
    # Si les deux joueurs sont présents
    if game['players']['guest']['name'] and game['players']['host']['name']:
        # Initialiser le compte à rebours si ce n'est pas déjà fait
        if game['countdown_start'] is None:
            game['countdown_start'] = time.time()
            game['status'] = 'countdown'
            game_sessions[game['game_id']] = game
            st.rerun()

        # Calculer le temps restant
        elapsed = time.time() - game['countdown_start']
        remaining = max(0, game['countdown_duration'] - elapsed)
        
        if remaining > 0:
            # Conteneur principal pour le compte à rebours
            countdown_container = st.empty()
            with countdown_container.container():
                st.markdown("# Préparation de la partie")
                # Afficher les joueurs avant le démarrage
                st.markdown("### 👥 Joueurs de la partie:")
                st.write(f"• {game['players']['host']['name']} (Créateur)")
                st.write(f"• {game['players']['guest']['name']} (Invité)")
                st.markdown(f"### ⏱️ La partie commence dans: {int(remaining)} secondes")
                st.progress(remaining / game['countdown_duration'])
        
        # Vérifier si le compte à rebours est terminé
        if remaining <= 0:
            game['status'] = 'playing'
            game['game_start_time'] = time.time()
            if not game['words_list']:
                game['words_list'] = prepare_words_list(dico, 20)
            game_sessions[game['game_id']] = game
            st.rerun()
        else:
            time.sleep(0.1)
            st.rerun()
    else:
        # Conteneur pour la salle d'attente
        waiting_container = st.empty()
        with waiting_container.container():
            st.subheader("🎮 Salle d'attente")
            st.code(game['game_id'], language="text")
            st.markdown("Partagez ce code avec votre adversaire!")
            
            st.subheader("👥 Joueurs connectés:")
            if game['players']['host']['name']:
                st.write(f"• {game['players']['host']['name']} (Créateur)")
            if game['players']['guest']['name']:
                st.write(f"• {game['players']['guest']['name']} (Invité)")
                
            if not game['players']['guest']['name']:
                st.info("En attente d'un autre joueur...")
            
            time.sleep(1)
            st.rerun()

def _share_match(game_id):
    """Fonction interne pour partager la partie"""
    base_url = str(current_url).split("?")[0]
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

st.dialog("Share")
def share_match():
    """Fonction décorée pour le dialogue de partage"""
    if 'game_id' in st.session_state:
        _share_match(st.session_state.game_id)

current_url = st_javascript("window.location.href")

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
    # Vérifier si le jeu est terminé avant d'afficher l'interface
    if 'game_over' in st.session_state and st.session_state.game_over:
        # Afficher l'écran de fin
        display_game_over(st.session_state.player_final, st.session_state.opponent_final)
    else:
        # Afficher l'interface normale du multijoueur
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