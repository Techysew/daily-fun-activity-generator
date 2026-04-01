import streamlit as st
import random
import os

# -------------------------
# Page setup
# -------------------------
st.set_page_config(
    page_title="Mood-Lifting Fun Activity Game",
    page_icon="",
    layout="centered"
)

st.title("🌟 Mood-Lifting Fun Activity Game 🎮")
st.write("Feeling bored ? Let's find something fun! 😄")

IMAGE_FOLDER = "F:/python fun activity/images"

# -------------------------
# Helper Functions
# -------------------------
def show_card(item):
    if os.path.exists(item["img"]):
        st.image(item["img"], width=120)
    st.write(f"✨ {item['text']}")

def filter_by_location(pool, vibe):
    if vibe == "Spend Time Alone 🧘‍♀️":
        return [a for a in pool if a["location"] in ["home", "any"]]
    else:
        return [a for a in pool if a["location"] in ["out", "any"]]

# -------------------------
# Smart Suggestion Generator (FREE AI-Like)
# -------------------------
def generate_smart_suggestions(vibe):

    alone_templates = [
        "Create a cozy reading corner and read something new 📖",
        "Try a 10-minute guided meditation 🧘",
        "Rearrange your room for a fresh vibe ✨",
        "Bake something simple and enjoy the smell 🍪",
        "Start a mini art challenge 🎨",
        "Watch a documentary on something interesting 🎬"
    ]

    out_templates = [
        "Explore a place in your town you've never visited 🌍",
        "Take a sunset walk and clear your mind 🌇",
        "Try a new cafe and rate the experience ☕",
        "Go people-watching at a park 🌳",
        "Take 5 aesthetic photos outside 📸",
        "Visit a bookstore and browse freely 📚"
    ]

    if "Alone" in vibe:
        suggestions = random.sample(alone_templates, 3)
    else:
        suggestions = random.sample(out_templates, 3)

    return suggestions

# -------------------------
# Activity Data
# -------------------------
stay_home_activities = [
    {"text": "Play a fun game 🎮", "img": f"{IMAGE_FOLDER}/game.png", "location": "home"},
    {"text": "Read a book 📖", "img": f"{IMAGE_FOLDER}/book.png", "location": "home"},
    {"text": "Draw or paint 🎨", "img": f"{IMAGE_FOLDER}/draw.png", "location": "home"},
    {"text": "Listen to music 🎧", "img": f"{IMAGE_FOLDER}/music.png", "location": "home"},
]

go_out_activities = [
    {"text": "Hang out with friends 👯", "img": f"{IMAGE_FOLDER}/friends.png", "location": "out"},
    {"text": "Go hiking 🏔️", "img": f"{IMAGE_FOLDER}/hiking.png", "location": "out"},
    {"text": "Visit a cafe ☕", "img": f"{IMAGE_FOLDER}/cafe.png", "location": "out"},
    {"text": "Go cycling 🚴", "img": f"{IMAGE_FOLDER}/cycling.png", "location": "out"},
]

foods = [
    {"text": "Enjoy Pizza 🍕", "img": f"{IMAGE_FOLDER}/pizza.png", "location": "home"},
    {"text": "Cook Pasta 🍝", "img": f"{IMAGE_FOLDER}/pasta.png", "location": "home"},
]

movies = [
    {"text": "Watch Avatar 🛸", "img": f"{IMAGE_FOLDER}/avatar.png", "location": "any"},
    {"text": "Watch Spider-Man 🕷️", "img": f"{IMAGE_FOLDER}/spider-man.png", "location": "any"},
]

self_care = [
    {"text": "Take a warm bath 🛁", "img": f"{IMAGE_FOLDER}/bath.png", "location": "home"},
    {"text": "Do stretching 🤸", "img": f"{IMAGE_FOLDER}/stretch.png", "location": "home"},
]

social = [
    {"text": "Call a friend 📞", "img": f"{IMAGE_FOLDER}/call.png", "location": "any"},
    {"text": "Attend a local event 🎟️", "img": f"{IMAGE_FOLDER}/event.png", "location": "out"},
]

