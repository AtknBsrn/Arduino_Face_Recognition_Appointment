import cv2
import face_recognition
import numpy as np
import serial
import time
from sound import randevu_sesi_oynat
import sqlite3
from face_recognition_db import get_face_encoding
from datetime import datetime, timedelta

# 📌 Arduino ile bağlantı başlat
arduino = serial.Serial('COM3', 9600)
time.sleep(2)

# 📌 Servo başlangıç açıları
servo_x = 90
servo_y = 90
arduino.write(f'{servo_x},{servo_y}\n'.encode())
time.sleep(1)

# 📌 Tarama Modu Değişkenleri
arama_modu = True
arama_yon_x = 5
arama_yon_y = 3
yuz_kayboldu_sayac = 0
yuz_kaybolma_limiti = 5

# 📌 Servo hareket sınırları
servo_x_min, servo_x_max = 0, 180
servo_y_min, servo_y_max = 60, 130  # Y ekseni artık daha geniş hareket edecek

# 📌 Veritabanından yüzleri al
known_face_encodings = []
known_face_names = []

conn = sqlite3.connect('face_recognition.db')
c = conn.cursor()
c.execute("SELECT name FROM users")
users = c.fetchall()
conn.close()

for user in users:
    name = user[0]
    encoding = get_face_encoding(name)
    if encoding is not None:
        known_face_encodings.append(encoding)
        known_face_names.append(name)

print(f"📌 {len(known_face_names)} kişi yüklendi: {known_face_names}")

# 📌 Kamera ayarları
video_capture = cv2.VideoCapture(0)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 480)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 360)
video_capture.set(cv2.CAP_PROP_FPS, 30)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

frame_counter = 0

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # 📌 Yüz tespitini her 5 karede bir yaparak hızlandırıyoruz
    if frame_counter % 5 == 0:
        face_locations = face_recognition.face_locations(rgb_frame, model="hog")
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    frame_counter += 1

    if face_locations:
        arama_modu = False
        yuz_kayboldu_sayac = 0
    else:
        yuz_kayboldu_sayac += 1
        if yuz_kayboldu_sayac == yuz_kaybolma_limiti:
            print("🔍 Yüz bulunamadı, tarama modu aktif...")

    if arama_modu:
        servo_x += arama_yon_x
        if servo_x >= servo_x_max or servo_x <= servo_x_min:
            arama_yon_x = -arama_yon_x

        servo_y += arama_yon_y
        if servo_y >= servo_y_max or servo_y <= servo_y_min:
            arama_yon_y = -arama_yon_y

        arduino.write(f'{servo_x},{servo_y}\n'.encode())
        time.sleep(0.05)

    else:
        for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
            x_center = (left + right) // 2
            y_center = (top + bottom) // 2

            frame_center_x = 480 // 2
            frame_center_y = 360 // 2

            x_hata = x_center - frame_center_x
            y_hata = y_center - frame_center_y

            hassasiyet = 5

            if abs(x_hata) > 30:
                if x_hata < 0:
                    servo_x += hassasiyet
                else:
                    servo_x -= hassasiyet

            if abs(y_hata) > 30:
                if y_hata < 0:
                    servo_y += hassasiyet
                else:
                    servo_y -= hassasiyet

            servo_x = max(0, min(180, servo_x))
            servo_y = max(servo_y_min, min(servo_y_max, servo_y))

            arduino.write(f'{servo_x},{servo_y}\n'.encode())
            time.sleep(0.05)

            # 📌 Yeşil bir kutu çiz ve ismi yaz
            name = "Bilinmiyor"
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.5)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Yüz Tanıma ve Servo Takip", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
arduino.close()
cv2.destroyAllWindows()
