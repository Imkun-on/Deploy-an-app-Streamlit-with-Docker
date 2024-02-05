import streamlit as st
import plotly.graph_objects as go
import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import seaborn as sns
import matplotlib.image as mpimg
import plotly.express as px
import hashlib
from datetime import datetime

cards = 'cards (1).csv'
cardsets = 'cards_cardsets.csv'

cards = pd.read_csv(cards)
cardsets = pd.read_csv(cardsets)

print("Colonne in cards:", cards.columns)

cards_na = cards.dropna(subset=['level', 'attribute'])

category_orders = sorted(cards['level'].unique())

# Filtraggio delle carte con livello 0
filtered_cards1 = cards.loc[cards['level'] == 0]

# Selezionare solo alcune colonne specifiche
filtered_cards = filtered_cards1[['name', 'race', 'level', 'atk', 'def', 'attribute', 'type']]

filtered_card = cards[(cards['type'].isin(['Spell Card', 'Trap Card'])) & (cards['race'].isin(['Continuous', 'Counter','Countinuous','Normal','Equip','Field','Ritual','Quick-Play']))]

filtered_fusion = cards[(cards['type'].isin(['Fusion Monster', 'Link Monster', 'XYZ Monster','Synchro Monster','Synchro Tuner Monster', 'Pendulum Effect Fusion Monster','Synchro Pendulum Effect Monster','Pendulum Effect Fusion Monster','Token','XYZ Pendulum Effect Monster']))] 

filtered_main = cards[(cards['type'].isin(['Effect Monster','Normal Monster','Flip Effect Monster','Union Effect Monster','Pendulum Effect Monster','Tuner Monster','Gemini Monster','Normal Tuner Monster','Spirit Monster','Ritual Effect Monster','Skill Card','Ritual Monster','Toon Monster','Pendulum Normal Monster','Pendulum Tuner Effect Monster','Pendulum Effect Ritual Monster','Pendulum Flip Effect Monster']))] 

banned_cards = cards[(cards['ban_tcg'].isin(['Semi-Limited', 'Limited', 'Banned']))]

banned_cards2 = cards[(cards['ban_ocg'].isin(['Semi-Limited', 'Limited', 'Banned']))]

banned_cards3 = cards[(cards['ban_goat'].isin(['Semi-Limited', 'Limited', 'Banned']))]

somma_per_attributo3 = cards.groupby('attribute')['upvotes'].sum().reset_index()
somma_per_attributo3 = somma_per_attributo3.sort_values(by='upvotes', ascending=False)

somma_per_attributo4 = cards_na.groupby('race')['upvotes'].sum().reset_index()
somma_per_attributo4 = somma_per_attributo4.sort_values(by='upvotes', ascending=False)

# Definizione della funzione per identificare le carte trappola
def is_trap_card(description):
    phrases = [
        "This card is also still a Trap",
        "This card is NOT treated as a Trap",
        "This card is also a Trap Card",
        "This card is treated as a Trap Card",
        "This card is still treated as a Trap Card",
        "This card is also still a Trap Card",
        "This card is NOT treated as a Trap Card"
    ]
    return any(phrase in description for phrase in phrases)

# Applicazione della funzione al dataframe
trap_cards = cards[cards['desc'].apply(is_trap_card)]

# Filtraggio delle carte
filtered_cardss = trap_cards.loc[(trap_cards['race'] == 'Continuous') | (trap_cards['race'] == 'Normal')]

# Selezione delle colonne di interesse
filtered_columns = filtered_cardss[['name', 'type', 'desc', 'race', 'upvotes']]

# Ordinamento del dataframe
filtered_columns_sorted = filtered_columns.sort_values(by='name', ascending=True)



cardsets1 = cardsets.drop(columns=["set_id", "set_code"])

cardsets1 = cardsets1.rename(columns={"card_id": "id"})


# Aggiunta di una colonna per il conteggio
cards['count'] = 1

# Gestione dei valori mancanti per la colonna 'staple'
cards['staple'] = cards['staple'].fillna('No')

# Calcolo del numero di carte staple e non staple
staple_counts = cards.groupby('staple')['count'].sum().reset_index()
staple_counts = staple_counts.rename(columns={'count': 'Count'})

# Calcolo del numero di carte staple per tipo
staple_type_counts = cards.groupby(['type', 'staple'])['count'].sum().reset_index()
staple_type_counts = staple_type_counts[staple_type_counts['staple'] == 'Yes']
staple_type_counts = staple_type_counts.rename(columns={'count': 'Count'})

custom_palettes = {
    "Spell Card": "#c9c9c9",
    "Link Monster": "#b768a2",
    "XYZ Monster": "#000000", 
    "Effect Monster": "#FF9912",
    "Tuner Monster": "#b3b3b3", 
    "Trap Card": "#1a1a1a", 
    "Fusion Monster": "#7a7a7a"}

fig = px.pie(staple_type_counts, values='Count', names='type', color_discrete_map=custom_palettes)
fig.update_layout(title="", legend_title="Type", title_x=0.5, width=900, height=600)

# Filtraggio delle carte staple
filtered_cards = cards.loc[(cards['staple'] == 'Yes')]
filtered_columns = filtered_cards[['name', 'type', 'upvotes', 'views', 'ban_tcg', 'ban_ocg', 'staple']]
filtered_columns_sorted = filtered_columns.sort_values(by='upvotes', ascending=True)

# Preparazione dei dati
cards_nas = cards.dropna(subset=['treated_as'])
type_counts = cards_nas['type'].value_counts().reset_index()
type_counts.columns = ['type', 'Count']

# Creazione del grafico a torta
fig = px.pie(type_counts, values='Count', names='type')
fig.update_layout(title="",legend_title="Type", title_x=0.5, width=900, height=800)

# Filtraggio delle carte 'treated_as'
cards_nas['treated_as'] = 'Yes'
filtered_cards = cards_nas.loc[cards_nas['treated_as'] == 'Yes']
filtered_columns = filtered_cards[['name', 'type', 'upvotes', 'views', 'ban_tcg', 'ban_ocg', 'treated_as', 'staple']]
filtered_columns = filtered_columns.sort_values(by='upvotes', ascending=True) 

##----------------------------------------------------------------------------------------------------------------------------------------------------------------##
# Placeholder per il contenuto principale
main_content = st.empty()

