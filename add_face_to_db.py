import sqlite3
import face_recognition
import numpy as np
import os

# Veritabanına bağlan
conn = sqlite3.connect('face_recognition.db')
c = conn.cursor()

# Eğer tablo yoksa oluştur
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        face_encoding BLOB
    )
''')

def add_face_encoding(name, image_path):
    print(f"[INFO] '{image_path}' dosyası kontrol ediliyor...")

    if not os.path.exists(image_path):
        print("[ERROR] Dosya bulunamadı! Lütfen fotoğraf çekin.")
        return

    # Fotoğrafı oku
    image = face_recognition.load_image_file(image_path)
    face_encodings = face_recognition.face_encodings(image)

    if not face_encodings:
        print("[ERROR] Yüz algılanamadı. Farklı bir fotoğraf deneyin.")
        return

    encoding = face_encodings[0]  # İlk yüzü al
    encoding_blob = encoding.tobytes()  # Binary olarak kaydet

    # Veriyi veritabanına ekle
    print(f"[INFO] '{name}' için yüz verisi kaydediliyor...")
    c.execute("INSERT INTO users (name, face_encoding) VALUES (?, ?)", (name, encoding_blob))
    conn.commit()
    print(f"[SUCCESS] '{name}' veritabanına başarıyla eklendi!")

# Kullanıcıdan isim al ve yüzü kaydet
name = input("Adınızı girin: ")
image_path = "faces/benim_yuzum2.jpg"  # Çektiğin fotoğrafın yolu
add_face_encoding(name, image_path)

conn.close()
print("[INFO] Veritabanı bağlantısı kapatıldı.")
