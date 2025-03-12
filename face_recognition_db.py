import sqlite3
import face_recognition
import numpy as np


# 📌 Veritabanı bağlantısını oluştur
def connect_db():
    return sqlite3.connect('face_recognition.db')


# 📌 Yüz encoding'ini veritabanından al
def get_face_encoding(name):
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT face_encoding FROM users WHERE name=?", (name,))
    result = c.fetchone()

    conn.close()

    if result:
        return np.frombuffer(result[0], dtype=np.float64)  # Doğru formatta veriyi al
    return None


# 📌 Yüz encoding'ini veritabanına ekle
def add_face_encoding(name, image_path):
    image = face_recognition.load_image_file(image_path)
    encodings = face_recognition.face_encodings(image)

    if not encodings:
        print("⚠ Yüz algılanamadı! Farklı bir fotoğraf deneyin.")
        return False

    encoding = encodings[0]

    conn = connect_db()
    c = conn.cursor()

    # Kullanıcı zaten var mı kontrol et
    c.execute("SELECT * FROM users WHERE name=?", (name,))
    result = c.fetchone()

    if result:
        c.execute("UPDATE users SET face_encoding=? WHERE name=?", (encoding.tobytes(), name))
        print(f"🔄 {name} için yüz verisi güncellendi.")
    else:
        c.execute("INSERT INTO users (name, face_encoding) VALUES (?, ?)", (name, encoding.tobytes()))
        print(f"✅ {name} için yeni yüz verisi eklendi.")

    conn.commit()
    conn.close()
    return True


# 📌 Kullanıcının randevu saatini veritabanına ekle veya güncelle
def add_randevu(name, randevu_saati):
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE name=?", (name,))
    result = c.fetchone()

    if result:
        c.execute("UPDATE users SET randevu_saati=? WHERE name=?", (randevu_saati, name))
        print(f"🔄 {name} için randevu saati güncellendi: {randevu_saati}")
    else:
        c.execute("INSERT INTO users (name, randevu_saati) VALUES (?, ?)", (name, randevu_saati))
        print(f"✅ {name} için yeni randevu eklendi: {randevu_saati}")

    conn.commit()
    conn.close()


# 📌 Kullanıcının randevu saatini al
def get_randevu(name):
    conn = connect_db()
    c = conn.cursor()

    c.execute("SELECT randevu_saati FROM users WHERE name=?", (name,))
    result = c.fetchone()

    conn.close()

    if result and result[0]:
        return result[0]
    return None
