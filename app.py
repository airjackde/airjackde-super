import streamlit as st
from gtts import gTTS
import tempfile

st.set_page_config(page_title="AIRJACKDE SUPER APP", page_icon="🚀", layout="wide")

if "messages" not in st.session_state:
    st.session_state.messages = []
if "page" not in st.session_state:
    st.session_state.page = "HOME"

with st.sidebar:
    st.title("👤 Profile")
    user_name = st.text_input("Your Name:", "Jackson")
    style = st.selectbox("Style:", ["Dark Neon", "Kenya Green 🇰🇪", "Ocean Blue", "Sunset Red"])
    if style == "Kenya Green 🇰🇪":
        primary = "#00ff00"
    elif style == "Ocean Blue":
        primary = "#00bfff"
    elif style == "Sunset Red":
        primary = "#ff4500"
    else:
        primary = "#00ffcc"
    st.markdown(f"<style>.stApp{{border-top:5px solid {primary}}}</style>", unsafe_allow_html=True)
    voice_on = st.toggle("🔊 Voice Reply", True)
    if st.button("🧹 Clear Memory"):
        st.session_state.messages = []
        st.rerun()

def speak(text):
    try:
        tts = gTTS(text=text, lang='en')
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
            tts.save(fp.name)
            st.audio(fp.name, autoplay=True)
    except:
        pass

if st.session_state.page == "HOME":
    st.markdown(f"<h1 style='text-align:center;color:{primary}'>🚀 AIRJACKDE SUPER APP</h1>", unsafe_allow_html=True)
    st.markdown(f"<h3 style='text-align:center'>Welcome {user_name}! Choose an App 👇</h3>", unsafe_allow_html=True)
    st.write("")
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("💬\nAI CHAT", use_container_width=True, type="primary"):
            st.session_state.page="CHAT"; st.rerun()
    with c2:
        if st.button("🎓\nEXAM SOLVER", use_container_width=True):
            st.session_state.page="EXAM"; st.rerun()
    with c3:
        if st.button("🌐\nTRANSLATOR", use_container_width=True):
            st.session_state.page="TRANS"; st.rerun()
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("▶️\nVIDEO HUB", use_container_width=True):
            st.session_state.page="VIDEO"; st.rerun()
    with c2:
        if st.button("🎬\nMOVIE HUB", use_container_width=True):
            st.session_state.page="MOVIE"; st.rerun()
    with c3:
        if st.button("📢\nCHANNELS", use_container_width=True):
            st.session_state.page="CHANNELS"; st.rerun()
    c1,c2,c3 = st.columns(3)
    with c1:
        if st.button("🎮\nGAME HUB", use_container_width=True):
            st.session_state.page="GAME"; st.rerun()
    with c2:
        if st.button("💾\nMY FILES", use_container_width=True):
            st.session_state.page="FILES"; st.rerun()
    with c3:
        if st.button("🎤\nVOICE CHAT", use_container_width=True):
            st.session_state.page="CHAT"; st.rerun()
    st.divider()
    st.info(f"👋 Hey {user_name}! You have 8 apps in 1 - all visible here! No more >> menu!")
else:
    if st.button("⬅️ BACK TO HOME"):
        st.session_state.page="HOME"; st.rerun()
    if st.session_state.page == "CHAT":
        st.header(f"💬 Chat - Hey {user_name}!")
        for m in st.session_state.messages:
            with st.chat_message(m["role"]):
                st.write(m["content"])
        st.audio_input("🎤 Tap to speak")
        p = st.chat_input(f"Message {user_name}...")
        if p:
            st.session_state.messages.append({"role":"user","content":p})
            with st.chat_message("user"):
                st.write(p)
            reply = f"Hey {user_name}! You said: {p}. I'm AIRJACKDE AI! 🚀"
            with st.chat_message("assistant"):
                st.write(reply)
                if voice_on:
                    speak(reply)
            st.session_state.messages.append({"role":"assistant","content":reply})
    elif st.session_state.page == "EXAM":
        st.header("🎓 Exam Solver")
        st.file_uploader("Upload exam photo")
        st.success("Add Groq API to get answers!")
    elif st.session_state.page == "GAME":
        st.header("🎮 Tic Tac Toe")
        if "board" not in st.session_state:
            st.session_state.board=[""]*9
        cols=st.columns(3)
        for i in range(9):
            with cols[i%3]:
                if st.button(st.session_state.board[i] or " ", key=f"g{i}", use_container_width=True):
                    st.session_state.board[i]="X"; st.rerun()
        if st.button("Reset"):
            st.session_state.board=[""]*9; st.rerun()
    else:
        st.header(f"{st.session_state.page} - Coming soon! Working!")
        st.info("This app will be fully active!")
