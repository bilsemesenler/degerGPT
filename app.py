import streamlit as st
import google.generativeai as genai

# Sayfa Ayarları
st.set_page_config(page_title="DeğerGPT", page_icon="🌟")
st.title("🌟 DeğerGPT: Bilge Arkadaşın")
st.markdown("Merhaba! Ben seninle değerlerimiz üzerine sohbet etmek için buradayım. Merak ettiğin bir şey mi var, yoksa bir hikaye ile mi başlayalım?")

# API Anahtarını Ayarla (Streamlit Secrets üzerinden alacağız)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Lütfen API anahtarını Ayarlar (Secrets) kısmına ekle!")

# DeğerGPT'nin Kişilik Talimatı (System Instruction)
SYSTEM_PROMPT = """
Senin adın DeğerGPT. Bir bilge arkadaş gibi; samimi, sıcak, 'sen' diliyle konuşan ve empati kuran bir tarzın var. 
Görevin: Öğrencilere dürüstlük, sorumluluk, saygı, yardımseverlik, adalet ve hoşgörü gibi değerleri öğretmek.
Yöntemin: Doğrudan öğüt verme. Sokratik sorgulama yap. Örnek olaylar (senaryolar) sun ve 'Sen olsan ne yapardın?' diye sor.
Öğrenci etik olmayan bir cevap verirse kızma, onu düşünmeye sevk edecek başka bir soru sor.
"""

# Sohbet geçmişini başlat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Geçmiş mesajları ekranda göster
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Kullanıcıdan giriş al
if prompt := st.chat_input("Bir değer seçelim mi? Mesela: Dürüstlük..."):
    # Kullanıcı mesajını ekle
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Yapay zeka yanıtı oluştur
    with st.chat_message("assistant"):
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=SYSTEM_PROMPT
        )
        
        # Geçmişi modele gönder
        chat = model.start_chat(history=[
            {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
            for m in st.session_state.messages[:-1]
        ])
        
        response = chat.send_message(prompt)
        full_response = response.text
        st.markdown(full_response)
    
    # Yanıtı geçmişe ekle
    st.session_state.messages.append({"role": "assistant", "content": full_response})