# Opzioni nella barra laterale
opzione = st.sidebar.selectbox("Select the variable:", ["Home", "Dataset", "Atk & Def by Levels", "Types", "Attributes", "Race", "Views & Votes", "Ban", "Card Trap Monster", "Rarity", "Staple", "Treated_as", "Temporal Analysis"])

##-----------------------------------HOME----------------------------------------------##
if opzione == "Home":
    with main_content.container():
        st.markdown("""
        <body>
<h1> <center> <b> <strong> <font size="10">Yu-Gi-Oh Cards Game</font></strong> </b> </center> </h1>
<h5>👇🏻 If you're not familiar with the Yu-Gi-Oh card game, then I recommend reading this brief introduction 👇🏻</h5>
    <p>Yu-Gi-Oh! is a card game where two players try to defeat each other by reducing the opponent's Life Points (down to 0) using a collection of monster, magic, and trap cards.</p>
    <p>In addition to your decks, you'll need some extra items to assist you in the game. These items include:</p>
    <ul>
        <li><strong>A coin</strong>: Some cards require flipping a coin.</li>
        <li><strong>Dice</strong>: Some cards require a dice roll.</li>
        <li><strong>Counters</strong>: Any small object that can be used as an indicator to keep track of certain metrics that may affect some cards.</li>
        <li><strong>Monster Tokens</strong></li>
    </ul>
    <p>For more information on the card game, visit the following link <a href="https://www.dacardworld.com/gaming/yu-gi-oh-cards/how-to-play#:~:text=%2DGi%2DOh!-,Yu%2DGi%2DOh!,%2C%20spell%2C%20and%20trap%20cards." target="_blank"> How to Play Yu-Gi-Oh! 🎲</a></p>
    <h1> <center> <b> <strong> <font size="6">How is a Yu-Gi-Oh card structured?</font></strong> </b> </center> </h1>
    <ul>
        <li><strong>Name</strong>: Each card has its unique name, used to identify the card.</li>
        <li><strong>Attribute</strong>: All monsters in the game have one of the 7 attributes: DARK, LIGHT, FIRE, WATER, EARTH, WIND, and DIVINE (located at the top right of the card).Spells/Traps do not have Attributes but indicate whether the card is a Spell or a Trap.</li>
        <li><strong>Image</strong>: The image used to represent the card.</li>
        <li><strong>Level</strong>: Most monsters in Yu-Gi-Oh have a Level, indicated by the number of stars below the name.</li>
        <li><strong>Type</strong>: Enclosed in square brackets, denotes the characteristic of the card. For monsters, it is located between the image and the card's description, while for spells and traps, it is located between the name and the image.</li>
        <li><strong>Description</strong>: The text indicating the effect of a card or its lore without having any impact on the game.</li>
        <li><strong>Attack and Defense</strong>: The offensive and defensive power of a monster.</li>
        <li><strong>ID</strong>: An 8-digit identification number of the card. It is found at the bottom left.</li>
        <li><strong>Set Number</strong>: All Yu-Gi-Oh cards have a set number. It is located below the bottom right corner of the image.</li>
        <li><strong>Eye of Anubis</strong>: The hologram of the Eye of Anubis is a foil security symbol placed at the bottom right of all official Yu-Gi-Oh! cards.</li>
        <li><strong>Border</strong>: The colored area to identify the cards at a glance.</li>
    </ul>
    <p> To enlarge, click on the various cards you find 👇</p>
    <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/89631139.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/89631139.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/55410871.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/55410871.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/43228023.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/43228023.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/59822133.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/59822133.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/17655904.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/17655904.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/56920308.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/56920308.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
  </div>
</body>
</html>""", unsafe_allow_html=True)


##-----------------------------------DATASET----------------------------------------------##
if opzione == "Dataset":
    with st.container():
      st.markdown("<h3 style='text-align: center;'>Dataset Summary</h3>", unsafe_allow_html=True)
                # Tabella delle variabili del dataset
      st.markdown("""
        | Variables | Description |
        |:----------|:------------|
        | *`Id`* | Card identification number. |
        | *`Name`* | Card name. |
        | *`Type`* | Card type. |
        | *`Desc`* | Card description. |
        | *`Atk`* | Attack value. |
        | *`Def`* | Defense value. |
        | *`Level`* | Monster card level. |
        | *`Race`* | Monster card race. |
        | *`Attribute`* | Monster card attribute. |
        | *`Scale`* | Pendulum scale value. |
        | *`Archetype`* | Cards that share a specified name string in a card's effect. |
        | *`Linkval`* | The Link value of the card if it's a "Link Monster". |
        | *`LinkMarkers`* | Represented by red arrows radiating outward from the artistic frame of the Link Monster. |
        | *`Image_url`* | Card image link. |
        | *`Imagew_url_small`* | Small card image link. |
        | *`Ban_Tcg`* | Card status in the TCG Forbidden List. |
        | *`Ban_Ocg`* | Card status in the OCG Forbidden List. |
        | *`Ban_Goat`* | Card status in the GOAT Format Forbidden List. |
        | *`Staple`* | Refers to a card that is generally powerful and can be played in any deck. |
        | *`Views`* | Number of card views. |
        | *`ViewsWeek`* | Number of card views per week. |
        | *`Upvotes`* | Number of positive votes for the card. |
        | *`Downvotes`* | Number of negative votes for the card. |
        | *`Formats`* | Card format. |
        | *`Treated_as`* | Card that, in the description, can be called by another name. |
        | *`Tcg_Date`* | Publication date of the card in TCG (America, Europe). |
        | *`Ocg_Date`* | Publication date of the card in OCG (Japan, Asia, China, Korea). |
        | *`Has_effect`* | Has an effect (1 yes & 0 no). |
        """, unsafe_allow_html=True)
    # Centrare il testo con HTML e CSS
    st.markdown("---", unsafe_allow_html=True)

    st.markdown("<h3 style='text-align: center;'>Dataset Structure</h3>", unsafe_allow_html=True)

    st.dataframe(cards)

##-----------------------------------ATK & DEF----------------------------------------------##

