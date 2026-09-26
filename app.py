import streamlit as st
import google.generativeai as genai
import time

# 1. Konfigurasi Halaman
st.set_page_config(page_title="WildFlow AI", page_icon="✨", layout="wide")

# CSS Custom untuk UI bersih (opsional)
st.markdown("""
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 2. Inisialisasi Status Login di Memori
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# ==========================================
# HALAMAN LOGIN
# ==========================================
if not st.session_state.logged_in:
    # Buat form login agar rapi di tengah
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("🔒 Login WildFlow AI")
        st.write("Silakan masukkan kredensial untuk mengakses sistem.")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit_button = st.form_submit_button("Masuk", use_container_width=True)
            
            if submit_button:
                # Cek kredensial (Ubah password di sini sesuai keinginan Anda)
                if username == "wildan" and password == "admin123":
                    st.session_state.logged_in = True
                    st.rerun() # Muat ulang halaman untuk masuk ke aplikasi
                else:
                    st.error("Username atau password salah!")

# ==========================================
# HALAMAN UTAMA WILDFLOW (Terbuka setelah login)
# ==========================================
else:
    # 3. Desain Sidebar (Menu Samping)
    with st.sidebar:
        st.title("✨ WildFlow AI")
        st.write("👤 Pengguna: **Wildan**")
        
        # Tombol Logout
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.logged_in = False
            st.rerun()
            
        st.divider()
        
        api_key = st.text_input("Gemini API Key", type="password")
        
        st.divider()
        
        # Tombol Obrolan Baru
        if st.button("➕ Obrolan Baru", use_container_width=True):
            st.session_state.messages = []
            if "chat_session" in st.session_state:
                del st.session_state.chat_session
            st.rerun()

    # 4. Tools (Fungsi Aksi)
    def cek_status_server(ip_address: str) -> str:
        """Mengecek status jaringan dan beban dari sebuah server berdasarkan IP Address."""
        if ip_address == "192.168.1.10":
            return "Status: UP. CPU Load: 15%. RAM: 2GB/8GB. Tidak ada anomali pada container."
        elif ip_address == "10.0.0.5":
            return "Status: DOWN. Koneksi timeout saat proses ping."
        else:
            return f"IP {ip_address} tidak dikenali dalam infrastruktur."

    # 5. Logika Utama AI
    if api_key:
        genai.configure(api_key=api_key)
        
        if "chat_session" not in st.session_state:
            model = genai.GenerativeModel(
                model_name='gemini-3.8-flash',
                tools=[cek_status_server],
                system_instruction="Kamu adalah WildFlow, AI asisten cerdas yang diciptakan oleh programmer bernama Wildan Sani. Gunakan nada bicara yang profesional namun ramah. Gunakan format markdown untuk menyusun jawaban agar rapi."
            )
            st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)
            st.session_state.messages = [{"role": "assistant", "content": "Halo! Saya WildFlow. Ada sistem yang perlu saya cek atau bantu hari ini?"}]

        # Render Riwayat Pesan dengan Avatar
        for message in st.session_state.messages:
            avatar = "🧑‍💻" if message["role"] == "user" else "✨"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])

        # Tangkap Input Pengguna
        if prompt := st.chat_input("Ketik pesan ke WildFlow di sini..."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user", avatar="🧑‍💻"):
                st.markdown(prompt)

            with st.chat_message("assistant", avatar="✨"):
                with st.spinner("Berpikir..."):
                    try:
                        response = st.session_state.chat_session.send_message(prompt)
                        
                        def stream_data(text):
                            for word in text.split(" "):
                                yield word + " "
                                time.sleep(0.04) 
                                
                        st.write_stream(stream_data(response.text))
                        st.session_state.messages.append({"role": "assistant", "content": response.text})
                    except Exception as e:
                        st.error(f"Terjadi kesalahan pada sistem AI: {e}")
    else:
        st.title("Selamat Datang di WildFlow AI ✨")
        st.write("Silakan masukkan **Gemini API Key** di menu sebelah kiri untuk mengaktifkan sistem.")
