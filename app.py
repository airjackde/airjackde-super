import streamlit as st
from groq import Groq
import os, base64, io, random, json
from PIL import Image
import fitz
from gtts import gTTS

st.set_page_config(page_title="AIRJACKDE SUPER APP", page_icon="🚀", layout="wide")

# --- CUSTOM STYLE ---
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

# --- NAME & STYLE MEMORY ---
if 'user_name' not in st.session_state: st.session_state.user_name = "Jackson"
if 'theme' not in st.session_state: st.session_state.theme = "Dark Neon"
if 'voice_on' not in st.session_state: st.session_state.voice_on = True

with st.sidebar:
    st.title("🚀 AIRJACKDE SUPER")
    
    # NAME & CUSTOM STYLE
    st.subheader("👤 Your Profile")
    st.session_state.user_name = st.text_input("Your Name:", st.session_state.user_name)
    st.session_state.theme = st.selectbox("Custom Style:", ["Dark Neon","Kenya Green","Ocean Blue","Sunset Orange","Hacker Black"])
    st.session_state.voice_on = st.toggle("🔊 Voice Reply", value=st.session_state.voice_on)
    
    # APPLY THEME
    themes = {
        "Dark Neon": "background: linear-gradient(135deg,#0f0f0f,#1a1a2e); color:#00ffcc",
        "Kenya Green": "background: linear-gradient(135deg,#006600,#000000); color:#ffffff",
        "Ocean Blue": "background: linear-gradient(135deg,#001f3f,#00a8ff); color:#ffffff",
        "Sunset Orange": "background: linear-gradient(135deg,#ff6a00,#ee0979); color:#ffffff",
        "Hacker Black": "background:#000000; color:#00ff00; font-family: monospace"
    }
    st.markdown(f"<style>.stApp{{ {themes[st.session_state.theme]} }}</style>", unsafe_allow_html=True)

    st.divider()
    menu = st.radio("MENU", [
        "💬 AI Chat",
        "🎓 Exam Solver",
        "🌐 Translator",
        "▶️ Video Hub",
        "🎬 Movie Hub",
        "📢 Channels",
        "🎮 Game Hub",
        "💾 My Files"
    ])
    st.divider()
    # MEMORY CONTROLS
    st.subheader("🧠 Memory")
    if st.button("🗑️ Clear Chat Memory"): st.session_state.msgs = [{"role":"assistant","content":f"Hey {st.session_state.user_name}! Memory cleared 👋"}]; st.rerun()
    st.caption(f"Chats: {len(st.session_state.get('msgs',[]))} messages saved")
    st.success(f"7 Apps in 1\nBy {st.session_state.user_name} 🇰🇪")

LANGS = ["English","French","Haitian Creole","Swahili","Spanish","Kiswahili Sheng"]

# --- HELPER FOR VOICE ---
def speak(text):
    if not st.session_state.voice_on: return None
    try:
        tts = gTTS(text=text[:500], lang='en')
        buf = io.BytesIO(); tts.write_to_fp(buf); buf.seek(0)
        return buf
    except: return None