if opzione == "Atk & Def by Levels":
    with st.container():
        st.markdown("""<body>
    <h2 style="text-align: center;">
  <b>
    <strong>
      <font size="6,9" color="darkslategray">Analysis of Atk & Def Values by Levels</font>
    </strong>
  </b>
     </h2>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)        
        st.markdown("<h3 style='text-align: center;'>Distribution of Card Levels</h3>", unsafe_allow_html=True)
        # Creazione del grafico
        fig = px.histogram(cards_na, x='level',color='level',category_orders={'level': category_orders})
        fig.update_layout(xaxis_title='Level',yaxis_title='Number of Cards', title_text="", legend_title_text='Level', title_x=0.5, width=900, height=700)
        # Mostra il grafico nella pagina Streamlit
        st.plotly_chart(fig)    
        st.markdown("---", unsafe_allow_html=True)    
        st.markdown("<h3 style='text-align: center;'>Comparison of Attack and Defense Values by Level</h3>", unsafe_allow_html=True)
        fig = px.scatter(cards_na, x='atk', y='def', color='level', symbol='has_effect', hover_name="type")
        fig.update_layout(legend=dict(orientation="h"))  
        fig.update_layout(xaxis_title='Attack Value', yaxis_title='Defense Value', title_text="",legend_title_text='Has Effect', title_x=0.5, width=900, height=800)
        # Mostra il grafico nella pagina Streamlit
        st.plotly_chart(fig)
        st.markdown("---", unsafe_allow_html=True)

        st.markdown("""<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <p>In the histogram, it's evident that the majority of monster cards fall into level 4.</p>
  <p>However, it's noteworthy that a card's level doesn't necessarily determine its strength. In fact, the analysis of the scatterplot reveals that many cards gain power through their unique effects. An example of this is represented by the following cards:</p>
  <div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/15397015.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/15397015.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/16428514.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/16428514.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/53143898.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/53143898.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/86120751.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/86120751.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/60303688.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/60303688.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <!-- Add more card divs as needed... -->
  </div>
</body>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <p>On the other hand, it's important to observe in the scatterplot that as the card level increases, so do the values of ATK and DEF.</p>
  <p>It's crucial to keep in mind that some cards don't follow this trend, as their ATK and DEF values (represented as "???") depend on specific effects indicated on the card. This is the case for cards like:</p>
  <div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/15862758.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/15862758.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/8400623.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/8400623.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/71544954.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/71544954.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/5008836.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/5008836.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/85115440.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/85115440.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
  </div>
</body>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <p>It's also important to note that most cards with ATK and DEF values equal to zero possess extraordinary effects, such as:</p>
  <div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/78371393.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/78371393.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/64631466.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/64631466.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/8062132.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/8062132.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/72677437.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/72677437.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/3657444.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/3657444.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <!-- Add more card divs as needed... -->
  </div>
  <p>These data confirm that a card's power is not exclusively tied to ATK and DEF values but is strongly influenced by special effects that can disrupt opponents' strategies.</p>
</body>
</html>""", unsafe_allow_html=True)

##-----------------------------------TYPES----------------------------------------------##

if opzione == "Types":
    with st.container():
        st.markdown("""<body>
    <h2 style="text-align: center;">
  <b>
    <strong>
      <font size="6,9" color="darkslategray">Analysis of the types of Yu-Gi-Oh! cards</font>
    </strong>
  </b>
     </h2>
     """, unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("""<body>
    <p>Due to the diverse range of card types available, I've chosen to divide this column into different sections, thus reflecting the structure of the playing arena.</p>
    <p align="center">
        <div style="display: flex; flex-wrap: wrap;">
        <div style="width: 33.33%; padding: 10px;">
            <a href="data:image/jpeg;base64,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"_blank">
                <img src="data:image/jpeg;base64,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" style="width: 100%;" alt="Image description">
            </a>
        </div>
              </div>
    </p>
    <h5>This allows me to gain a clearer insight into the following aspects:</h5>
    <ul>
        <li>Extra Deck</li>
        <li>Main Deck</li>
        <li>Spell & Trap Zone</li>
    </ul>
    <p> I begin by examining the Spell & Trap Zone, which encompasses various types of cards: </p>
    <ul>
        <li><strong>Quick-Play Spells:</strong> Allow the turn player to activate Quick-Play Spell Cards from their hand during any Phase of their turn. Additionally, each player can activate Set Quick-Play Spell Cards during any Phase in any player's turn. Quick-Play Spell Cards are recognizable by the lightning bolt symbol.</li>
        <li><strong>Equip Spells:</strong> Can be equipped to face-up monsters on the field. These cards are marked with a target symbol.</li>
        <li><strong>Continuous Spells:</strong> Remain on the field once activated. They are recognizable by the infinity symbol.</li>
        <li><strong>Field Spells:</strong> Often focused on boosting ATK and/or DEF for cards with specific attributes, types, or archetypes. They are distinguished by the compass rose symbol.</li>
        <li><strong>Normal Spells:</strong> Allow the turn player to set a Normal Spell Card and activate it in the same turn. This option is useful if the player intends to use the effects of cards that require discarding cards from the hand to protect their cards on the field. Normal Spell Cards do not have any distinctive symbols.</li>
        <li><strong>Ritual Spells:</strong> Used to ritually summon Ritual Monsters and are characterized by the flaming chalice symbol.</li>
    </ul>
    <p> Now, let's move on to Trap Cards: </p>
    <ul>
        <li><strong>Normal Traps:</strong> Can be activated in response to the effects of Effect Monsters, Spell Cards, as well as most other Trap Cards and Quick-Play Spell Cards. Normal Trap Cards do not have any distinctive symbols.</li>
        <li><strong>Counter Traps:</strong> Most of these cards can only be activated to negate or punish the activation of other cards or the Summoning of monsters. These cards are recognizable by the curved arrow symbol.</li>
        <li><strong>Continuous Traps:</strong> Remain on the field after activation. The effects of these cards will remain active until the owner is unable to pay the cost or fulfill the conditions specified on the card (if any) OR until it is destroyed.</li>
    </ul>

<p>As for the Extra Deck zone, I will examine this area in detail in the temporal analysis.</p>

</body>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center;'>Distribution of Spell and Trap Cards</h3>", unsafe_allow_html=True)
        # Grafico per le carte Spell e Trap
        fig1 = px.histogram(filtered_card, x="race", color="race", facet_col="type")
        fig1.update_layout(yaxis_title='Number of Cards', title_text="", legend_title_text='Type', title_x=0.5, width=900, height=700)
        st.plotly_chart(fig1)
        # Grafico per le carte dell'extra deck
        custom_palette = {
            "Fusion Monster": "#b768a2",
            "Link Monster": "#483d8b",
            "XYZ Monster": "#1a1a1a",
            "Synchro Monster": "#c9c9c9",
            "Synchro Tuner Monster": "#b3b3b3",
            "Token": "#7a7a7a",
            "Pendulum Effect Fusion Monster": "#a020f0",
            "Synchro Pendulum Effect Monster": "#7d26cd",
            "XYZ Pendulum Effect Monster": "#212121"}
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center;'>Which cards are most common in the extra deck?</h3>", unsafe_allow_html=True)
        fig2 = px.histogram(filtered_fusion, x="type", color="type", color_discrete_map=custom_palette)
        fig2.update_layout(xaxis_title='Type', yaxis_title='Number of Cards', title_text="", legend_title_text='Type', title_x=0.5, width=900, height=700)
        fig2.update_xaxes(categoryorder='total descending')
        st.plotly_chart(fig2)
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center;'>Which monster type is most common?</h3>", unsafe_allow_html=True)
        # Grafico per i tipi di mostri nel main deck
        fig3 = px.histogram(filtered_main, x="type", color="type")
        fig3.update_layout(yaxis_title='Number of Cards', xaxis_title='Type', title_text="", legend_title_text='Type', title_x=0.5, width=900, height=700)
        fig3.update_xaxes(categoryorder='total descending')
        st.plotly_chart(fig3)
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <p>From the following histograms, it is evident that normal Spell and Trap cards are the most common, followed by Continuous and Quick-Play Spell cards. For Traps, Continuous Traps follow Quick-Play Traps.</p>

  <p>The reason for this distribution is simply because some Spell cards include elements necessary to summon monsters from the Extra Deck through Fusion or Synchro, as well as for the special summoning of monsters that can only be summoned using a specific Spell or Trap card.</p>

  <p>Regarding monsters in the Extra Deck, Xyz monsters are the most frequent, followed by Fusion monsters, with Synchro monsters in third place.</p>
  
  <p>The reason Xyz monsters are more common and appreciated is that they do not require the use of Spell cards for summoning, only monsters whose levels are indicated on the card. This feature also applies to Synchro monsters. However, what makes Xyz monsters unique is their ability to detach the monsters used for the summoning to activate an additional effect.</p>

  <p>It should be noted that among Fusion monsters, some do not require Spell cards to be summoned.</p>

  <p>As for Link Monsters, being recently introduced, there are 30 fewer in total compared to Synchro monsters, suggesting that in the future, this new type might secure the third position.</p>

  <p>In the third histogram, the most common type consists of monsters with effects capable of triggering a chain reaction for summoning other monsters or annihilating the opponent's cards. As for Ritual monsters, their minority is due to the fact that they can only be summoned through Ritual Spell cards. In fact, even in the first histogram, Ritual Spell cards occupy the last position.</p>

  <p>Here's a list for better understanding:</p>
  <div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/80796456.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/80796456.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/6150044.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/6150044.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/24094653.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/24094653.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/91998119.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/91998119.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/60800381.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/60800381.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/98978921.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/98978921.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/64631466.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/64631466.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/41426869.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/41426869.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/8062132.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/8062132.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/16067089.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/16067089.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <!-- Add more card divs as needed... -->
  </div>
</body>
    """, unsafe_allow_html=True)

##-----------------------------------ATTRIBUTES----------------------------------------------##

if opzione == "Attributes":
    with st.container():
        st.markdown("""
        <h2 style="text-align: center;">
  <b>
    <strong>
      <font size="6,9" color="darkslategray">Analysis of Yu-Gi-Oh! cards attributes</font>
    </strong>
  </b>
     </h2>
    """, unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)

        # Definizione della palette di colori personalizzata
        custom_palette = {
            "DARK": "#5d3954",
            "EARTH": "#cd853f",
            "LIGHT": "#fedf00",
            "WATER": "#00b2ee",
            "WIND": "#00ff7f",
            "FIRE": "#ff0000",
            "DIVINE": "#ffae42"
        }
        st.markdown("<h3 style='text-align: center;'>Which attribute is the most common and which is the least?</h3>", unsafe_allow_html=True)
        # Creazione del primo grafico Plotly
        fig1 = px.histogram(cards_na, x='attribute', color='attribute', color_discrete_map=custom_palette)
        fig1.update_layout(xaxis_title='Attribute', yaxis_title='Frequency', title_text="", legend_title_text='Attribute', title_x=0.5, width=900, height=700)
        fig1.update_xaxes(categoryorder='total descending')
        st.plotly_chart(fig1)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Which attribute is the most preferred and which is the least?</h3>", unsafe_allow_html=True)
        # Creazione del secondo grafico Plotly
        fig2 = px.bar(somma_per_attributo3, x='attribute', color='attribute', color_discrete_map=custom_palette, y='upvotes', title="Sum of Visual Upvotes per Attribute")
        fig2.update_layout(xaxis_title='Attribute', yaxis_title='Frequency', title_text="", legend_title_text='Attribute', title_x=0.5, width=900, height=700)
        st.plotly_chart(fig2)
        st.markdown("---", unsafe_allow_html=True)

        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
  <h4> <center> <b> <strong> <font size="6">What are the most common attributes and which ones are the most favored?</font></strong> </b> </center> </h4>

  <p>In both histograms, the "Dark" attribute takes the first position, followed by "Earth," "Light," "Water," "Wind," and "Fire." However, when focusing on preference, it is noticeable that the "Light" attribute is more appreciated than "Earth," while "Wind" is less popular than "Fire."</p>

  <p>But what makes one attribute more appreciated than the other? Let's examine them one by one:
    <ul>
      <li><strong>Darkness:</strong> It stands out as the best attribute, both for the effectiveness of the cards and for deck or archetype creation, creating a powerful synergy with spells and traps. Konami strives to integrate cards from other attributes into this, as demonstrated in the "PredaPlant" archetype, where plant monsters are part of the "Darkness" attribute instead of the "Earth" attribute.</li>
      <li><strong>Light:</strong> Similarly to darkness, the "Light" attribute includes various races, including fairies, machines, warriors, dragons, and demons. These two attributes stand out for the versatility of their abilities. Two notable examples are the "Cyber Dragon" and "ABC" archetypes.</li>
      <li><strong>Earth:</strong> Most monsters of this attribute specialize in negating the effects of other monsters, spells, and traps. This aspect is evident in archetypes such as "Ancient Gear," "Naturia," and "Infinity Track."</li>
      <li><strong>Water:</strong> Thanks to their versatility, water monsters can be used in various strategies due to their diverse abilities. The predominant strategy for "Water" decks is to build a defensive wall on the opponent's field while accumulating resources. This tactic makes most "WATER" decks oriented towards a more defensive play, but it takes time to properly execute the combos. A tangible example is provided by the cards of the 'Nubian' archetype (one of my favorites).</li>
      <li><strong>Fire:</strong> "Fire" monsters often focus on the "Burn" mechanic, inflicting effect damage to the opponent. However, this attribute is less appreciated due to the scarcity of notable archetypes, such as "Infernable Knight," "Vulcanics," "Flamewell," "Shiranouiu," and "Hazy Flames." The reason for Konami's low consideration of this attribute remains a mystery.</li>
      <li><strong>Wind:</strong> This attribute takes the penultimate position, with the fewest support cards compared to other attributes (excluding "DIVINE"). The amount of support cards for spells and traps is significantly lower than other attributes, despite the generally limited presence of spell and trap cards related to existing attributes and the minimum requirements to dedicate a significant number of these cards to a specific attribute family.</li>
      <li><strong>Divine:</strong> This attribute ranks last, represented by only six monsters, including the famous three Egyptian deities. The "Winged Dragon of Ra" even offers two alternative forms, while the "Creator" completes the group. Only two of these cards are widely recognized as significant, namely "Sphere Mode of Ra" and "Creator."</li>
    </ul>
  <p>Here is a list of cards by attribute to have a clearer view of what you've read.</p>
  <div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/66309175.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/66309175.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/1546123.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/1546123.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/33198837.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/33198837.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/20003527.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/20003527.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/32543380.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/32543380.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/73125233.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/73125233.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
      <a href="https://images.ygoprodeck.com/images/cards/10000080.jpg" target="_blank">
        <img src="https://images.ygoprodeck.com/images/cards/10000080.jpg" style="width: 100%;" alt="Image description">
      </a>
    </div>
    <!-- Add more card divs as needed... -->
  </div>
  <p>In conclusion, the preference for attributes is influenced by a combination of card effects and gameplay strategies. Each of these attributes has its own role and unique characteristics within the game, offering enthusiasts a wide variety of tactical options.</p>
</body>""", unsafe_allow_html=True)

