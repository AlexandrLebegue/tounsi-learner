import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
import streamlit as st
from pages import menu_sidebar
import random
menu_sidebar.show_menu()



def load_prononciation():
    st.write("La prononciation en tunisien se distingue par des sons spécifiques, comme les voyelles longues et certaines consonnes.")

def load_conjugaison():
    # Section Conjugaison
    st.write("# 📖 Conjugaison")
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
    
def load_pronoms_personnels():
    st.write("Les pronoms personnels en tunisien incluent : 'ana' (je), 'inta' (tu), 'houwa' (il), 'hiya' (elle), etc.")

def load_nombres():
    # Section Nombres
    st.write("# 🔢 Nombres ")
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

def load_grammaire():
    st.write("# 📖 Grammaire de Base du Tunisien")
    
    # Introduction
    st.write("""
    Découvrez les règles de base de la grammaire tunisienne! 
    Le dialecte tunisien est une version simplifiée de l'arabe classique, 
    avec des influences du français, de l'italien et du berbère.
    """)
    
    # Sections de grammaire
    sections = st.selectbox(
        "Choisissez une section :",
        ["Pronoms", "Verbes", "Formation des phrases", "Négation", "Questions"]
    )
    
    if sections == "Pronoms":
        st.write("## 👤 Les Pronoms Personnels")
        pronoms_data = {
            'Français': ['Je', 'Tu (masc.)', 'Tu (fém.)', 'Il', 'Elle', 'Nous', 'Vous', 'Ils/Elles'],
            'Tunisien': ['Ana', 'Inti (m)', 'Inti (f)', 'Huwa', 'Hiya', '7na', 'Intuma', 'Huma'],
            'Exemple': [
                'Ana nemchi (Je vais)',
                'Inti temchi (Tu vas)',
                'Inti temchi (Tu vas)',
                'Huwa yemchi (Il va)',
                'Hiya temchi (Elle va)',
                '7na nemchiw (Nous allons)',
                'Intuma temchiw (Vous allez)',
                'Huma yemchiw (Ils/Elles vont)'
            ]
        }
        st.dataframe(pd.DataFrame(pronoms_data))
        
        st.info("""
        💡 Astuce: Contrairement au français, en tunisien:
        - Le pronom est souvent obligatoire
        - Il existe une distinction entre tu masculin et féminin
        """)
        
    elif sections == "Verbes":
        st.write("## ⚡ Les Verbes")
        
        # Temps des verbes
        st.write("### 🕒 Les Temps principaux")
        temps_data = {
            'Temps': ['Présent', 'Passé', 'Futur'],
            'Formation': [
                'Préfixe n/t/y + verbe',
                'Verbe + t/it',
                'Bech + présent'
            ],
            'Exemple': [
                'nemchi (je vais)',
                'mchit (je suis allé)',
                'bech nemchi (je vais aller)'
            ]
        }
        st.dataframe(pd.DataFrame(temps_data))
        
        # Verbes courants
        st.write("### 📝 Verbes courants")
        verbes = {
            'mcha': 'aller',
            'kla': 'manger',
            'chreb': 'boire',
            'raked': 'dormir',
            '7eb': 'aimer/vouloir'
        }
        for verbe, trad in verbes.items():
            st.write(f"• **{verbe}** - {trad}")
            
    elif sections == "Formation des phrases":
        st.write("## 🔨 Formation des Phrases")
        st.write("""
        La structure de base est : **Sujet + Verbe + Complément**
        
        Exemples:
        - Ana nemchi lel dar (Je vais à la maison)
        - Hiya takel pizza (Elle mange une pizza)
        - 7na n7ebou el bhar (Nous aimons la mer)
        """)
        
        st.success("""
        🔑 Points clés:
        1. L'ordre des mots est similaire au français
        2. Les articles sont simplifiés (el = le/la/les)
        3. Pas de conjugaison complexe comme en arabe classique
        """)
        
    elif sections == "Négation":
        st.write("## ❌ La Négation")
        st.write("""
        Pour former la négation en tunisien, on utilise:
        **ma... ch** autour du verbe ou de l'adjectif
        """)
        
        negation_examples = {
            'Affirmatif': ['Nemchi', 'N7eb', 'Naaref', 'Behi'],
            'Négatif': ['Mamchich', 'Ma7ebch', 'Manarefch', 'Mabehi ch'],
            'Traduction': [
                'Je ne vais pas',
                'Je ne veux pas',
                'Je ne sais pas',
                'Ce n\'est pas bien'
            ]
        }
        st.dataframe(pd.DataFrame(negation_examples))
        
    else:  # Questions
        st.write("## ❓ Les Questions")
        st.write("### Mots interrogatifs courants:")
        
        questions_data = {
            'Tunisien': ['Chkoun?', 'Chnowa?', 'Win?', '9addech?', 'Ki/eh?', '3lech?'],
            'Français': ['Qui?', 'Quoi?', 'Où?', 'Combien?', 'Comment?', 'Pourquoi?'],
            'Exemple': [
                'Chkoun inti? (Qui es-tu?)',
                'Chnowa t7eb? (Que veux-tu?)',
                'Win mchit? (Où es-tu allé?)',
                '9addech el wa9t? (Quelle heure est-il?)',
                'Kifech inti? (Comment vas-tu?)',
                '3lech ma jitch? (Pourquoi n\'es-tu pas venu?)'
            ]
        }
        st.dataframe(pd.DataFrame(questions_data))
    
    # Section pratique interactive
    st.write("## 🎯 Pratiquons!")
    
    # Mini exercice selon la section
    st.write("### ✍️ Exercice")
    if st.button("Générer un exercice"):
        exercices = {
            "Pronoms": [
                "Traduisez: Je suis fatigué",
                "Comment dire: Nous allons au marché",
                "Conjuguez: être content (fer7an) avec tous les pronoms"
            ],
            "Verbes": [
                "Conjuguez 'mcha' au présent",
                "Mettez 'kla' au futur",
                "Donnez le passé de '7eb'"
            ],
            "Formation des phrases": [
                "Formez une phrase avec: dar (maison) + kbira (grande)",
                "Traduisez: Le chat dort dans le jardin",
                "Créez une phrase avec: ana + 7eb + mchi"
            ],
            "Négation": [
                "Mettez à la forme négative: 'Ana n7eb el birra'",
                "Comment dire: Je ne veux pas dormir",
                "Niez la phrase: 'El jow behi'"
            ],
            "Questions": [
                "Posez une question sur l'heure",
                "Demandez 'où habites-tu?'",
                "Formez une question avec 'chkoun'"
            ]
        }
        st.write(random.choice(exercices[sections]))
        
    # Astuces culturelles
    st.write("## 🎭 Note culturelle")
    cultural_notes = {
        "Pronoms": "Le vouvoiement est moins utilisé qu'en français, mais reste important avec les personnes âgées.",
        "Verbes": "Les Tunisiens mélangent souvent des verbes français tunisifiés dans leurs phrases.",
        "Formation des phrases": "Le tunisien est très expressif, n'hésitez pas à utiliser des gestes!",
        "Négation": "La négation peut être renforcée avec 'khaled' pour dire 'pas du tout'.",
        "Questions": "L'intonation est très importante dans les questions tunisiennes."
    }
    st.info(cultural_notes[sections])

