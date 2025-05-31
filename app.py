import streamlit as st
from Crypto.Cipher import AES, DES
from Crypto.Util.Padding import unpad
import base64
import io

# --- Fungsi Dekripsi AES ---
def aes_decrypt(data, key):
    iv = base64.b64decode(data[:24])  # Mengambil IV dari data
    ct = base64.b64decode(data[24:])  # Mengambil ciphertext
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt

# --- Fungsi Dekripsi DES ---
def des_decrypt(data, key):
    iv = base64.b64decode(data[:24])  # Mengambil IV dari data
    ct = base64.b64decode(data[24:])  # Mengambil ciphertext
    cipher = DES.new(key, DES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), DES.block_size)
    return pt

# --- UI Utama ---
st.set_page_config(page_title="🔓 File Decryption App", page_icon="🔑", layout="wide")

# Load CSS
with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Sidebar menu
st.sidebar.title("Menu")
menu_options = ["Home", "Decrypt File"]
choice = st.sidebar.selectbox("Pilih Halaman", menu_options)

# Konten untuk setiap menu
if choice == "Home":
    st.title("🔓 Aplikasi Dekripsi File")
    st.markdown("<h5 style='text-align: center; color: gray;'>Dekripsi file Anda dengan mudah dan aman</h5>", unsafe_allow_html=True)

    # Deskripsi Fitur
    st.subheader("Fitur Utama")
    st.markdown("""
    - **Mendukung Berbagai Algoritma**: Aplikasi ini mendukung dekripsi menggunakan algoritma AES dan DES, yang merupakan standar enkripsi yang kuat.
    - **Mudah Digunakan**: Cukup unggah file terenkripsi Anda, masukkan kunci yang sesuai, dan klik tombol dekripsi.
    - **Keamanan Data**: Semua dekripsi dilakukan secara lokal, dan tidak ada data yang disimpan di server.
    """)

    # Instruksi Penggunaan
    st.subheader("Instruksi Penggunaan")
    st.markdown("""
    1. **Unggah File**: Pilih file terenkripsi dengan ekstensi `.enc`.
    2. **Masukkan Kunci**: Masukkan kunci yang digunakan untuk mengenkripsi file.
    3. **Dekripsi File**: Klik tombol 'Decrypt' untuk mendekripsi file.
    4. **Unduh File**: Setelah proses selesai, Anda dapat mengunduh file yang telah didekripsi.
    """)

    # Tambahkan gambar atau ikon dengan ukuran yang diatur
    st.image("https://cdn-icons-png.freepik.com/512/17008/17008364.png", 
             caption="Aplikasi Dekripsi File", 
             width=100,  # Atur lebar gambar sesuai kebutuhan
             use_container_width=False)  # Set False jika ingin menggunakan width

    # Tambahkan informasi tambahan
    st.subheader("Tentang Aplikasi")
    st.markdown("""
    Aplikasi ini dirancang untuk membantu pengguna mendekripsi file yang telah dienkripsi dengan aman. 
    Dengan antarmuka yang sederhana dan intuitif, Anda dapat dengan mudah mengelola file sensitif Anda.
    """)

elif choice == "Decrypt File":
    st.title("Dekripsi File")
    
    # Input untuk dekripsi
    uploaded_file = st.file_uploader("Upload file terenkripsi (dengan ekstensi .enc)", type=["enc"])
    key_input = st.text_input("Masukkan kunci (16 karakter untuk AES, 8 karakter untuk DES)", max_chars=16)
    
    if uploaded_file and (len(key_input) == 16 or len(key_input) == 8):
        key = key_input.encode()
        data = uploaded_file.read()

        if st.button("Decrypt"):
            try:
                if len(key_input) == 16:  # AES
                    decrypted_data = aes_decrypt(data.decode('utf-8'), key)
                    algorithm = "AES"
                elif len(key_input) == 8:  # DES
                    decrypted_data = des_decrypt(data.decode('utf-8'), key)
                    algorithm = "DES"

                # Menggunakan BytesIO untuk mengunduh file langsung
                decrypted_file = io.BytesIO(decrypted_data)
                st.success("✅ File berhasil didekripsi!")
                st.download_button("⬇️ Download Decrypted File", decrypted_file, file_name=uploaded_file.name.replace(".enc", ""), mime="application/octet-stream")
            except Exception as e:
                st.error(f"❌ Gagal dekripsi: {e}")
    else:
        st.info("📝 Silakan upload file dan masukkan kunci yang sesuai.")

# Footer
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>© 2025 File Decryption App By Litbang. All rights reserved.</p>", unsafe_allow_html=True)
