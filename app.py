import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="DeğerGPT", page_icon="🌟")
st.title("🌟 DeğerGPT: Bilge Arkadaşın")

# API Key kontrolü
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Secrets kısmında API anahtarı bulunamadı!")
    st.stop()

SYSTEM_PROMPT = "Sen bilge bir arkadaşsın. Değerler eğitimi veriyorsun."

# app.py içindeki bu satırı bul ve değiştir:
try:
    model = genai.GenerativeModel(
        model_name='models/gemini-1.0-pro', # 'gemini-1.5-flash' yerine bunu yazdık
        system_instruction=SYSTEM_PROMPT
    )
except Exception as e:
    st.error(f"Model yüklenirken hata oluştu: {e}")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Neler hissediyorsun?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Basit bir deneme: Geçmişi göndermeden önce modelin çalışıp çalışmadığını test edelim
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Yanıt üretilirken bir hata oluştu: {e}")
            st.info("Eğer 'NotFound' hatası alıyorsan, model ismini 'models/gemini-1.0-pro' olarak değiştirmeyi dene.")
