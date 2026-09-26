import streamlit as st
import google.generativeai as genai

# Konfigurasi Halaman
st.set_page_config(page_title="WildFlow Agent", page_icon="⚡")
st.title("⚡ WildFlow System")
st.caption("AI SysAdmin Assistant - Interactive Mode")

# Sidebar untuk input API Key
api_key = st.sidebar.text_input("Masukkan Gemini API Key", type="password")

# Tools (Fungsi Aksi WildFlow)
def cek_status_server(ip_address: str) -> str:
    """Mengecek status jaringan dan beban dari sebuah server berdasarkan IP Address."""
    if ip_address == "192.168.1.10":
        return "Status: UP. CPU Load: 15%. RAM: 2GB/8GB. Tidak ada anomali pada container."
    elif ip_address == "10.0.0.5":
        return "Status: DOWN. Koneksi timeout saat proses ping."
    else:
        return f"IP {ip_address} tidak dikenali dalam infrastruktur."

# Logika Utama
if api_key:
    genai.configure(api_key=api_key)
    
    # Inisialisasi Session State agar memori tidak hilang
    if "chat_session" not in st.session_state:
        # PERBAIKAN FINAL: Menggunakan model generasi terbaru Gemini 2.5 Flash
        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            tools=[cek_status_server]
        )
        st.session_state.chat_session = model.start_chat(enable_automatic_function_calling=True)
        st.session_state.messages = []

    # Render ulang riwayat pesan
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Tangkap input pengguna
    if prompt := st.chat_input("Tanya WildFlow (misal: Cek status IP 192.168.1.10)"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Proses response AI dengan penanganan error
        with st.chat_message("assistant"):
            with st.spinner("WildFlow sedang memproses..."):
                try:
                    response = st.session_state.chat_session.send_message(prompt)
                    st.markdown(response.text)
                    st.session_state.messages.append({"role": "assistant", "content": response.text})
                except Exception as e:
                    st.error(f"Terjadi kesalahan pada sistem AI: {e}")
else:
    st.info("Silakan masukkan Gemini API Key di menu sebelah kiri untuk mengaktifkan WildFlow.")
