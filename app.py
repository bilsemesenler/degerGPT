import streamlit as st
from google import genai
import os

# Bu satırı importların hemen altına ekle
os.environ["GOOGLE_API_USE_BETA_VERSION"] = "0"

# Sayfa Yapılandırması
st.set_page_config(page_title="DeğerGPT", page_icon="🌟")
st.title("🌟 DeğerGPT: Bilge Arkadaşın")

# 1. API Anahtarını Streamlit Secrets'tan alalım
# Secrets kısmında sol kutuya GEMINI_API_KEY, sağa anahtarını yazmalısın.
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    client = genai.Client(api_key=api_key)
else:
    st.error("Hata: GEMINI_API_KEY Secrets kısmında bulunamadı!")
    st.stop()

# 2. Karakter Tanımlaması (System Instruction)
SYSTEM_PROMPT = (
    "Senin adın DeğerGPT. Bir bilge arkadaş gibi; samimi, sıcak, 'sen' diliyle konuşan ve empati kuran bir tarzın var. "
    "Görevin: Öğrencilere dürüstlük, sorumluluk, saygı, yardımseverlik, adalet ve hoşgörü gibi değerleri öğretmek. "
    "Yöntemin: Doğrudan öğüt verme. Sokratik sorgulama yap. Örnek olaylar sun ve 'Sen olsan ne yapardın?' diye sor."
)

# Sohbet geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Eski mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Kullanıcı Girişi
if prompt := st.chat_input("Nelerden konuşalım?"):
    # Kullanıcı mesajını göster ve kaydet
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay Zekâ Yanıtı
    with st.chat_message("assistant"):
        try:
            # Senin paylaştığın yeni nesil Client yapısı
            # Not: gemini-3-flash-preview henüz herkese açık olmayabilir, 
            # hata alırsan 'gemini-2.0-flash' veya 'gemini-1.5-flash' yazabilirsin.
            
            response = client.models.generate_content(
                model="gemini-1.5-flash", # Başındaki models/ kısmını sildik
                contents=prompt,
                config={
                    'system_instruction': SYSTEM_PROMPT,
                    'temperature': 0.7
                }
            )
            
            ai_response = response.text
            st.markdown(ai_response)
            st.session_state.messages.append({"role": "assistant", "content": ai_response})
            
        except Exception as e:
            st.error(f"Bir hata oluştu: {e}")
