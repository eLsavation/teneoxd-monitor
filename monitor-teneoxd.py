import time
import re
import requests

# Konfigurasi bot Telegram
BOT_TOKEN = ''
CHAT_ID = ''
LOG_FILE = 'output.log'

# Fungsi untuk mengirim pesan ke Telegram
def send_telegram_message(message):
    url = f'https://api.telegram.org/bot{BOT_TOKEN}/sendMessage'
    data = {
        'chat_id': CHAT_ID,
        'text': message
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        print("Pesan berhasil dikirim:", message)
    else:
        print("Gagal mengirim pesan:", response.json())

# Fungsi untuk menghapus karakter kontrol atau escape sequence
def remove_ansi_escape_sequences(text):
    ansi_escape = re.compile(r'\x1b\[[0-9;]*m')
    return ansi_escape.sub('', text)

# Fungsi untuk memantau file log
def monitor_log_file():
    with open(LOG_FILE, 'r') as file:
        # Pindahkan posisi pointer ke akhir file
        file.seek(0, 2)

        while True:
            line = file.readline()
            if not line:
                time.sleep(0.1)  # Tunggu jika tidak ada data baru
                continue

            # Hapus whitespace atau karakter tak terlihat
            line = line.strip()

            # Hapus karakter kontrol ANSI dari log
            line = remove_ansi_escape_sequences(line)

            # Proses log jika bukan "send PING server !" dan "waiting for"
            if "send PING server !" not in line and "waiting for" not in line:
                print("Mengirim log:", line)  # Debugging: lihat log yang akan dikirim
                send_telegram_message(line)

# Jalankan pemantauan
if __name__ == "__main__":
    monitor_log_file()
