import cv2
import face_recognition
import numpy as np
import serial
import time
from sound import randevu_sesi_oynat
import sqlite3
from face_recognition_db import get_face_encoding
from datetime import datetime, timedelta
import psutil
import os
import threading

class DummySerial:
    def write(self, data):
        print(f"[Mock Serial] Veri gönderildi: {data.decode().strip()}")

    def close(self):
        print("[Mock Serial] Bağlantı kapatıldı.")

arduino = DummySerial()

servo_x = 90
servo_y = 90
arduino.write(f'{servo_x},{servo_y}\n'.encode())
time.sleep(1)

arama_modu = True
arama_yon_x = 5
arama_yon_y = 3
yuz_kayboldu_sayac = 0
yuz_kaybolma_limiti = 5

servo_x_min, servo_x_max = 0, 180
servo_y_min, servo_y_max = 60, 130  

process = psutil.Process(os.getpid())
def monitor_performance():
    while True:
        cpu = process.cpu_percent()
        ram = process.memory_info().rss / (1024 * 1024)
        print(f"[Sistem Kullanımı] CPU: %{cpu:.1f} | RAM: {ram:.2f} MB")
        time.sleep(3)  # Her 3 saniyede bir güncelle

# Performans izleme thread'i başlat
threading.Thread(target=monitor_performance, daemon=True).start()



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

print(f"{len(known_face_names)} kişi yüklendi: {known_face_names}")

randevu_hatirlatildi = {}

video_capture = cv2.VideoCapture(0, cv2.CAP_DSHOW)
video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
video_capture.set(cv2.CAP_PROP_FPS, 30)
video_capture.set(cv2.CAP_PROP_BUFFERSIZE, 1)

frame_width = int(video_capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
frame_center_x = frame_width // 2
frame_center_y = frame_height // 2

frame_counter = 0

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    if frame_counter % 3 == 0:
        face_locations = face_recognition.face_locations(rgb_frame)
        face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    frame_counter += 1

    if face_locations:
        arama_modu = False
        yuz_kayboldu_sayac = 0
    else:
        yuz_kayboldu_sayac += 1
        if yuz_kayboldu_sayac == yuz_kaybolma_limiti:
            print("Yüz bulunamadı, tarama modu aktif...")

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

            x_hata = x_center - frame_center_x
            y_hata = y_center - frame_center_y

            x_hassasiyet = max(2, min(6, abs(x_hata) // 20))
            y_hassasiyet = max(2, min(5, abs(y_hata) // 20))

            if abs(x_hata) > 25:
                if x_hata < 0:
                    servo_x += x_hassasiyet
                else:
                    servo_x -= x_hassasiyet

            if abs(y_hata) > 25:
                if y_hata < 0:
                    servo_y -= y_hassasiyet
                else:
                    servo_y += y_hassasiyet

            servo_x = max(servo_x_min, min(servo_x_max, servo_x))
            servo_y = max(servo_y_min, min(servo_y_max, servo_y))

            arduino.write(f'{servo_x},{servo_y}\n'.encode())
            time.sleep(0.05)

            name = "Bilinmiyor"
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.6)
            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)

            if matches[best_match_index]:
                name = known_face_names[best_match_index]

                if name not in randevu_hatirlatildi:
                    conn = sqlite3.connect('face_recognition.db')
                    c = conn.cursor()
                    c.execute("SELECT randevu_saati FROM users WHERE name=?", (name,))
                    result = c.fetchone()
                    conn.close()

                    if result and result[0]:
                        randevu_saati = result[0]
                        print(f"{name} için randevu bulundu: {randevu_saati}")
                        randevu_sesi_oynat(name, f"{randevu_saati} saatinde randevun var.")
                        randevu_hatirlatildi[name] = True

                su_an = datetime.now().strftime("%H:%M")
                randevu_datetime = datetime.strptime(randevu_saati, "%H:%M")
                su_an_datetime = datetime.strptime(su_an, "%H:%M")

                fark_10dk = randevu_datetime - timedelta(minutes=10)
                fark_5dk = randevu_datetime - timedelta(minutes=5)

                if su_an_datetime == fark_10dk and f"{name}_10dk" not in randevu_hatirlatildi:
                    print(f"{name}, randevuya 10 dakika kaldı!")
                    randevu_sesi_oynat(name, "Randevuna 10 dakika kaldı.")
                    randevu_hatirlatildi[f"{name}_10dk"] = True

                elif su_an_datetime == fark_5dk and f"{name}_5dk" not in randevu_hatirlatildi:
                    print(f"{name}, randevuya 5 dakika kaldı!")
                    randevu_sesi_oynat(name, "Randevuna 5 dakika kaldı.")
                    randevu_hatirlatildi[f"{name}_5dk"] = True

            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name, (left + 6, top - 6), cv2.FONT_HERSHEY_DUPLEX, 0.7, (0, 255, 0), 2)

    cv2.imshow("Yüz Tanıma ve Servo Takip", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
arduino.close()
cv2.destroyAllWindows()
