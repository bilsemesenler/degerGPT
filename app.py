import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="DeğerGPT", page_icon="🌟")
st.title("🌟 DeğerGPT: Bilge Arkadaşın")

# API Anahtarı Kontrolü
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen Streamlit Secrets kısmına GOOGLE_API_KEY ekle!")
    st.stop()

# DeğerGPT'nin Kişilik Talimatı
SYSTEM_PROMPT = "Senin adın DeğerGPT. Bir bilge arkadaş gibi; samimi, sıcak, 'sen' diliyle konuşan ve empati kuran bir tarzın var. Görevin: Öğrencilere dürüstlük, sorumluluk, saygı, yardımseverlik, adalet ve hoşgörü gibi değerleri öğretmek. Yöntemin: Doğrudan öğüt verme. Sokratik sorgulama yap. Örnek olaylar sun ve 'Sen olsan ne yapardın?' diye sor."

# --- MODEL TANIMLAMA (EN UYUMLU YÖNTEM) ---
# Burada model ismini 'gemini-pro' olarak sadeleştiriyoruz
try:
    model = genai.GenerativeModel('gemini-pro') 
except Exception as e:
    st.error(f"Model başlatılamadı: {e}")

# Sohbet geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcı girişi
if prompt := st.chat_input("Mesajını yaz..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # SİSTEM TALİMATINI MESAJIN BAŞINA EKLEYEREK GÖNDERİYORUZ (En güvenli yol)
            full_prompt = f"{SYSTEM_PROMPT}\n\nKullanıcı diyor ki: {prompt}"
            
            response = model.generate_content(full_prompt)
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            else:
                st.warning("Modelden boş yanıt döndü.")
        except Exception as e:
            st.error(f"Hata detayı: {e}")
            st.info("İpucu: Eğer hala 404 alıyorsan, lütfen Google AI Studio'dan yeni bir API KEY alıp Secrets kısmına yapıştır.")
