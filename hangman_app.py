import streamlit as st
import random

st.set_page_config(
    page_title="Hangman Game 🎯",
    page_icon="🎯",
    layout="centered"
)

# ✅ Game Data with Clues
categories = {
    "Fruits": {
        "apple": "A red or green round fruit",
        "banana": "Long and yellow fruit",
        "mango": "King of fruits, juicy and yellow",
        "grape": "Small round purple/green fruits",
        "orange": "Round citrus fruit"
    },
    "Vehicles": {
        "car": "Has 4 wheels, runs on roads",
        "train": "Runs on tracks",
        "airplane": "Flies in the sky",
        "bicycle": "2 wheels, human-powered",
        "truck": "Used to carry heavy loads"
    },
    "Programming": {
        "python": "A popular programming language",
        "function": "Block of reusable code",
        "developer": "Person who writes code",
        "variable": "Stores values",
        "coding": "The process of writing programs"
    }
}

# ✅ Session State Initialization
if 'category_selected' not in st.session_state:
    st.session_state.category_selected = False
if 'word_pool' not in st.session_state:
    st.session_state.word_pool = {}
if 'word' not in st.session_state:
    st.session_state.word = ""
    st.session_state.clue = ""
    st.session_state.word_letters = set()
    st.session_state.guessed_letters = set()
    st.session_state.attempts = 6
    st.session_state.game_over = False

# ✅ CSS Styling
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
        }
        .stButton>button {
            color: white;
            background-color: #4CAF50;
            border-radius: 10px;
            height: 3em;
            width: 100%;
        }
        .stTextInput>div>div>input {
            border-radius: 10px;
            height: 3em;
        }
    </style>
""", unsafe_allow_html=True)

st.title("🎯 Hangman - Word Guessing Game with Clues")
st.subheader("Guess the word based on the clue! 🚀")

# ✅ Category Selection
if not st.session_state.category_selected:
    st.subheader("🎯 Select a Category to Start:")
    category = st.selectbox("🗂️ Choose Category", list(categories.keys()))

    if st.button("🚀 Start Game"):
        st.session_state.category = category
        st.session_state.word_pool = categories[category].copy()
        st.session_state.category_selected = True
        st.rerun()

# ✅ Game Logic
if st.session_state.category_selected:
    if st.session_state.word == "":
        if st.session_state.word_pool:
            word, clue = random.choice(list(st.session_state.word_pool.items()))
            st.session_state.word = word
            st.session_state.clue = clue
            st.session_state.word_letters = set(word)
            st.session_state.guessed_letters = set()
            st.session_state.attempts = 6
            st.session_state.game_over = False
            del st.session_state.word_pool[word]
        else:
            st.success("🎉 You completed all words in this category!")
            if st.button("🔄 Choose Another Category"):
                st.session_state.category_selected = False
                st.session_state.word = ""
                st.session_state.clue = ""
                st.rerun()

    if st.session_state.word != "":
        word = st.session_state.word

        st.subheader(f"📌 Category: {st.session_state.category}")
        st.subheader(f"💡 Clue: {st.session_state.clue}")
        st.subheader(f"🅰️ The word has {len(word)} letters.")

        word_display = [letter if letter in st.session_state.guessed_letters else '_' for letter in word]
        st.markdown(f"### 🔠 Word: {' '.join(word_display)}")

        # ✅ Input guess with FORM + KEY (🔥 input auto-clears 🔥)
        with st.form(key=f"form_{st.session_state.attempts}_{len(st.session_state.guessed_letters)}"):
            guess = st.text_input("🎯 Enter a letter:", max_chars=1).lower()
            submit = st.form_submit_button("Submit")

        if submit and guess:
            if len(guess) != 1 or not guess.isalpha():
                st.warning("⚠️ Please enter a single alphabet letter.")
            elif guess in st.session_state.guessed_letters:
                st.warning("⚠️ You already guessed that letter!")
            elif guess in st.session_state.word_letters:
                st.session_state.guessed_letters.add(guess)
                st.session_state.word_letters.remove(guess)
                st.success("✅ Correct guess!")
            else:
                st.session_state.guessed_letters.add(guess)
                st.session_state.attempts -= 1
                st.error("❌ Wrong guess!")

        # ✅ Status Info
        st.info(f"🅿️ Guessed letters: {' '.join(st.session_state.guessed_letters)}")
        st.info(f"💖 Attempts left: {st.session_state.attempts}")

        # ✅ Check win/lose
        if len(st.session_state.word_letters) == 0:
            st.success(f"🎉 You won! The word was **{word.upper()}**")
            st.session_state.game_over = True
        elif st.session_state.attempts == 0:
            st.error(f"❌ Game Over! The word was **{word.upper()}**")
            st.session_state.game_over = True

        # ✅ Play Next Word
        if st.session_state.game_over:
            if st.session_state.word_pool:
                if st.button("▶️ Next Word"):
                    st.session_state.word = ""
                    st.session_state.clue = ""
                    st.rerun()
            else:
                st.success("🎉 You completed all words in this category!")
                if st.button("🔄 Choose Another Category"):
                    st.session_state.category_selected = False
                    st.session_state.word = ""
                    st.session_state.clue = ""
                    st.rerun()