##-----------------------------------RACES----------------------------------------------##
if opzione == "Race":
    with st.container():
        st.markdown("""
        <h3 style="text-align: center;">
  <b>
    <strong>
      <font size="8" color="darkslategray">Breed Analysis</font>
    </strong>
  </b>
     </h3>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Which race is the most common and which one is the least?</h3>", unsafe_allow_html=True)
        figx = px.histogram(cards_na, x='race',color='race')
        figx.update_layout(xaxis_title='Race', yaxis_title='Number of Cards', title_text="", legend_title_text='Race', width=900, height=800, title_x=0.5)
        figx.update_xaxes(tickangle=45)
        figx.update_xaxes(categoryorder='total descending')
        st.plotly_chart(figx)

        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center;'>Which breed is more popular than the others?</h3>", unsafe_allow_html=True)
        st.dataframe(somma_per_attributo4)
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div style="display: flex; flex-direction: row; overflow-x: auto;">
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/15180041.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/15180041.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/83104731.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/83104731.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/31764700.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/31764700.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/40737112.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/40737112.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/61257789.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/61257789.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>     
    </div>
</body>
</html>""", unsafe_allow_html=True)

        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("""
        <body>
<h3> <center> <b> <strong> <font size="6">Yu-Gi-Oh! and Its Races: What Makes Some More Popular Than Others?</font></strong> </b> </center> </h3>


<p>From the histogram, it's noticeable that the "warrior" category takes the first place, followed by "machine," "demon," "spellcaster," and "dragon."</p>
    <h3>What makes this category better than the others?</h3>
    <ul>
        <li><strong>Warrior:</strong> "Warrior" is a diverse, versatile, and popular Monster Card type. There are Warriors of every Attribute, mainly EARTH, DARK, and LIGHT. Their varied and versatile strategies make them arguably one of the best types.</li>
        <li><strong>Machine:</strong> "Machine" monsters rely on high ATTACK values and a variety of powerful effects. Their general strategy varies, but they often have the ability to negate the effects of specific opponent's cards and/or destroy them.</li>
        <li><strong>Demon:</strong> "Demons" are one of the most established and powerful Types in the Yu-Gi-Oh! franchise. Most demons focus on offensive "beatdown" tactics and destroying opponent's cards, putting pressure with stunning effects, lockdown, banishment effects, or deck milling.</li>
        <li><strong>Spellcaster:</strong> Most of these creatures have effects and can be very versatile, often used with Magic Card support. Among all types, Spellcasters are the most present in current Forbidden and Limited lists.</li>
        <li><strong>Dragon:</strong> "Dragons" tend to be the strongest boss monsters or have remarkable effects, being one of the most established and powerful Monster types in the entire franchise. Dragon monsters are known for having higher ATTACK values than any other monster type in the game and being one of the most popular monster types.</li>
    </ul>
    <h3>So why are all the other cards not falling into this category less common?</h3>
    <p>To answer this question, I consider only the most relevant types positively and negatively.</p>
    <p>Regarding the positive points:</p>
    <ul>
        <li><strong>Zombie:</strong> Zombie types have some of the best generic support cards in the entire game, like "Uni-Zombie" and "Mezuki" present in every Zombie deck. "Zombie World" on the field (which turns all cards into Zombie types) can also lock the opponent in summoning any non-Zombie type monsters when "Rivalry Of Warlords" is on the field.</li>
        <li><strong>Cyberse:</strong> It's the latest type to enter Yu-Gi-Oh!, and despite its young age, it's one of the best. The Cyberse type is a significant part of the Link Monster mechanics, with most Monsters being Link Monsters. When it comes to dedicated Cyberse decks, "Salamangreat" has consistently been on top since its introduction, despite some of its cards being banned.</li>
    </ul>
    <p>Regarding the negative points:</p>
    <ul>
        <li><strong>Divine-Beast:</strong> The only cards that make up the Divine-Beast Type are the iconic Egyptian God Cards. The only Divine-Beast card that sees some utility is "The Winged Dragon of Ra - Sphere Mode" as a way to clear the opponent's field.</li>
        <li><strong>Pyro:</strong> It's one of the unluckiest. Over the years, it has received very little support, and what it got had a very limited impact on the metagame. The only usable Pyro-type deck was "Volcanic," which has long surpassed its peak.</li>
        <li><strong>Reptile:</strong> It's a type that has the potential to be one of the best types in the entire game. Reptiles have many great archetypes like "Aliens" and "Worms," but none of them come close to being good. Maybe one day Reptiles will get the "Rock" type treatment where a new archetype makes them one of the best, but for now, Reptiles are at the bottom of the barrel.</li>
        <li><strong>Fish:</strong> There has never been a good Fish-type archetype, with the only exception being some Mermail cards, consisting of Fish, Sea Serpent, and Aqua. Despite that, there are no good Fish-type decks that can make use of these powerful cards, leaving them as the worst of the worst when it comes to types.</li>
    </ul>
    <p>However, there's a key reason why some types of cards are more common than others, and it's closely tied to the release dates of the cards. Over the years, new card types and races have been introduced, a topic I'll delve into in detail later. (Temporal Analysis section)</p>
</body>""", unsafe_allow_html=True)

        


