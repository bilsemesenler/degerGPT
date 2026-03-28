import streamlit as st
import google.generativeai as genai
import os

# 1. Sayfa Yapılandırması
st.set_page_config(page_title="DeğerGPT", page_icon="🌟", layout="centered")

# 2. API Anahtarı Bağlantısı
# Streamlit Secrets kısmında soldaki kutuya GOOGLE_API_KEY yazmalısın.
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Hata: API Anahtarı bulunamadı! Lütfen Streamlit ayarlarından Secrets kısmına 'GOOGLE_API_KEY' ekleyin.")
    st.stop()

# 3. DeğerGPT Kişilik Ayarı (System Instruction)
instruction = (
    "Senin adın DeğerGPT. Bir bilge arkadaş gibi; samimi, sıcak, 'sen' diliyle konuşan ve empati kuran bir tarzın var. "
    "Görevin: Öğrencilere dürüstlük, sorumluluk, saygı, yardımseverlik, adalet ve hoşgörü gibi değerleri öğretmek. "
    "Yöntemin: Doğrudan öğüt verme. Sokratik sorgulama yap. Örnek olaylar sun ve 'Sen olsan ne yapardın?' diye sor."
)

# 4. Model Başlatma (En uyumlu sürüm: gemini-1.5-flash)
try:
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )
except Exception as e:
    st.error(f"Model başlatılamadı, lütfen sayfayı yenileyin. Hata: {e}")

# 5. Sohbet Geçmişi Yönetimi
if "messages" not in st.session_state:
    st.session_state.messages = []

# Başlık ve Karşılama
st.title("🌟 DeğerGPT: Bilge Arkadaşın")
st.caption("Yapay Zekâ ile Değerler Eğitimi Projesi")

# Geçmiş mesajları ekrana bas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Kullanıcı Girişi ve Yanıt Döngüsü
if prompt := st.chat_input("Merhaba de ve başlayalım..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zekadan yanıt al
    with st.chat_message("assistant"):
        try:
            # Mesaj geçmişini Gemini formatına çevir
            history = []
            for m in st.session_state.messages[:-1]:
                role = "user" if m["role"] == "user" else "model"
                history.append({"role": role, "parts": [m["content"]]})
            
            chat = model.start_chat(history=history)
            response = chat.send_message(prompt)
            
            # Yanıtı göster ve kaydet
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
            
        except Exception as e:
            st.error(f"Yanıt oluşturulamadı. Hata: {e}")
            st.info("İpucu: Eğer 404 hatası alıyorsanız, API anahtarınızın aktif olduğundan ve kısıtlanmadığından emin olun.")
