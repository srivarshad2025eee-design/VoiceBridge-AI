import streamlit as st
from sarvamai import SarvamAI

st.set_page_config(
    page_title="VoiceBridge AI",
    page_icon="🎙️",
    layout="wide"
)

# ---------- DESIGN ----------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0B1026, #172554, #312E81);
    color: white;
}
.block-container {
    max-width: 1050px;
    padding-top: 2rem;
}
h1, h2, h3, p, label {
    color: white !important;
}
.hero {
    text-align: center;
    padding: 35px 15px;
    background: linear-gradient(120deg, #172554, #4338CA);
    border: 1px solid #6478D8;
    border-radius: 22px;
    margin-bottom: 25px;
}
.hero h1 {
    font-size: 46px;
    font-weight: 800;
    margin-bottom: 8px;
}
.hero p {
    color: #C7D2FE !important;
    font-size: 17px;
}
.feature {
    background: #18264A;
    border: 1px solid #344875;
    border-radius: 16px;
    padding: 18px;
    text-align: center;
    margin-bottom: 12px;
}
.stButton > button {
    width: 100%;
    background: linear-gradient(90deg, #06B6D4, #6366F1);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 12px;
    font-weight: 700;
}
.stButton > button:hover {
    border: 1px solid #67E8F9;
    color: white;
}
.result-card {
    background: #18264A;
    border: 1px solid #3B5285;
    border-radius: 15px;
    padding: 20px;
    margin-top: 12px;
    color: white;
}
.footer {
    text-align: center;
    color: #A5B4FC;
    padding: 25px;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)

# ---------- LANGUAGES ----------
languages = {
    "Tamil 🇮🇳": "ta-IN",
    "English 🌐": "en-IN",
    "Hindi 🇮🇳": "hi-IN",
    "Telugu 🇮🇳": "te-IN",
    "Malayalam 🇮🇳": "ml-IN",
    "Kannada 🇮🇳": "kn-IN",
    "Bengali 🇮🇳": "bn-IN",
    "Marathi 🇮🇳": "mr-IN",
    "Gujarati 🇮🇳": "gu-IN",
    "Punjabi 🇮🇳": "pa-IN"
}

# ---------- HEADER ----------
st.markdown("""
<div class="hero">
    <h1>🎙️ VoiceBridge AI</h1>
    <p>Your Voice. Any Language. No Barriers.</p>
    <p>Speak naturally. Understand globally.</p>
</div>
""", unsafe_allow_html=True)

# ---------- FEATURES ----------
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div class="feature">
    <h2>🎤</h2>
    <b>Voice Recognition</b>
    <p>Convert speech into text</p>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="feature">
    <h2>🌍</h2>
    <b>Multilingual AI</b>
    <p>Translate across languages</p>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="feature">
    <h2>⚡</h2>
    <b>Simple Experience</b>
    <p>Easy voice-based interaction</p>
    </div>
    """, unsafe_allow_html=True)

st.write("")
st.subheader("✨ Start Your Translation")

# ---------- LANGUAGE SELECTION ----------
left, right = st.columns(2)

with left:
    source = st.selectbox(
        "🎯 Speak in",
        list(languages.keys()),
        index=0
    )

with right:
    target_options = [
        lang for lang in languages if lang != source
    ]
    target = st.selectbox(
        "🌐 Translate into",
        target_options,
        index=0
    )

st.write("")

# ---------- VOICE INPUT ----------
st.markdown("### 🎙️ Record Your Voice")
audio = st.audio_input("Tap below to record your message")

if st.button("✨ Convert Speech to Text"):
    if audio is None:
        st.warning("Please record your voice first.")
    else:
        try:
            with st.spinner("Listening to your voice..."):
                client = SarvamAI(
                    api_subscription_key=st.secrets["SARVAM_API_KEY"]
                )

                result = client.speech_to_text.transcribe(
                    file=audio,
                    model="saaras:v4",
                    language_code=languages[source],
                    mode="transcribe"
                )

                st.session_state["spoken_text"] = result.transcript
                st.session_state["spoken_language"] = source
                st.session_state.pop("translated_text", None)

            st.success("Speech converted successfully!")

        except Exception as e:
            st.error(f"Speech recognition failed: {e}")

# ---------- TRANSCRIPT ----------
if st.session_state.get("spoken_text"):
    st.markdown("### 📝 Recognized Speech")

    st.markdown(
        f'<div class="result-card">{st.session_state["spoken_text"]}</div>',
        unsafe_allow_html=True
    )

    st.write("")

    if st.button("🌍 Translate Text"):
        try:
            with st.spinner("Translating your message..."):
                client = SarvamAI(
                    api_subscription_key=st.secrets["SARVAM_API_KEY"]
                )

                translation = client.text.translate(
                    input=st.session_state["spoken_text"],
                    source_language_code=languages[
                        st.session_state["spoken_language"]
                    ],
                    target_language_code=languages[target],
                    model="mayura:v1"
                )

                st.session_state["translated_text"] = (
                    translation.translated_text
                )

            st.success("Translation completed!")

        except Exception as e:
            st.error(f"Translation failed: {e}")

# ---------- TRANSLATION RESULT ----------
if st.session_state.get("translated_text"):
    st.markdown("### ✨ Your Translation")

    st.markdown(
        f'<div class="result-card">{st.session_state["translated_text"]}</div>',
        unsafe_allow_html=True
    )

    st.download_button(
        "⬇️ Download Translation",
        data=st.session_state["translated_text"],
        file_name="VoiceBridge_Translation.txt",
        mime="text/plain"
    )

# ---------- FOOTER ----------
st.markdown("""
<div class="footer">
    VOICEBRIDGE AI | Powered by Sarvam AI<br>
    Connecting People Through Language
</div>
""", unsafe_allow_html=True)