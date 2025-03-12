import sqlite3
import face_recognition
import cv2
import numpy as np

# Veritabanından yüz encoding'lerini çekme
def get_all_faces():
    conn = sqlite3.connect('face_recognition.db')
    c = conn.cursor()
    c.execute("SELECT name, face_encoding FROM users")
    users = c.fetchall()
    conn.close()

    known_face_encodings = []
    known_face_names = []

    for name, encoding_blob in users:
        encoding = np.frombuffer(encoding_blob, dtype=np.float64)
        known_face_encodings.append(encoding)
        known_face_names.append(name)

    return known_face_encodings, known_face_names

# Kayıtlı yüzleri yükle
known_face_encodings, known_face_names = get_all_faces()

# Kamerayı başlat
video_capture = cv2.VideoCapture(0)

while True:
    ret, frame = video_capture.read()
    if not ret:
        break

    # Yüzleri tespit et
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    for (top, right, bottom, left), face_encoding in zip(face_locations, face_encodings):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Bilinmiyor"

        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        # Yüzün etrafına kutu çiz ve ismi yaz
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    cv2.imshow('Yüz Tanıma Sistemi', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