def load_vocabulaire_de_base():
    # Section Vocabulaire de Base
    st.write("# 📚 Vocabulaire de Base")
    st.write("**📅 Tableau récapitulatif**")
    # Création du dictionnaire de vocabulaire
    vocab_data = {
        'Français': [
            'Bonjour', 
            'Au revoir', 
            'Comment ça va?',
            'Merci',
            'S\'il vous plaît',
            'Oui',
            'Non',
            'Je m\'appelle...',
            'Enchanté(e)',
            'Je ne comprends pas'
        ],
        'Tunisien': [
            'Aslema',
            'Besslema',
            'Chneya 7welek?',
            'Yaichek',
            'Min fadhlek',
            'Ih',
            'Le',
            'Ismi...',
            'Metcharfin',
            'Manefhemch'
        ],
        'Prononciation': [
            'As-le-ma',
            'Bes-le-ma',
            'Shney-ya hwel-ek',
            'Yai-chek',
            'Min fadh-lek',
            'Ih',
            'Le',
            'Is-mi',
            'Met-char-fin',
            'Ma-nef-hemch'
        ]
    }
    
    # Affichage du tableau de vocabulaire
    st.dataframe(pd.DataFrame(vocab_data))
    
    # Section des règles de base
    st.write("**📝 Règles de base**")
    st.write("""
    - Le dialecte tunisien utilise souvent des sons qui n'existent pas en français
    - Les chiffres sont parfois utilisés pour représenter des sons particuliers:
        * 7 = son 'H' fort
        * 3 = son 'A' guttural
        * 9 = son 'Q' guttural
    """)
    
    # Section interactive
    categorie = st.selectbox(
        "Choisissez une catégorie de phrases :",
        ['Salutations', 'Expressions courantes', 'Questions basiques']
    )
    
    if categorie == 'Salutations':
        st.write("""
        🌅 **Le matin:** "Sbe7 el khir" (Bonjour)
        🌙 **Le soir:** "Mse el khir" (Bonsoir)
        """)
    elif categorie == 'Expressions courantes':
        st.write("""
        👍 **D'accord:** "Mriguel"
        😊 **Très bien:** "Behi barcha"
        🙏 **De rien:** "Lé chwey"
        """)
    else:
        st.write("""
        🤔 **Où est...?:** "Win...?"
        💰 **Combien ça coûte?:** "9addech?"
        🕒 **Quelle heure est-il?:** "9addech fel wa9t?"
        """)
    
    # Astuce du jour
    st.write("💡 **Astuce du jour**")
    st.info("""
    En tunisien, on ajoute souvent 'ch' à la fin des verbes pour les rendre négatifs.
    Exemple: 
    - "Nefhem" (Je comprends) 
    - "Manefhemch" (Je ne comprends pas)
    """)


