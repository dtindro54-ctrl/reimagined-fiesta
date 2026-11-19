import os
import requests
from datetime import datetime
from openai import OpenAI

# Menggunakan GitHub Models bawaan (Gratis dengan token GitHub Anda)
client = OpenAI(
    base_url="https://models.inference.ai.azure.com",
    api_key=os.environ["GITHUB_TOKEN"],
)

MODEL = "gpt-4o-mini"

def tanya_agen(peran, instruksi, bahan=""):
    res = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"Kamu adalah {peran}. Jawab dalam bahasa Indonesia yang rapi dan langsung ke inti."},
            {"role": "user", "content": f"{instruksi}\n\nBahan kerja:\n{bahan}"}
        ]
    )
    return res.choices[0].message.content

topik = os.environ.get("TOPIK_UTAMA", "Tips produktivitas bisnis dengan AI")

# AGEN 1: Koordinator
brief = tanya_agen("Agen 1: Manajer Proyek", f"Buat brief singkat dan 3 poin utama untuk topik: {topik}")

# AGEN 2: Riset
riset = tanya_agen("Agen 2: Peneliti & Analis", "Berikan data pendukung, tren, dan solusi praktis dari brief berikut.", brief)

# AGEN 3: Penulis
naskah = tanya_agen("Agen 3: Penulis Konten", "Tulis artikel singkat dan caption media sosial yang menarik.", riset)

# AGEN 4: Produser Aset (Membuat file HTML siap pakai/produk digital)
produk_html = tanya_agen("Agen 4: Produser Produk Digital", "Ubah naskah berikut menjadi kode halaman HTML bersih dengan CSS modern yang siap diterbitkan.", naskah)

# AGEN 5: Peninjau Kritis (QA)
final_caption = tanya_agen("Agen 5: Quality Assurance", "Periksa ulang caption media sosial dari naskah ini agar siap posting tanpa kesalahan ketik. Berikan HANYA teks caption final.", naskah)

# AGEN 6: Eksekutor & Pemasar
waktu = datetime.now().strftime("%Y%m%d_%H%M")
os.makedirs("hasil_produk", exist_ok=True)
nama_file = f"hasil_produk/produk_{waktu}.html"

with open(nama_file, "w", encoding="utf-8") as f:
    f.write(produk_html)

with open(f"hasil_produk/caption_{waktu}.txt", "w", encoding="utf-8") as f:
    f.write(final_caption)

print("Produk berhasil dieksekusi:", nama_file)

# Opsional: Kirim otomatis ke Telegram / Webhook Medsos jika sudah diatur
webhook_url = os.environ.get("WEBHOOK_MEDSOS")
if webhook_url:
    requests.post(webhook_url, json={"caption": final_caption, "file": nama_file})
