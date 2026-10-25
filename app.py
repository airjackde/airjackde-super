import streamlit as st
from groq import Groq
import os, base64, io, random
from PIL import Image
import fitz

st.set_page_config(page_title="AIRJACKDE SUPER APP", page_icon="🚀", layout="wide")
api_key = st.secrets.get("GROQ_API_KEY") or os.environ.get("GROQ_API_KEY")
client = Groq(api_key=api_key) if api_key else None

with st.sidebar:
    st.title("🚀 AIRJACKDE SUPER")
    st.caption("By Jackson | Eldoret 🇰🇪")
    menu = st.radio("MENU", ["💬 AI Chat","🎓 Exam Solver","🌐 Translator","▶️ Video Hub","🎬 Movie Hub","📢 Channels","🎮 Game Hub",])
    st.divider()
    st.success("7 Apps in 1")

LANGS = ["English","French","Haitian Creole","Swahili","Spanish","German","Arabic","Chinese"]

if menu == "💬 AI Chat":
    st.header("💬 AI Chat")
    if "msgs" not in st.session_state: st.session_state.msgs=[{"role":"assistant","content":"Hey! I'm AIRJACKDE AI 👋"}]
    for m in st.session_state.msgs:
        with st.chat_message(m["role"]): st.write(m["content"])
    if p:=st.chat_input("Message..."):
        st.session_state.msgs.append({"role":"user","content":p})
        with st.chat_message("user"): st.write(p)
        with st.chat_message("assistant"):
            comp=client.chat.completions.create(model="openai/gpt-oss-20b",messages=[{"role":"system","content":"Friendly helper"},{"role":"user","content":p}],max_tokens=1000)
            ans=comp.choices[0].message.content; st.write(ans); st.session_state.msgs.append({"role":"assistant","content":ans})

elif menu == "🎓 Exam Solver":
    st.header("🎓 Exam Solver")
    up=st.file_uploader("Upload question",type=["png","jpg","jpeg","pdf"])
    b64=None; pdf_text=""
    if up:
        if up.type=="application/pdf":
            doc=fitz.open(stream=up.read(),filetype="pdf"); pdf_text="".join([doc[i].get_text() for i in range(min(len(doc),3))]); st.text_area("PDF Text",pdf_text[:3000],height=150)
        else:
            img=Image.open(up); st.image(img,use_container_width=True); buf=io.BytesIO(); img.convert("RGB").save(buf,format="JPEG"); b64=base64.b64encode(buf.getvalue()).decode()
    q=st.text_input("What to solve?")
    if st.button("Solve Now",type="primary"):
        msgs=[{"role":"system","content":"Expert tutor"}]
        if b64: msgs.append({"role":"user","content":[{"type":"text","text":q},{"type":"image_url","image_url":{"url":f"data:image/jpeg;base64,{b64}"}}]}); model="meta-llama/llama-4-scout-17b-16e-instruct"
        else: msgs.append({"role":"user","content":f"{pdf_text}\n{q}"}); model="openai/gpt-oss-20b"
        comp=client.chat.completions.create(model=model,messages=msgs,max_tokens=2000); st.write(comp.choices[0].message.content)

elif menu == "🌐 Translator":
    st.header("🌐 Translator")
    c1,c2=st.columns(2)
    with c1: src=st.selectbox("From",LANGS,index=0)
    with c2: tgt=st.selectbox("To",LANGS,index=1)
    txt=st.text_area("Text",height=120)
    if st.button("Translate",type="primary"):
        comp=client.chat.completions.create(model="openai/gpt-oss-20b",messages=[{"role":"system","content":f"Translate from {src} to {tgt}. Only translation."},{"role":"user","content":txt}],max_tokens=800)
        st.success(comp.choices[0].message.content)

