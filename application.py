"""
This is the main page of the project, please find below a brief presentation of the project, as well as the associated code.
Ceci est la page principale du projet, veuillez trouver ci dessous une brève présentation du projet, ainsi que le code associé.
"""

# Importing libraries / Import des librairies
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_option_menu import option_menu
import os
import pandas as pd
import numpy as np

# Display of web application title and logo / Affichage du titre et du logo de l'application web
st.set_page_config(page_title="Game Action A-League 24/25 ", page_icon="📈", layout="centered")

# Language in session_state / Langue dans session_state
if "lang" not in st.session_state:
    st.session_state["lang"] = "English"

lang = st.sidebar.selectbox("Choose your language / Choisissez votre langue", ["English","Français"])
st.session_state["lang"] = lang

# Horizontal menu at the top of the page / Création du menu horizontal
menu = option_menu(
    menu_title=None,
    options=["Menu", "Match", "Équipe","Joueur"] if lang == "Français" else
            ["Home", "Match", "Team","Player"],
    icons=["house", "crosshair","people","person"],orientation="horizontal"
)

# Glossary per language / Glossaire par langue
glossary_overview_fr = """
### Vue d'ensemble :
- **Mouvement** : Indicateur du danger représenté par un joueur ou une équipe en fonction de leur positionnement en termes d'options de passe.
- **Course sans ballon** : Indicateur du danger représenté par un joueur ou une équipe en fonction de leur positionnement en termes de courses sans ballon.
- **Bonnes décisions** : Pourcentage de choix corrects effectués par un joueur ou une équipe (sur minimun 2 choix de passe possibles).
- **Pression** : Indicateur de la pression exercée par un joueur ou une équipe en termes d'influence sur le danger représenté par l'équipe adverse.
"""

glossary_overview_eng = """
### Summary :
- **Movement** : Indicator of the danger created by a player or a team based on their positioning in terms of passing options
- **Off-Ball Runs** : Indicator of the danger created by a player or a team based on their positioning through off-ball movements.
- **Good decisions** : Percentage of correct choices made by a player or a team (out of minimun two possible passing options)
- **Press** : Indicator of the pressure applied by a player or a team in terms of their influence on the danger created by the opposition.
"""

glossary_phase_fr = """
### Phase de jeu :
- **Phase de Construction** : Le ballon se situe dans le tiers défensif de l’équipe en possession; le porteur est sous pression ou les joueurs adverses sont positionnés très haut.
- **Phase de Création** : Phase par défaut, généralement située autour du tiers central du terrain. Elle peut aussi apparaître dans le tiers défensif de l’équipe en possession si le porteur n’est pas sous pression, ou dans le tiers offensif si la dernière ligne défensive adverse est positionnée loin de sa surface de réparation.
- **Phase de conclusion de l'action** : Le ballon se trouve dans le tiers offensif (ou défensif selon le point de vue) ou dans le tiers central; la ligne défensive est proche de la surface, avec une possession établie depuis au moins une seconde.
- **Jeu direct** : Commence par une passe longue (32 mètres ou plus le long de l’axe x, sans être une transversale) depuis la moitié de terrain de l’équipe en possession, ciblant un joueur proche de la zone de réception, et dure jusqu’à cette réception.
- **Attaque rapide** : Débute par une récupération du ballon dans la moitié de terrain adverse, suivie d’une progression rapide vers l’avant.
- **Phase de transition** : Débute par une récupération du ballon dans sa propre moitié de terrain, suivie d’une progression rapide vers l’avant.
- **Coup de pied arrêté** : Inclut les corners, les coups francs et les longues touches dirigées vers la surface. La phase se termine lorsque l’adversaire établit une possession claire, que le ballon est dégagé vers la moitié de terrain de l’équipe défendante, qu’il sort du terrain, ou que 20 secondes se sont écoulées depuis l’exécution.
- **Phase désorganisée** : Possession courte et disputée. Pour ne pas être classée comme désorganisée, la possession doit inclure au moins trois passes avec au maximum une tête, ou durer au moins 5 secondes.
"""

glossary_phase_eng = """
### Phase of play :
- **Build-up** : The ball is in the team’s own third; the ball carrier is under pressure or the opposing players are positioned and stay very high.
- **Create** : This is the default phase, typically occurring near the middle third of the pitch. However, it can also take place: In the team in possession defensive third, if the ball carrier is not under pressure, or in the team in possession attacking third, if the defending team’s last defensive line is positioned away from its penalty area.
- **Finish** : The ball is in the final (attacking or defending depending on point of view) or middle third; the defensive line is close to the penalty area, with established possession for at least 1 second.
- **Direct play** : Begins with a long ball pass (32+ meters along the x axis, without being a switch of play) from own half targeting a player near reception, lasting until reception.
- **Quick break** : Starts with regaining possession in the opponent’s half, followed by rapid progression up the pitch.
- **Transition** : Begins with regaining possession in own half, followed by rapid progression up the pitch.
- **Set Play** : This phase includes corners, free-kicks, and long throw-ins directed into the penalty area. The phase ends when: The opposition establishes clear possession, or the ball is cleared back to the defending team’s half, or the ball goes out of play, or 20 seconds have passed since the set piece was taken.
- **Chaotic** : A chaotic phase is marked by a short contested possession. For a phase to avoid being labelled chaotic, it must meet one of these criteria: Include at least three passes with no more than one header, or Involve at least 5 seconds of possession.
"""

glossary_state_fr = """
### État du score :
- **Mène** : L'équipe mène au score.
- **A égalité** : Situation d'égalité au score.
- **Mené** : L'équipe est menée au score.
"""

glossary_state_eng = """
### Game states :
- **Winning** : The team is leading the score
- **Drawing** : Tied score
- **Losing** : The team is trailing in the score
"""

glossary_pitch_fr = """
### Zone sur le terrain :
- **Gauche** : L'action se situe sur le côté gauche du terrain.
- **Centre** : L'action se situe au centre du terrain.
- **Droit** : L'action se situe sur le côté droit du terrain.
- **2ème tiers** : L'action se situe dans le 2ème tiers adverse.
- **Dernier tiers** : L'action se situe dans le dernier tiers adverse.
- **Penalty** : L'action se situe dans la surface adverse.
"""

glossary_pitch_eng = """
### Area on the pitch :
- **Left** : The action takes place on the left side of the pitch.
- **Centre** : The action takes place in the central area of the pitch.
- **Right** : The action takes place on the right side of the pitch.
- **Middle third** : The action takes place in the opposition’s middle third.
- **Final third** : The action takes place in the opposition’s final third.
- **Penalty area** : The action takes place inside the opposition’s penalty area.
"""

glossary_speed_fr = """
### Vitesse de la course :
- **Footing** : Vitesse moyenne inférieure à 15 km/h.
- **Course à faible intensité** : Vitesse moyenne entre 15 km/h et 20 km/h.
- **Course à intensité moyenne** : Vitesse moyenne entre 20 km/h et 25 km/h.
- **Course à haute intensité** : Vitesse moyenne supérieure à 25 km/h.
"""

glossary_speed_eng = """
### Speed of run :
- **Jogging** : Speed average below 15 km/h
- **Low intensity run* : Speed average between 15 km/h and 20km/h
- **Medium intensity run** : Speed average between 20 km/h and 25km/h
- **High intensity run** : Speed average above 25km/h
"""

