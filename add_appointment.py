import sqlite3

def randevu_ekle():
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()

    name = input("Adınızı girin: ")
    randevu_saati = input("Randevu saatini HH:MM formatında girin: ")

    
    try:
        saat, dakika = map(int, randevu_saati.split(":"))
    except ValueError:
        print("⚠ Hatalı saat formatı! Lütfen HH:MM şeklinde girin.")
        return

    c.execute("UPDATE users SET randevu_saati=? WHERE name=?", (randevu_saati, name))
    conn.commit()
    conn.close()
    print(f"✅ {name} için randevu {randevu_saati} olarak kaydedildi!")

randevu_ekle()
