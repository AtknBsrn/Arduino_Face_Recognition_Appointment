import sqlite3

def randevu_ekle():
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()

    name = input("Adınızı girin: ")
    randevu_saati = input("Randevu saatini HH:MM formatında girin: ")

    c.execute("SELECT * FROM users WHERE name=?", (name,))
    result = c.fetchone()

    if result:
        c.execute("UPDATE users SET randevu_saati=? WHERE name=?", (randevu_saati, name))
        print(f"{name} için randevu saati güncellendi: {randevu_saati}")
    else:
        c.execute("INSERT INTO users (name, randevu_saati) VALUES (?, ?)", (name, randevu_saati))
        print(f"{name} için yeni randevu kaydedildi: {randevu_saati}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    randevu_ekle()
