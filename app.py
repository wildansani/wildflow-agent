import streamlit as st
import google.generativeai as genai
import time

# 1. Konfigurasi Halaman (Mode Layar Penuh seperti Gemini)
st.set_page_config(page_title="WildFlow AI", page_icon="✨", layout="wide")

# CSS Custom untuk menyembunyikan elemen bawaan Streamlit agar UI lebih bersih
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Desain Sidebar (Menu Samping)
with st.sidebar:
    st.title("✨ WildFlow AI")
    st.caption("Powered by Gemini 3.8 Flash")
    
    api_key = st.text_input("Gemini API Key", type="password")
    
    st.divider()
    
    # Tombol Obrolan Baru
    if st.button("➕ Obrolan Baru", use_container_width=True):
        st.session_state.messages = []
        if "chat_session" in st.session_state:
            del st.session_state.chat_session
        st.rerun()

# 3. Tools (Fungsi Aksi)
def cek_status_server(ip_address: str) -> str:
    """Mengecek status jaringan dan beban dari sebuah server berdasarkan IP Address."""
    if ip_address == "192.168.1.10":
        return "Status: UP. CPU Load: 15%. RAM: 2GB/8GB. Tidak ada anomali pada container."
    elif ip_address == "10.0.0.5":
        return "Status: DOWN. Koneksi timeout saat proses ping."
    else:
        return f"IP {ip_address} tidak dikenali dalam infrastruktur."

# 4. Logika Utama
if api_key:
    genai.configure(api_key=api_key)
    
    # Inisialisasi Sesi & Persona
    if "chat_session" not in st.session_state:
        model = genai.GenerativeModel(
            model_name='gemini-3.8-flash',
            tools=[cek_status_server],
            system_instruction="Kamu adalah WildFlow, AI asisten cerdas yang diciptakan oleh programmer bernama Wildan Sani. Gunakan nada bicara yang profesional namun ramah. Gunakan format markdown untuk menyusun jawaban agar rapi."
        )
        st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)
        # Pesan sambutan bawaan
        st.session_state.messages = [{"role": "assistant", "content": "Halo! Saya WildFlow. Ada sistem yang perlu saya cek atau bantu hari ini?"}]

    # 5. Render Riwayat Pesan dengan Avatar
    for message in st.session_state.messages:
        avatar = "🧑‍💻" if message["role"] == "user" else "✨"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    # 6. Tangkap Input Pengguna
    if prompt := st.chat_input("Ketik pesan ke WildFlow di sini..."):
        # Tampilkan input pengguna
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.markdown(prompt)

        # Tampilkan respons AI dengan efek streaming (mengetik)
        with st.chat_message("assistant", avatar="✨"):
            with st.spinner("Berpikir..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    
                    # Generator untuk membuat efek teks mengalir (streaming)
                    def stream_data(text):
                        for word in text.split(" "):
                            yield word + " "
                            time.sleep(0.04) # Kecepatan mengetik
                            
                    st.write_stream(stream_data(response.text))
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada sistem AI: {e}")
else:
    # Tampilan Halaman Depan jika API Key belum dimasukkan
    st.title("Selamat Datang di WildFlow AI ✨")
    st.write("Silakan masukkan **Gemini API Key** di menu sebelah kiri untuk mengaktifkan sistem.")