# --- GAME HUB ---
if menu == "🎮 Game Hub":
    st.header(f"🎮 Game Hub - Welcome {st.session_state.user_name}!")
    game = st.selectbox("Choose Game:", ["❌⭕ Tic Tac Toe","✊ Rock Paper Scissors","🧠 Math Quiz","🔤 Word Scramble","🎯 Guess Number","💡 AI Game Creator"])
    if game.startswith("❌"):
        st.subheader("Tic Tac Toe")
        if 'board' not in st.session_state: st.session_state.board = [""]*9; st.session_state.turn="X"
        cols = st.columns(3)
        for i in range(9):
            with cols[i%3]:
                if st.button(st.session_state.board[i] or " ", key=f"b{i}", use_container_width=True):
                    if st.session_state.board[i]=="":
                        st.session_state.board[i]=st.session_state.turn
                        st.session_state.turn="O" if st.session_state.turn=="X" else "X"
                        st.rerun()
        b=st.session_state.board; wins=[(0,1,2),(3,4,5),(6,7,8),(0,3,6),(1,4,7),(2,5,8),(0,4,8),(2,4,6)]
        for a,b1,c in wins:
            if b[a]==b[b1]==b[c]!="": st.balloons(); st.success(f"Player {b[a]} Wins!"); break
        if st.button("Reset"): st.session_state.board=[""]*9; st.rerun()
    elif game.startswith("✊"):
        st.subheader("Rock Paper Scissors")
        choice=st.radio("Your choice:",["Rock","Paper","Scissors"],horizontal=True)
        if st.button("Play!"):
            comp=random.choice(["Rock","Paper","Scissors"]); st.write(f"Computer: {comp}")
            if choice==comp: st.info("Draw!")
            elif (choice=="Rock" and comp=="Scissors") or (choice=="Paper" and comp=="Rock") or (choice=="Scissors" and comp=="Paper"): st.success("You Win!"); st.balloons()
            else: st.error("You Lose!")
    elif game.startswith("🧠"):
        st.subheader("Math Quiz")
        if 'score' not in st.session_state: st.session_state.score=0; st.session_state.q=0
        if st.session_state.q<5:
            a=random.randint(1,20); b=random.randint(1,20); op=random.choice(["+","-","*"]); ans=eval(f"{a}{op}{b}")
            st.write(f"Q {st.session_state.q+1}/5: {a} {op} {b} ?")
            user_ans=st.number_input("Answer:",step=1)
            if st.button("Submit"):
                if user_ans==ans: st.success("Correct!"); st.session_state.score+=1
                else: st.error(f"Wrong! {ans}"); st.session_state.q+=1; st.rerun()
        else:
            st.success(f"Game Over! Score: {st.session_state.score}/5")
            if st.button("Play Again"): st.session_state.score=0; st.session_state.q=0; st.rerun()
    elif game.startswith("🔤"):
        st.subheader("Word Scramble")
        words=["PYTHON","ELDORET","JACKSON","KENYA","GROQ","AIRJACKDE"]
        if 'word' not in st.session_state: w=random.choice(words); st.session_state.word=w; l=list(w); random.shuffle(l); st.session_state.scrambled="".join(l)
        st.write(f"Scrambled: **{st.session_state.scrambled}**")
        guess=st.text_input("Guess:").upper()
        if st.button("Check"):
            if guess==st.session_state.word: st.success("Correct!"); st.balloons(); del st.session_state['word']
            else: st.error("Try again!")
    elif game.startswith("🎯"):
        st.subheader("Guess 1-100")
        if 'num' not in st.session_state: st.session_state.num=random.randint(1,100); st.session_state.tries=0
        g=st.number_input("Guess:",1,100)
        if st.button("Guess"):
            st.session_state.tries+=1
            if g==st.session_state.num: st.success(f"Won in {st.session_state.tries}!"); st.balloons(); del st.session_state['num']
            elif g<st.session_state.num: st.info("Too low!")
            else: st.info("Too high!")
    else:
        st.subheader("AI Game Creator")
        idea=st.text_input("What game to create?")
        if st.button("Create with AI") and client:
            comp=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"system","content":"Create simple Streamlit game code."},{"role":"user","content":idea}],max_tokens=2000)
            st.code(comp.choices[0].message.content)