glossary_off_ball_fr = """
### Type de course sans ballon :
- **Appel en profondeur** : Le joueur attaque l’espace derrière la dernière ligne défensive.
- **Appel en soutien** : Le joueur se dirige vers le porteur de balle pour recevoir une passe courte.
- **Appel pour recevoir un centre** : Course dans la surface pour recevoir un centre possible dans la situation.
- **Décrochage** : Le joueur décroche vers son propre camp pour ouvrir un angle de passe ou créer une supériorité dans la zone de possession.
- **Chevauchement** : Course dans le couloir ou le demi-espace, en passant de l’arrière vers l’avant du porteur ou du receveur, avec ce dernier plus large que le porteur.
- **Appel dans le demi-espace** : Course partant de l’axe vers le demi-espace.
- **Appel vers l’aile** : Course partant de l’axe ou du demi-espace vers le couloir, avec le joueur plus large que le porteur à la fin de la course.
- **Course vers l’avant** : Le joueur court devant le porteur vers le but adverse sans attaquer l’espace derrière la dernière ligne défensive.
- **Course de soutien** : Le joueur apporte un soutien par l’arrière ou à hauteur du porteur pour participer au jeu offensif ou aux transitions rapides.
- **Appel intérieur** : Course dans le couloir ou le demi-espace, en passant de l’arrière vers l’avant du porteur, en se positionnant plus à l’intérieur que lui.
"""

glossary_off_ball_eng = """
### Off-ball runs :
- **In behind** : Runner is attacking space behind the last defensive line
- **Coming short** : The runner is running towards the player in possession to receive a short ball.
- **Cross receiver** : Run in the penalty box to receive the ball from a cross (the cross does not need to happen, it just need to be a situation where the cross could have happened)
- **Dropping off** : The player dropping off (towards his own side) to open up a passing angle/to create superiority in possession.
- **Overlap** : An Overlap run is a Run with the following characteristics: The runner is running in the wide channel or half spaces, the runner is running from behind to in front of the player on the ball or receiving the ball and the receiver is wider than the player in possession
- **Pulling half space** : A pulling half-space run is a Run with the following characteristics: The start of the run is in center and the end of the run is in the half-space area
- **Pulling wide** : A pulling wide run is a Run with the following characteristics:The start of the run is in center (or half space), the end of the run is in the wide channel and the runner is wider than the player in possession at the end of the run
- **Run ahead of the ball** : A Run ahead is a Run with the following characteristics : The runner in front of the player in control of the ball, the runner is running towards the opponent goal and the runner is not attacking space behind the last defense line (otherwise it is a run in behind)
- **Support** : Player supports from behind/level by trying to engage in offensive/transition play (typically during fast transitions).
- **Underlap** : An Underlap run is a Run with the following characteristics : The runner is running in the wide channel or half spaces, the runner is running from behind to in front of the player on the ball or receiving the ball and the receiver is inside compare to the player in possession
"""

glossary_press_type_fr = """
### Type de pression :
- **Pression** : Un défenseur applique une pression directe en avançant ou en se déplaçant latéralement vers le joueur en possession.
- **Pressing** : Pression individuelle au sein d’une chaîne de pressing. Le joueur agit dans un cadre collectif, ce qui modifie le contexte de l’action.
- **Contre-pressing** : Après une perte de balle, un défenseur applique une pression sur l’équipe en possession dans les 3 secondes suivant la récupération adverse.
- **Pressing de récupération** : Un défenseur court vers son propre but pour tenter d’exercer une pression sur le porteur de balle.
- **Autre** : Le défenseur n’applique pas de pression active sur l’attaquant en possession, par exemple s’il reste en position, jockeye en reculant ou latéralement, ou se retrouve proche du porteur après une interception sans initier de pression.
"""

glossary_press_type_eng = """
### Type of pressure :
- **Pressure** : A defender applies direct pressure (moves forward or sideways towards the player in possession).
- **Pressing** : Is the same as pressure except within a pressing chain. Given the player is acting as part of a collective this changes the context of the engagement. 
- **Counter Press** : After a team loses possession in open play, a defender must apply pressure to the team in possession within 3 seconds of the ball being turned over.
- **Recovery Press** : A defender runs backwards to attempt to apply pressure to the ball carrier.
- **Other** : A defender is not directly applying pressure to the attacker in possession. There are several situations this includes: An attacker dribbles towards the defender and the defender stays in the position they are in. In this situation the attacker is engaging the defender therefore we do not classify this as the defender actively applying pressure, or a defender is jockeying the attacker, moving backwards or to the side as the attacker carries the ball. The defender is also goalside of the attacker, or a Contested Duel. We attempt to separate situations where a defender is already close to an attacker when the ball is turned over. We do not consider these situations as pressure actions since the defender may have just lost the ball to the player in possession and is applying pressure simply by being close, or if a player was targeted with a pass which was Intercepted and the defender is not actively applying pressure, they are just close to the new player in possession.

"""

# Labels per language / Labels par langue
GAME_PHASE_LABELS = {
    "Français": {"Phase de construction": "build_up","Phase de création": "create","Phase de conclusion de l'action": "finish","Jeu direct": "direct",
        "Attaque rapide": "quick_break","Phase de transition": "transition","Coup de pied arrêté": "set_play","Phase désorganisée": "chaotic",},
    "English": {"Build up": "build_up","Create": "create","Finish": "finish","Direct play": "direct","Quick break": "quick_break",
        "Transition": "transition","Set play": "set_play","Chaotic": "chaotic"},
}

PITCH_LABELS = {
    "Français": {"Gauche": "left","Centre": "center","Droit": "right","2ème tier": "middle_third","Dernier tier": "attacking_third","Penalty": "penalty"},
    "English": {"Left": "left","Center": "center","Right": "right","Middle third": "middle_third","Final third": "attacking_third","Penalty area": "penalty"},
}

SPEED_LABELS = {
    "Français": {"Footing": "jogging","Course à faible intensité": "running","Course à intensité moyenne": "hsr","Course à haute intensité": "sprinting",},
    "English": {"Jogging": "jogging","Low intensity run": "running","Medium intensity run": "hsr","High intensity run": "sprinting",},
}

OFF_BALL_LABELS = {
    "Français": {"Appel en profondeur": "behind","Appel en soutien": "coming_short","Appel pour recevoir un centre": "cross_receiver","Décrochage": "dropping_off",
        "Chevauchement": "overlap","Appel dans le demi-espace": "pulling_half_space","Appel vers l’aile": "pulling_wide","Course vers l’avant": "run_ahead_of_the_ball",
        "Course de soutien": "support","Appel intérieur": "underlap"},
    "English": {"In behind": "behind","Coming short": "coming_short","Cross receiver": "cross_receiver","Dropping off": "dropping_off","Overlap": "overlap",
        "Pulling half-space": "pulling_half_space","Pulling wide": "pulling_wide","Run ahead of the ball": "run_ahead_of_the_ball","Support": "support"},
}

PRESS_LABELS = {
    "Français": {"Pressing": "pressing","Pression": "pressure","Contre-pressing": "counter_press","Pressing de récupération": "recovery_press","Autre": "other",},
    "English": {"Pressing": "pressing","Pressure": "pressure","Counter press": "counter_press","Recovery press": "recovery_press","Other": "other"},
}

# Category group names / Groupe de statistiques
CATEGORY_GROUP_NAMES = {
    "Français": {"game_phase": "Phase de jeu","score_state": "Etat du score","pitch_zone": "Zone sur le terrain",
        "speed": "Vitesse de la course","off_ball": "Type de course sans ballon","press": "Type de pression"},
    "English": {"game_phase": "Game phase","score_state": "Score state","pitch_zone": "Zone on the pitch",
        "speed": "Running speed","off_ball": "Type of off-ball run","press": "Type of pressure"},
}