##-----------------------------------VIEWS & VOTES----------------------------------------------##

if opzione == "Views & Votes":
    with st.container():
        st.markdown("""
        <h3 style="text-align: center;">
  <b>
    <strong>
      <font size="8" color="darkslategray">Analysis between views and votes of Yu-Gi-Oh! cards</font>
    </strong>
  </b>
     </h3>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Do cards with effects tend to have more upvotes and, at the same time, more views?</h3>", unsafe_allow_html=True)

        # Grafico degli upvotes
        fig1 = px.scatter(cards, x='upvotes', y='views', color='type', symbol="has_effect")
        fig1.update_layout(xaxis_title='Upvotes', yaxis_title='Views', title_text="", legend_title_text='Type', title_x=0.5, width=900, height=850)
        st.plotly_chart(fig1)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Top 10 Upvotes Cards</h3>", unsafe_allow_html=True)

        # Tabella degli upvotes
        filtered_cards_upvotes = cards.loc[(cards['upvotes'] <= 2608) & (cards['upvotes'] >= 423)]
        filtered_columns_upvotes = filtered_cards_upvotes[['name', 'upvotes', 'views']].sort_values(by='upvotes', ascending=False)
        st.dataframe(filtered_columns_upvotes)

        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div style="display: flex; flex-direction: row; overflow-x: auto;">
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/5405694.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/5405694.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/46986414.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/46986414.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/62873545.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/62873545.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/72989439.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/72989439.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/54484652.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/54484652.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/77498348.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/77498348.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/10000020.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/10000020.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/12580477.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/12580477.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/2099841.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/2099841.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/89631139.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/89631139.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>        
    </div>
</body>""", unsafe_allow_html=True)        
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Are cards with negatively reviewed effects also the most discussed?</h3>", unsafe_allow_html=True)
        # Grafico dei downvotes
        fig2 = px.scatter(cards, x='downvotes', y='views', color='type', symbol="has_effect")
        fig2.update_layout(xaxis_title='Downvotes', yaxis_title='Views', title_text="", legend_title_text='Type', title_x=0.5, width=900, height=850)
        st.plotly_chart(fig2)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Top 10 Downvotes Cards</h3>", unsafe_allow_html=True)
        # Tabella dei downvotes
        filtered_cards_downvotes = cards.loc[(cards['downvotes'] <= 533) & (cards['downvotes'] >= 109)]
        filtered_columns_downvotes = filtered_cards_downvotes[['name', 'downvotes', 'views', 'ban_tcg', 'ban_ocg', 'ban_goat']].sort_values(by='downvotes', ascending=True)
        st.dataframe(filtered_columns_downvotes)
        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <div style="display: flex; flex-direction: row; overflow-x: auto;">
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/61740673.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/61740673.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/88581108.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/88581108.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/89631139.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/89631139.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/11384280.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/11384280.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/46986414.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/46986414.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/2099841.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/2099841.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
                <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/76375976.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/76375976.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/71791814.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/71791814.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/34541863.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/34541863.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/50588353.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/50588353.jpg" style="width: 100%;" alt="Descrizione dell'immagine">
            </a>
        </div>
    </div>