# --- AI CHAT WITH VOICE + MEMORY ---
elif menu.startswith("💬"):
    st.header(f"💬 AI Chat - Hey {st.session_state.user_name}!")
    
    # MEMORY
    if "msgs" not in st.session_state: st.session_state.msgs=[{"role":"assistant","content":f"Hey {st.session_state.user_name}! I'm AIRJACKDE AI 👋 How can I help?"}]
    
    for m in st.session_state.msgs:
        with st.chat_message(m["role"], avatar="😊" if m["role"]=="user" else "🤖"): st.write(m["content"])
    
    # VOICE INPUT
    st.write("🎤 Voice Input:")
    audio = st.audio_input("Tap to speak")
    voice_text = None
    if audio and client:
        with st.spinner("Transcribing your voice..."):
            try:
                # Groq Whisper
                transcription = client.audio.transcriptions.create(file=("audio.wav", audio.read()), model="whisper-large-v3-turbo", response_format="text")
                voice_text = transcription
                st.info(f"You said: {voice_text}")
            except Exception as e: st.error(f"Voice error: {e}")

    prompt = st.chat_input(f"Message {st.session_state.user_name}...")
    final_prompt = voice_text or prompt
    
    if final_prompt:
        st.session_state.msgs.append({"role":"user","content":final_prompt})
        with st.chat_message("user", avatar="😊"): st.write(final_prompt)
        if client:
            with st.chat_message("assistant", avatar="🤖"):
                comp=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"system","content":f"You are AIRJACKDE AI, friendly assistant for {st.session_state.user_name} from Eldoret Kenya. Remember conversation history. Speak same language as user. Be helpful."},*st.session_state.msgs],max_tokens=1000)
                ans=comp.choices[0].message.content; st.write(ans)
                # VOICE OUTPUT
                audio_buf = speak(ans)
                if audio_buf: st.audio(audio_buf, format="audio/mp3")
                st.session_state.msgs.append({"role":"assistant","content":ans})
        else:
            st.error("Add GROQ_API_KEY in Secrets")

elif menu.startswith("🎓"):
    st.header("🎓 Exam Solver")
    up=st.file_uploader("Upload photo/PDF",type=["png","jpg","jpeg","pdf"])
    b64=None; pdf_text=""
    if up:
        if up.type=="application/pdf":
            doc=fitz.open(stream=up.read(),filetype="pdf"); pdf_text="".join([doc[i].get_text() for i in range(min(len(doc),3))]); st.text_area("PDF",pdf_text[:3000])
        else:
            img=Image.open(up); st.image(img); buf=io.BytesIO(); img.convert("RGB").save(buf,format="JPEG"); b64=base64.b64encode(buf.getvalue()).decode()
    q=st.text_input("Question:")
    if st.button("Solve") and client:
        msgs=[{"role":"system","content":f"Expert tutor for {st.session_state.user_name}, step-by-step"}]
        if b64:
            msgs.append({"role":"user","content":[{"type":"text","text":q},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]})
            model="meta-llama/llama-4-scout-17b-16e-instruct"
        else:
            msgs.append({"role":"user","content":f"{pdf_text}\n{q}"}); model="llama-3.1-8b-instant"
        comp=client.chat.completions.create(model=model,messages=msgs,max_tokens=2500); st.write(comp.choices[0].message.content)

elif menu.startswith("🌐"):
    st.header("🌐 Translator")
    c1,c2=st.columns(2)
    with c1: src=st.selectbox("From",LANGS,index=0)
    with c2: tgt=st.selectbox("To",LANGS,index=1)
    txt=st.text_area("Text")
    if st.button("Translate") and client:
        comp=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"system","content":f"Translate from {src} to {tgt}"},{"role":"user","content":txt}]); st.success(comp.choices[0].message.content)

elif menu.startswith("▶️"):
    st.header("▶️ Video Hub")
    s=st.text_input("Search videos")
    if s: st.markdown(f"[Search {s} on YouTube](https://www.youtube.com/results?search_query={s})")
    st.video("https://www.youtube.com/watch?v=rfscVS0vtbw")

elif menu.startswith("🎬"):
    st.header("🎬 Movie Hub")
    g=st.selectbox("Genre",["Action","Comedy","Education"])
    if st.button("Recommend") and client:
        comp=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"system","content":"Recommend 5 movies"},{"role":"user","content":g}]); st.write(comp.choices[0].message.content)

elif menu.startswith("📢"):
    st.header("📢 Channels")
    st.write(f"Welcome {st.session_state.user_name} - Channels: Past Papers, Coding, UoE Eldoret")
    st.chat_message("user").write("Anyone has past paper?")
    st.chat_message("assistant").write("Yes, check Exam Solver!")

else:
    st.header("💾 My Files - Memory")
    st.json(st.session_state.msgs[:5])
    st.info("Your chats are saved in memory as long as tab is open. Clear with sidebar button.")

st.caption(f"AIRJACKDE SUPER APP | 7 Apps + Voice + Memory | By {st.session_state.user_name} 🇰🇪 | Style: {st.session_state.theme}")