SCORE_STATE_LABELS = {
    "Français": {"Mène": "winning","A égalité": "drawing","Mené": "loosing",},
    "English": {"Winning": "winning","Drawing": "drawing","Losing": "loosing",},
}

# Function to build statistic categories / Fonction pour construire les catégories de statistique
def build_categories(df: pd.DataFrame, prefix: str, lang: str):
    categories = {}

    phase_labels_map = GAME_PHASE_LABELS[lang]
    pitch_labels_map = PITCH_LABELS[lang]
    speed_labels_map = SPEED_LABELS[lang]
    off_ball_labels_map = OFF_BALL_LABELS[lang]
    press_labels_map = PRESS_LABELS[lang]
    label_state_map = SCORE_STATE_LABELS[lang]
    group_names = CATEGORY_GROUP_NAMES[lang]

    # Game phase / Phase de jeu
    if prefix in {"top_movement", "top_off_ball_runs", "top_choice"}:
        columns_phase = {}
        for label, suf in phase_labels_map.items():
            col = f"{prefix}_{suf}"
            if col in df.columns:
                columns_phase[label] = col
        if columns_phase:
            categories[group_names["game_phase"]] = columns_phase

    # Score state / État du match
    columns_state = {}
    for label, suf in label_state_map.items():
        col = f"{prefix}_{suf}"
        if col in df.columns:
            columns_state[label] = col
    if columns_state:
        categories[group_names["score_state"]] = columns_state

    # Zone on the pitch / Zone sur le terrain
    if prefix in {"top_movement", "top_off_ball_runs", "top_choice"}:
        columns_pitch = {}
        for label, suf in pitch_labels_map.items():
            col = f"{prefix}_{suf}"
            if col in df.columns:
                columns_pitch[label] = col
        if columns_pitch:
            categories[group_names["pitch_zone"]] = columns_pitch

    # Running speed / Vitesse du déplacement
    if prefix in {"top_movement", "top_off_ball_runs", "top_choice"}:
        columns_speed = {}
        for label, suf in speed_labels_map.items():
            col = f"{prefix}_{suf}"
            if col in df.columns:
                columns_speed[label] = col
        if columns_speed:
            categories[group_names["speed"]] = columns_speed

    # Type of off ball run / Type de course sans ballon
    if prefix == "top_off_ball_runs":
        columns_off_ball = {}
        for label, suf in off_ball_labels_map.items():
            col = f"{prefix}_{suf}"
            if col in df.columns:
                columns_off_ball[label] = col
        if columns_off_ball:
            categories[group_names["off_ball"]] = columns_off_ball

    # Type of pressure / Type de pression
    if prefix == "top_press":
        columns_press = {}
        for label, suf in press_labels_map.items():
            col = f"{prefix}_{suf}"
            if col in df.columns:
                columns_press[label] = col
        if columns_press:
            categories[group_names["press"]] = columns_press

    return categories

# Display glossary in the sidebar / Afficher le glossaire dans la barre latérale
def render_glossary(lang: str):
    title = "📚 Glossary" if lang == "English" else "📚 Glossaire"
    with st.sidebar.expander(title):
        if lang == "English":
            st.markdown(glossary_overview_eng)
            st.markdown(glossary_phase_eng)
            st.markdown(glossary_state_eng)
            st.markdown(glossary_pitch_eng)
            st.markdown(glossary_speed_eng)
            st.markdown(glossary_off_ball_eng)
            st.markdown(glossary_press_type_eng)
        else:
            st.markdown(glossary_overview_fr)
            st.markdown(glossary_phase_fr)
            st.markdown(glossary_state_fr)
            st.markdown(glossary_pitch_fr)
            st.markdown(glossary_speed_fr)
            st.markdown(glossary_off_ball_fr)
            st.markdown(glossary_press_type_fr)

