import sqlite3

def randevu_ekle():
    """
    Kullanıcıdan randevu bilgilerini alıp veritabanına ekler.
    """
    conn = sqlite3.connect('face_recognition.db')  # Veritabanına bağlan
    c = conn.cursor()

    # 📌 Kullanıcıdan bilgileri al
    name = input("Adınızı girin: ")
    randevu_saati = input("Randevu saatini HH:MM formatında girin: ")

    # 📌 Kullanıcı zaten var mı kontrol et
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    result = c.fetchone()

    if result:
        # Kullanıcı zaten varsa randevu saatini güncelle
        c.execute("UPDATE users SET randevu_saati=? WHERE name=?", (randevu_saati, name))
        print(f"{name} için randevu saati güncellendi: {randevu_saati}")
    else:
        # Kullanıcı yoksa yeni kayıt oluştur
        c.execute("INSERT INTO users (name, randevu_saati) VALUES (?, ?)", (name, randevu_saati))
        print(f"{name} için yeni randevu kaydedildi: {randevu_saati}")

    # 📌 Veritabanını kaydet ve bağlantıyı kapat
    conn.commit()
    conn.close()

if __name__ == "__main__":
    randevu_ekle()
