import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

def scrape_all_pages():
    base_url = "https://simbelmawa.kemdikbud.go.id/magang/lowongan?page="
    all_data = []

    for page_num in range(1, 40):  # sesuaikan jika lebih dari 39 halaman
        print(f"Scraping halaman {page_num}...")
        response = requests.get(base_url + str(page_num), headers={"User-Agent": "Mozilla/5.0"})
        soup = BeautifulSoup(response.text, "html.parser")
        app_div = soup.find("div", id="app")

        if not app_div or 'data-page' not in app_div.attrs:
            print("⚠️  Tidak menemukan data-page di halaman ini. Selesai.")
            break

        data_page = json.loads(app_div['data-page'])

        lowongan_list = data_page["props"]["data"]["data"]
        if not lowongan_list:
            print("✅ Semua data telah diambil.")
            break

        for item in lowongan_list:
            posisi = item.get("posisi_magang", "")
            mitra = item.get("mitra", "")
            kategori = item.get("kategori_posisi", "")
            lokasi = item.get("lokasi_penempatan", "")
            deskripsi = item.get("deskripsi", "")
            all_data.append([posisi, mitra, kategori, lokasi, deskripsi])

    # Simpan ke Excel
    df = pd.DataFrame(all_data, columns=["Posisi", "Mitra", "Bidang", "Lokasi", "Deskripsi"])
    df.to_excel("lowongan_simbelmawa_all_with_desc.xlsx", index=False)
    print("✅ Semua data berhasil disimpan ke lowongan_simbelmawa_all_with_desc.xlsx")

    return df

# Jalankan scraping
df = scrape_all_pages()
df.head()