# Function to center tabs / Fonction pour Centrer les onglets
def center_tabs_css():
    st.markdown(
        """
        <style>
        .stTabs [data-baseweb="tab-list"] {
            justify-content: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

## Functions for the different pages from this project / Fonctions pour les différentes pages de ce projet

# Home page / Page d'accueil
def home():
    if lang == "English":
        # Page title
        st.markdown("<h3 style='text-align: center;'>Project on SkillCorner's game action evaluation metrics by Romain Traboul</h3>", unsafe_allow_html=True)

        st.image("src/image/logo_app.png", use_column_width=True) # Banner display

        st.markdown("<h4 style='text-align: center;'>Project presentation</h4>", unsafe_allow_html=True) # Subtitle

        # Project description
        st.markdown(
            """
            <p style="text-align: justify;">
            <br>
            As part of the PySport X SkillCorner Analytics Cup challenge, we have access to tracking and Game Intelligence Dynamic Events data from 10 matches of the Australian A-League during the 24/25 season.
            The goal of this project is to visualize player performance through the use of two models related to action evaluation:
            <ul>
                <li><strong>xThreat</strong>: The probability that a goal will be scored within 10 seconds if a given player were the target of a completed pass at a certain moment.</li>
                <li><strong>Expected Possession Value</strong>: Estimates the chances that a team will score within the next 90 seconds or before the ball goes out of play.</li>
            </ul>

            <br>
            <p style="text-align: justify;">
            To achieve this, several features are available:
            
            <ul>
                <li><strong>📊 Player Analysis</strong>: Analyze the player of your choice through these statistical indicators.</li>
                <li><strong>🥇 Team Analysis</strong>: Aggregate statistics for the selected team.</li>
                <li><strong>🔎 Match Analysis</strong>: Compare action evaluation statistics between the two teams.</li>
            </ul>

            <br>

            For more details about this project, you can access:
            <ul>
                <li><a href="https://github.com/Twiist33/Expected_Threat/blob/main/src/documentation/Documentation_Expected_Threat_ENG.pdf" target="_blank">The project documentation</a></li>
                <li><a href="https://github.com/Twiist33/Expected_Threat" target="_blank">The application source code</a></li>
                <li><a href="https://github.com/SkillCorner/opendata" target="_blank">The link to PySport x SkillCorner data</a></li>
            </ul>
            """,
            unsafe_allow_html=True
        )

    else:
        # Titre de la page
        st.markdown("<h3 style='text-align: center;'>Projet autour des métriques d'évaluation des actions de jeu de SkillCorner par Romain Traboul</h3>", unsafe_allow_html=True)

        st.image("src/image/logo_app.png", use_column_width=True) # Affichage de la bannière

        st.markdown("<h4 style='text-align: center;'>Présentation du projet</h4>", unsafe_allow_html=True) # Sous-titre

        # Description du projet
        st.markdown(
            """
            <p style="text-align: justify;">
            <br>
            Dans le cadre du challenge PySport X SkillCorner Analytics Cup, nous disposons des données de tracking et de Game Intelligence Dynamic Events pour 10 matchs d'Australian A-League sur la saison 24/25.
            L'objectif de ce projet sera de visualiser les performances des joueurs à travers l'utilisation des données de 2 modèles liés à l'évaluation des actions de jeu :
            <ul>
                <li><strong>xThreat</strong> : Probabilité qu'un but soit marqué dans les 10 secondes si un joueur donné était la cible d'une passe complète à un moment donné</li>
                <li><strong>Expected Possession Value</strong> : Détermine les chances qu'une équipe marque dans les 90 secondes suivantes ou avant que le ballon ne sorte du terrain</li>
            </ul>

            <br>

            <p style="text-align: justify;">
            Pour cela, plusieurs fonctionnalités sont disponibles :

            <ul>
                <li><strong>📊 Analyse d'un Joueur</strong> : Analyse du joueur de votre choix à travers ces indicateurs statistiques</li>
                <li><strong>🥇 Analyse d'une Équipe </strong> : Aggrégation des statistiques pour l'équipe choisie</li>
                <li><strong>🔎 Analyse d'un match </strong> : Confrontation des statistiques liées à l'évaluation des actions de jeu entre les deux équipes</li>
            </ul>

            <br>

            Pour plus de détails sur ce projet, vous avez à votre disposition :
            <ul>
                <li><a href="https://github.com/Twiist33/Expected_Threat/blob/main/src/documentation/Documentation_Expected_Threat_FR.pdf" target="_blank">La documentation du projet</a></li>
                <li><a href="https://github.com/Twiist33/Expected_Threat" target="_blank">Le code associé à l'application</a></li>
                <li><a href="https://github.com/SkillCorner/opendata" target="_blank">Le lien pour accèder aux données de PySport x SkillCorner</a></li>

            </ul>
            """,
            unsafe_allow_html=True
        )

# Match analysis page / Page de l'analyse d'un match
def match_analysis():
    if lang == "English":
        st.markdown("<h4 style='text-align: center;'>🔎 Match analysis</h4>", unsafe_allow_html=True)  # Display the title

        info_matchs = pd.read_csv("src/data/info_matches/informations_matchs_870.csv")  # Load match information

        # Create the label "Home team vs Away team"
        info_matchs["match_label"] = info_matchs["home_team_name"] + " vs " + info_matchs["away_team_name"]
        list_matchs = [""] + info_matchs["match_label"].tolist()

        selected_match_label = st.sidebar.selectbox("Select a match:", list_matchs)  # Match selection in the sidebar

        render_glossary(lang) # Display the glossary in English

        if not selected_match_label:
            st.image("src/image/match_image.jpg")
            st.info("Open the sidebar to choose the language and the match to analyze")
            return

        # Retrieve the match_id corresponding to the chosen label
        selected_row = info_matchs.loc[info_matchs["match_label"] == selected_match_label].iloc[0]
        selected_match_id = selected_row["match_id"]
        stats_path = f"src/data/matches/{selected_match_id}_stats.csv"
        stats_match_selected = pd.read_csv(stats_path)

        # Function to display a top 5
        def display_top5(df: pd.DataFrame, col_stat: str, title: str, center: bool = True):
            # Sort and select columns
            top5 = (
                df.sort_values(col_stat, ascending=False)
                  .loc[:, ["player_name", "player_position", "team_shortname", col_stat]]
                  .head(5)
                  .reset_index(drop=True)
            )

            # Rank
            top5.index = top5.index + 1
            top5.index.name = "Rank"

            top5_display = top5.rename(columns={"player_name": "Player","player_position": "Pos.","team_shortname": "Team",col_stat: "Stat"}) # Rename columns for display in English

            st.markdown(f"<h5 style='text-align: center;'>{title}</h5>", unsafe_allow_html=True)  # Display the subtitle

            # Display the table
            if center:
                col_l, col_center, col_r = st.columns([1, 3, 1])
                with col_center:
                    st.dataframe(top5_display, width='stretch')
            else:
                st.dataframe(top5_display, width='stretch')

        center_tabs_css() # CSS function to center tabs

        # Create tabs
        tab_summary, tab_movement, tab_off_ball, tab_choice, tab_press = st.tabs(["Overview", "Top Movement", "Top Off-ball runs", "Top Good decisions", "Top Pressure"])

        # Overview tab
        with tab_summary:
            # top_movement and top_off_ball_runs
            col1, col2 = st.columns(2)
            with col1:
                display_top5(stats_match_selected, "top_movement", "🧭 Top 5 Movement", center=False)
            with col2:
                display_top5(stats_match_selected, "top_off_ball_runs", "🏃‍♂️ Top 5 Off-ball runs", center=False)

            # top_choice and top_press
            col3, col4 = st.columns(2)
            with col3:
                display_top5(stats_match_selected, "top_choice", "🧠 Top 5 Good decisions", center=False)
            with col4:
                display_top5(stats_match_selected, "top_press", "🛡️ Top 5 Pressure", center=False)

        # Top movement tab
        with tab_movement:
            display_top5(stats_match_selected, "top_movement", "🧭 Top 5 Movement")  # Global ranking

            categories_movement = build_categories(stats_match_selected, "top_movement", lang="English")  # Category analysis

            if categories_movement:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtered by category</h5>", unsafe_allow_html=True)

                cat_movement = st.selectbox("Choose a category:", list(categories_movement.keys()), key="cat_movement")

                stats_available = categories_movement[cat_movement]
                label_stat_movement = st.selectbox("Choose a statistic in this category:", list(stats_available.keys()), key="stat_movement")

                col_stat = stats_available[label_stat_movement]
                display_top5(stats_match_selected, col_stat, "")
            else:
                st.info("No detailed category available for Top movement in this match.")

        # Top off-ball runs tab
        with tab_off_ball:
            display_top5(stats_match_selected, "top_off_ball_runs", "🏃‍♂️ Top 5 Off-ball runs")  # Global ranking

            categories_off_ball = build_categories(stats_match_selected, "top_off_ball_runs", lang="English")

            if categories_off_ball:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtered by category</h5>", unsafe_allow_html=True)

                cat_off_ball = st.selectbox("Choose a category:", list(categories_off_ball.keys()), key="cat_off_ball")

                stats_available = categories_off_ball[cat_off_ball]
                label_stat_off_ball = st.selectbox("Choose a statistic in this category:", list(stats_available.keys()), key="stat_off_ball")

                col_stat = stats_available[label_stat_off_ball]
                display_top5(stats_match_selected, col_stat, "")
            else:
                st.info("No detailed category available for Top off-ball runs in this match.")

        # Top choice tab
        with tab_choice:
            display_top5(stats_match_selected, "top_choice", "🧠 Top 5 Good decisions")  # Global ranking

            categories_choice = build_categories(stats_match_selected, "top_choice", lang="English")

            if categories_choice:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtered by category</h5>", unsafe_allow_html=True)

                cat_choice = st.selectbox("Choose a category:", list(categories_choice.keys()), key="cat_choice")

                stats_available = categories_choice[cat_choice]
                label_stat_choice = st.selectbox("Choose a statistic in this category:", list(stats_available.keys()), key="stat_choice")

                col_stat = stats_available[label_stat_choice]
                display_top5(stats_match_selected, col_stat, "")
            else:
                st.info("No detailed category available for Top choice in this match.")

        # Top press tab
        with tab_press:
            display_top5(stats_match_selected, "top_press", "🛡️ Top 5 Pressure")  # Global ranking

            categories_press = build_categories(stats_match_selected, "top_press", lang="English")

            if categories_press:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtered by category</h5>", unsafe_allow_html=True)

                cat_press = st.selectbox("Choose a category:", list(categories_press.keys()), key="cat_press")

                stats_available = categories_press[cat_press]
                label_stat_press = st.selectbox("Choose a statistic in this category:", list(stats_available.keys()), key="stat_press")

                col_stat = stats_available[label_stat_press]
                display_top5(stats_match_selected, col_stat, "")
            else:
                st.info("No detailed category available for Top press in this match.")

    else:
        st.markdown("<h4 style='text-align: center;'>🔎 Analyse d'un match</h4>",unsafe_allow_html=True) # Afficher le titre

        info_matchs = pd.read_csv("src/data/info_matches/informations_matchs_870.csv") # Chargement des informations de matchs

        # Création du libellé "Equipe domicile vs Equipe extérieure"
        info_matchs["match_label"] = (info_matchs["home_team_name"] + " vs " + info_matchs["away_team_name"])
        list_matchs = [""] + info_matchs["match_label"].tolist()

        selected_match_label = st.sidebar.selectbox("Choisissez un match :", list_matchs) # Sélection du match dans la barre latérale

        render_glossary(lang) # Affichage du glossaire en français

        if not selected_match_label:
            st.image("src/image/match_image.jpg")
            st.info("Dérouler la barre latérale pour choisir la langue et le match à analyser")
            return

        # Récupérer le match_id correspondant au libellé choisi
        selected_row = info_matchs.loc[info_matchs["match_label"] == selected_match_label].iloc[0]
        selected_match_id = selected_row["match_id"]
        stats_path = f"src/data/matches/{selected_match_id}_stats.csv"
        stats_match_selected = pd.read_csv(stats_path)

        # Fonction pour afficher un top 5
        def display_top5(df: pd.DataFrame, col_stat: str, title: str, center: bool = True):
            # Tri et sélection des colonnes
            top5 = (
                df.sort_values(col_stat, ascending=False)
                  .loc[:, ["player_name", "player_position", "team_shortname", col_stat]]
                  .head(5)
                  .reset_index(drop=True)
            )

            # Rang
            top5.index = top5.index + 1
            top5.index.name = "Rang"

            # Renommer les colonnes pour l’affichage en français
            top5_affiche = top5.rename(columns={"player_name": "Joueur","player_position": "Poste","team_shortname": "Équipe",col_stat: "Stat"})

            st.markdown(f"<h5 style='text-align: center;'>{title}</h5>",unsafe_allow_html=True) # Affichage du sous-titre

            # Affichage du tableau
            if center:
                col_g, col_center, col_d = st.columns([1, 3, 1])
                with col_center:
                    st.dataframe(top5_affiche, width='stretch')
            else:
                st.dataframe(top5_affiche, width='stretch')

        center_tabs_css() # Fonction CSS pour centrer les onglets

        # Création des onglets
        onglet_summary, onglet_movement, onglet_off_ball, onglet_choice, onglet_press = st.tabs(["Vue d’ensemble", "Top Mouvement","Top Course sans ballon",
            "Top Bonnes décisions", "Top Pression"])

        # Onglet vue d'ensemble
        with onglet_summary:
            # top_movement et top_off_ball_runs
            col1, col2 = st.columns(2)
            with col1:
                display_top5(stats_match_selected,"top_movement","🧭 Top 5 Mouvement",center=False)
            with col2:
                display_top5(stats_match_selected,"top_off_ball_runs","🏃‍♂️ Top 5 Course sans ballon",center=False)

            # top_choice et top_press
            col3, col4 = st.columns(2)
            with col3:
                display_top5(stats_match_selected,"top_choice","🧠 Top 5 Bonnes décisions",center=False)
            with col4:
                display_top5(stats_match_selected,"top_press","🛡️ Top 5 Pression",center=False)

        # Onglet Top movement
        with onglet_movement:
            display_top5(stats_match_selected,"top_movement","🧭 Top 5 Mouvement") # Classement global

            categories_movement = build_categories(stats_match_selected, "top_movement", lang="Français") # Analyse par catégorie

            if categories_movement:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_movement = st.selectbox("Choisissez une catégorie :",list(categories_movement.keys()),key="cat_movement")

                stats_available = categories_movement[cat_movement]
                label_stat_movement = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="stat_movement")

                col_stat = stats_available[label_stat_movement]
                display_top5(stats_match_selected,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Top movement sur ce match.")

        # Onglet Top off ball runs
        with onglet_off_ball:

            display_top5(stats_match_selected,"top_off_ball_runs","🏃‍♂️ Top 5 Course sans ballon") # Classement global

            categories_off_ball = build_categories(stats_match_selected, "top_off_ball_runs", lang="Français")

            if categories_off_ball:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_off_ball = st.selectbox("Choisissez une catégorie :",list(categories_off_ball.keys()),key="cat_off_ball")

                stats_available = categories_off_ball[cat_off_ball]
                label_stat_off_ball = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="stat_off_ball")

                col_stat = stats_available[label_stat_off_ball]
                display_top5(stats_match_selected,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Top off-ball runs sur ce match.")

        # Onglet Top choice
        with onglet_choice:

            display_top5(stats_match_selected,"top_choice","🧠 Top 5 Bonnes décisions") # Classement global

            categories_choice = build_categories(stats_match_selected, "top_choice", lang="Français")

            if categories_choice:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_choice = st.selectbox("Choisissez une catégorie :",list(categories_choice.keys()),key="cat_choice")

                stats_available = categories_choice[cat_choice]
                label_stat_choice = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="stat_choice")

                col_stat = stats_available[label_stat_choice]
                display_top5(stats_match_selected,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Top choice sur ce match.")

        # Onglet Top press
        with onglet_press:

            display_top5(stats_match_selected,"top_press","🛡️ Top 5 Pression ") # Classement global

            categories_press = build_categories(stats_match_selected, "top_press", lang="Français")

            if categories_press:
                st.markdown("<h5 style='text-align: center;'>🪄 Top 5 filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_press = st.selectbox("Choisissez une catégorie :",list(categories_press.keys()),key="cat_press")

                stats_available = categories_press[cat_press]
                label_stat_press = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="stat_press")

                col_stat = stats_available[label_stat_press]
                display_top5(stats_match_selected,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Top press sur ce match.")

# Team analysis page / Page de l'analyse d'une équipe
def team_analysis():
    if lang == "English":
        st.markdown("<h4 style='text-align: center;'>🥇 Team analysis</h4>", unsafe_allow_html=True)  # Title

        info_teams = pd.read_csv("src/data/teams/team.csv")  # Load team info

        list_teams = [""] + info_teams["team_shortname"].tolist()  # Team list

        selected_team_label = st.sidebar.selectbox("Select a team:", list_teams)  # Team selection
        
        render_glossary(lang) # Glossary in English

        if not selected_team_label:
            st.image("src/image/team_image.jpg")
            st.info("Open the sidebar to choose the language and the team to analyse")
            return

        stats_teams = info_teams.copy()

        # Function to display the full table sorted by a given stat
        def display_table_full(df: pd.DataFrame, col_stat: str, title: str, center: bool = True):
            if col_stat not in df.columns:
                st.warning(f"Column {col_stat} missing from data.")
                return

            # Sort teams by the chosen statistic
            table = (
                df.sort_values(col_stat, ascending=False)
                .loc[:, ["team_shortname", col_stat]]
                .reset_index(drop=True)
            )

            # Rank
            table.index = table.index + 1
            table.index.name = "Rank"

            table_display = table.rename(columns={"team_shortname": "Team", col_stat: "Stat"})  # Rename columns for display

            # Style to highlight selected team
            def highlight_team(row):
                color = "background-color: #757575" if row["Team"] == selected_team_label else ""
                return [color] * len(row)

            styled_table = (
                table_display
                .style
                .apply(highlight_team, axis=1)
                .format({"Stat": "{:.2f}"})  # display with 2 decimals
            )

            # Title
            if title:
                st.markdown(f"<h5 style='text-align: center;'>{title}</h5>", unsafe_allow_html=True)

            # Centered display or not
            if center:
                col_g, col_center, col_d = st.columns([1, 3, 1])
                with col_center:
                    st.table(styled_table)
            else:
                st.table(styled_table)

        center_tabs_css() # CSS function to center tabs

        # Tabs creation
        tab_summary, tab_movement, tab_off_ball, tab_choice, tab_press = st.tabs(["Overview", "Top movement", "Top off-ball runs", "Top good decisions", "Top pressure"])

        # Overview tab
        with tab_summary:
            col1, col2 = st.columns(2)
            with col1:
                display_table_full(stats_teams, "top_movement", "🧭 Top movement", center=False)
            with col2:
                display_table_full(stats_teams, "top_off_ball_runs", "🏃‍♂️ Top off-ball runs", center=False)

            col3, col4 = st.columns(2)
            with col3:
                display_table_full(stats_teams, "top_choice", "🧠 Top good decisions", center=False)
            with col4:
                display_table_full(stats_teams, "top_press", "🛡️ Top pressure", center=False)

        # Movement tab
        with tab_movement:
            display_table_full(stats_teams, "top_movement", "🧭 Top movement")

            categories_movement = build_categories(stats_teams, "top_movement", lang="English")

            if categories_movement:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_movement = st.selectbox("Select a category:", list(categories_movement.keys()), key="team_cat_movement")

                stats_available = categories_movement[cat_movement]
                label_stat_movement = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="team_stat_movement",)

                col_stat = stats_available[label_stat_movement]
                display_table_full(stats_teams, col_stat, "")
            else:
                st.info("No detailed categories available for Movement for teams.")

        # Off-ball runs tab
        with tab_off_ball:
            display_table_full(stats_teams, "top_off_ball_runs", "🏃‍♂️ Top off-ball runs")

            categories_off_ball = build_categories(stats_teams, "top_off_ball_runs", lang="English")

            if categories_off_ball:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_off_ball = st.selectbox("Select a category:", list(categories_off_ball.keys()), key="team_cat_off_ball")

                stats_available = categories_off_ball[cat_off_ball]
                label_stat_off_ball = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="team_stat_off_ball",)

                col_stat = stats_available[label_stat_off_ball]
                display_table_full(stats_teams, col_stat, "")
            else:
                st.info("No detailed categories available for off-ball runs for teams.")

        # Good decisions tab
        with tab_choice:
            display_table_full(stats_teams, "top_choice", "🧠 Top good decisions")

            categories_choice = build_categories(stats_teams, "top_choice", lang="English")

            if categories_choice:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_choice = st.selectbox("Select a category:", list(categories_choice.keys()), key="team_cat_choice")

                stats_available = categories_choice[cat_choice]
                label_stat_choice = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="team_stat_choice",)

                col_stat = stats_available[label_stat_choice]
                display_table_full(stats_teams, col_stat, "")
            else:
                st.info("No detailed categories available for good decisions for teams.")

        # Pressure tab
        with tab_press:
            display_table_full(stats_teams, "top_press", "🛡️ Top pressure")

            categories_press = build_categories(stats_teams, "top_press", lang="English")

            if categories_press:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_press = st.selectbox("Select a category:", list(categories_press.keys()), key="team_cat_press")

                stats_available = categories_press[cat_press]
                label_stat_press = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="team_stat_press")

                col_stat = stats_available[label_stat_press]
                display_table_full(stats_teams, col_stat, "")
            else:
                st.info("No detailed categories available for pressure for teams.")
    else:
        st.markdown("<h4 style='text-align: center;'>🥇 Analyse d'une équipe</h4>",unsafe_allow_html=True) # On affiche le titre

        info_teams = pd.read_csv("src/data/teams/team.csv") # Chargement des informations des équipes

        list_teams = [""] + info_teams["team_shortname"].tolist() # Liste des équipes

        selected_team_label = st.sidebar.selectbox("Choisissez une équipe :", list_teams) # Sélection de l'équipe
        
        render_glossary(lang) # Affichage du glossaire en français

        if not selected_team_label:
            st.image("src/image/team_image.jpg")
            st.info("Dérouler la barre latérale pour choisir la langue et l'équipe à analyser")
            return

        stats_teams = info_teams.copy()

        # Fonction pour afficher le tableau complet trié par une stat
        def display_table_full(df: pd.DataFrame, col_stat: str, title: str, center: bool = True):
            if col_stat not in df.columns:
                st.warning(f"Colonne {col_stat} absente dans les données.")
                return

            # Tri des équipes selon la statistique choisie
            table = (
                df.sort_values(col_stat, ascending=False)
                  .loc[:, ["team_shortname", col_stat]]
                  .reset_index(drop=True)
            )

            # Rang
            table.index = table.index + 1
            table.index.name = "Rang"

            table_display = table.rename(columns={"team_shortname": "Équipe",col_stat: "Stat"}) # Renommer les colonnes pour l'affichage

            # Style pour surligner l'équipe sélectionnée
            def highlight_team(row):
                color = "background-color: #757575" if row["Équipe"] == selected_team_label else ""
                return [color] * len(row)

            styled_table = (
                table_display
                .style
                #.apply(highlight_team, axis=1)
                .format({"Stat": "{:.2f}"})  # affichage à 2 décimales
            )

            # Titre
            if title:
                st.markdown(f"<h5 style='text-align: center;'>{title}</h5>",unsafe_allow_html=True)

            # Affichage centré ou non
            if center:
                col_g, col_center, col_d = st.columns([1, 3, 1])
                with col_center:
                    st.table(styled_table)
            else:
                st.table(styled_table)

        center_tabs_css() # CSS pour centrer les onglets

        # Création des onglets
        tab_summary, tab_movement, tab_off_ball, tab_choice, tab_press = st.tabs(["Vue d’ensemble","Top Mouvement","Top Course sans ballon","Top Bonnes décisions","Top Pression"])

        # Vue d’ensemble
        with tab_summary:
            col1, col2 = st.columns(2)
            with col1:
                display_table_full(stats_teams,"top_movement","🧭 Top Mouvement",center=False)
            with col2:
                display_table_full(stats_teams,"top_off_ball_runs","🏃‍♂️ Top Course sans ballon",center=False)

            col3, col4 = st.columns(2)
            with col3:
                display_table_full(stats_teams,"top_choice","🧠 Top Bonnes décisions",center=False)
            with col4:
                display_table_full(stats_teams,"top_press","🛡️ Top Pression",center=False)

        # Onglet Mouvement
        with tab_movement:
            display_table_full(stats_teams,"top_movement","🧭 Top Mouvement")

            categories_movement = build_categories(stats_teams, "top_movement", lang="Français")
            
            if categories_movement:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>",unsafe_allow_html=True)

                cat_movement = st.selectbox("Choisissez une catégorie :",list(categories_movement.keys()),key="team_cat_movement")

                stats_available = categories_movement[cat_movement]
                label_stat_movement = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="team_stat_movement")

                col_stat = stats_available[label_stat_movement]
                display_table_full(stats_teams,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Mouvement pour les équipes.")

        # Onglet Course sans ballon
        with tab_off_ball:
            display_table_full(stats_teams,"top_off_ball_runs","🏃‍♂️ Top Course sans ballon")

            categories_off_ball = build_categories(stats_teams, "top_off_ball_runs", lang="Français")

            if categories_off_ball:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>",unsafe_allow_html=True)

                cat_off_ball = st.selectbox("Choisissez une catégorie :",list(categories_off_ball.keys()),key="team_cat_off_ball")

                stats_available = categories_off_ball[cat_off_ball]
                label_stat_off_ball = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="team_stat_off_ball")

                col_stat = stats_available[label_stat_off_ball]
                display_table_full(stats_teams,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Course sans ballon pour les équipes.")

        # Onglet Bonnes décisions
        with tab_choice:
            display_table_full(stats_teams,"top_choice","🧠 Top Bonnes décisions")

            categories_choice = build_categories(stats_teams, "top_choice", lang="Français")

            if categories_choice:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>",unsafe_allow_html=True)

                cat_choice = st.selectbox("Choisissez une catégorie :",list(categories_choice.keys()),key="team_cat_choice")

                stats_available = categories_choice[cat_choice]
                label_stat_choice = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="team_stat_choice")

                col_stat = stats_available[label_stat_choice]
                display_table_full(stats_teams,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Bonnes décisions pour les équipes.")

        # Onglet Pression
        with tab_press:
            display_table_full(stats_teams,"top_press","🛡️ Top Pression")

            categories_press = build_categories(stats_teams, "top_press", lang="Français")

            if categories_press:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>",unsafe_allow_html=True)

                cat_press = st.selectbox("Choisissez une catégorie :",list(categories_press.keys()),key="team_cat_press")

                stats_available = categories_press[cat_press]
                label_stat_press = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="team_stat_press")

                col_stat = stats_available[label_stat_press]
                display_table_full(stats_teams,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Pression pour les équipes.")

# Player analysis page / Page de l'analyse d'un joueur
def player_analysis():
    if lang == "English":
        st.markdown("<h4 style='text-align: center;'>📊 Player analysis</h4>", unsafe_allow_html=True)  # Title

        info_players = pd.read_csv("src/data/players/player.csv")  # Load data

        # Team selection
        teams = [""] + sorted(info_players["team_shortname"].dropna().unique().tolist())
        selected_team = st.sidebar.selectbox("Select a team:", teams)

        # Filter players from selected team
        if selected_team:
            players_team = info_players[info_players["team_shortname"] == selected_team].copy()
        else:
            players_team = info_players.iloc[0:0].copy()  # Empty dataframe

        players_team["player_label"] = players_team["player_name"]

        list_players = [""] + sorted(players_team["player_label"].unique().tolist())
        selected_player_label = st.sidebar.selectbox("Select a player:", list_players)

        render_glossary(lang) # Glossary in English

        # If no player selected, show intro image
        if not selected_team or not selected_player_label:
            st.image("src/image/player_image.jpg")
            st.info("Open the sidebar to choose the language and the player to analyse")
            return

        stats_players = info_players.copy()  # Stats for all players

        # Function to display Top 5 including selected player
        def display_top5_with_player(df: pd.DataFrame, col_stat: str, title: str, center: bool = True):
            if col_stat not in df.columns:
                st.warning(f"Column {col_stat} missing from data.")
                return

            # Keep only required columns
            table = (
                df.sort_values(col_stat, ascending=False)
                  .loc[:, ["player_name", "player_position", "team_shortname", col_stat]]
                  .reset_index(drop=True)
            )

            # Rank
            table = table.reset_index(drop=True)
            table.index = table.index + 1
            table.index.name = "Rank"

            # Rows corresponding to selected player
            mask_player = table["player_name"] == selected_player_label
            table_player = table[mask_player].iloc[[0]]

            top5 = table.head(5)  # Top 5

            # If player is not in Top 5 but exists in ranking
            if table_player is not None and not (top5["player_name"] == selected_player_label).any():
                top4 = table.head(4)
                display_table = pd.concat([top4, table_player], ignore_index=False)
            else:
                display_table = top5

            display_table = display_table.rename(columns={"player_name": "Player","player_position": "Pos.","team_shortname": "Team",col_stat: "Stat"}) # Rename columns

            # Style to highlight selected player
            def highlight_player(row):
                color = "background-color: #757575" if row["Player"] == selected_player_label else ""
                return [color] * len(row)

            styled_table = (
                display_table
                .style
                .apply(highlight_player, axis=1)
                .format({"Stat": "{:.2f}"})
            )

            # Title
            if title:
                st.markdown(f"<h5 style='text-align: center;'>{title}</h5>", unsafe_allow_html=True)

            # Center table or not
            if center:
                col_g, col_center, col_d = st.columns([1, 3, 1])
                with col_center:
                    st.table(styled_table)
            else:
                st.table(styled_table)

        center_tabs_css() # Function to center tabs in CSS

        # Tabs creation
        tab_summary, tab_movement, tab_off_ball, tab_choice, tab_press = st.tabs(["Overview", "Top movement", "Top off-ball runs", "Top good decisions", "Top pressure"])

        # Overview tab
        with tab_summary:
            col1, col2 = st.columns(2)
            with col1:
                display_top5_with_player(stats_players, "top_movement", "🧭 Top movement", center=False)
            with col2:
                display_top5_with_player(stats_players, "top_off_ball_runs", "🏃‍♂️ Top off-ball runs", center=False)

            col3, col4 = st.columns(2)
            with col3:
                display_top5_with_player(stats_players, "top_choice", "🧠 Top good decisions", center=False)
            with col4:
                display_top5_with_player(stats_players, "top_press", "🛡️ Top pressure", center=False)

        # Movement tab
        with tab_movement:
            display_top5_with_player(stats_players, "top_movement", "🧭 Top movement")

            categories_movement = build_categories(stats_players, "top_movement", lang="English")

            if categories_movement:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_movement = st.selectbox("Select a category:", list(categories_movement.keys()), key="player_cat_movement")

                stats_available = categories_movement[cat_movement]
                label_stat_movement = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="player_stat_movement",)

                col_stat = stats_available[label_stat_movement]
                display_top5_with_player(stats_players, col_stat, "")
            else:
                st.info("No detailed categories available for Movement for players.")

        # Off-ball runs tab
        with tab_off_ball:
            display_top5_with_player(stats_players, "top_off_ball_runs", "🏃‍♂️ Top off-ball runs")

            categories_off_ball = build_categories(stats_players, "top_off_ball_runs", lang="English")

            if categories_off_ball:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_off_ball = st.selectbox("Select a category:", list(categories_off_ball.keys()), key="player_cat_off_ball")

                stats_available = categories_off_ball[cat_off_ball]
                label_stat_off_ball = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="player_stat_off_ball")

                col_stat = stats_available[label_stat_off_ball]
                display_top5_with_player(stats_players, col_stat, "")
            else:
                st.info("No detailed categories available for off-ball runs for players.")

        # Good decisions tab
        with tab_choice:
            display_top5_with_player(stats_players, "top_choice", "🧠 Top good decisions")

            categories_choice = build_categories(stats_players, "top_choice", lang="English")

            if categories_choice:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_choice = st.selectbox("Select a category:", list(categories_choice.keys()), key="player_cat_choice")

                stats_available = categories_choice[cat_choice]
                label_stat_choice = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="player_stat_choice")

                col_stat = stats_available[label_stat_choice]
                display_top5_with_player(stats_players, col_stat, "")
            else:
                st.info("No detailed categories available for good decisions for players.")

        # Pressure tab
        with tab_press:
            display_top5_with_player(stats_players, "top_press", "🛡️ Top pressure")

            categories_press = build_categories(stats_players, "top_press", lang="English")

            if categories_press:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtered by category</h5>", unsafe_allow_html=True)

                cat_press = st.selectbox("Select a category:", list(categories_press.keys()), key="player_cat_press")

                stats_available = categories_press[cat_press]
                label_stat_press = st.selectbox("Select a statistic in this category:",list(stats_available.keys()),key="player_stat_press")

                col_stat = stats_available[label_stat_press]
                display_top5_with_player(stats_players, col_stat, "")
            else:
                st.info("No detailed categories available for pressure for players.")
    else:
        st.markdown("<h4 style='text-align: center;'>📊 Analyse d'un joueur</h4>", unsafe_allow_html=True) # On affiche le titre

        info_players = pd.read_csv("src/data/players/player.csv") # On récupère les données 

        # Sélection de l'équipe
        teams = [""] + sorted(info_players["team_shortname"].dropna().unique().tolist())
        selected_team = st.sidebar.selectbox("Choisissez une équipe :", teams)

        # Filtre des joueurs de l'équipe sélectionnée
        if selected_team:
            players_team = info_players[info_players["team_shortname"] == selected_team].copy()
        else:
            players_team = info_players.iloc[0:0].copy()  # Dataframe vide

        players_team["player_label"] = players_team["player_name"]

        list_players = [""] + sorted(players_team["player_label"].unique().tolist())
        selected_player_label = st.sidebar.selectbox("Choisissez un joueur :", list_players)

        render_glossary(lang) # Affichage du glossaire en français

        # Si aucun joueur sélectionné, on affiche l'image d'intro
        if not selected_team or not selected_player_label:
            st.image("src/image/player_image.jpg")
            st.info("Dérouler la barre latérale pour choisir la langue et le joueur à analyser")
            return

        stats_players = info_players.copy() # On récupère les stats de tous les joueurs

        # Fonction pour afficher le Top 5
        def display_top5_with_player(df: pd.DataFrame, col_stat: str, title: str, center: bool = True):
            if col_stat not in df.columns:
                st.warning(f"Colonne {col_stat} absente dans les données.")
                return

            # On garde seulement les colonnes nécessaires
            table = (
                df.sort_values(col_stat, ascending=False)
                  .loc[:, ["player_name", "player_position", "team_shortname", col_stat]]
                  .reset_index(drop=True)
            )

            # Rang
            table = table.reset_index(drop=True)
            table.index = table.index + 1
            table.index.name = "Rang"

            # On cherche les lignes correspondant au joueur sélectionné
            mask_player = table["player_name"] == selected_player_label
            table_player = table[mask_player].iloc[[0]]

            top5 = table.head(5) # On établit le Top 5

            # Si le joueur n'est pas dans le Top 5 et existe dans le classement
            if table_player is not None and not (top5["player_name"] == selected_player_label).any():
                top4 = table.head(4)
                display_table = pd.concat([top4, table_player], ignore_index=False)
            else:
                display_table = top5

            display_table = display_table.rename(columns={"player_name": "Joueur","player_position": "Poste","team_shortname": "Équipe",col_stat: "Stat"}) # Renommer les colonnes

            # Style pour surligner le joueur sélectionné
            def highlight_player(row):
                color = "background-color: #757575" if row["Joueur"] == selected_player_label else ""
                return [color] * len(row)

            styled_table = (
                display_table
                .style
                .apply(highlight_player, axis=1)
                .format({"Stat": "{:.2f}"})
            )

            # Titre
            if title:
                st.markdown(f"<h5 style='text-align: center;'>{title}</h5>", unsafe_allow_html=True)

            # Affichage centré ou non
            if center:
                col_g, col_center, col_d = st.columns([1, 3, 1])
                with col_center:
                    st.table(styled_table)
            else:
                st.table(styled_table)

        center_tabs_css() # Fonction pour centrer les onglets en CSS

        # Création des onglets
        tab_summary, tab_movement, tab_off_ball, tab_choice, tab_press = st.tabs(["Vue d’ensemble", "Top Mouvement", "Top Course sans ballon", "Top Bonnes décisions", "Top Pression"])

        # Vue d’ensemble
        with tab_summary:
            col1, col2 = st.columns(2)
            with col1:
                display_top5_with_player(stats_players,"top_movement","🧭 Top Mouvement",center=False)
            with col2:
                display_top5_with_player(stats_players,"top_off_ball_runs","🏃‍♂️ Top Course sans ballon",center=False)

            col3, col4 = st.columns(2)
            with col3:
                display_top5_with_player(stats_players,"top_choice","🧠 Top Bonnes décisions",center=False)
            with col4:
                display_top5_with_player(stats_players,"top_press","🛡️ Top Pression",center=False)

        # Onglet Mouvement
        with tab_movement:
            display_top5_with_player(stats_players,"top_movement","🧭 Top Mouvement")

            categories_movement = build_categories(stats_players, "top_movement", lang="Français")

            if categories_movement:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_movement = st.selectbox("Choisissez une catégorie :",list(categories_movement.keys()),key="player_cat_movement")

                stats_available = categories_movement[cat_movement]
                label_stat_movement = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="player_stat_movement")

                col_stat = stats_available[label_stat_movement]
                display_top5_with_player(stats_players,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Mouvement pour les joueurs.")

        # Onglet Course sans ballon
        with tab_off_ball:
            display_top5_with_player(stats_players,"top_off_ball_runs","🏃‍♂️ Top Course sans ballon")

            categories_off_ball = build_categories(stats_players, "top_off_ball_runs", lang="Français")

            if categories_off_ball:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_off_ball = st.selectbox("Choisissez une catégorie :",list(categories_off_ball.keys()),key="player_cat_off_ball")

                stats_available = categories_off_ball[cat_off_ball]
                label_stat_off_ball = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="player_stat_off_ball")

                col_stat = stats_available[label_stat_off_ball]
                display_top5_with_player(stats_players,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Course sans ballon pour les joueurs.")

        # Onglet Bonnes décisions
        with tab_choice:
            display_top5_with_player(stats_players,"top_choice","🧠 Top Bonnes décisions")

            categories_choice = build_categories(stats_players, "top_choice", lang="Français")

            if categories_choice:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_choice = st.selectbox("Choisissez une catégorie :",list(categories_choice.keys()),key="player_cat_choice")

                stats_available = categories_choice[cat_choice]
                label_stat_choice = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="player_stat_choice")

                col_stat = stats_available[label_stat_choice]
                display_top5_with_player(stats_players,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Bonnes décisions pour les joueurs.")

        # Onglet Pression
        with tab_press:
            display_top5_with_player(stats_players,"top_press","🛡️ Top Pression")

            categories_press = build_categories(stats_players, "top_press", lang="Français")

            if categories_press:
                st.markdown("<h5 style='text-align: center;'>🪄 Top filtré par catégorie</h5>", unsafe_allow_html=True)

                cat_press = st.selectbox("Choisissez une catégorie :",list(categories_press.keys()),key="player_cat_press")

                stats_available = categories_press[cat_press]
                label_stat_press = st.selectbox("Choisissez une statistique dans cette catégorie :",list(stats_available.keys()),key="player_stat_press")

                col_stat = stats_available[label_stat_press]
                display_top5_with_player(stats_players,col_stat,"")
            else:
                st.info("Aucune catégorie détaillée disponible pour Pression pour les joueurs.")

# Call of the function associated with the user request / Appel de la fonction associé à la demande de l'utilisateur
if menu in ["Menu", "Home"]:
    home()
elif menu in ["Match"]:
    match_analysis()
elif menu in ["Équipe", "Team"]:
    team_analysis()
elif menu in ["Joueur", "Player"]:
    player_analysis()