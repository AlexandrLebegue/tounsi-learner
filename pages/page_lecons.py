import streamlit as st
import pandas as pd
import streamlit_antd_components as sac
import streamlit as st
from pages import menu_sidebar
import random

st.session_state["current_page"] = "Leçons"
menu_sidebar.show_menu()

def load_prononciation():
    st.write("# 🗣️ Guide de Prononciation Tunisienne")
    
    # Introduction
    st.write("""
    La prononciation tunisienne a ses particularités uniques! 
    Découvrez comment maîtriser les sons spéciaux du dialecte tunisien.
    """)
    
    # Sons spéciaux avec chiffres
    st.write("## 🔢 Sons Spéciaux (Notation avec chiffres)")
    special_sounds = {
        'Chiffre': ['3', '7', '9', '5', '8'],
        'Son': ['ع', 'ح', 'ق', 'خ', 'غ'],
        'Description': [
            'Son guttural "ain"',
            'H fort du fond de la gorge',
            'Q dur/profond',
            'Comme la jota espagnole',
            'R grasseyé/gargarisé'
        ],
        'Exemple': [
            '3aslema (Bonjour)',
            '7lowa (Belle/Bon)',
            '9ahwa (Café)',
            '5obz (Pain)',
            '8ali (Cher)'
        ]
    }
    st.dataframe(pd.DataFrame(special_sounds))
    
    # Section interactive des sons
    st.write("## 🎯 Pratique des Sons")
    son = st.selectbox(
        "Choisissez un son à pratiquer:",
        ["3 (ain)", "7 (H fort)", "9 (Q dur)", "5 (Kh)", "8 (Gh)"]
    )
    
    # Afficher des exemples selon le son choisi
    exemples_sons = {
        "3 (ain)": {
            "Mots simples": ["3ayn (œil)", "3sel (miel)", "3am (année)"],
            "Conseil": "Imaginez faire le son 'a' en ouvrant bien la gorge"
        },
        "7 (H fort)": {
            "Mots simples": ["7out (poisson)", "7lib (lait)", "7ar (épicé)"],
            "Conseil": "Comme un H aspiré très fort, comme quand on souffle sur des lunettes"
        },
        "9 (Q dur)": {
            "Mots simples": ["9alb (cœur)", "9rib (proche)", "9dim (ancien)"],
            "Conseil": "Comme un K mais prononcé plus profondément dans la gorge"
        },
        "5 (Kh)": {
            "Mots simples": ["5obz (pain)", "5ali (mon oncle)", "5ir (bien)"],
            "Conseil": "Comme la jota espagnole dans 'Juan' ou le ch allemand dans 'Bach'"
        },
        "8 (Gh)": {
            "Mots simples": ["8ali (cher)", "8ada (déjeuner)", "8ar (grotte)"],
            "Conseil": "Comme un R grasseyé français mais plus guttural"
        }
    }
    
    st.write("### 📝 Exemples et conseils")
    for mot in exemples_sons[son]["Mots simples"]:
        st.write(f"• {mot}")
    st.info(f"💡 Conseil: {exemples_sons[son]['Conseil']}")
    
    # Voyelles et diphtongues
    st.write("## 🔤 Voyelles et Diphtongues")
    vowels_data = {
        'Son': ['a', 'i', 'ou', 'ay', 'aw'],
        'Comme en français': [
            'papa',
            'lit',
            'bout',
            'aïe',
            'au'
        ],
        'Exemple tunisien': [
            'dar (maison)',
            'bib (porte)',
            'soug (marché)',
            'zaytoun (olive)',
            'mawjoud (présent)'
        ]
    }
    st.dataframe(pd.DataFrame(vowels_data))
    
    # Section règles de prononciation
    st.write("## 📚 Règles Principales")
    rules = {
        "Accentuation": """
        - L'accent est généralement sur l'avant-dernière syllabe
        - Les mots courts sont souvent accentués sur la première syllabe
        """,
        "Assimilation": """
        - Le 'l' de l'article 'el' s'assimile aux lettres solaires
        - Exemple: el + dar → ed-dar (la maison)
        """,
        "Élision": """
        - Les voyelles courtes peuvent disparaître en parole rapide
        - Exemple: ki(f) wash → kwash (comment)
        """
    }
    
    rule_choice = st.selectbox("Choisissez une règle:", list(rules.keys()))
    st.write(rules[rule_choice])
    
    # Exercice pratique
    st.write("## ✍️ Exercice de Prononciation")
    phrases = [
        "3aslema ya 7bibi",
        "9ahwa bel 7lib",
        "5obz w zaytoun",
        "8ali barcha",
        "Taw nemchiw lel soug"
    ]
    phrase = st.selectbox("Choisissez une phrase à pratiquer:", phrases)
    
    if st.button("Analyser la prononciation"):
        st.write("### 🔍 Analyse par syllabe:")
        # Exemple avec la première phrase
        if phrase == "3aslema ya 7bibi":
            st.write("""
            1. **3as** - commencez par le son guttural '3'
            2. **le** - syllabe simple
            3. **ma** - syllabe finale ouverte
            4. **ya** - liaison douce
            5. **7bi** - attention au 'H' fort
            6. **bi** - terminaison simple
            """)
    
    # Conseils de pratique
    st.write("## 💡 Conseils de pratique")
    st.success("""
    1. Écoutez beaucoup de tunisien (musique, films, séries)
    2. Pratiquez les sons difficiles isolément
    3. Enregistrez-vous pour comparer
    4. Commencez par des mots courts
    5. N'ayez pas peur de faire des erreurs!
    """)
    
    # Variations régionales
    st.write("## 🗺️ Variations Régionales")
    with st.expander("Voir les variations"):
        st.write("""
        - **Tunis** : Prononciation plus "douce", influence française
        - **Sfax** : Prononciation plus "dure", conservation des sons traditionnels
        - **Sousse** : Entre les deux, plus mélodique
        - **Sud** : Conservation de sons bédouins traditionnels
        """)
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
    st.write("# 👥 Les Pronoms Personnels")
    
    # Introduction
    st.write("""
    Les pronoms personnels sont essentiels dans le dialecte tunisien. 
    Contrairement au français, ils sont presque toujours exprimés dans la phrase 
    et ont quelques particularités intéressantes!
    """)
    
    # Tableau principal des pronoms
    st.write("## 📊 Tableau des Pronoms")
    pronoms_data = {
        'Pronom (FR)': ['Je', 'Tu (m)', 'Tu (f)', 'Il', 'Elle', 'Nous', 'Vous', 'Ils/Elles'],
        'Pronom (TN)': ['Ana', 'Inti/Inta', 'Inti', 'Huwa', 'Hiya', '7na', 'Intuma', 'Huma'],
        'Exemple': [
            'Ana fi dar (Je suis à la maison)',
            'Inti/Inta win? (Tu es où?)',
            'Inti mchi3a? (Tu pars?)',
            'Huwa yemchi (Il part)',
            'Hiya temchi (Elle part)',
            '7na mchina (Nous sommes partis)',
            'Intuma win? (Vous êtes où?)',
            'Huma yemchiw (Ils partent)'
        ],
        'Prononciation': [
            'A-na',
            'In-ti/In-ta',
            'In-ti',
            'Hou-wa',
            'Hi-ya',
            'H-na',
            'In-tou-ma',
            'Hou-ma'
        ]
    }
    st.dataframe(pd.DataFrame(pronoms_data))
    
    # Section des formes possessives
    st.write("## 🎯 Pronoms Possessifs")
    possessifs_data = {
        'Base': ['Mon/Ma', 'Ton/Ta', 'Son/Sa', 'Notre', 'Votre', 'Leur'],
        'Suffixe': ['-i', '-ek', '-ou/-ha', '-na', '-kom', '-hom'],
        'Exemple': [
            'Dari (Ma maison)',
            'Darek (Ta maison)',
            'Darou/Darha (Sa maison)',
            'Darna (Notre maison)',
            'Darkom (Votre maison)',
            'Darhom (Leur maison)'
        ]
    }
    st.dataframe(pd.DataFrame(possessifs_data))
    
    # Section interactive
    st.write("## 🎮 Pratique Interactive")
    
    # Choix de catégorie
    categorie = st.radio(
        "Choisissez une catégorie à pratiquer:",
        ["Pronoms Sujets", "Pronoms Possessifs", "Combinaisons"]
    )
    
    if categorie == "Pronoms Sujets":
        st.write("### 🎯 Exercice: Complétez avec le bon pronom")
        situations = {
            "_____ mchi lel souk": "Qui va au marché?",
            "_____ takel pizza": "Qui mange une pizza?",
            "_____ te7ki français?": "Qui parle français?"
        }
        situation = st.selectbox("Choisissez une phrase à compléter:", list(situations.keys()))
        reponse = st.text_input("Votre réponse:")
        if st.button("Vérifier"):
            st.write("💡 Plusieurs réponses sont possibles! Par exemple:")
            pronoms_possibles = {
                "Ana": "Je",
                "Inti": "Tu",
                "Huwa": "Il",
                "Hiya": "Elle"
            }
            for pronom, trad in pronoms_possibles.items():
                st.write(f"• {pronom} ({trad})")

    elif categorie == "Pronoms Possessifs":
        st.write("### 🏠 Exercice: Les possessions")
        objets = ["dar (maison)", "kteb (livre)", "telephone", "sayara (voiture)"]
        objet = st.selectbox("Choisissez un objet:", objets)
        st.write("Comment dire 'mon/ma' + cet objet?")
        if st.button("Voir la réponse"):
            objet_base = objet.split(" ")[0]
            st.success(f"{objet_base}i")
            st.info("Ajoutez simplement 'i' à la fin du mot!")
            
    else:  # Combinaisons
        st.write("### 🔄 Combinez les pronoms")
        st.write("Comment combiner les pronoms dans une phrase?")
        exemple = st.selectbox(
            "Choisissez un exemple:",
            [
                "Ana w inti (Moi et toi)",
                "7na w huma (Nous et eux)",
                "Inti w huwa (Toi et lui)"
            ]
        )
        if st.button("Plus d'explications"):
            st.info("""
            En tunisien, la combinaison de pronoms est simple:
            - Utilisez 'w' (et) entre les pronoms
            - L'ordre est souvent du plus proche au plus lointain
            - Le verbe s'accorde avec le groupe entier
            """)
    
    # Astuces et particularités
    st.write("## 💡 Astuces importantes")
    with st.expander("Voir les astuces"):
        st.write("""
        1. **Genre**: Le 'tu' a deux formes en tunisien (masculin/féminin)
        2. **Usage**: Les pronoms sont rarement omis contrairement au français
        3. **Position**: Le pronom vient généralement avant le verbe
        4. **Politesse**: 'Intuma' peut être utilisé par politesse avec une personne
        5. **Combinaison**: On peut combiner les pronoms avec 'w' (et)
        """)
    
    # Section culturelle
    st.write("## 🎭 Aspect Culturel")
    st.info("""
    Dans la culture tunisienne, l'usage des pronoms reflète le respect et la hiérarchie sociale:
    - Les jeunes utilisent 'intuma' avec les aînés par respect
    - Entre amis du même âge, on utilise 'inti/inta'
    - Avec les personnes âgées, on peut ajouter '3ammi/khalti' (oncle/tante) avant le pronom
    """)
    
    # Quiz final
    st.write("## 🎯 Quiz Rapide")
    if st.button("Commencer le quiz"):
        questions = [
            "Comment dit-on 'Je' en tunisien?",
            "Quelle est la différence entre 'inti' et 'inta'?",
            "Comment forme-t-on un possessif?",
            "Comment dit-on 'leur maison'?"
        ]
        q = random.choice(questions)
        st.write(f"Question: {q}")
        st.text_input("Votre réponse:")
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
    st.write("# 🎭 Formes de Politesse en Tunisien")
    
    # Introduction
    st.write("""
    La politesse est un aspect fondamental de la culture tunisienne. 
    Découvrez comment être poli et respectueux en dialecte tunisien!
    """)
    
    # Salutations de base
    st.write("## 👋 Salutations de Base")
    salutations_data = {
        'Situation': ['Matin', 'Après-midi', 'Soir', 'Général', 'Départ'],
        'Expression': [
            'Sbe7 el khir',
            'Messa el khir',
            'Tusbah 3ala khir',
            'Aslema / Slem',
            'Besslema'
        ],
        'Réponse': [
            'Sbe7 ennour',
            'Messa ennour',
            'Winti men ahlou',
            'Aslema / Slem',
            'Allah yselmek'
        ],
        'Usage': [
            'Le matin jusqu\'à 12h',
            'De 12h au coucher du soleil',
            'Avant d\'aller dormir',
            'À tout moment',
            'En partant'
        ]
    }
    st.dataframe(pd.DataFrame(salutations_data))
    
    # Formules de respect
    st.write("## 🙏 Formules de Respect")
    respect_data = {
        'Situation': [
            'Personnes âgées',
            'Parents',
            'Professeurs',
            'Inconnus',
            'Commerçants'
        ],
        'Terme': [
            '3ammi/khalti',
            'Weldek/Bintek',
            'Sidi/Lella',
            'Si/Siti',
            'Haj/Haja'
        ],
        'Utilisation': [
            'Pour s\'adresser aux personnes âgées (oncle/tante)',
            'Pour montrer du respect aux parents d\'autres',
            'Pour s\'adresser aux enseignants',
            'Pour s\'adresser poliment à un inconnu',
            'Pour les personnes ayant fait le pèlerinage ou âgées'
        ]
    }
    st.dataframe(pd.DataFrame(respect_data))
    
    # Section interactive
    st.write("## 🎮 Situations Pratiques")
    situation = st.selectbox(
        "Choisissez une situation:",
        [
            "Rencontrer quelqu'un pour la première fois",
            "Demander poliment un service",
            "Remercier quelqu'un",
            "S'excuser",
            "Prendre congé"
        ]
    )
    
    # Dictionnaire des situations
    situations = {
        "Rencontrer quelqu'un pour la première fois": {
            "Expressions": [
                "Metcharfin (Enchanté)",
                "Tcharafna (Honoré de vous rencontrer)",
                "Rabbi ysahhel (Que Dieu facilite notre rencontre)"
            ],
            "Conseil": "Accompagnez toujours d'un sourire et d'une légère inclinaison de la tête"
        },
        "Demander poliment un service": {
            "Expressions": [
                "Min fadhlek (S'il vous plaît)",
                "Law sma7t (Si vous permettez)",
                "3andi tlab (J'ai une demande)"
            ],
            "Conseil": "Commencez toujours par des salutations avant de faire votre demande"
        },
        "Remercier quelqu'un": {
            "Expressions": [
                "Yaichek (Merci)",
                "Barak Allahou fik (Que Dieu vous bénisse)",
                "Teslam (Merci beaucoup)"
            ],
            "Conseil": "Les Tunisiens apprécient les remerciements expressifs"
        },
        "S'excuser": {
            "Expressions": [
                "Sam7ni (Pardon)",
                "Ma3thira (Excusez-moi)",
                "Mea5ithni (Ne m'en voulez pas)"
            ],
            "Conseil": "L'humilité est appréciée dans les excuses"
        },
        "Prendre congé": {
            "Expressions": [
                "Besslema (Au revoir)",
                "Rabbi m3ak (Que Dieu soit avec vous)",
                "Tawwa nchufek (À bientôt)"
            ],
            "Conseil": "Ne partez jamais brusquement, prenez le temps de dire au revoir"
        }
    }
    
    # Afficher les expressions pour la situation choisie
    st.write("### 📝 Expressions appropriées:")
    for expr in situations[situation]["Expressions"]:
        st.write(f"• {expr}")
    st.info(f"💡 Conseil: {situations[situation]['Conseil']}")
    
    # Gestuelle et langage corporel
    st.write("## 🤝 Gestuelle et Langage Corporel")
    with st.expander("Voir les gestes importants"):
        st.write("""
        - **Poignée de main**: Ferme mais pas trop forte
        - **Distance**: Gardez une distance respectable avec le sexe opposé
        - **Regard**: Direct mais pas insistant
        - **Main sur le cœur**: En saluant ou remerciant pour plus de sincérité
        - **Hochement de tête**: Pour acquiescer respectueusement
        """)
    
    # Faux pas à éviter
    st.write("## ⚠️ Faux Pas à Éviter")
    faux_pas = {
        "À faire": [
            "Saluer avant toute conversation",
            "Utiliser les formules de respect appropriées",
            "Attendre d'être invité à s'asseoir",
            "Accepter le thé/café offert"
        ],
        "À éviter": [
            "Tutoyer les personnes âgées",
            "Interrompre une personne qui parle",
            "Refuser directement une invitation",
            "Critiquer ouvertement"
        ]
    }
    col1, col2 = st.columns(2)
    with col1:
        st.write("### ✅ À faire")
        for item in faux_pas["À faire"]:
            st.write(f"• {item}")
    with col2:
        st.write("### ❌ À éviter")
        for item in faux_pas["À éviter"]:
            st.write(f"• {item}")
    
    # Quiz de politesse
    st.write("## 🎯 Quiz de Politesse")
    if st.button("Commencer le quiz"):
        quiz_questions = [
            "Comment saluez-vous une personne âgée le matin?",
            "Quelle est la formule appropriée pour demander poliment?",
            "Comment remerciez-vous quelqu'un chaleureusement?",
            "Quelle expression utilisez-vous pour prendre congé?"
        ]
        q = random.choice(quiz_questions)
        st.write(f"Question: {q}")
        st.text_input("Votre réponse:")
        r
def load_default():
    # Titre de l'application
    st.title("👩‍🏫 - La leçon ennuyeuse !")
    # Introduction
    st.caption("""
        Place au cour de Tunisien 🤓, ne t'endors pas trop vite! On a mis des quizzs! """)
    st.divider()
    st.info("Ouvre la barre latéral pour avoir accès à plus de cours !")    

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

def load_selected(selected):
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

load_selected(selected)