</body>
</html>""", unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("""
        <body>
    <p>In both charts, a card stands out, "Ash Blossom & Joyous Spring," which, despite having a significant number of views, is also the least rated compared to others.</p>
    
<div>
        <a href="https://images.ygoprodeck.com/images/cards/14558127.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/14558127.jpg" alt="Image" style="float: left; margin-right: 30px; width: 200px; height: 300px;">
        </a>
        <p>But why is this card so discussed?</p>
        <p>There are several reasons:</p>
        <ul>
            <li><strong>Secret Rare Edition:</strong> Originally printed in the "Maximum Crisis" series in May 2017, this card was only available in Secret Rare edition, and a set of three copies could cost up to €200.00.</li>
            <li><strong>Triple Effect:</strong> "Ash Blossom & Joyous Spring" is known for its triple effect, allowing it to counter various opponent's effects:</li>
            <li><strong>(1)</strong> Special summon a monster from the deck.</li>
            <li><strong>(2)</strong> Send a card from the deck to the graveyard.</li>
            <li><strong>(3)</strong> Add a card from the deck to the hand.</li>
        </ul>       
    </div>
</body>""", unsafe_allow_html=True)

    st.markdown("""
        <!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <p>However, this doesn't necessarily mean that monster cards with effects are the most discussed. For instance, in the first scatterplot, the card with the highest number of positive votes is "Black Luster Soldier," which, unlike "Ash Blossom & Joyous Spring," has no special effect.</p>
    """, unsafe_allow_html=True)
    st.markdown("---", unsafe_allow_html=True)
    st.markdown("""
    <h6>So, why is "Black Luster Soldier" so beloved despite having a considerable number of views?</h6>
    <p>The reasons are intriguing:</p>
    <ul>
        <li><strong>Absence of the Identification Number:</strong> "Black Luster Soldier" is one of the rare Yu-Gi-Oh! cards that lacks the eight-digit identification number at the bottom left, at least until its reprint in the "Legendary Collection 3: Yugi's World" series.</li>
        <li><strong>The Card's History:</strong> In the first Yu-Gi-Oh! tournament dated 1999, the winner was awarded a copy of the "Black Luster Soldier" card printed in stainless steel. It is said that only a few copies of this card exist, and one of them was put up for sale in 2013 by its original winner at the staggering price of 20 million dollars. Although the original seller had initially asked for a much higher price, it is said that they settled for an offer of "only" 2 million dollars.</li>
    </ul>
    <div style="display: flex; flex-direction: row; overflow-x: auto;">
            <div style="width: 33.33%; padding: 10px;">
            <a href="https://cdn.idntimes.com/content-images/community/2022/11/819gmmoupzl-ac-sy500-56965fbaa68adf470a17cc45ea5d328d-85149eced310f2e3793970d105f0aab1.jpg" target="_blank">
                <img src="https://cdn.idntimes.com/content-images/community/2022/11/819gmmoupzl-ac-sy500-56965fbaa68adf470a17cc45ea5d328d-85149eced310f2e3793970d105f0aab1.jpg" style="float: left; margin-right: 30px; width: 300px; height: 400px;">
            </a>
        </div>
    </div>
    <p>Ultimately, the value of cards is not determined solely by gameplay effects but also by the story surrounding the card itself and the type of print. These factors drive collectors to desire particular cards beyond players.</p>