# -------------------------
# Session State
# -------------------------
if "deck" not in st.session_state:
    st.session_state.deck = []

if "revealed" not in st.session_state:
    st.session_state.revealed = []

if "mode" not in st.session_state:
    st.session_state.mode = None

# -------------------------
# Choose Vibe
# -------------------------
st.subheader("Step 1: Choose Your Vibe")
vibe = st.radio("How do you feel today?", ("Spend Time Alone 🧘‍♀️", "Go Out 🌳"))

reveal_btn = st.button("Generate My Fun Deck 🎯")
surprise_btn = st.button("Surprise Me ")

# -------------------------
# Generate Deck Mode
# -------------------------
if reveal_btn:
    st.session_state.deck = []
    st.session_state.revealed = []
    st.session_state.mode = "deck"

    categories = [foods, movies, self_care]

    if vibe == "Spend Time Alone 🧘‍♀️":
        categories.append(stay_home_activities)
    else:
        categories.append(go_out_activities + social)

    for cat in categories:
        filtered = filter_by_location(cat, vibe)
        if filtered:
            if cat == go_out_activities + social:
                # pick 2 from go out
                picks = random.sample(filtered, min(2, len(filtered)))
                st.session_state.deck.extend(picks)
            else:
                st.session_state.deck.append(random.choice(filtered))

    st.success("🎴 Deck generated! Flip and shuffle for fun!")

# -------------------------
# Surprise Mode
# -------------------------
if surprise_btn:
    st.session_state.deck = []
    st.session_state.revealed = []
    st.session_state.mode = "surprise"

    categories = [foods, movies, self_care]

    if vibe == "Spend Time Alone 🧘‍♀️":
        categories.append(stay_home_activities)
    else:
        categories.append(go_out_activities + social)

    for cat in categories:
        filtered = filter_by_location(cat, vibe)
        if filtered:
            st.session_state.deck.append(random.choice(filtered))

    st.success("🎉 Surprise! Here's your mood boost!")

# -------------------------
# Display Section
# -------------------------
if st.session_state.mode == "deck":

    for idx, card in enumerate(st.session_state.deck):

        col1, col2 = st.columns([2, 1])

        with col1:
            if idx not in st.session_state.revealed:
                if st.button(f"🎴 Reveal Activity {idx+1}", key=f"reveal_{idx}"):
                    st.session_state.revealed.append(idx)
            else:
                show_card(card)

        with col2:
            if idx in st.session_state.revealed:
                if st.button("🔄 Shuffle", key=f"shuffle_{idx}"):

                    if card in foods:
                        pool = foods
                    elif card in movies:
                        pool = movies
                    elif card in self_care:
                        pool = self_care
                    elif card in stay_home_activities:
                        pool = stay_home_activities
                    elif card in go_out_activities:
                        pool = go_out_activities
                    else:
                        pool = social

                    filtered = filter_by_location(pool, vibe)
                    available = [a for a in filtered if a not in st.session_state.deck]

                    if available:
                        st.session_state.deck[idx] = random.choice(available)
                        st.session_state.revealed.remove(idx)

    # Smart Suggestions Button
    st.markdown("### 💡 Want Extra Smart Ideas?")
    if st.button("Generate Smart Suggestions"):
        suggestions = generate_smart_suggestions(vibe)
        for s in suggestions:
            st.info(f"✨ {s}")

elif st.session_state.mode == "surprise":

    st.subheader("✨ Today's Surprise Plan")

    for card in st.session_state.deck:
        show_card(card)

    st.markdown("### 💡 Want Extra Smart Ideas?")
    if st.button("Generate Smart Suggestions"):
        suggestions = generate_smart_suggestions(vibe)
        for s in suggestions:
            st.info(f"✨ {s}")

st.markdown("---")
st.write("💡 Flip, shuffle, or get smart suggestions to boost your mood!")