elif menu == "▶️ Video Hub":
    st.header("▶️ Video Hub - Like YouTube")
    s=st.text_input("Search videos")
    if s: st.markdown(f"[Search '{s}' on YouTube](https://www.youtube.com/results?search_query={s.replace(' ','+')})")
    st.video("https://www.youtube.com/watch?v=rfscVS0vtbw")

elif menu == "🎬 Movie Hub":
    st.header("🎬 Movie Hub")
    genre=st.selectbox("Genre",["Action","Comedy","Education","Nollywood","Kenyan"])
    if st.button("Get Recommendations",type="primary"):
        comp=client.chat.completions.create(model="openai/gpt-oss-20b",messages=[{"role":"system","content":"Netflix recommender, 5 movies"},{"role":"user","content":f"Recommend 5 {genre} movies"}],max_tokens=800)
        st.write(comp.choices[0].message.content)

elif menu == "📢 Channels":
    st.header("📢 Channels - Telegram Style")
    ch=st.selectbox("Channel",["📚 Past Papers KE","💻 Coding Help","🎓 UoE Eldoret"])
    st.success(f"You joined {ch}")
    msg=st.text_input(f"Post to {ch}")
    if msg: st.write(f"Posted: {msg}")

else:
    st.header("🎮 Game Hub - With VR Football")
    game=st.selectbox("Choose:",["❌⭕ Tic Tac Toe","✊ Rock Paper","🧠 Math Quiz","⚽ VR Football","🥅 Penalty"])
    if game.startswith("❌"):
        if 'board' not in st.session_state: st.session_state.board=[""]*9
        cols=st.columns(3)
        for i in range(9):
            with cols[i%3]:
                if st.button(st.session_state.board[i] or " ",key=f"b{i}",use_container_width=True):
                    if st.session_state.board[i]=="": st.session_state.board[i]="X"; st.rerun()
        if st.button("Reset"): st.session_state.board=[""]*9; st.rerun()
    elif game.startswith("✊"):
        choice=st.radio("You:",["Rock","Paper","Scissors"],horizontal=True)
        if st.button("Play!"):
            comp=random.choice(["Rock","Paper","Scissors"]); st.write(f"Computer: {comp}")
            if choice==comp: st.info("Draw")
            elif (choice=="Rock" and comp=="Scissors") or (choice=="Paper" and comp=="Rock") or (choice=="Scissors" and comp=="Paper"): st.success("You Win!"); st.balloons()
            else: st.error("You Lose!")
    elif game.startswith("🧠"):
        a=random.randint(1,20); b=random.randint(1,20)
        st.write(f"What is {a} + {b}?"); ans=st.number_input("Answer",step=1)
        if st.button("Check"):
            if ans==a+b: st.success("Correct!"); st.balloons()
            else: st.error(f"Wrong, {a+b}")
    elif game.startswith("⚽"):
        st.subheader("⚽ VR Football Stadium")
        vr_html="""
        <html><head><script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script></head>
        <body><a-scene embedded style="height:450px;width:100%">
          <a-sky color="#87CEEB"></a-sky>
          <a-plane position="0 0 -4" rotation="-90 0 0" width="20" height="20" color="#2E8B57"></a-plane>
          <a-sphere position="0 0.3 -2" radius="0.3" color="white"></a-sphere>
          <a-text value="AIRJACKDE VR" position="-1 3 -5" color="yellow"></a-text>
          <a-camera><a-cursor></a-cursor></a-camera>
        </a-scene>
        <button onclick="alert('GOAL!')" style="padding:15px;background:green;color:white;width:100%">⚽ KICK!</button>
        </body></html>"""
        import streamlit.components.v1 as components; components.html(vr_html,height=550)
    else:
        st.subheader("🥅 Penalty")
        d=st.radio("Shoot:",["Left","Center","Right"],horizontal=True)
        if st.button("Shoot!"):
            k=random.choice(["Left","Center","Right"]); st.write(f"Keeper: {k}")
            if d!=k: st.success("GOAL! ⚽"); st.balloons()
            else: st.error("Saved!")