def load_expressions_courantes():
    st.write("# 🎯 Expressions Courantes")
    
    # Introduction amusante
    st.write("""
    Découvrez les expressions qui vous feront parler comme un vrai Tunisien! 
    Ces phrases sont utilisées quotidiennement dans les rues de Tunis, Sfax, ou Sousse 🇹🇳
    """)
    
    # Sections d'expressions par catégorie
    categories = {
        "😊 Expressions positives": {
            "3aslema": "Tout va bien (littéralement: c'est du miel)",
            "Mabrouk": "Félicitations",
            "3ala rouhek": "Tu es génial (littéralement: sur ton âme)",
            "Taw taw": "D'accord, tout de suite!",
            "Mriguel": "C'est cool, ça roule"
        },
        "😤 Expressions d'agacement": {
            "Ya hasra": "Quel dommage!",
            "Yezi barka": "Arrête, ça suffit!",
            "Ya latif": "Oh mon Dieu! (expression d'exaspération)",
            "Mela aya": "Alors quoi encore?",
            "Chnoua hedha": "C'est quoi ce truc?"
        },
        "🤣 Expressions drôles": {
            "Mahlek": "Que tu es beau/belle! (avec ironie possible)",
            "Sahbi rabbi yehfdek": "Mon ami que Dieu te protège (utilisé pour tout et n'importe quoi)",
            "Weldek ma3adech yekber": "Ton fils ne grandira plus (quand quelqu'un fait quelque chose de bien)",
            "3andek chwaya mokh?": "As-tu un peu de cerveau? (gentille moquerie)",
            "Wallah la3dhim": "Je te jure! (utilisé même pour les plus petites choses)"
        }
    }
    
    # Sélection de catégorie interactive
    category = st.selectbox("Choisissez une catégorie:", list(categories.keys()))
    
    # Affichage des expressions de la catégorie sélectionnée
    selected_expressions = categories[category]
    expressions_df = pd.DataFrame({
        'Expression': list(selected_expressions.keys()),
        'Signification': list(selected_expressions.values())
    })
    st.dataframe(expressions_df)
    
    # Section interactive - Testez vos connaissances
    st.write("## 🎮 Testez vos connaissances!")
    
    # Quiz simple
    quiz_expression = st.selectbox(
        "Que signifie cette expression?",
        list(selected_expressions.keys())
    )
    
    if st.button("Voir la réponse"):
        st.success(f"🎉 Réponse: {selected_expressions[quiz_expression]}")
    
    # Section des situations courantes
    st.write("## 🎭 Situations courantes")
    situations = {
        "Au café": [
            "3andi kahwa bel 7lib - Un café au lait s'il vous plaît",
            "Zidli chwaya sukkar - Ajoutez-moi un peu de sucre",
            "9addech? - C'est combien?"
        ],
        "Au marché": [
            "Ghali barcha! - C'est trop cher!",
            "Na9es chwaya - Baisse un peu le prix",
            "Aka7el 3liya - Fais-moi un bon prix"
        ],
        "Entre amis": [
            "Nemchiw nel3bou ballon? - On va jouer au foot?",
            "Tji tel3ab m3ana? - Tu viens jouer avec nous?",
            "Chbik mafamech? - Pourquoi tu n'es pas venu?"
        ]
    }
    
    situation = st.selectbox("Choisissez une situation:", list(situations.keys()))
    for phrase in situations[situation]:
        st.write(f"• {phrase}")
    
    # Conseils d'utilisation
    st.write("## 💡 Conseils d'utilisation")
    st.info("""
    - Les expressions tunisiennes sont très contextuelles
    - Le ton est aussi important que les mots
    - N'hésitez pas à utiliser les gestes pour accompagner vos expressions
    - Les Tunisiens apprécient beaucoup quand les étrangers essaient de parler leur dialecte!
    """)
    
    # Easter Egg
    if st.button("🎁 Découvrez une expression secrète!"):
        expressions_secretes = [
            "Chkoun ya7ki 3lik? - Qui parle de toi? (Quand quelqu'un éternue)",
            "3andek fil ! - Tu as un éléphant! (Quand quelqu'un a de la chance)",
            "Koul 3am w inti b'khir - Que chaque année te trouve en bonne santé",
            "Saret sa3a - Ça fait une heure! (Même si ça fait 5 minutes)"
        ]
        st.success(random.choice(expressions_secretes))
    
    # Niveau de maîtrise
    st.write("## 📊 Évaluez votre niveau")
    niveau = st.slider("Combien d'expressions connaissez-vous?", 0, 20)
    
    if niveau < 5:
        st.write("🌱 Débutant - Continuez à pratiquer!")
    elif niveau < 10:
        st.write("🌿 Intermédiaire - Vous commencez à bien vous débrouiller!")
    elif niveau < 15:
        st.write("🌳 Avancé - Presque un Tunisien!")
    else:
        st.write("🎭 Expert - Vous êtes un vrai Tunisien maintenant!")