</body>""", unsafe_allow_html=True)

##-----------------------------------BAN----------------------------------------------##
if opzione == "Ban":
    with st.container():
        st.markdown("""
        <h3 style="text-align: center;">
  <b>
    <strong>
      <font size="10" color="darkslategray">Analysis of Banned, Limited and Semi-Limited Yu-Gi-Oh! cards</font>
    </strong>
  </b>
</h3>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("""
        <p>As mentioned earlier, I proceed with the analysis using these two scatterplots to understand whether cards are limited, banned, or semi-limited due to their effect or for other reasons.</p>

<p>To further clarify the meaning of these terms:</p>
<ul>
    <li><strong>Banned:</strong> These cards cannot be used in any official duel, often due to their unfair power.</li>
    <li><strong>Semi-Limited:</strong> You are allowed to include only two copies of any Yu-Gi-Oh! card in your deck.</li>
    <li><strong>Limited:</strong> You can include in your deck only one copy of any Yu-Gi-Oh! card with a limited edition.</li>
</ul>

<p>These definitions will help you better understand the restrictions that can be applied to cards within the game.</p>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Which cards fall into the Forbidden/Limited category? (OCG)</h3>", unsafe_allow_html=True)
        # Grafico per le carte bannate in OCG
        fig1 = px.scatter(banned_cards2, x='ban_ocg', y='name', color='type', symbol="has_effect", hover_name="race")
        fig1.update_layout(xaxis_title='Ban_ocg', yaxis_title='Card Name', title_text="", legend_title_text='Type', title_x=0.5, width=900, height=850)
        fig1.update_yaxes(showticklabels=False)
        st.plotly_chart(fig1)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Which cards fall into the Forbidden/Limited category? (TCG)</h3>", unsafe_allow_html=True)
        # Grafico per le carte bannate in TCG
        fig2 = px.scatter(banned_cards, x='ban_tcg', y='name', color='type', symbol="has_effect", hover_name="race")
        fig2.update_layout(xaxis_title='Ban_Tcg', yaxis_title='Card Name', title_text="", legend_title_text='Type', title_x=0.5, width=900, height=850)
        fig2.update_yaxes(showticklabels=False)
        st.plotly_chart(fig2)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("""
        <html>
<body>
    <p>In both graphs, most cards with an effect, including those discussed earlier, fall into the "Bannable," "Semi-Limited," and "Limited" categories.</p>
    <p>However, to great surprise, in both graphs, there are 4 effectless cards that are Limited, and they are none other than the pieces of "Exodia the Forbidden One."</p>
    <div style="display: flex; flex-direction: row; overflow-x: auto;">
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/8124921.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/8124921.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/70903634.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/70903634.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/33396948.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/33396948.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/7902349.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/7902349.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/44519536.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/44519536.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
    </div>
    
<h4>Why are these effectless cards so feared?</h4>
    <p>The fear is due to the effect of Exodia the Forbidden One, which allows you to win the game if you have all 5 pieces in your hand. Moreover, new strategies exploiting various card effects have been discovered, making it easier to draw a large number of cards from the deck and simplifying the possibility of obtaining all 5 pieces of Exodia in the fewest number of turns.</p>
    <p>For more details on one of the strategies, visit the following site: 👉🏻 <a href="https://www.db.yugioh-card.com/yugiohdb/member_deck.action?cgid=49ce8d50627a96108420c3cb3695c4f2&dno=1&request_locale=it" target="_blank">Exodia the Forbidden One Strategy Site</a>.</p>
</body>
</html>""", unsafe_allow_html=True)
  
##-----------------------------------CARD TRAP MONSTER----------------------------------------------##

if opzione == "Card Trap Monster":
    with st.container():
        st.markdown("""
        <html lang="en">
        <h3 style="text-align: center;">
  <b>
    <strong>
      <font size="10" color="darkslategray">Analysis of cards trap-monster</font>
    </strong>
  </b>
</h3>""",unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("""
        <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<p>It's important to remember that monster cards are not the only ones present; in fact, there is a category of special trap cards that can be summoned as monster cards and, at the same time, function as trap cards.</p>
<p>They may seem useless, but some slightly crazy players (for example, me) have exploited the effects of these cards to create a deck. The reason? To have the chance to immediately summon Xyz monsters (which require monsters with the same level to be summoned). For more information, visit the following link <a href="https://ygoprodeck.com/deck/trap-monster-deck-70608" target="_blank"> Trap Monster Deck 🎲</a></p>
<div style="display: flex; flex-direction: row; overflow-x: auto;">
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/87772572.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/87772572.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/23626223.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/23626223.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/98414735.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/98414735.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/49514333.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/49514333.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
        <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/38761908.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/38761908.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
            <div style="width: 33.33%; padding: 10px;">
            <a href="https://images.ygoprodeck.com/images/cards/35035481.jpg" target="_blank">
                <img src="https://images.ygoprodeck.com/images/cards/35035481.jpg" style="width: 100%;" alt="Image Description">
            </a>
        </div>
    </div>
    </body>
    </html>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)     
        st.markdown("<h3 style='text-align: center;'>Trap Card Monsters</h3>", unsafe_allow_html=True)
        st.dataframe(filtered_columns_sorted) 

