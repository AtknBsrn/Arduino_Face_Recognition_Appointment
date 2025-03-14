import cv2
import os

save_dir = "faces"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow("Yüz Kaydetmek İçin 's' Tuşuna Bas", frame)

    if cv2.waitKey(1) & 0xFF == ord('s'):
        save_path = os.path.join(save_dir, "benim_yuzum.jpg")
        cv2.imwrite(save_path, frame)
        print(f"Fotoğraf kaydedildi: {save_path}")
        break

cap.release()
cv2.destroyAllWindows()