def load_formes_de_politesse():
    st.write("Les formes de politesse incluent des expressions comme : 'afek' (s'il te plaît), 'barakallah fik' (merci beaucoup).")

def load_default():
    # Titre de l'application
    st.title("👩‍🏫 - La leçon ennuyeuse !")
    # Introduction
    st.caption("""
        Place au cour de Tunisien 🤓, ne t'endors pas trop vite! On a mis des quizzs! """)

    st.divider()

    load_conjugaison()


# Ajout d'informations sur l'utilisation
with st.sidebar:
    st.divider()

    selected = sac.menu([
    sac.MenuItem('Leçons', children = [
        sac.MenuItem('Prononciation', dashed = True),
        sac.MenuItem('Conjugaison', dashed = False),
        sac.MenuItem('Pronoms personnels'),
        sac.MenuItem('Nombres'),
        sac.MenuItem('Grammaire'),
        sac.MenuItem('Vocabulaire de base'),
        sac.MenuItem('Expressions courantes'),
        sac.MenuItem('Formes de politesse')
    ])
], open_all=True)


# Vérification de l'élément sélectionné et chargement de la leçon correspondante
if selected == 'Prononciation':
    load_prononciation()
elif selected == 'Conjugaison':
    load_conjugaison()
elif selected == 'Pronoms personnels':
    load_pronoms_personnels()
elif selected == 'Nombres':
    load_nombres()
elif selected == 'Grammaire':
    load_grammaire()
elif selected == 'Vocabulaire de base':
    load_vocabulaire_de_base()
elif selected == 'Expressions courantes':
    load_expressions_courantes()
elif selected == 'Formes de politesse':
    load_formes_de_politesse()
else:
    load_default()  # Charge une page par défaut ou une instruction par défaut