##-----------------------------------RARITY----------------------------------------------##
if opzione == "Rarity":
    with st.container():
        st.markdown("""
        <h3 style="text-align: center;">
  <b>
    <strong>
      <font size="10" color="darkslategray">Analysis cards rarity</font>
    </strong>
  </b>
</h3>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Types of Card Rarities</h3>", unsafe_allow_html=True)
        figy = px.histogram(merged_data, y='set_rarity', color='set_rarity')
        figy.update_yaxes(categoryorder='total ascending') 
        figy.update_layout(title='', xaxis_title='Number of Cards', yaxis_title='Rarity Type', title_x=0.5, width=900, height=850)
        st.plotly_chart(figy)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("<h3 style='text-align: center;'>Top  Card Rarities</h3>", unsafe_allow_html=True)
        filtered_cards = merged_data.loc[(merged_data['name'] == 'Minerva, the Exalted Lightsworn') | (merged_data['name'] == 'Blue-Eyes White Dragon') | (merged_data['name'] == 'Tyler the Great Warrior') | (merged_data['name'] == 'Dark Magician') | (merged_data['name'] == 'Crush Card Virus') | (merged_data['name'] == 'Cyber-Stein')]
        filtered_cards[['name', 'type', 'desc','attribute','views','upvotes','downvotes','set_rarity','id']]
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<p>It can be noted that common cards are among the most widespread, followed by super rare, ultra rare, rare, and secret rare cards. At the end of the graph, there are 5 categories, each composed of a single card: 10000 Secret Rare, Super, Duel Terminal Normal Rare Parallel Rare, C, and Ultra Secret Rare, indicating that there are only 5 cards in these categories.</p>
<p>It is well known that the value of a card increases the rarer it is, but this value is not only due to its rarity but also to the card's effect, printing method, the number of copies in existence, and the story behind the card. (An example of this can be found in the card 'Black Luster Soldier').</p>
<p>However, there is another extremely rare card in addition to the one mentioned earlier, namely <strong>"Tyler the Great Warrior"</strong>. There is only one copy in circulation, and it was created by Tyler Gressle, who drew the card in 2005 as part of a Make-a-Wish request when he was 14 years old and battling a rare form of liver cancer. 18 years later, he decided to sell the card. The final auction offer raised a whopping $311,211.</p>
<p>Here is a list of other rare and expensive cards.</p>
<div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/68811206.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/68811206.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/89631139.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/89631139.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/46986414.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/46986414.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/57728570.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/57728570.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/30100551.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/30100551.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/69015963.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/69015963.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
</div>
</body>
</html>""", unsafe_allow_html=True)


##-----------------------------------STAPLE----------------------------------------------##
if opzione == "Staple":
    with st.container():
        st.markdown("""
        <h3 style="text-align: center;">
  <b>
    <strong>
      <font size="10" color="darkslategray">Analysis of staple card</font>
    </strong>
  </b>
</h3>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)   
        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<p>'Staple' cards represent a set of cards that play a crucial role during a duel, as they can significantly influence the opponent's turn or provide greater consistency to one's deck.</p>
""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True)      
        st.markdown("<h3 style='text-align: center;'>Distribution of Staple Cards by Type in %</h3>", unsafe_allow_html=True)
        st.plotly_chart(fig)
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center;'>Table of Staple Cards</h3>", unsafe_allow_html=True)
        st.dataframe(filtered_columns_sorted)
        st.markdown("---", unsafe_allow_html=True)   
        st.markdown("""
<p>Overall, there are 64 of these special cards, but it's interesting to note that 20 of them fall into the categories of 'Limited,' 'Semi-Limited,' and 'Forbidden.'</p>
<div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/12580477.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/12580477.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/83764719.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/83764719.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/24224830.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/24224830.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/37818794.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/37818794.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/35261759.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/35261759.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/70369116.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/70369116.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
</div>
    </body>
    </html>
    """, unsafe_allow_html=True)        

##-----------------------------------TREATED_AS----------------------------------------------##      

if opzione == "Treated_as":
    with st.container():
        st.markdown("""
        <h3 style="text-align: center;">
  <b>
    <strong>
      <font size="10" color="darkslategray">Analysis of Treated_as card</font>
    </strong>
  </b>
</h3>""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("""
        <html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<p>Cards falling under the <strong>'treated_as'</strong> category are those whose description can be considered with a <strong>different name</strong> or with the <strong>same name but a different image.</strong></p>
""", unsafe_allow_html=True)
        st.markdown("---", unsafe_allow_html=True) 
        st.markdown("<h3 style='text-align: center;'>Distribution of Treated_As Cards by Type in %</h3>", unsafe_allow_html=True)  
        st.plotly_chart(fig)
        st.markdown("---", unsafe_allow_html=True)   
        # Visualizzazione della tabella
        st.markdown("<h3 style='text-align: center;'>Table of Treated_as Cards</h3>", unsafe_allow_html=True)
        st.dataframe(filtered_columns)
        st.markdown("---", unsafe_allow_html=True)
        st.markdown("""
<p>Out of the 106 cards in this category, only 4 are classified as 'Limited,' 'Semi-Limited,' or 'Forbidden,' and some of these also fall into the 'staple' category.</p>
<div style="display: flex; flex-direction: row; overflow-x: auto;">
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/27927359.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/27927359.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/295517.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/295517.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/80316585.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/80316585.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/68679595.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/68679595.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/17732278.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/17732278.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
    <div style="width: 33.33%; padding: 10px;">
        <a href="https://images.ygoprodeck.com/images/cards/13857930.jpg" target="_blank">
            <img src="https://images.ygoprodeck.com/images/cards/13857930.jpg" style="width: 100%;" alt="Image description">
        </a>
    </div>
</div>
    </body>
    </html>""", unsafe_allow_html=True)



        
